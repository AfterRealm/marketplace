#!/usr/bin/env python3
"""
claude-voice — hands-free voice input for the Claude Desktop App in any language.

Hold a hotkey, speak in any of the 99 languages Whisper supports, release, and
the transcribed text is typed into whatever window currently has focus
(ideally the Claude Desktop App's chat input).

This fixes the case where official voice mode's English-only STT mangles
non-English speech. Your voice is transcribed correctly, typed in, and Claude
responds in the same language as always — text you can read.

No API key required. No data leaves your machine except the text that gets
typed into Claude (same as typing).
"""

from __future__ import annotations

__version__ = "0.2.0"

import argparse
import os
import queue
import shutil
import subprocess
import sys
import tempfile
import threading
import time
from dataclasses import dataclass
from pathlib import Path

try:
    import yaml
except ImportError:
    yaml = None

try:
    import numpy as np
    import sounddevice as sd
    import soundfile as sf
except ImportError:
    print("Missing audio deps. Run: pip install numpy sounddevice soundfile", file=sys.stderr)
    sys.exit(1)

try:
    from faster_whisper import WhisperModel
except ImportError:
    print("Missing Whisper. Run: pip install faster-whisper", file=sys.stderr)
    sys.exit(1)

try:
    from pynput import keyboard
    from pynput.keyboard import Controller as KeyController
except ImportError:
    print("Missing hotkey lib. Run: pip install pynput", file=sys.stderr)
    sys.exit(1)

# Optional: active-window title detection for the focus-safety check.
try:
    if sys.platform == "win32":
        import ctypes
        from ctypes import wintypes
    else:
        ctypes = None
except Exception:
    ctypes = None


# ─── CONFIG ────────────────────────────────────────────────

@dataclass
class Config:
    hotkey: str = "<f8>"
    language: str | None = None
    whisper_model: str = "small"
    whisper_device: str = "cpu"
    whisper_compute: str = "int8"
    samplerate: int = 16000
    auto_send: bool = True              # press Enter after typing the transcript
    target_window: str = "claude"       # only type if focused window title contains this (case-insensitive). "" to disable.
    print_transcript: bool = True
    max_record_seconds: int = 60        # hard cap on a single hold-to-talk clip — protects against runaway memory
    # ── Mic sensitivity (for quiet / whispered speech) ──
    mic_gain: float = 1.0               # manual pre-amp multiplier applied before normalization (1.0 = off)
    auto_normalize: bool = True         # peak-normalize quiet audio toward normalize_target_peak
    normalize_target_peak: float = 0.8  # target peak (0.0-1.0) after normalization; only boosts, never attenuates
    whisper_mode: bool = False          # preset bundle for whispered/quiet speech — tweaks gain + VAD + Whisper params

    @classmethod
    def load(cls, path: Path | None) -> "Config":
        if path is None or not path.exists() or yaml is None:
            return cls()
        try:
            raw = yaml.safe_load(path.read_text(encoding="utf-8"))
        except Exception as e:
            print(f"[claude-voice] config.yaml failed to parse ({e}); using defaults.", file=sys.stderr)
            return cls()
        if raw is None:
            raw = {}
        if not isinstance(raw, dict):
            print(f"[claude-voice] config.yaml must be a mapping at the top level, got {type(raw).__name__}; using defaults.", file=sys.stderr)
            return cls()
        cfg = cls()
        for key, val in raw.items():
            if hasattr(cfg, key):
                setattr(cfg, key, val)
            else:
                print(f"[claude-voice] config.yaml: unknown key '{key}' ignored.", file=sys.stderr)
        return cfg


# Preset bumper — called ONCE from main() after all config + CLI overrides are merged.
# Single source of truth so CLI users and config-file users get identical whisper_mode values.
def _apply_whisper_preset(cfg: "Config") -> None:
    if not cfg.whisper_mode:
        return
    if cfg.mic_gain <= 1.0:
        cfg.mic_gain = 4.0
    if cfg.normalize_target_peak < 0.95:
        cfg.normalize_target_peak = 0.95


# ─── AUDIO CAPTURE ─────────────────────────────────────────

class Recorder:
    def __init__(
        self,
        samplerate: int,
        max_seconds: int = 60,
        mic_gain: float = 1.0,
        auto_normalize: bool = True,
        normalize_target_peak: float = 0.8,
    ):
        self.samplerate = samplerate
        self.max_seconds = max_seconds
        self.mic_gain = mic_gain
        self.auto_normalize = auto_normalize
        self.normalize_target_peak = normalize_target_peak
        self.frames: list = []
        self.recording = False
        self._stream = None

    def _on_frame(self, indata, frame_count, time_info, status):
        if self.recording:
            self.frames.append(indata.copy())

    def start(self):
        self.frames = []
        self.recording = True
        self._stream = sd.InputStream(
            samplerate=self.samplerate,
            channels=1,
            dtype="float32",
            callback=self._on_frame,
        )
        self._stream.start()

    def stop(self) -> str | None:
        self.recording = False
        if self._stream is not None:
            try:
                self._stream.stop()
                self._stream.close()
            except Exception:
                pass
            self._stream = None
        if not self.frames:
            return None
        data = np.concatenate(self.frames, axis=0)
        if len(data) < self.samplerate * 0.2:
            return None
        max_samples = self.samplerate * self.max_seconds
        if len(data) > max_samples:
            print(f"[claude-voice] recording capped at {self.max_seconds}s "
                  f"(adjust via config `max_record_seconds`).", flush=True)
            data = data[:max_samples]

        # ── Sensitivity boost for quiet / whispered speech ──
        touched = False
        # 1) Manual pre-amp (user-set or whisper_mode preset)
        if self.mic_gain != 1.0:
            data = data * self.mic_gain
            touched = True
        # 2) Auto peak-normalize — boost quiet audio AND attenuate any peak that gain
        #    pushed past 1.0 (otherwise the clip in step 3 would introduce distortion).
        if self.auto_normalize:
            peak = float(np.max(np.abs(data)))
            if peak > 1e-6:  # ignore pure silence / division-by-zero
                scale = self.normalize_target_peak / peak
                if scale > 1.0 or peak > 1.0:
                    data = data * scale
                    touched = True
        # 3) Safety clip — only needed if we actually touched the signal
        if touched:
            data = np.clip(data, -1.0, 1.0)

        tmp = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
        sf.write(tmp.name, data, self.samplerate)
        tmp.close()
        return tmp.name


# ─── TRANSCRIPTION ─────────────────────────────────────────

_MODEL_SIZES = {"tiny": "~75 MB", "base": "~150 MB", "small": "~500 MB", "medium": "~1.5 GB", "large-v3": "~3 GB"}


class Transcriber:
    def __init__(self, cfg: Config):
        self.cfg = cfg
        size_hint = _MODEL_SIZES.get(cfg.whisper_model, "size unknown")
        print(f"[claude-voice] loading Whisper model '{cfg.whisper_model}' on {cfg.whisper_device}...", flush=True)
        print(f"[claude-voice] first run downloads {size_hint} to ~/.cache/huggingface/. "
              f"Progress (if any) appears below. This can take 1–5 minutes on first run.", flush=True)
        try:
            self.model = WhisperModel(
                cfg.whisper_model,
                device=cfg.whisper_device,
                compute_type=cfg.whisper_compute,
            )
        except Exception as e:
            print(f"[claude-voice] failed to load Whisper model: {e}", flush=True)
            print("[claude-voice] check your internet connection and try again. "
                  "If you're behind a proxy, set HTTPS_PROXY before launching.", flush=True)
            raise SystemExit(1)
        print("[claude-voice] Whisper ready.", flush=True)

    def transcribe(self, wav_path: str) -> str:
        kwargs: dict = {
            "language": self.cfg.language,
            "vad_filter": True,
        }
        if self.cfg.whisper_mode:
            # Quiet / whispered speech tuning:
            # - Keep VAD enabled but loosen its threshold. Pure-off VAD lets Whisper
            #   hallucinate "Thanks for watching!" etc. on accidental hotkey bumps.
            #   threshold=0.15 is loose enough to pass whispered audio while still
            #   filtering true silence.
            # - Lower no_speech threshold so Whisper doesn't dismiss quiet frames.
            # - Disable previous-text conditioning (stops hallucinated fill-in).
            # - Prime the model with an initial prompt hinting at quiet input.
            kwargs["vad_parameters"] = {"threshold": 0.15}
            kwargs["no_speech_threshold"] = 0.2
            kwargs["condition_on_previous_text"] = False
            # Only prime with an English hint when the user is transcribing English
            # (or auto-detecting, which is already English-biased on short clips).
            # Priming an explicitly non-English session with English text would nudge
            # the model toward English tokens — exactly what this multilingual plugin
            # is built to avoid.
            if self.cfg.language in (None, "", "en"):
                kwargs["initial_prompt"] = "The following contains quiet or whispered speech."
        segments, _ = self.model.transcribe(wav_path, **kwargs)
        return "".join(seg.text for seg in segments).strip()


# ─── TEXT INJECTION ─────────────────────────────────────────

def _linux_active_title() -> str:
    """Linux: try xdotool first, fall back to xprop + wmctrl."""
    try:
        return subprocess.check_output(
            ["xdotool", "getactivewindow", "getwindowname"],
            stderr=subprocess.DEVNULL, timeout=1.0,
        ).decode().strip()
    except Exception:
        pass
    try:
        wid = subprocess.check_output(
            ["xprop", "-root", "_NET_ACTIVE_WINDOW"],
            stderr=subprocess.DEVNULL, timeout=1.0,
        ).decode().split()[-1]
        for ln in subprocess.check_output(
            ["wmctrl", "-l"], stderr=subprocess.DEVNULL, timeout=1.0,
        ).decode().splitlines():
            if ln.startswith(wid):
                # wmctrl -l format: <id> <desktop> <host> <title...>
                return ln.split(None, 3)[-1].strip()
    except Exception:
        pass
    return ""


def active_window_title() -> str:
    """Return the title (or app name) of the focused window. '' on failure."""
    if sys.platform == "win32" and ctypes is not None:
        try:
            hwnd = ctypes.windll.user32.GetForegroundWindow()
            length = ctypes.windll.user32.GetWindowTextLengthW(hwnd)
            buf = ctypes.create_unicode_buffer(length + 1)
            ctypes.windll.user32.GetWindowTextW(hwnd, buf, length + 1)
            return buf.value or ""
        except Exception:
            return ""
    if sys.platform == "darwin":
        try:
            out = subprocess.check_output(
                ["osascript", "-e",
                 'tell application "System Events" to get name of first application process whose frontmost is true'],
                stderr=subprocess.DEVNULL, timeout=1.0,
            )
            return out.decode().strip()
        except Exception:
            return ""
    return _linux_active_title()


def focus_detection_supported() -> bool:
    """True if we can actually read the focused window title on this platform."""
    if sys.platform == "win32":
        return ctypes is not None
    if sys.platform == "darwin":
        return True  # osascript ships with macOS
    # Linux: need xdotool, or (xprop + wmctrl)
    if shutil.which("xdotool"):
        return True
    return shutil.which("xprop") is not None and shutil.which("wmctrl") is not None


def _set_clipboard(text: str) -> bool:
    """Set the system clipboard to text. Returns True on success."""
    try:
        if sys.platform == "win32":
            # clip.exe expects utf-16-le on Windows for unicode
            p = subprocess.Popen(["clip"], stdin=subprocess.PIPE, shell=False)
            p.communicate(input=text.encode("utf-16-le"))
            return p.returncode == 0
        elif sys.platform == "darwin":
            p = subprocess.Popen(["pbcopy"], stdin=subprocess.PIPE)
            p.communicate(input=text.encode("utf-8"))
            return p.returncode == 0
        else:
            for cmd in (["xclip", "-selection", "clipboard"], ["xsel", "-b", "-i"]):
                try:
                    p = subprocess.Popen(cmd, stdin=subprocess.PIPE)
                    p.communicate(input=text.encode("utf-8"))
                    if p.returncode == 0:
                        return True
                except FileNotFoundError:
                    continue
            return False
    except Exception:
        return False


def type_text(text: str, auto_send: bool) -> bool:
    """Paste text via the clipboard and optionally press Enter. Returns True on success."""
    if not _set_clipboard(text):
        print("[claude-voice] clipboard unavailable — paste aborted. "
              "Ensure 'clip' (Windows), 'pbcopy' (macOS), or 'xclip'/'xsel' (Linux) is on PATH.",
              flush=True)
        return False
    controller = KeyController()
    time.sleep(0.08)
    mod = keyboard.Key.cmd if sys.platform == "darwin" else keyboard.Key.ctrl
    controller.press(mod); controller.press('v')
    controller.release('v'); controller.release(mod)
    if auto_send:
        time.sleep(0.12)
        controller.press(keyboard.Key.enter)
        controller.release(keyboard.Key.enter)
    return True


# ─── MAIN LOOP ─────────────────────────────────────────────

def _print_platform_warnings() -> None:
    """Warn about platform-specific UX pitfalls that would otherwise fail silently."""
    if sys.platform == "darwin":
        print("[claude-voice] macOS note: if the hotkey does nothing, open", flush=True)
        print("  System Settings → Privacy & Security → Accessibility", flush=True)
        print("  and add Terminal (or your Python binary) to the allowed list.", flush=True)
        print("  You may also need to grant Input Monitoring permission.", flush=True)
    elif sys.platform.startswith("linux"):
        if os.environ.get("XDG_SESSION_TYPE") == "wayland" or os.environ.get("WAYLAND_DISPLAY"):
            print("[claude-voice] WARNING: Wayland detected. Global hotkeys via pynput", flush=True)
            print("  are unreliable on Wayland. If the hotkey does nothing, log into", flush=True)
            print("  an Xorg/X11 session instead.", flush=True)


def run(cfg: Config) -> None:
    _print_platform_warnings()
    recorder = Recorder(
        cfg.samplerate,
        max_seconds=cfg.max_record_seconds,
        mic_gain=cfg.mic_gain,
        auto_normalize=cfg.auto_normalize,
        normalize_target_peak=cfg.normalize_target_peak,
    )
    transcriber = Transcriber(cfg)

    print(f"[claude-voice] hold '{cfg.hotkey}' to talk. Release to send into focused window.", flush=True)
    print(f"[claude-voice] language = {cfg.language or 'auto-detect'} · max clip = {cfg.max_record_seconds}s", flush=True)
    if cfg.whisper_mode:
        print(f"[claude-voice] whisper_mode ON — mic_gain={cfg.mic_gain:.1f}x, "
              f"target peak={cfg.normalize_target_peak:.2f}, relaxed VAD + transcription thresholds.", flush=True)
    elif cfg.mic_gain != 1.0 or not cfg.auto_normalize:
        print(f"[claude-voice] mic_gain={cfg.mic_gain:.1f}x · auto_normalize={cfg.auto_normalize}", flush=True)
    if cfg.target_window:
        if focus_detection_supported():
            print(f"[claude-voice] focus safety ON — only typing into windows containing: '{cfg.target_window}'", flush=True)
        else:
            print("[claude-voice] focus detection unavailable on this platform "
                  "(install 'xdotool' or 'wmctrl' on Linux to enable). Focus safety DISABLED.", flush=True)
            cfg.target_window = ""
    else:
        print("[claude-voice] focus safety OFF — will type into whatever window has focus. Be careful.", flush=True)
    print("[claude-voice] press Ctrl+C in this window to quit.", flush=True)

    # Parse hotkey into required key-name set
    required = set()
    for part in cfg.hotkey.split("+"):
        part = part.strip()
        if part.startswith("<") and part.endswith(">"):
            part = part[1:-1]
        required.add(part.lower())

    def key_names(k):
        """Return all possible names a key can match (raw + generic variants)."""
        names = set()
        if hasattr(k, "name") and k.name:
            n = k.name.lower()
            names.add(n)
            # Also add the generic form so "<ctrl>" matches ctrl_l/ctrl_r
            for mod in ("ctrl", "shift", "alt", "cmd", "meta"):
                if n.startswith(mod):
                    names.add(mod)
                    break
        if hasattr(k, "char") and k.char:
            names.add(k.char.lower())
        return names

    held: set = set()
    active = {"rec": False}
    work_q: queue.Queue = queue.Queue()

    def check_combo():
        if required.issubset(held) and not active["rec"]:
            try:
                recorder.start()
            except Exception as e:
                print(f"[claude-voice] recording failed to start: {e}", flush=True)
                print("[claude-voice] is your microphone in use by another app? "
                      "close it and try again.", flush=True)
                return
            active["rec"] = True
            print("\n[REC] recording...", flush=True)
        elif active["rec"] and not required.issubset(held):
            active["rec"] = False
            wav = recorder.stop()
            if wav:
                work_q.put(wav)
            else:
                print("[claude-voice] too short, ignored.", flush=True)

    def on_press(key):
        names = key_names(key)
        matching = names & required
        if matching:
            held.update(matching)
            check_combo()

    def on_release(key):
        names = key_names(key)
        matching = names & held
        if matching:
            for n in matching:
                held.discard(n)
            check_combo()

    listener = keyboard.Listener(on_press=on_press, on_release=on_release)
    listener.start()

    def worker():
        while True:
            wav = work_q.get()
            if wav is None:
                return
            try:
                text = transcriber.transcribe(wav)
                if not text:
                    print("[claude-voice] empty transcript, skipping.", flush=True)
                    continue
                if cfg.print_transcript:
                    print(f"[YOU] {text}", flush=True)
                # Focus safety
                if cfg.target_window:
                    title = active_window_title()
                    if not title:
                        hint = " (focus detection returned empty — on Linux install xdotool or wmctrl; use --any-window to bypass)"
                        print(f"[claude-voice] focus is ''{hint} — not typing.", flush=True)
                        continue
                    if cfg.target_window.lower() not in title.lower():
                        print(f"[claude-voice] focus is '{title}' — not typing (no match for '{cfg.target_window}'). Switch focus to the Claude window first.", flush=True)
                        continue
                if type_text(text, cfg.auto_send):
                    print("[claude-voice] sent.", flush=True)
            except Exception as e:
                print(f"[error] {e}", flush=True)
            finally:
                try: os.unlink(wav)
                except Exception: pass

    t = threading.Thread(target=worker, daemon=True)
    t.start()

    try:
        while True:
            time.sleep(0.5)
    except KeyboardInterrupt:
        print("\n[claude-voice] bye.")
        listener.stop()
        work_q.put(None)


# ─── CLI ENTRY ─────────────────────────────────────────────

def _gain_arg(s: str) -> float:
    """argparse validator: mic_gain must be a sensible multiplier."""
    try:
        v = float(s)
    except ValueError:
        raise argparse.ArgumentTypeError(f"mic-gain must be a number, got '{s}'")
    if not 0.1 <= v <= 20.0:
        raise argparse.ArgumentTypeError(f"mic-gain must be between 0.1 and 20.0, got {v}")
    return v


def main() -> int:
    parser = argparse.ArgumentParser(description="Voice input for the Claude Desktop App in any language.")
    parser.add_argument("--version", action="version", version=f"claude-voice {__version__}")
    # Default to config.yaml next to the plugin root (parent of scripts/), not the CWD
    default_cfg = Path(__file__).resolve().parent.parent / "config.yaml"
    parser.add_argument("--config", type=Path, default=default_cfg)
    parser.add_argument("--language", "-l", help="Pin language (fr, es, de, ja, ...). Omit for auto-detect.")
    parser.add_argument("--model", help="Whisper model: tiny / base / small / medium / large-v3.")
    parser.add_argument("--hotkey", help="Override hotkey, pynput chord format. Example: '<f8>' or '<ctrl>+<alt>+<v>'.")
    parser.add_argument("--max-seconds", type=int, help="Hard cap on a single hold-to-talk clip (default 60).")
    parser.add_argument("--no-send", action="store_true", help="Type transcript but don't press Enter.")
    parser.add_argument("--any-window", action="store_true", help="Disable focus safety; type into any focused window.")
    parser.add_argument("--whisper-mode", action="store_true",
        help="Preset bundle for quiet/whispered speech: boosts mic gain, relaxes VAD + Whisper thresholds.")
    parser.add_argument("--mic-gain", type=_gain_arg,
        help="Manual pre-amp multiplier for quiet mics (0.1-20.0, e.g. 2.5). Applied before auto-normalization.")
    args = parser.parse_args()

    cfg = Config.load(args.config if args.config.exists() else None)
    if args.language: cfg.language = args.language
    if args.model: cfg.whisper_model = args.model
    if args.hotkey: cfg.hotkey = args.hotkey
    if args.max_seconds: cfg.max_record_seconds = args.max_seconds
    if args.no_send: cfg.auto_send = False
    if args.any_window: cfg.target_window = ""
    if args.whisper_mode: cfg.whisper_mode = True
    if args.mic_gain is not None: cfg.mic_gain = args.mic_gain

    # Clamp config-loaded mic_gain too (YAML bypasses argparse validation)
    cfg.mic_gain = max(0.1, min(20.0, cfg.mic_gain))

    # Single source of truth for the whisper_mode preset — runs after all overrides.
    _apply_whisper_preset(cfg)

    run(cfg)
    return 0


if __name__ == "__main__":
    sys.exit(main())

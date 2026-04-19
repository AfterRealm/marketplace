# Changelog

## v0.2.0 — Quiet-speech support

- **`whisper_mode` preset bundle** — one config flag (or `--whisper-mode` CLI flag) tunes the full pipeline for quiet or whispered speech: boosts mic pre-amp to 4.0x, raises normalize target to 0.95, loosens the silero VAD threshold to 0.15 (still blocks silence, lets whispers through), lowers Whisper's `no_speech_threshold` to 0.2, disables `condition_on_previous_text` (stops hallucinated fill-in), and primes the model with a quiet-speech `initial_prompt` (English-only, so non-English sessions aren't biased)
- **Auto-normalization** — every recording now peak-normalizes toward a target peak (default 0.8). Boosts quiet audio AND rolls back signal that `mic_gain` pushed past 1.0, so hot gain doesn't hard-clip. Default ON
- **Manual `mic_gain` knob** — config key + `--mic-gain` CLI flag for power users with known-quiet mics. Validated to the 0.1–20.0 range (both argparse and YAML-load paths)
- **`/voice` skill gained a 4th onboarding question** — "How do you usually speak when recording?" (Normal / Quietly or whispered / Not sure). Picks the right preset at first launch, no config editing needed. Uses the AskUserQuestion tool's 4-question maximum
- **SessionStart update notifier** — new `scripts/update_check.py` + `hooks/hooks.json`. On session start, compares installed version to the latest GitHub release and prints a one-liner if newer. Silent when up-to-date, silent on network error. Matches Father Time's pattern
- New CLI flags: `--whisper-mode`, `--mic-gain`
- New config keys: `whisper_mode`, `mic_gain`, `auto_normalize`, `normalize_target_peak`
- Hardened: config.yaml parse errors and non-dict top-level YAML now fall back to defaults with a clear stderr warning instead of crashing
- `__version__` + `plugin.json.version` bumped to `0.2.0`

## v0.1.0 — Initial release

- Hold-to-talk voice input for the Claude Desktop App and Claude Code Desktop
- Local `faster-whisper` STT — 99 languages, auto-detect or pinned
- Cross-platform: Windows / macOS / Linux (X11)
- Transcript pastes via system clipboard (atomic, handles unicode/accents)
- Focus safety — only pastes into windows with "claude" in the title (works on Windows, macOS, and Linux with xdotool/wmctrl+xprop)
- Cross-platform global hotkey via `pynput` (configurable)
- `/voice` skill walks users through 3 setup questions (language, model, hotkey)
- Plugin-local venv install (`.venv/`) — dodges PEP 668, keeps heavy deps isolated
- CLI flags: `--language`, `--model`, `--hotkey`, `--max-seconds`, `--no-send`, `--any-window`, `--version`
- Default Whisper model: `small` — the sweet spot for accuracy vs. download size
- Default hotkey: `F8` — single key, rarely conflicts (Ctrl+Shift+Space available but may clash with IMEs / Discord)
- 60-second cap on a single clip, configurable via `max_record_seconds` or `--max-seconds` (~3.8 MB of RAM per minute at default sample rate)
- Audio captured and deleted locally; nothing leaves the machine except the pasted text
- Loud startup warnings for macOS Accessibility permission and Linux Wayland sessions — two environments where the hotkey would otherwise silently fail
- Graceful failure handling: clipboard missing → paste aborted with instructions; mic unavailable → logged; Whisper download failure → clean exit with HTTPS_PROXY hint
- No TTS pipeline — Claude's text replies are handled by the Desktop App natively

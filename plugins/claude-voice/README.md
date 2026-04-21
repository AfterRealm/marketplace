# claude-voice

**Talk to Claude in your own language.**

*A lightweight, multilingual-first voice-input plugin for anywhere you type into Claude — the **Claude Desktop App**, **Claude Code Desktop**, or a regular **Claude Code terminal**. If official `/voice` gives you gibberish in your language, this is for you.*

Claude's built-in voice mode only understands English. If you speak French, Spanish, German, Japanese, Arabic, Portuguese — anything else — your words come out as English-phonetic nonsense and Claude doesn't understand you.

This plugin fixes that. You press a key, you speak your language, and what you said gets typed into whatever Claude window has focus — the Desktop App chat, the Code Desktop GUI, or even a plain terminal running `claude`. Claude reads it, understands it, and replies normally. No subscription to anything new, no API keys, nothing sent to the cloud.

No MCP server, no TTS pipeline, no long config — just a Claude plugin + a Python script. Because focus safety matches on any window title containing "claude", it works across all three surfaces out of the box.

> ⚠️ **Platform status:** Fully tested on **Windows**. macOS and Linux code paths are implemented but untested in the wild — if you install on Mac or Linux, please [open an issue](https://github.com/AfterRealm/claude-voice/issues) (good or bad) so we can confirm or fix. See [Testers welcome](#testers-welcome) at the bottom for what would help most.

---

## Who this is for

- You subscribe to Claude (Pro, Max, or Team).
- You prefer speaking to typing — or you want to practice speaking a language.
- Your language is one of the [99 Whisper supports](https://github.com/openai/whisper#available-models-and-languages) (pretty much all common languages).
- You're on **Windows, macOS, or Linux**.

---

## What you'll need before installing

You need **three things installed on your computer**. Don't worry — these are free and take a few minutes total.

### 1. Python 3.10 or newer

Python is a programming language this tool is written in. Your computer needs it.

- **Windows / macOS:** download from [python.org/downloads](https://www.python.org/downloads/). On Windows, make sure to tick the box "**Add Python to PATH**" during install.
- **Linux:** usually already installed. If not, `sudo apt install python3 python3-pip`.

Check it works: open a terminal and run `python --version`. You should see something like `Python 3.12.x`.

> **macOS / Linux note:** if `python --version` errors with "command not found" but `python3 --version` works, alias or symlink `python` → `python3`. The update-checker hook invokes `python` directly; without that alias, you won't get notifications when new versions ship. One-time fix: `sudo ln -s $(which python3) /usr/local/bin/python` (macOS/Linux), or add `alias python=python3` to your shell profile.

### 2. Claude Code CLI

This is Claude's command-line tool. It's the piece that handles plugin installs. You'd need it even if you only use the Claude Desktop App.

Install from [claude.com/claude-code](https://claude.com/claude-code). Sign in once using your existing Claude account.

Check it works: open a terminal and run `claude --version`. You should see a version number.

### 3. A microphone

If you've ever done a video call on this computer, you're good.

---

## Installing the plugin (step by step)

If you've never used a terminal before, follow along word-for-word. This takes about 5 minutes.

### Step 1: Open a terminal

This is a black window where you type commands. Don't be intimidated — you'll paste two lines.

- **Windows:** Press the Windows key, type `cmd`, press Enter. A black window opens.
- **macOS:** Press Cmd+Space, type `terminal`, press Enter.
- **Linux:** You almost certainly know how.

### Step 2: Tell Claude about the plugin

Copy the line below **exactly** (including the word `claude` at the start), paste it into the terminal, and press Enter.

```
claude plugin marketplace add AfterRealm/claude-voice
```

You'll see some text scroll by. That's Claude bookmarking where the plugin lives. If you see a message saying "marketplace added" or similar, it worked.

If you see `'claude' is not recognized` or `command not found`: you haven't installed the Claude CLI yet (see the "What you'll need" section above). Install it first, close and reopen the terminal, then try again.

### Step 3: Install the plugin

Paste this next line and press Enter:

```
claude plugin install claude-voice
```

You'll see "installed" or similar when it's done. This is quick — a few seconds.

### Step 4: Restart Claude

**Completely quit the Claude Desktop App** (not just minimize — actually close it). Then reopen it. Plugins only activate after a restart.

### Step 5: You're done!

Nothing else to install yet. The Whisper voice model and Python packages download automatically the first time you use the plugin (next section).

**Something went wrong?** Jump to the [Troubleshooting](#troubleshooting) section — common install hiccups are covered there.

---

## Using it the first time

1. Open the Claude Desktop App.
2. In the chat box, type `/voice` and press Enter — or just say something like *"start voice mode in French"*.
3. Claude will ask you **four quick questions**:
   - **What language will you be speaking?** (pick yours, or "auto-detect")
   - **Which model size?** Stick with the recommended **small** for your first try. It's a good balance of accuracy and download size (~500 MB).
   - **Which key starts recording?** Stick with the recommended **F8** unless you have a reason to change it — it's a single key that rarely conflicts with anything else.
   - **How do you usually speak when recording?** Pick **"Quietly or whispered"** if you tend to be soft-spoken — it turns on a preset that boosts the mic and relaxes silence-detection so your speech doesn't get dropped. Otherwise stick with **"Normal speaking voice"**.
4. Claude will then spend a minute or two setting things up:
   - First time only: it downloads Python dependencies (~200 MB).
   - First time with each model: it downloads the Whisper voice model (~500 MB for "small").
   - **This takes 1–5 minutes depending on your internet speed.** A small black terminal window appears and shows progress.
5. When the terminal window says `Whisper ready.`, you're good to go.

### Talking to Claude

1. Click the Claude chat input box so it's focused (blinking cursor in it).
2. **Hold** the hotkey (default **F8**).
3. Speak. Whatever language you chose.
4. **Release** the key.
5. A second or two later, your words appear in the Claude chat input and auto-send. Claude replies as normal.

That's the whole loop. Speak, release, read the reply, speak again.

### Recording length cap

A single hold-to-talk clip is **capped at 60 seconds by default**. If you hold the hotkey longer, recording stops at 60s and only that portion is transcribed — this protects against a stuck key eating gigabytes of RAM, or Whisper stalling for minutes on a runaway clip.

Rough sizing: 16 kHz mono float32 audio is about **3.8 MB per minute** held in memory until transcription finishes. A 60s clip ≈ 3.8 MB; a 5-minute clip ≈ 19 MB; a 20-minute clip ≈ 76 MB plus a potentially multi-minute Whisper pass on CPU.

**To change the cap** (e.g. for long dictation):

- **Quick way** — re-run the script with `--max-seconds 300` (5 minutes).
- **Permanent** — edit `config.yaml` in the plugin folder and set `max_record_seconds: 300`.

Going above a few minutes per clip is only practical if you have a GPU or use the `tiny` / `base` model. Going below 60s is fine if you're using this purely for short voice commands.

### Stopping voice mode

Close the small black terminal window. That kills the voice listener. Claude Desktop keeps running normally.

---

## Bilingual trick

You can **speak one language and have Claude reply in another.** Useful if you're learning a language or want explanations in your native tongue.

Tell Claude once at the start:

> *"I'm going to speak to you in French, but please reply in English."*

Claude will remember. Then voice-chat away.

---

## Soft-spoken or whispering? Turn on Whisper mode

If you tend to speak quietly, whisper, or have a mic that picks up your voice faintly, turn on **Whisper mode** — a preset bundle tuned for soft speech (not to be confused with *Whisper the model*; they happen to share the name).

When Whisper mode is on, claude-voice:

- **Primes the transcriber** with a hint that the audio contains quiet or whispered speech — reduces hallucinations on near-silent frames.
- **Lowers the no-speech threshold to 0.2** so quiet frames aren't dropped as silence.
- **Caps auto-normalize gain at 0.95** to avoid clipping when the signal is boosted.

Two ways to enable it:

- **During `/voice` setup**, pick **"Quietly or whispered"** when asked how you usually speak.
- **Manually** — edit `config.yaml` in the plugin folder and set `whisper_mode: true`.

If your mic is hardware-quiet (built-in laptop, far-field headset), also bump `mic_gain` to `2.0`–`3.0` in the same config. Whisper mode caps auto-normalize at 0.95 by default, so pre-amp via `mic_gain` is the right lever for quiet sources.

Verified live: whispered A–Z test transcribed cleanly on a soft-spoken Windows mic.

---

## First-time macOS setup

macOS blocks global hotkeys by default. The first time you run claude-voice on a Mac, the hotkey will do nothing until you grant permission.

1. Open **System Settings** → **Privacy & Security**.
2. Click **Accessibility**.
3. Click the **+** button and add the **Terminal** app (or whatever terminal you use — iTerm, WezTerm, etc.) to the allowed list. Make sure the toggle is ON.
4. Go back and click **Input Monitoring** in the same Privacy panel; add Terminal there too.
5. Fully quit and reopen the Claude Desktop App, then re-run `/voice`.

Without these permissions, the hotkey won't fire and there's no error message — the script will look like it's running normally. This is a macOS design choice, not a bug.

## Linux: X11 vs Wayland

claude-voice uses global-hotkey and window-focus libraries that work great on **X11 (Xorg)** and are unreliable on **Wayland**. If you're on a modern distro (Fedora 40+, Ubuntu 24.04+, GNOME 45+ on most distros, Sway, Hyprland), you may be on Wayland without realizing it.

Check: `echo $XDG_SESSION_TYPE` — if it says `wayland`, either log out and pick an "X11" or "Xorg" session from your display manager, or use claude-voice from a compositor that exposes the global-shortcut portal (very limited right now). A proper evdev-based backend is on the roadmap for a future release.

Also install `xdotool` (or `wmctrl` + `xprop`) for focus safety to work on Linux:
```bash
sudo apt install xdotool   # Debian/Ubuntu
sudo dnf install xdotool   # Fedora
```

## Troubleshooting

**I pressed the hotkey but nothing happened.**
- The terminal window needs to say `Whisper ready.` first. If it still says "loading Whisper model," wait — it's downloading.
- Make sure you clicked into the Claude chat input first. The hotkey won't paste anywhere else (on purpose, for safety).
- On **macOS**, you probably need to grant Accessibility + Input Monitoring permission — see the section above.
- On **Linux**, you're probably on Wayland — see the section above.
- Another app might be using that hotkey. IMEs (Chinese/Japanese/Korean input) and Discord push-to-talk commonly claim Ctrl+Shift+Space. Re-run `/voice` and pick F8 instead.
- On Windows, if you opened Claude "as administrator," the hotkey won't fire. Close Claude and reopen it normally.

**It transcribed my French as English nonsense.**
- You picked "auto-detect" — it guessed wrong on a short clip. Close the terminal window, re-run `/voice`, and pick your actual language this time.

**It sometimes transcribes English as English even though I picked French.**
- Known quirk of Whisper. When your audio is very clearly English, the model can override your language choice. Doesn't happen when you actually speak the pinned language. Not a problem for normal use.

**My French has typos / weird words.**
- You're on the `small` model. Re-run `/voice` and pick `medium` — it's more accurate (~1.5 GB download, runs slower on CPU).

**The terminal window disappeared.**
- Voice mode crashed. Run `/voice` again — it'll reopen.

**I don't want the transcript to auto-send.**
- Advanced: edit the config file (see below) and set `auto_send: false`. Or run from the command line with `--no-send`.

---

## Privacy

- **Your voice stays on your computer.** Whisper transcribes locally. No audio is uploaded anywhere.
- Audio clips are deleted immediately after transcription. They're only on disk for about 1 second.
- The only thing that leaves your machine is the **text** that gets typed into Claude — exactly as if you'd typed it yourself.
- No telemetry. No analytics. No accounts.
- The only network call is a one-time download of the Whisper model from Hugging Face (a public model host).

Curious? The whole voice pipeline is a single Python file, [`scripts/claude_voice.py`](scripts/claude_voice.py). You can read every line.

---

## Advanced: changing settings later

If you want to change the language, model, or hotkey later, easiest way is to re-run `/voice` in Claude and pick new answers.

For permanent changes, edit `config.yaml` in the plugin folder. Typical locations:

- **Windows:** `%USERPROFILE%\.claude\plugins\cache\AfterRealm\claude-voice\`
- **macOS:** `~/.claude/plugins/cache/AfterRealm/claude-voice/`
- **Linux:** `~/.claude/plugins/cache/AfterRealm/claude-voice/`

Copy `config.example.yaml` → `config.yaml` in that folder, edit to taste. See [`config.example.yaml`](config.example.yaml) for every option. Restart the voice script (close the terminal, re-run `/voice`) after editing.

Or skip the plugin entirely and run the script directly from a clone:

```bash
git clone https://github.com/AfterRealm/claude-voice.git
cd claude-voice
python -m venv .venv
# Windows:
.venv\Scripts\pip install -r scripts/requirements.txt
.venv\Scripts\python scripts/claude_voice.py --language fr --model small
# macOS / Linux:
.venv/bin/pip install -r scripts/requirements.txt
.venv/bin/python scripts/claude_voice.py --language fr --model small
```

Flags: `--language <code>` / `--model <size>` / `--hotkey "<combo>"` / `--max-seconds <n>` / `--no-send` / `--any-window` / `--version`.

---

## Whisper model sizes

| Model | Download | Speed on CPU | Accuracy | Best for |
|---|---|---|---|---|
| `tiny` | ~75 MB | Fastest | Rough | Quick tests in English |
| `base` | ~150 MB | Fast | OK | English only |
| `small` | ~500 MB | Medium | Good | **Recommended** — most languages |
| `medium` | ~1.5 GB | Slow on CPU | Very good | Professional accuracy |
| `large-v3` | ~3 GB | Needs GPU | Best | Near-human; NVIDIA GPU required |

---

## License

MIT — see [LICENSE](LICENSE). Free to use, modify, redistribute.

## Related projects

claude-voice isn't the only Claude voice plugin out there. Different tools solve different slices of the problem — if this one isn't the right fit, try:

- **[VoiceMode (mbailey/voicemode)](https://github.com/mbailey/voicemode)** — full two-way voice conversations (STT + TTS) for Claude Code, MCP-based. The featured option if you want to hear replies spoken back.
- **[claude-stt (jarrodwatts/claude-stt)](https://github.com/jarrodwatts/claude-stt)** — live streaming dictation for Claude Code. Transcription as you speak, not push-to-talk.
- **[voice-to-claude (enesbasbug/voice-to-claude)](https://github.com/enesbasbug/voice-to-claude)** — push-to-talk for Claude Code using whisper.cpp with Metal GPU acceleration. Mac-focused.
- **[claude-ptt (aaddrick/claude-ptt)](https://github.com/aaddrick/claude-ptt)** — push-to-talk for Claude Code, local or OpenAI API backend.
- **[Wispr Flow](https://wisprflow.ai/use-cases/claude)** — commercial cross-app dictation SaaS.

**Where claude-voice fits in that lineup:**
multilingual-first positioning; works across the **Claude Desktop App, Claude Code Desktop, and regular Claude Code terminals** (one plugin, three surfaces); plain Claude plugin format (no MCP); lightweight install (just a venv). If you want 2-way TTS, VoiceMode is the better call. If you want a simple multilingual voice input that drops into *any* Claude window that has focus, stay here.

## Credits

claude-voice is a thin wrapper around excellent open-source work:

- **[Whisper](https://github.com/openai/whisper)** (OpenAI) — the speech recognition model that does the real work (MIT)
- **[faster-whisper](https://github.com/SYSTRAN/faster-whisper)** — CTranslate2 port of Whisper, dramatically faster on CPU (MIT)
- **[pynput](https://github.com/moses-palmer/pynput)** — global hotkey and clipboard control (LGPL-3.0)
- **[sounddevice](https://python-sounddevice.readthedocs.io/)** + **[soundfile](https://github.com/bastibe/python-soundfile)** — audio capture and WAV writing (MIT / BSD-3-Clause)

All dependencies ship under permissive licenses compatible with claude-voice's own MIT license.

## Testers welcome

claude-voice was built and verified on **Windows 11**. The macOS and Linux (X11) code paths are written against standard libraries (pynput, sounddevice, osascript, xdotool) that are known to work cross-platform, but **no one has actually run it on those OSes yet**. If you install it on a Mac or a Linux box, a short issue report is genuinely valuable — either outcome.

What would help most:

- **Your OS + version** (e.g. "macOS 15 Sequoia, Apple Silicon" / "Ubuntu 24.04 X11" / "Fedora 40 Wayland").
- **Did `/voice` finish setup without errors?** Venv created, deps installed, Whisper downloaded?
- **Does the hotkey fire?** Hold F8, does the terminal show `[REC] recording...`?
- **Does the transcript paste into the Claude chat input?** In your actual spoken language?
- **Did focus safety behave?** Try pressing the hotkey with a non-Claude window focused — does it refuse to paste?
- **On macOS only:** did you need to grant Accessibility / Input Monitoring permissions, and did the README section on that actually cover what you had to do?

Open an [issue](https://github.com/AfterRealm/claude-voice/issues) with answers. Negative reports are just as useful as positive ones — if the hotkey didn't fire, or the paste landed wrong, that's the signal that closes the gap.

## Contributing

Pull requests welcome. See [GitHub issues](https://github.com/AfterRealm/claude-voice/issues) for ideas or to report bugs.

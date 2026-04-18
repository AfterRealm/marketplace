# Changelog

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

# Session Continuity

**Claude asks "pick up where we left off, or start fresh?" — tells you what "where you left off" actually was, and names the session for you.**

A Claude Code plugin that checks for prior session history the moment a session starts, then asks a real, clickable question about it instead of leaving that discipline to memory or a stray `/rename` you meant to type three sessions ago.

---

## The problem

Claude Code sessions pile up per project with no names, and by the time you have twelve of them, `claude --resume` is just a wall of UUIDs and first-lines-of-the-first-message. `/rename` fixes this, but only if you remember to run it — and you won't, because naming a session is never the thing you opened the terminal to do.

## What it does

Every time a session starts (fresh or `--resume`), a hook silently checks whether this project directory has been worked in before. If it has, Claude opens with a real question — not a suggestion buried in a paragraph:

```
? Continuing this project's prior work?
> Continue → rename to 'Api_Refactor_V4'
    Renames to 'Api_Refactor_V4'. Last time: You: can you add rate
    limiting to the upload endpoint  |  Claude: Added a token-bucket
    limiter, tests pass — next is wiring it into the retry middleware.
  Continue, keep current name
  Starting something new instead
  Turn this off
```

Pick an option (or type a name of your own) and Claude renames the session itself, right then — no `/rename` required. If it's a brand-new project with no history at all, it offers once to name this first session and then gets out of the way.

**The first time you ever run it**, it asks how it should behave before doing anything else — enable it, enable it but skip the nudge on brand-new projects, or turn it off entirely — and remembers your answer. Every prompt after that still carries a "Turn this off" option, so changing your mind never means uninstalling anything.

## Why this works everywhere

No config, no registry file, no convention to adopt. Claude Code already stores every session's transcript at `~/.claude/projects/<project>/*.jsonl` — this plugin just reads that. It recovers any name you've ever set with `/rename` straight from the transcript, so it works from the very first install with zero setup. If your project happens to keep a `sessions/HANDOFF.md`-style checkpoint file, it'll surface a snippet of that too — but that's a bonus, never a requirement.

It works identically on Windows, macOS, and Linux — same detection logic, same config file semantics, and a hook command that finds whichever Python interpreter (`python3` or `python`) is actually on your PATH.

## Install

```bash
claude plugin marketplace add AfterRealm/session-continuity
claude plugin install session-continuity
```

Restart Claude Code afterward — hooks are picked up on startup.

## What it never does

- Never touches session content, only a session's *name*.
- Never renames anything without you choosing to.
- Never blocks your actual message — it asks once, alongside addressing whatever you came in to do, not instead of it.
- Never runs during scripted/unattended sessions (e.g. `claude -p`) — no risk of an automation pipeline getting stuck on a question meant for a human.
- Never phones home. No network calls, no telemetry, no external dependencies.

## Configuring it later

Ask Claude to turn it off, or run directly:

```bash
python session-continuity/scripts/configure.py --enabled false
python session-continuity/scripts/configure.py --show
```

Settings live in `~/.claude/session-continuity.json`:

| Key | Default | Meaning |
|---|---|---|
| `enabled` | `true` | Master on/off switch |
| `ask_on_new_project` | `true` | Whether brand-new projects (no history at all) get a one-time naming offer |
| `offer_continuity_digest` | `true` | Whether the "where you left off" summary is included |

## How it works, technically

- **`hooks/hooks.json`** registers a `SessionStart` hook, firing only on `startup` and `resume` (never `clear` or `compact`, so it can't interrupt something mid-task). The command tries `python3` first and falls back to `python`, so it doesn't matter which one is actually on your PATH.
- **`session_start.py`** resolves the current project directory from the hook's own payload (`transcript_path`, exact and instant — never guessed from a reconstructed path), looks at prior transcripts in that same directory, pulls out any past session titles and, when available, the tail end of the most recent one for the "where you left off" digest. It works out a sensible next name — bumping a version number if one exists (`Project_V6`), or starting fresh (`Project_V1`) — and prints an instruction for Claude to act on; it doesn't talk to you directly, and it never lets an error surface as a failed hook.
- **`apply_rename.py`** is what actually renames the session, called by Claude — not the hook — once you've confirmed. It does exactly what Claude Code's built-in `/rename` command does: append a `{"type": "custom-title", ...}` record to the session's own transcript file, located by `CLAUDE_CODE_SESSION_ID` alone (never by current directory, which can drift over a long conversation). Because renaming is just the most recent record winning, doing it again (with this plugin or `/rename` itself) simply supersedes the last one — there's no way to end up stuck or corrupted.
- **`configure.py`** reads and writes the config file above.
- Title lookups are cached by `(path, size, mtime)`, so a completed transcript is only ever fully scanned once, no matter how many sessions you start afterward.

## Requirements

- Claude Code, obviously.
- Python 3 on your `PATH` (as `python3` or `python`).
- That's it. No API keys, no accounts, no dependencies to `pip install`.

## License

MIT — see [LICENSE](LICENSE).

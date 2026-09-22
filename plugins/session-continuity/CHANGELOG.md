# Changelog

## 2.1.0 — 2026-09-21

### Fixed
- The naming suggestion bumped the **highest version number found
  anywhere in the project's history**, not the version of the session
  actually being continued — so "Continue" could suggest a name
  completely unrelated to the prior thread the digest was just quoting
  (e.g. bumping some unrelated old session to V9→V10 while showing a
  digest from a totally different, unversioned recent one). It now bumps
  the **most recent prior session's own name** specifically — the same
  session the digest is pulled from — and only falls back to a
  project-wide scan when that particular session was never named at all.

## 2.0.0 — 2026-09-21

Follows an external code review that surfaced several correctness bugs
and cross-platform gaps ahead of public release. Fixed all of them and
folded in the two biggest suggested improvements: a real "where you left
off" digest, and first-run configurability.

### Fixed (real bugs, not just polish)
- **Project-directory resolution was wrong for any path containing a dot**
  (`.claude`, `node.js-app`, `v1.2`, etc.) — the old slug logic only
  translated `\ / :` and whitespace, not every non-alphanumeric character
  Claude Code actually replaces. Detection now resolves the project
  directory from the hook's own `transcript_path` first (exact, O(1)),
  falling back to a session-id glob, and only as a last resort to a
  slugifier that now matches Claude Code's real algorithm exactly.
- **`apply_rename.py` trusted `os.getcwd()`**, which can drift over a
  long conversation. It now locates the transcript purely by
  `CLAUDE_CODE_SESSION_ID`, glob-matched under `~/.claude/projects/*/`,
  regardless of current directory.
- **Re-asked on every `--resume`**, even when the session already had a
  name. It now checks the current session's own transcript first and
  stays silent if it's already named.
- **Tail-only title scan could miss an early rename** in a large
  transcript, and a single corrupted/truncated match could hide every
  earlier one. Title extraction now walks every candidate match from the
  end backwards until one actually parses, with results cached by
  `(path, size, mtime)` so this only ever costs a full read once per
  transcript.
- **Unsafe transcript append**: if the last line of a transcript wasn't
  newline-terminated (a partial/crashed write), appending would corrupt
  it. Now checks and inserts a leading newline first.
- **Empty/missing session id could make a brand-new project self-detect
  as having history.** Now resolved directly from the hook payload with
  a safe fallback to the environment variable.
- **Version-bump suggestions could collide with an existing name** if it
  fell outside the scanned window. Suggestions are now checked against
  every recovered name and de-duplicated.
- **Hardcoded `python` broke on most macOS/Linux installs** (which only
  have `python3`), and there was no top-level exception guard — meaning
  the hook could fail loudly on every single startup for a large share
  of installs. Fixed on both fronts: the hook command now tries `python3`
  first and falls back to `python`, and `session_start.py` never lets an
  exception escape `main()`.

### Added
- **"Where you left off" digest.** When prior history is found, the last
  exchange from the most recent transcript is pulled into the
  confirmation prompt, so "Continue" means something concrete, not just
  a name.
- **Configurable, opt-out anytime.** First run asks how the plugin should
  behave (enable / enable-but-skip-new-projects / disable) via
  `AskUserQuestion`, written to `~/.claude/session-continuity.json`.
  Every subsequent prompt also carries a "Turn this off" option. New
  `scripts/configure.py` reads/writes the config.
- **Stays silent for unattended/scripted runs** (e.g. `claude -p`), so it
  never injects a confirmation prompt into automation.
- Filters subagent/sidechain transcripts out of the prior-session count.

### Changed
- Verified Windows and macOS/Linux behave identically: same detection
  logic, same config location semantics (via `Path.home()`), and a hook
  command that resolves the right Python interpreter on both.

## 1.2.0 — 2026-09-21

### Changed
- The confirmation step now uses `AskUserQuestion` (structured options)
  instead of a plain-text yes/no. Plain-text nudges were easy to miss in
  a busy reply and left "did they say yes" up to parsing free text —
  structured options remove both problems and make the auto-rename
  trigger unambiguous.

## 1.1.0 — 2026-09-21

### Changed
- Detection no longer depends on a hand-maintained session registry
  file. It now scans `~/.claude/projects/<slug>/*.jsonl` directly —
  Claude Code's own transcript storage — so it works out of the box for
  anyone, recovering prior `/rename` titles straight from each
  transcript's title record.
- The nudge now always includes a concrete suggested name, whether or
  not prior history was found.

### Added
- `scripts/apply_rename.py`: applies a session name automatically by
  replicating `/rename`'s own mechanism (appending a custom-title record
  to the session's transcript). Claude runs this itself once the user
  confirms — no manual `/rename` needed.

## 1.0.0 — 2026-09-21

Initial release.

### Added
- `SessionStart` hook that detects prior session history for the current
  project (`sessions/HANDOFF.md`, `sessions/INDEX.md`, or an entry in
  `~/.claude/session_registry.md`) and nudges Claude to ask whether the
  user is continuing that work or starting fresh.
- Version-bump suggestion for `/rename` based on the highest existing
  session name for the project.
- Only fires on `startup`/`resume` sources, so it doesn't interrupt
  in-progress sessions on `clear` or `compact`.

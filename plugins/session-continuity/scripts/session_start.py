"""
Session Continuity — SessionStart hook.

Detects prior session history for the current project using two signals:

1. Universal (works for anyone, no setup): prior transcripts for this
   exact project directory under ~/.claude/projects/<slug>/*.jsonl —
   located via the hook payload's own transcript_path when available, so
   there's no path-slugging to get wrong. Session names ever set via
   /rename are recovered from each transcript's "custom-title" record,
   cached by (path, size, mtime) so repeat scans are cheap.
2. Optional bonus: a sessions/HANDOFF.md or sessions/INDEX.md checkpoint
   file in the project, if the user happens to keep one.

On a genuine first run (no config file yet), it also asks how the plugin
should behave going forward — this is the opt-out/configure step — before
folding into the normal per-session nudge.

Prints an instruction telling Claude to ask, via AskUserQuestion, whether
the user is continuing prior work or starting fresh, with a concrete
suggested session name and (when available) a one-line "where you left
off" digest pulled from the most recent prior transcript. Claude applies
the chosen name itself via apply_rename.py — see that script.

Never raises past main(): a hook that fails loudly on every startup is
worse than a hook that silently does nothing.
"""
import json
import os
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _session_continuity_lib import (  # noqa: E402
    force_utf8_stdout,
    is_attended,
    is_first_run,
    is_sidechain_transcript,
    mark_asked,
    was_asked,
    extract_last_exchange,
    load_cache,
    load_config,
    read_title_cached,
    resolve_project_context,
    save_cache,
)

force_utf8_stdout()

# Only nudge when a session is actually beginning, not mid-task events.
# /clear starts a new session (new id, new transcript), so it counts.
ACTIONABLE_SOURCES = {"startup", "resume", "clear"}

# Cap work per hook run to the N most recently touched prior transcripts.
# Cheap in practice: completed transcripts are cached by (size, mtime)
# after their first scan and never re-read.
MAX_PRIOR_FILES_SCANNED = 25

# Cross-platform python invocation: try python3 first (the common case on
# macOS/Linux and Windows-with-Git-Bash), fall back to python (the common
# case on a plain Windows install). See README for the rare
# Windows-without-Git-Bash caveat.
PY_INVOKE = 'command -v python3 >/dev/null 2>&1 && python3 "{script}" {args} || python "{script}" {args}'


def read_stdin_payload():
    try:
        raw = sys.stdin.read()
        return json.loads(raw) if raw.strip() else {}
    except Exception:
        return {}


def find_local_checkpoint(cwd: Path):
    """Return handoff/index info if this project uses the sessions/
    checkpoint convention. Purely a bonus signal — never required."""
    sessions_dir = cwd / "sessions"
    handoff = sessions_dir / "HANDOFF.md"
    index = sessions_dir / "INDEX.md"

    handoff_text = None
    if handoff.exists():
        try:
            handoff_text = handoff.read_text(encoding="utf-8", errors="ignore").strip()
        except Exception:
            handoff_text = None

    index_latest = None
    if index.exists():
        try:
            for line in index.read_text(encoding="utf-8", errors="ignore").splitlines():
                stripped = line.strip()
                if stripped.startswith("|") and "---" not in stripped and "Date" not in stripped:
                    index_latest = stripped
                    break
        except Exception:
            index_latest = None

    if handoff_text is None and index_latest is None:
        return None
    return {"handoff": handoff_text, "index_latest": index_latest}


def find_prior_sessions(project_dir: Path, current_session_id: str):
    """Scan a project's transcript directory for prior sessions
    (excluding the current one and any sidechain/subagent transcripts).
    Returns (total_count, [names in recency order], most_recent_path,
    most_recent_title). most_recent_title is the title of files[0]
    specifically (may be None if that particular session was never
    named), distinct from `names`, which is every recovered title across
    the scanned window regardless of recency."""
    if project_dir is None or not project_dir.exists():
        return 0, [], None, None

    files = [
        f for f in project_dir.glob("*.jsonl")
        if f.stem != current_session_id
    ]
    if not files:
        return 0, [], None, None

    files.sort(key=lambda f: f.stat().st_mtime, reverse=True)
    files = [f for f in files if not is_sidechain_transcript(f)]
    if not files:
        return 0, [], None, None

    cache = load_cache()
    names = []
    for f in files[:MAX_PRIOR_FILES_SCANNED]:
        title = read_title_cached(f, cache)
        if title and title not in names:  # /clear copies titles forward
            names.append(title)
    most_recent_title = read_title_cached(files[0], cache)
    save_cache(cache)

    return len(files), names, files[0], most_recent_title


def parse_version(name: str):
    """Return (prefix, version_number) if `name` ends in something that
    looks like a version, or None. Guards against false positives like a
    year (".. 2027") by rejecting numbers >= 1000."""
    m = re.match(r"^(.*?)[\s_]*[Vv]?(\d+)$", name)
    if m and int(m.group(2)) < 1000:
        return m.group(1).rstrip("_ "), int(m.group(2))
    return None


def suggest_name(folder_name: str, prior_count: int, prior_names, most_recent_title=None):
    """Suggest a concrete session name. Primarily bumps the version of
    the MOST RECENT prior session specifically (that's the thread "Continue"
    would actually be continuing) rather than the highest version number
    anywhere in the project's history, which can suggest a name totally
    unrelated to what's actually being picked back up. Falls back to a
    project-wide scan only when the most recent session was never named,
    and finally to a fresh base name. Guards against suggesting a name
    that's already taken."""
    base = re.sub(r"[^A-Za-z0-9]+", "_", folder_name).strip("_") or "Session"
    existing = set(prior_names)

    if most_recent_title:
        parsed = parse_version(most_recent_title)
        if parsed:
            prefix, num = parsed
            sep = "_" if prefix and not prefix.endswith(("_", "-", " ")) else ""
            candidate = f"{prefix or base}{sep}V{num + 1}"
        else:
            candidate = f"{most_recent_title}_V2"
    else:
        best = None
        for name in prior_names:
            parsed = parse_version(name)
            if parsed and (best is None or parsed[1] > best[1]):
                best = (parsed[0] or base, parsed[1])
        if best:
            prefix, num = best
            sep = "_" if prefix and not prefix.endswith(("_", "-", " ")) else ""
            candidate = f"{prefix}{sep}V{num + 1}"
        elif prior_count > 0:
            candidate = f"{base}_V{prior_count + 1}"
        else:
            candidate = f"{base}_V1"

    # Never suggest a name that's already in use, even if the version
    # math landed on one we didn't see in the scanned window.
    n = 1
    final = candidate
    while final in existing:
        n += 1
        final = f"{candidate}_{n}"
    return final


def py_invoke(script_path: Path, args: str = "") -> str:
    return PY_INVOKE.format(script=script_path, args=args)


NAME_PLACEHOLDER = '"<chosen name>"'


def run():
    if not is_attended():
        return  # scripted/unattended run (e.g. `claude -p`): stay silent

    payload = read_stdin_payload()
    source = payload.get("source", "startup")
    if source not in ACTIONABLE_SOURCES:
        return

    config = load_config()
    scripts_dir = Path(__file__).resolve().parent
    apply_rename = scripts_dir / "apply_rename.py"
    configure = scripts_dir / "configure.py"

    if is_first_run():
        print(
            "[session-continuity] First run for this plugin. Before addressing the "
            "user's message, briefly (one line) explain what it does — checks for "
            "prior sessions in a project and offers to name/rename sessions for you "
            "— then call AskUserQuestion: \"Enable session-continuity?\" with options "
            "\"Enable\" (Recommended), \"Enable, but don't ask on brand-new projects\", "
            "and \"Disable\". Apply the choice by running one of: "
            f'{py_invoke(configure, "--enabled true --ask-on-new true")} | '
            f'{py_invoke(configure, "--enabled true --ask-on-new false")} | '
            f'{py_invoke(configure, "--enabled false")} '
            "(pick the one matching their answer). This writes ~/.claude/session-"
            "continuity.json so this question is never asked again. If they chose "
            "anything but Disable, continue below with the normal check for this "
            "project; if Disable, skip it and just address their message."
        )
        if not config.get("enabled", True):
            return
        # Fall through to the normal check using in-memory defaults for
        # *this* run — the config file itself will reflect their actual
        # choice once Claude runs configure.py per the instruction above.

    if not config.get("enabled", True):
        return

    project_dir, session_id = resolve_project_context(payload)
    cwd = Path(payload.get("cwd") or os.getcwd())
    folder_name = cwd.name

    # Ask once per session id. A title in the transcript isn't proof the
    # flow ran: /clear copies the old /rename name into the new session's
    # transcript as its first record.
    if session_id and was_asked(session_id):
        return

    current_title = None
    if session_id and project_dir:
        current_transcript = project_dir / f"{session_id}.jsonl"
        if current_transcript.exists():
            cache = load_cache()
            current_title = read_title_cached(current_transcript, cache)
            save_cache(cache)

    # A resumed session that's already named has been through this before
    # (or was named by hand), so leave it alone.
    if source == "resume" and current_title:
        return

    if session_id:
        mark_asked(session_id)

    local = find_local_checkpoint(cwd)
    prior_count, prior_names, most_recent, most_recent_title = find_prior_sessions(project_dir, session_id)

    turn_off_hint = (
        f'To turn this off entirely, run: {py_invoke(configure, "--enabled false")}'
    )

    if prior_count == 0 and local is None:
        if not config.get("ask_on_new_project", True):
            return
        suggestion = suggest_name(folder_name, 0, [])
        print(
            "[session-continuity] No prior session history found for this project "
            f"(\"{folder_name}\"). Before addressing the user's message, call "
            "AskUserQuestion with a question like \"Name this session?\" and options: "
            f"\"Name it '{suggestion}'\" (Recommended), \"Not now\", and \"Don't ask "
            "for new projects\". If they pick the first (or type their own name "
            f'instead), apply it by running: {py_invoke(apply_rename, NAME_PLACEHOLDER)} '
            "— don't just tell them to type /rename. If \"Don't ask for new projects\", "
            f'run: {py_invoke(configure, "--ask-on-new false")}. {turn_off_hint} Ask '
            "this once, get the answer, then proceed to their actual message."
        )
        return

    suggestion = suggest_name(folder_name, prior_count, prior_names, most_recent_title)
    digest = None
    if config.get("offer_continuity_digest", True) and most_recent is not None:
        digest = extract_last_exchange(most_recent)

    parts = [f"[session-continuity] This project (\"{folder_name}\") has prior session history."]

    if current_title:
        parts.append(f"This session is currently named '{current_title}' (carried over from before /clear).")
    keep_label = f"Continue, keep '{current_title}'" if current_title else "Continue, keep current name"

    if prior_count:
        seen = f" Recovered names: {', '.join(prior_names)}." if prior_names else " None of them were named."
        parts.append(f"{prior_count} prior transcript(s) found for this project directory.{seen}")

    if digest:
        parts.append(f"Where the most recent prior session left off: {digest}")

    if local and local.get("handoff"):
        parts.append(f"sessions/HANDOFF.md found:\n{local['handoff'][:600]}")
    elif local and local.get("index_latest"):
        parts.append(f"sessions/INDEX.md latest entry: {local['index_latest']}")

    continue_desc = f"Renames to '{suggestion}'."
    if digest:
        continue_desc += f" Last time: {digest}"

    parts.append(
        "Before addressing the user's message, call AskUserQuestion with a question "
        "like \"Continuing this project's prior work?\" and options (put the digest, "
        f"if any, in the option's description field): \"Continue → rename to "
        f"'{suggestion}'\" (Recommended, description: \"{continue_desc}\"), \"{keep_label}\", "
        "\"Starting something new instead\", and \"Turn this off\". "
        f'Based on the answer (or a custom name they type), apply it by running: '
        f'{py_invoke(apply_rename, NAME_PLACEHOLDER)} — don\'t just '
        "tell them to type /rename; if they chose to keep the current name or it's not "
        f'worth naming, don\'t run anything. If "Turn this off": {py_invoke(configure, "--enabled false")}. '
        "Ask this once, get the answer, then proceed to their actual message."
    )

    print("\n".join(parts))


def main():
    try:
        run()
    except Exception:
        # A hook that fails loudly on every startup is worse than one
        # that silently does nothing this one time.
        pass
    sys.exit(0)


if __name__ == "__main__":
    main()

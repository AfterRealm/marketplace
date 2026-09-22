"""
Session Continuity — apply a session rename programmatically.

Replicates exactly what Claude Code's own /rename command does: appends a
{"type": "custom-title", "customTitle": ..., "sessionId": ...} record to
the current session's own transcript file. Claude Code reads the last
such record as the session's display name, so renaming again (including
via /rename itself) simply supersedes this one — always reversible.

Usage: python apply_rename.py "New Session Name"

Run this from Claude's own Bash tool mid-conversation (not from a hook),
after the user has confirmed they want the session (re)named. The
transcript is located purely by the CLAUDE_CODE_SESSION_ID environment
variable (glob-matched under ~/.claude/projects/*/), never by cwd —
cwd can drift over the course of a conversation and is not a reliable
way to find the right project directory.
"""
import json
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _session_continuity_lib import (  # noqa: E402
    resolve_transcript_by_session_id,
    slugify_cwd,
    PROJECTS_ROOT,
)


def main():
    if len(sys.argv) < 2 or not sys.argv[1].strip():
        print('error: usage: apply_rename.py "New Session Name"', file=sys.stderr)
        sys.exit(1)
    new_title = sys.argv[1].strip()

    session_id = os.environ.get("CLAUDE_CODE_SESSION_ID", "").strip()
    if not session_id:
        print("error: CLAUDE_CODE_SESSION_ID not set in this environment", file=sys.stderr)
        sys.exit(1)

    transcript = resolve_transcript_by_session_id(session_id)
    if transcript is None:
        # Last-resort fallback in case the transcript directory uses an
        # older naming scheme this glob doesn't match for some reason.
        candidate = PROJECTS_ROOT / slugify_cwd(os.getcwd()) / f"{session_id}.jsonl"
        if candidate.exists():
            transcript = candidate

    if transcript is None or not transcript.exists():
        print(
            f"error: could not locate a transcript for session {session_id} "
            f"under {PROJECTS_ROOT}",
            file=sys.stderr,
        )
        sys.exit(1)

    record = json.dumps({
        "type": "custom-title",
        "customTitle": new_title,
        "sessionId": session_id,
    })

    # Guard against appending onto a partial last line (e.g. from a
    # crashed write) by making sure our record starts on its own line.
    # ("ab" mode is write-only in Python, so the check needs its own
    # read-mode handle first.)
    needs_leading_newline = False
    size = transcript.stat().st_size
    if size > 0:
        with open(transcript, "rb") as rf:
            rf.seek(-1, os.SEEK_END)
            needs_leading_newline = rf.read(1) != b"\n"

    with open(transcript, "ab") as f:
        if needs_leading_newline:
            f.write(b"\n")
        f.write((record + "\n").encode("utf-8"))
        f.flush()
        os.fsync(f.fileno())

    print(f"Session renamed to: {new_title}")


if __name__ == "__main__":
    main()

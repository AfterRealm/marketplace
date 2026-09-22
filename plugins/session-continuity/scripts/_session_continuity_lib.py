"""
Session Continuity — shared library.

Common code used by session_start.py, apply_rename.py, and configure.py:
  - Locating the current session's transcript and project directory
    (transcript_path from the hook payload first, session-id glob second,
    slugified cwd as a last resort — never trust cwd alone, it can drift)
  - The project-directory slug algorithm, fixed to match Claude Code's
    actual behavior (every non-alphanumeric character maps to '-', not
    just path separators and colons)
  - Reading/writing the plugin's config and title-scan cache
  - Extracting a session's custom-title (the /rename record) robustly,
    scanning backwards through every candidate match rather than trusting
    only the last one blindly
  - Detecting whether this is an attended (interactive) session, so the
    plugin stays silent for scripted/unattended runs

Pure standard library, no external dependencies, Windows/macOS/Linux safe.
"""
import json
import os
import re
import sys
from pathlib import Path

HOME = Path.home()
PROJECTS_ROOT = HOME / ".claude" / "projects"
CONFIG_PATH = HOME / ".claude" / "session-continuity.json"
CACHE_PATH = HOME / ".claude" / "session-continuity-cache.json"

DEFAULT_CONFIG = {
    "enabled": True,
    "ask_on_new_project": True,
    "offer_continuity_digest": True,
}

# Cap how much of a giant transcript we read in one go when we can't rely
# on the cache (first time we ever see that file). 20MB comfortably covers
# the vast majority of real sessions without risking a multi-hundred-MB
# read on a monster transcript.
MAX_FULL_READ_BYTES = 20_000_000
TAIL_BYTES_FALLBACK = 3_000_000


def slugify_cwd(cwd: str) -> str:
    """Exactly mirror Claude Code's project-directory slug: every
    non-alphanumeric character (not just \\ / : and whitespace) becomes
    '-'. Verified against a real project dir containing a dot:
    C:\\Users\\x\\.claude\\y -> C--Users-x--claude-y"""
    return re.sub(r"[^A-Za-z0-9]", "-", cwd)


def is_attended() -> bool:
    """False for scripted/unattended runs (e.g. `claude -p`), so the
    plugin never injects an AskUserQuestion instruction into automation.
    Defaults to attended (True) unless explicitly marked otherwise, since
    older Claude Code versions may not set this var at all."""
    return os.environ.get("CLAUDE_CODE_SESSION_ATTENDED", "1") != "0"


def load_config() -> dict:
    cfg = dict(DEFAULT_CONFIG)
    try:
        if CONFIG_PATH.exists():
            cfg.update(json.loads(CONFIG_PATH.read_text(encoding="utf-8")))
    except Exception:
        pass
    return cfg


def save_config(cfg: dict) -> None:
    CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
    merged = load_config()
    merged.update(cfg)
    CONFIG_PATH.write_text(json.dumps(merged, indent=2) + "\n", encoding="utf-8")


def is_first_run() -> bool:
    return not CONFIG_PATH.exists()


def load_cache() -> dict:
    try:
        if CACHE_PATH.exists():
            return json.loads(CACHE_PATH.read_text(encoding="utf-8"))
    except Exception:
        pass
    return {}


def save_cache(cache: dict) -> None:
    try:
        CACHE_PATH.parent.mkdir(parents=True, exist_ok=True)
        CACHE_PATH.write_text(json.dumps(cache), encoding="utf-8")
    except Exception:
        pass  # cache is a pure optimization; never let it break the hook


ASKED_KEY = "_asked_sessions"
ASKED_MAX = 500


def was_asked(session_id: str) -> bool:
    """True if this session id has already been through the naming prompt."""
    return session_id in load_cache().get(ASKED_KEY, {})


def mark_asked(session_id: str) -> None:
    """Remember that this session id has been asked, keeping only the most
    recent ASKED_MAX ids so the cache can't grow forever."""
    import time
    cache = load_cache()
    asked = cache.get(ASKED_KEY, {})
    asked[session_id] = time.time()
    if len(asked) > ASKED_MAX:
        asked = dict(sorted(asked.items(), key=lambda kv: kv[1])[-ASKED_MAX:])
    cache[ASKED_KEY] = asked
    save_cache(cache)


def resolve_project_context(payload: dict):
    """Return (project_dir: Path|None, session_id: str) for the session
    this hook is running in. Prefers the hook payload's own
    transcript_path (exact, O(1), immune to path-slugging bugs); falls
    back to locating the transcript by session id; falls back to a
    slugified cwd only as a last resort."""
    session_id = (payload.get("session_id") or "").strip() or os.environ.get(
        "CLAUDE_CODE_SESSION_ID", ""
    ).strip()

    transcript_path = payload.get("transcript_path")
    if transcript_path:
        p = Path(transcript_path)
        return p.parent, (session_id or p.stem)

    if session_id and PROJECTS_ROOT.exists():
        matches = list(PROJECTS_ROOT.glob(f"*/{session_id}.jsonl"))
        if matches:
            return matches[0].parent, session_id

    cwd = payload.get("cwd") or os.getcwd()
    slug = slugify_cwd(cwd)
    project_dir = PROJECTS_ROOT / slug
    return (project_dir if project_dir.exists() else None), session_id


def resolve_transcript_by_session_id(session_id: str):
    """Locate a transcript file purely by session id, ignoring cwd
    entirely. Used by apply_rename.py, which runs later in the
    conversation where cwd may have drifted from the project root."""
    if not session_id or not PROJECTS_ROOT.exists():
        return None
    matches = list(PROJECTS_ROOT.glob(f"*/{session_id}.jsonl"))
    return matches[0] if matches else None


def _find_all(data: bytes, needle: bytes):
    start = 0
    while True:
        idx = data.find(needle, start)
        if idx == -1:
            return
        yield idx
        start = idx + 1


def extract_custom_title_from_bytes(data: bytes):
    """Walk every '"custom-title"' occurrence from the end backwards and
    return the first one that actually parses as a valid custom-title
    record. A single corrupted/truncated match (e.g. from a tail-seek
    landing mid-line) no longer hides every earlier one."""
    offsets = list(_find_all(data, b'"custom-title"'))
    for idx in reversed(offsets):
        line_start = data.rfind(b"\n", 0, idx) + 1
        line_end = data.find(b"\n", idx)
        if line_end == -1:
            line_end = len(data)
        try:
            obj = json.loads(data[line_start:line_end])
        except Exception:
            continue
        if obj.get("type") == "custom-title":
            title = obj.get("customTitle")
            if title:
                return title.strip()
    return None


def read_title_cached(jsonl_path: Path, cache: dict):
    """Return the custom-title for a (presumably completed, so
    effectively immutable) prior transcript, using the on-disk cache
    keyed by (path, size, mtime) to avoid re-reading files that haven't
    changed since the last scan. Mutates `cache` in place; caller is
    responsible for persisting it once via save_cache()."""
    try:
        st = jsonl_path.stat()
    except Exception:
        return None

    key = str(jsonl_path)
    entry = cache.get(key)
    if entry and entry.get("size") == st.st_size and entry.get("mtime") == st.st_mtime:
        return entry.get("title")

    try:
        with open(jsonl_path, "rb") as f:
            if st.st_size > MAX_FULL_READ_BYTES:
                # Monster transcript: fall back to a tail-only read rather
                # than risk a huge memory spike. Rare, and only degrades
                # to "title not found" for a rename that happened very
                # early in an unusually large session.
                f.seek(max(0, st.st_size - TAIL_BYTES_FALLBACK))
            data = f.read()
    except Exception:
        return None

    title = extract_custom_title_from_bytes(data)
    cache[key] = {"size": st.st_size, "mtime": st.st_mtime, "title": title}
    return title


def is_sidechain_transcript(jsonl_path: Path) -> bool:
    """Best-effort filter for subagent/sidechain transcripts so they
    don't inflate the "prior sessions" count. Only skips a file when we
    can positively confirm it's a sidechain; any parse failure or
    ambiguity errs toward including the file."""
    try:
        with open(jsonl_path, "rb") as f:
            head = f.read(4096)
        for line in head.split(b"\n"):
            if not line.strip():
                continue
            obj = json.loads(line)
            return bool(obj.get("isSidechain"))
    except Exception:
        pass
    return False


def extract_last_exchange(jsonl_path: Path, max_chars: int = 260):
    """Best-effort 'where you left off' digest: the last user message and
    last assistant reply found in the tail of a transcript. Returns None
    if nothing usable is found — this is a nice-to-have, never required."""
    try:
        size = jsonl_path.stat().st_size
        with open(jsonl_path, "rb") as f:
            if size > TAIL_BYTES_FALLBACK:
                f.seek(size - TAIL_BYTES_FALLBACK)
            data = f.read()
    except Exception:
        return None

    def extract_text(content):
        if isinstance(content, str):
            return content
        if isinstance(content, list):
            for item in content:
                if isinstance(item, dict) and item.get("type") == "text":
                    return item.get("text", "")
        return ""

    last_user, last_assistant = None, None
    for raw_line in data.split(b"\n"):
        if not raw_line.strip():
            continue
        try:
            obj = json.loads(raw_line)
        except Exception:
            continue
        obj_type = obj.get("type")
        if obj_type not in ("user", "assistant"):
            continue
        message = obj.get("message")
        if not isinstance(message, dict):
            continue
        text = extract_text(message.get("content")).strip()
        if not text:
            continue
        if obj_type == "user":
            last_user = text
        else:
            last_assistant = text

    if not last_user and not last_assistant:
        return None

    def trim(s):
        s = " ".join(s.split())
        return s if len(s) <= max_chars else s[: max_chars - 1].rstrip() + "\u2026"

    parts = []
    if last_user:
        parts.append(f"You: {trim(last_user)}")
    if last_assistant:
        parts.append(f"Claude: {trim(last_assistant)}")
    return "  |  ".join(parts)


def force_utf8_stdout():
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

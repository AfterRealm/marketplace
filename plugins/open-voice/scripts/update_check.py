"""
open-voice — Update checker.
Compares installed plugin version against latest GitHub release.
Runs on SessionStart (via hooks/hooks.json) and notifies the user if newer.
Fails silently on any error — never blocks or noisies a session.
"""
import json
import os
import urllib.request
from pathlib import Path

REPO = "AfterRealm/open-voice"
GITHUB_API = f"https://api.github.com/repos/{REPO}/releases/latest"
UA_VERSION = "0.3.1"  # stays in sync with plugin.json version


def get_installed_version():
    """Read version from the installed plugin.json."""
    plugin_root = os.environ.get("CLAUDE_PLUGIN_ROOT", "")
    if plugin_root:
        p = Path(plugin_root) / ".claude-plugin" / "plugin.json"
    else:
        p = Path(__file__).parent.parent / ".claude-plugin" / "plugin.json"
    try:
        data = json.loads(p.read_text(encoding="utf-8"))
        return data.get("version", "0.0.0")
    except Exception:
        return None


def get_latest_version():
    """Fetch latest release tag from GitHub. Returns None on any failure."""
    req = urllib.request.Request(
        GITHUB_API,
        headers={
            "Accept": "application/vnd.github+json",
            "User-Agent": f"open-voice-plugin/{UA_VERSION}",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=5) as resp:
            data = json.loads(resp.read().decode())
            tag = data.get("tag_name", "")
            return tag.lstrip("v") if tag else None
    except Exception:
        return None


def version_tuple(v):
    """Convert version string to comparable tuple. Non-numeric parts → 0."""
    parts = []
    for x in v.split("."):
        try:
            parts.append(int(x))
        except ValueError:
            parts.append(0)
    return tuple(parts)


def main():
    installed = get_installed_version()
    if not installed:
        return
    latest = get_latest_version()
    if not latest:
        return
    if version_tuple(latest) > version_tuple(installed):
        print(f"open-voice update available: v{installed} -> v{latest}")
        print('Run: claude plugin update open-voice')


if __name__ == "__main__":
    main()

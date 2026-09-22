"""
Session Continuity — read or update the plugin's config.

Usage:
    python configure.py --show
    python configure.py --enabled true|false
    python configure.py --ask-on-new true|false
    python configure.py --digest true|false
    (any combination in one call)

Run by Claude in response to the user's answer to the first-run setup
question, or any time the user asks to change how the plugin behaves
(e.g. "turn off session naming"). Writes ~/.claude/session-continuity.json.
"""
import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _session_continuity_lib import load_config, save_config  # noqa: E402


def parse_bool(value: str) -> bool:
    return value.strip().lower() in ("true", "1", "yes", "on")


def main():
    parser = argparse.ArgumentParser(description="Configure session-continuity")
    parser.add_argument("--enabled", type=parse_bool)
    parser.add_argument("--ask-on-new", dest="ask_on_new_project", type=parse_bool)
    parser.add_argument("--digest", dest="offer_continuity_digest", type=parse_bool)
    parser.add_argument("--show", action="store_true")
    args = parser.parse_args()

    if args.show:
        print(json.dumps(load_config(), indent=2))
        return

    updates = {
        k: v for k, v in vars(args).items()
        if k != "show" and v is not None
    }
    if not updates:
        print(json.dumps(load_config(), indent=2))
        return

    save_config(updates)
    print(f"Updated: {json.dumps(updates)}")
    print(json.dumps(load_config(), indent=2))


if __name__ == "__main__":
    main()

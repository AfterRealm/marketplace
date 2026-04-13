#!/usr/bin/env python3
"""
Level Up — Agent Scanner
Discovers, inspects, and promotes Claude Code agents.

Usage:
  scan_agents.py --action list                              List all agents
  scan_agents.py --action inspect --name NAME [--project P] Show agent details
  scan_agents.py --action promote --name NAME --project P   Copy project agent to global
  scan_agents.py --help                                     Show this help
"""

import argparse
import json
import re
import shutil
import sys
from pathlib import Path


def get_global_agents_dir():
    return Path.home() / ".claude" / "agents"


def get_desktop_path():
    return Path.home() / "Desktop"


def parse_agent_frontmatter(filepath):
    """Extract frontmatter fields from an agent .md file."""
    try:
        content = filepath.read_text(encoding="utf-8")
    except Exception:
        return {"name": filepath.stem, "description": "", "raw": ""}

    result = {"name": filepath.stem, "description": "", "model": "", "raw": content}

    # Parse YAML frontmatter
    fm_match = re.match(r"^---\s*\n(.*?)\n---", content, re.DOTALL)
    if fm_match:
        fm = fm_match.group(1)
        for field in ["name", "description", "model"]:
            m = re.search(rf"^{field}:\s*(.+)$", fm, re.MULTILINE)
            if m:
                val = m.group(1).strip().strip("'\"")
                result[field] = val

    return result


def scan_all_agents():
    """Scan global and all Desktop project agents."""
    agents = []

    # Global
    global_dir = get_global_agents_dir()
    if global_dir.exists():
        for f in sorted(global_dir.glob("*.md")):
            info = parse_agent_frontmatter(f)
            agents.append({
                "name": info["name"],
                "scope": "global",
                "project": "global",
                "path": str(f),
                "description": info["description"],
                "model": info["model"]
            })

    # Desktop projects
    desktop = get_desktop_path()
    if desktop.exists():
        for proj_dir in sorted(desktop.iterdir()):
            if not proj_dir.is_dir():
                continue
            agents_dir = proj_dir / ".claude" / "agents"
            if agents_dir.exists():
                for f in sorted(agents_dir.glob("*.md")):
                    info = parse_agent_frontmatter(f)
                    agents.append({
                        "name": info["name"],
                        "scope": "project",
                        "project": proj_dir.name,
                        "path": str(f),
                        "description": info["description"],
                        "model": info["model"]
                    })

    return agents


def find_agent(name, project=None):
    """Find a specific agent by name and optionally project."""
    agents = scan_all_agents()
    for a in agents:
        if a["name"] == name:
            if project is None or a["project"] == project:
                return a
    return None


def action_list():
    """List all agents as JSON."""
    agents = scan_all_agents()
    print(json.dumps({"agents": agents, "total": len(agents)}, indent=2))


def action_inspect(name, project=None):
    """Show full details of a specific agent."""
    agent = find_agent(name, project)
    if not agent:
        print(json.dumps({"error": f"Agent '{name}' not found"}), file=sys.stderr)
        sys.exit(1)

    info = parse_agent_frontmatter(Path(agent["path"]))
    result = {**agent, "content": info["raw"]}
    print(json.dumps(result, indent=2))


def action_promote(name, project):
    """Copy a project agent to global scope."""
    agent = find_agent(name, project)
    if not agent:
        print(json.dumps({"error": f"Agent '{name}' not found in project '{project}'"}), file=sys.stderr)
        sys.exit(1)

    if agent["scope"] == "global":
        print(json.dumps({"error": f"Agent '{name}' is already global"}), file=sys.stderr)
        sys.exit(1)

    global_dir = get_global_agents_dir()
    global_dir.mkdir(parents=True, exist_ok=True)
    dest = global_dir / f"{name}.md"

    if dest.exists():
        print(json.dumps({"error": f"A global agent named '{name}' already exists"}), file=sys.stderr)
        sys.exit(1)

    shutil.copy2(agent["path"], dest)
    print(json.dumps({
        "action": "promoted",
        "name": name,
        "from": agent["path"],
        "to": str(dest)
    }, indent=2))


def main():
    parser = argparse.ArgumentParser(
        description="Level Up — Agent Scanner. Discover, inspect, and promote Claude Code agents."
    )
    parser.add_argument("--action", required=True, choices=["list", "inspect", "promote"],
                        help="Action to perform")
    parser.add_argument("--name", help="Agent name (without .md)")
    parser.add_argument("--project", help="Project name (folder name on Desktop)")
    args = parser.parse_args()

    if args.action == "list":
        action_list()
    elif args.action == "inspect":
        if not args.name:
            print(json.dumps({"error": "--name required for inspect"}), file=sys.stderr)
            sys.exit(1)
        action_inspect(args.name, args.project)
    elif args.action == "promote":
        if not args.name or not args.project:
            print(json.dumps({"error": "--name and --project required for promote"}), file=sys.stderr)
            sys.exit(1)
        action_promote(args.name, args.project)


if __name__ == "__main__":
    main()

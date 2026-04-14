#!/usr/bin/env python3
"""
Level Up — Agent Scanner
Discovers, inspects, promotes, versions, and merges Claude Code agents.

Usage:
  scan_agents.py --action list                              List all agents
  scan_agents.py --action inspect --name NAME [--project P] Show agent details
  scan_agents.py --action promote --name NAME --project P   Copy project agent to global
  scan_agents.py --action version --name NAME [--project P] Snapshot current agent state
  scan_agents.py --action version --name NAME [--project P] --restore TS  Restore a snapshot
  scan_agents.py --action list-versions --name NAME [--project P]  List snapshots
  scan_agents.py --action merge-prep --name N1 --project P1 --name2 N2 --project2 P2
  scan_agents.py --help                                     Show this help
"""

import argparse
import json
import os
import re
import shutil
import sys
from datetime import datetime
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


def get_versions_dir():
    """Base directory for agent version snapshots."""
    return Path(__file__).resolve().parent.parent / "versions"


def action_version(name, project=None, restore=None):
    """Snapshot or restore an agent version."""
    agent = find_agent(name, project)
    if not agent:
        label = f"'{name}'" + (f" in project '{project}'" if project else "")
        print(json.dumps({"error": f"Agent {label} not found"}), file=sys.stderr)
        sys.exit(1)

    agent_key = f"{agent['project']}--{name}" if agent["scope"] == "project" else f"global--{name}"
    versions_dir = get_versions_dir() / agent_key
    versions_dir.mkdir(parents=True, exist_ok=True)

    if restore:
        # Find the snapshot to restore
        snapshot_file = versions_dir / f"{restore}.md"
        if not snapshot_file.exists():
            print(json.dumps({"error": f"Snapshot '{restore}' not found for agent '{name}'"}), file=sys.stderr)
            sys.exit(1)

        # Auto-snapshot current state as safety net
        now = datetime.now().strftime("%Y%m%d-%H%M%S")
        safety_snapshot = versions_dir / f"{now}.md"
        shutil.copy2(agent["path"], safety_snapshot)

        # Restore
        shutil.copy2(str(snapshot_file), agent["path"])
        print(json.dumps({
            "action": "restored",
            "name": name,
            "project": agent["project"],
            "restored_from": str(snapshot_file),
            "restored_to": agent["path"],
            "safety_snapshot": str(safety_snapshot),
        }, indent=2))
    else:
        # Create snapshot
        now = datetime.now().strftime("%Y%m%d-%H%M%S")
        snapshot = versions_dir / f"{now}.md"
        shutil.copy2(agent["path"], str(snapshot))
        print(json.dumps({
            "action": "versioned",
            "name": name,
            "project": agent["project"],
            "snapshot_path": str(snapshot),
            "timestamp": now,
        }, indent=2))


def action_list_versions(name, project=None):
    """List all version snapshots for an agent."""
    agent = find_agent(name, project)
    if not agent:
        label = f"'{name}'" + (f" in project '{project}'" if project else "")
        print(json.dumps({"error": f"Agent {label} not found"}), file=sys.stderr)
        sys.exit(1)

    agent_key = f"{agent['project']}--{name}" if agent["scope"] == "project" else f"global--{name}"
    versions_dir = get_versions_dir() / agent_key

    versions = []
    if versions_dir.exists():
        for f in sorted(versions_dir.glob("*.md"), reverse=True):
            versions.append({
                "timestamp": f.stem,
                "path": str(f),
                "size_bytes": f.stat().st_size,
            })

    print(json.dumps({
        "agent": name,
        "project": agent["project"],
        "scope": agent["scope"],
        "total_versions": len(versions),
        "versions": versions,
    }, indent=2))


def parse_agent_sections(content):
    """Split agent content into frontmatter and heading-based sections."""
    sections = []
    frontmatter = {}

    # Extract frontmatter
    fm_match = re.match(r"^---\s*\n(.*?)\n---\s*\n?", content, re.DOTALL)
    body = content
    if fm_match:
        fm_text = fm_match.group(1)
        body = content[fm_match.end():]
        for line in fm_text.strip().split("\n"):
            m = re.match(r"^(\w[\w-]*):\s*(.+)$", line)
            if m:
                frontmatter[m.group(1)] = m.group(2).strip().strip("'\"")

    # Split body on ## headings
    parts = re.split(r"(?=^## )", body, flags=re.MULTILINE)
    for part in parts:
        part = part.strip()
        if not part:
            continue
        heading_match = re.match(r"^## (.+)\n", part)
        if heading_match:
            sections.append({
                "heading": heading_match.group(1).strip(),
                "content": part[heading_match.end():].strip(),
            })
        else:
            # Preamble before any heading
            sections.append({
                "heading": "(preamble)",
                "content": part,
            })

    return frontmatter, sections


def action_merge_prep(name1, project1, name2, project2):
    """Read two agents and return structured comparison."""
    agent1 = find_agent(name1, project1)
    if not agent1:
        print(json.dumps({"error": f"Agent '{name1}' not found in project '{project1}'"}), file=sys.stderr)
        sys.exit(1)

    agent2 = find_agent(name2, project2)
    if not agent2:
        print(json.dumps({"error": f"Agent '{name2}' not found in project '{project2}'"}), file=sys.stderr)
        sys.exit(1)

    info1 = parse_agent_frontmatter(Path(agent1["path"]))
    info2 = parse_agent_frontmatter(Path(agent2["path"]))

    fm1, sections1 = parse_agent_sections(info1["raw"])
    fm2, sections2 = parse_agent_sections(info2["raw"])

    headings1 = {s["heading"] for s in sections1}
    headings2 = {s["heading"] for s in sections2}

    common = sorted(headings1 & headings2)
    unique_to_1 = sorted(headings1 - headings2)
    unique_to_2 = sorted(headings2 - headings1)

    result = {
        "agent1": {
            "name": name1,
            "project": project1,
            "frontmatter": fm1,
            "sections": sections1,
        },
        "agent2": {
            "name": name2,
            "project": project2,
            "frontmatter": fm2,
            "sections": sections2,
        },
        "common_sections": common,
        "unique_to_1": unique_to_1,
        "unique_to_2": unique_to_2,
    }

    print(json.dumps(result, indent=2))


def main():
    parser = argparse.ArgumentParser(
        description="Level Up — Agent Scanner. Discover, inspect, promote, version, and merge Claude Code agents.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --action list                                    List all agents
  %(prog)s --action inspect --name fasciculus               Inspect an agent
  %(prog)s --action promote --name myagent --project "Ark Claude"  Promote to global
  %(prog)s --action version --name fasciculus --project "Claude Command Center"  Snapshot
  %(prog)s --action version --name fasciculus --restore 20260413-153000  Restore snapshot
  %(prog)s --action list-versions --name fasciculus         List snapshots
  %(prog)s --action merge-prep --name agent1 --project P1 --name2 agent2 --project2 P2
        """
    )
    parser.add_argument("--action", required=True,
                        choices=["list", "inspect", "promote", "version", "list-versions", "merge-prep"],
                        help="Action to perform")
    parser.add_argument("--name", help="Agent name (without .md)")
    parser.add_argument("--project", help="Project name (folder name on Desktop)")
    parser.add_argument("--restore", help="Timestamp to restore (for version action)")
    parser.add_argument("--name2", help="Second agent name (for merge-prep)")
    parser.add_argument("--project2", help="Second agent's project (for merge-prep)")
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
    elif args.action == "version":
        if not args.name:
            print(json.dumps({"error": "--name required for version"}), file=sys.stderr)
            sys.exit(1)
        action_version(args.name, args.project, args.restore)
    elif args.action == "list-versions":
        if not args.name:
            print(json.dumps({"error": "--name required for list-versions"}), file=sys.stderr)
            sys.exit(1)
        action_list_versions(args.name, args.project)
    elif args.action == "merge-prep":
        if not all([args.name, args.project, args.name2, args.project2]):
            print(json.dumps({"error": "--name, --project, --name2, --project2 all required for merge-prep"}),
                  file=sys.stderr)
            sys.exit(1)
        action_merge_prep(args.name, args.project, args.name2, args.project2)


if __name__ == "__main__":
    main()

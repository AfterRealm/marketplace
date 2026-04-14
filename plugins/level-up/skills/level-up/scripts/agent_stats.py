#!/usr/bin/env python3
"""
Level Up — Agent Usage Stats
Scans Claude Code session files for agent invocation data.

Two-pass approach per session:
  1. Parent JSONL -> agent identity (type, name, description, timestamp)
  2. Subagent JONSLs -> actual token costs (summed from the subagent's own conversation)
  Matched by creation order within each session.

Usage:
  agent_stats.py --action summary [--since PERIOD] [--project P]
  agent_stats.py --action detail --agent-type TYPE [--since PERIOD]
  agent_stats.py --action unused [--since PERIOD]
  agent_stats.py --help
"""

import argparse
import json
import re
import sys
import urllib.request
import urllib.error
from collections import defaultdict
from datetime import datetime, timedelta, timezone
from pathlib import Path


USAGE_CACHE_PATH = Path.home() / ".claude" / "usage_cache.json"
USAGE_API_URL = "https://api.anthropic.com/api/oauth/usage"
USAGE_CACHE_TTL = 300  # 5 minutes


def fetch_weekly_usage():
    """Fetch the user's 7-day usage utilization from Anthropic.
    Returns dict with {utilization, resets_at} or None on failure.
    Uses cached result if fresh enough."""
    # Check cache first
    if USAGE_CACHE_PATH.exists():
        try:
            cache = json.loads(USAGE_CACHE_PATH.read_text(encoding="utf-8"))
            cached_at = cache.get("cached_at", 0)
            if (datetime.now(timezone.utc).timestamp() - cached_at) < USAGE_CACHE_TTL:
                sd = cache.get("seven_day", {})
                if sd:
                    return {"utilization": sd.get("utilization", 0), "resets_at": sd.get("resets_at", "")}
        except (json.JSONDecodeError, OSError):
            pass

    # Find OAuth token
    token = None
    for cred_path in [Path.home() / ".claude" / ".credentials.json", Path.home() / ".claude" / "credentials.json"]:
        if cred_path.exists():
            try:
                creds = json.loads(cred_path.read_text(encoding="utf-8"))
                token = creds.get("claudeAiOauth", {}).get("accessToken")
                if token:
                    break
            except (json.JSONDecodeError, OSError):
                continue
    if not token:
        return None

    # Fetch from API
    try:
        req = urllib.request.Request(USAGE_API_URL, headers={
            "Accept": "application/json",
            "Authorization": f"Bearer {token}",
            "anthropic-beta": "oauth-2025-04-20",
            "User-Agent": "level-up/1.1.0",
        })
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode("utf-8"))

        # Cache the result
        data["cached_at"] = datetime.now(timezone.utc).timestamp()
        try:
            USAGE_CACHE_PATH.write_text(json.dumps(data), encoding="utf-8")
        except OSError:
            pass

        sd = data.get("seven_day", {})
        return {"utilization": sd.get("utilization", 0), "resets_at": sd.get("resets_at", "")}
    except (urllib.error.URLError, OSError, json.JSONDecodeError):
        return None


def get_projects_dir():
    return Path.home() / ".claude" / "projects"


def get_global_agents_dir():
    return Path.home() / ".claude" / "agents"


def get_desktop_path():
    return Path.home() / "Desktop"


def decode_project_name(dir_name):
    """C--Users-mered-Desktop-Ark-Claude -> Ark Claude"""
    home = Path.home()
    # Build prefixes dynamically from the user's actual home directory
    # Claude encodes paths as C--Users-username-... (replacing separators with --)
    home_encoded = str(home).replace("\\", "-").replace("/", "-").replace(":", "-")
    desktop_prefix = f"{home_encoded}-Desktop-"
    skills_prefix = f"{home_encoded}--claude-skills-"
    home_prefix = f"{home_encoded}-"

    for prefix in [desktop_prefix, skills_prefix, home_prefix]:
        if dir_name.startswith(prefix):
            return dir_name[len(prefix):].replace("-", " ")
    return dir_name.replace("-", " ")


def parse_since(since_str):
    if since_str == "all":
        return None
    now = datetime.now(timezone.utc)
    m = re.match(r"^(\d+)d$", since_str)
    if m:
        return now - timedelta(days=int(m.group(1)))
    try:
        dt = datetime.fromisoformat(since_str)
        return dt if dt.tzinfo else dt.replace(tzinfo=timezone.utc)
    except ValueError:
        print(json.dumps({"error": f"Invalid --since: {since_str}"}), file=sys.stderr)
        sys.exit(1)


def parse_ts(ts_str):
    try:
        s = ts_str.rstrip("Z")
        if "+" not in s and "-" not in s[10:]:
            s += "+00:00"
        return datetime.fromisoformat(s)
    except (ValueError, TypeError):
        return None


def read_subagent_file(filepath):
    """Read a subagent JSONL: extract first timestamp, turn count, and sum token usage."""
    totals = {"input": 0, "output": 0, "cache_create": 0, "cache_read": 0, "turns": 0}
    first_ts = None
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            for line in f:
                try:
                    entry = json.loads(line)
                except json.JSONDecodeError:
                    continue
                # Grab first timestamp
                if first_ts is None and entry.get("timestamp"):
                    first_ts = parse_ts(entry["timestamp"])
                # Count turns and sum usage from assistant messages
                if entry.get("type") == "assistant":
                    u = entry.get("message", {}).get("usage", {})
                    if u:
                        totals["turns"] += 1
                        totals["input"] += u.get("input_tokens", 0)
                        totals["output"] += u.get("output_tokens", 0)
                        totals["cache_create"] += u.get("cache_creation_input_tokens", 0)
                        totals["cache_read"] += u.get("cache_read_input_tokens", 0)
    except (OSError, UnicodeDecodeError):
        pass
    totals["total"] = totals["input"] + totals["output"] + totals["cache_create"] + totals["cache_read"]
    return first_ts, totals


def get_agent_invocations_from_parent(filepath, cutoff):
    """Extract Agent tool_use calls from a parent JSONL. Returns list of {type, name, desc, timestamp}."""
    invocations = []
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            for line in f:
                if '"Agent"' not in line:
                    continue
                try:
                    entry = json.loads(line)
                except json.JSONDecodeError:
                    continue
                if entry.get("type") != "assistant":
                    continue
                for item in entry.get("message", {}).get("content", []):
                    if item.get("type") == "tool_use" and item.get("name") == "Agent":
                        ts = entry.get("timestamp", "")
                        if cutoff and ts:
                            dt = parse_ts(ts)
                            if dt and dt < cutoff:
                                continue
                        inp = item.get("input", {})
                        invocations.append({
                            "agent_type": inp.get("subagent_type", "general-purpose"),
                            "agent_name": inp.get("name", ""),
                            "description": inp.get("description", ""),
                            "timestamp": ts,
                        })
    except (OSError, UnicodeDecodeError):
        pass
    return invocations


def scan_session(parent_jsonl, cutoff, project_filter=None):
    """Process one session: identity from parent, costs from subagent files.
    Matches by closest timestamp — parent records when Agent was called,
    subagent's first entry records when it started. Should be within seconds.
    Returns (results, unmatched_count)."""
    proj_name = decode_project_name(parent_jsonl.parent.name)
    if project_filter and proj_name.lower() != project_filter.lower():
        return [], 0

    # Skip old files
    if cutoff:
        try:
            if datetime.fromtimestamp(parent_jsonl.stat().st_mtime, tz=timezone.utc) < cutoff:
                return [], 0
        except OSError:
            return [], 0

    # Get agent identities from parent
    identities = get_agent_invocations_from_parent(parent_jsonl, cutoff)
    if not identities:
        return [], 0

    # Read all subagent files: first timestamp + token totals
    session_id = parent_jsonl.stem
    sub_dir = parent_jsonl.parent / session_id / "subagents"
    subagents = []  # list of (first_ts, totals)
    if sub_dir.exists():
        for sf in sub_dir.glob("agent-*.jsonl"):
            first_ts, totals = read_subagent_file(sf)
            if first_ts:
                subagents.append({"ts": first_ts, "totals": totals, "matched": False})

    # Match each parent invocation to the closest-timestamp subagent
    empty_cost = {"input": 0, "output": 0, "cache_create": 0, "cache_read": 0, "total": 0, "turns": 0}
    results = []
    unmatched = 0
    for identity in identities:
        parent_ts = parse_ts(identity["timestamp"]) if identity["timestamp"] else None
        best_match = None
        best_delta = None

        if parent_ts:
            for sub in subagents:
                if sub["matched"]:
                    continue
                delta = abs((parent_ts - sub["ts"]).total_seconds())
                if best_delta is None or delta < best_delta:
                    best_delta = delta
                    best_match = sub

        # Only accept matches within 60 seconds — beyond that it's likely wrong
        matched = False
        if best_match and best_delta is not None and best_delta < 60:
            best_match["matched"] = True
            cost = best_match["totals"]
            matched = True
        else:
            cost = empty_cost
            unmatched += 1

        results.append({
            "agent_type": identity["agent_type"],
            "agent_name": identity["agent_name"],
            "description": identity["description"],
            "timestamp": identity["timestamp"],
            "project": proj_name,
            "turns": cost["turns"],
            "input_tokens": cost["input"],
            "output_tokens": cost["output"],
            "cache_creation_tokens": cost["cache_create"],
            "cache_read_tokens": cost["cache_read"],
            "total_tokens": cost["total"],
            "matched": matched,
        })

    return results, unmatched


def scan_all(cutoff, project_filter=None):
    """Walk all sessions and collect agent invocations with real costs.
    Returns (invocations, sessions_scanned, unmatched_count)."""
    projects_dir = get_projects_dir()
    all_invocations = []
    sessions_scanned = 0
    total_unmatched = 0
    if not projects_dir.exists():
        return all_invocations, sessions_scanned, total_unmatched
    for proj_dir in projects_dir.iterdir():
        if not proj_dir.is_dir():
            continue
        for jsonl in proj_dir.glob("*.jsonl"):
            sessions_scanned += 1
            results, unmatched = scan_session(jsonl, cutoff, project_filter)
            all_invocations.extend(results)
            total_unmatched += unmatched
    return all_invocations, sessions_scanned, total_unmatched


def scan_disk_agents():
    agents = []
    gd = get_global_agents_dir()
    if gd.exists():
        for f in sorted(gd.glob("*.md")):
            agents.append({"name": f.stem, "scope": "global", "project": "global", "path": str(f)})
    desktop = get_desktop_path()
    if desktop.exists():
        for pd in sorted(desktop.iterdir()):
            if not pd.is_dir():
                continue
            ad = pd / ".claude" / "agents"
            if ad.exists():
                for f in sorted(ad.glob("*.md")):
                    agents.append({"name": f.stem, "scope": "project", "project": pd.name, "path": str(f)})
    return agents


def action_summary(cutoff, project_filter, since_label):
    invocations, sessions_scanned, unmatched = scan_all(cutoff, project_filter)
    by_type = defaultdict(list)
    for inv in invocations:
        by_type[inv["agent_type"]].append(inv)

    agents = []
    for atype, invs in sorted(by_type.items(), key=lambda x: -len(x[1])):
        projects = defaultdict(int)
        for inv in invs:
            projects[inv["project"]] += 1
        il = [i["input_tokens"] for i in invs]
        ol = [i["output_tokens"] for i in invs]
        wl = [i["input_tokens"] + i["output_tokens"] for i in invs]
        cl = [i["cache_creation_tokens"] + i["cache_read_tokens"] for i in invs]
        tl = [i["total_tokens"] for i in invs]
        ts = [i["timestamp"] for i in invs if i["timestamp"]]
        turns_list = [i.get("turns", 0) for i in invs]
        agents.append({
            "agent_type": atype,
            "invocations": len(invs),
            "projects": dict(projects),
            "avg_turns": sum(turns_list) // len(turns_list) if turns_list else 0,
            "avg_work_tokens": sum(wl) // len(wl) if wl else 0,
            "avg_cache_tokens": sum(cl) // len(cl) if cl else 0,
            "avg_total_tokens": sum(tl) // len(tl) if tl else 0,
            "avg_input_tokens": sum(il) // len(il) if il else 0,
            "avg_output_tokens": sum(ol) // len(ol) if ol else 0,
            "last_used": max(ts) if ts else "",
        })
    total_work = sum(i["input_tokens"] + i["output_tokens"] for i in invocations)
    total_all = sum(i["total_tokens"] for i in invocations)

    # Fetch weekly usage context
    usage = fetch_weekly_usage()
    usage_info = {}
    if usage:
        usage_info = {
            "weekly_utilization_pct": round(usage["utilization"], 1),
            "weekly_resets_at": usage["resets_at"],
        }

    caveats = [
        f"Based on {sessions_scanned} sessions on disk.",
        "Deleted sessions not included.",
        "Per-agent costs matched by timestamp proximity (<60s); approximate.",
    ]
    if unmatched > 0:
        caveats.append(f"{unmatched} invocation(s) could not be matched to subagent files (counted with 0 tokens).")

    result = {
        "period": since_label,
        "total_invocations": len(invocations),
        "agent_types": len(agents),
        "sessions_scanned": sessions_scanned,
        "unmatched_invocations": unmatched,
        "total_work_tokens": total_work,
        "total_usage_tokens": total_all,
        "caveats": caveats,
        "agents": agents,
    }
    if usage_info:
        result["weekly_usage"] = usage_info
    print(json.dumps(result, indent=2))


def action_detail(agent_type, cutoff, project_filter, since_label):
    invocations, _, _ = scan_all(cutoff, project_filter)
    matching = [i for i in invocations if i["agent_type"].lower() == agent_type.lower()]
    if not matching:
        matching = [i for i in invocations if i.get("agent_name", "").lower() == agent_type.lower()]
    if not matching:
        print(json.dumps({"error": f"No invocations found for '{agent_type}'"}), file=sys.stderr)
        sys.exit(1)
    projects = defaultdict(int)
    for inv in matching:
        projects[inv["project"]] += 1
    il = [i["input_tokens"] for i in matching]
    ol = [i["output_tokens"] for i in matching]
    wl = [i["input_tokens"] + i["output_tokens"] for i in matching]
    cl = [i["cache_creation_tokens"] + i["cache_read_tokens"] for i in matching]
    tl = [i["total_tokens"] for i in matching]
    turns_list = [i.get("turns", 0) for i in matching]
    ts = sorted([i["timestamp"] for i in matching if i["timestamp"]])
    descs = list(set(i["description"] for i in matching if i["description"]))[:10]
    print(json.dumps({
        "agent_type": agent_type, "period": since_label, "invocations": len(matching),
        "projects": dict(projects),
        "avg_turns": sum(turns_list) // len(turns_list) if turns_list else 0,
        "min_turns": min(turns_list) if turns_list else 0,
        "max_turns": max(turns_list) if turns_list else 0,
        "avg_work_tokens": sum(wl) // len(wl) if wl else 0,
        "avg_cache_tokens": sum(cl) // len(cl) if cl else 0,
        "avg_total_tokens": sum(tl) // len(tl) if tl else 0,
        "min_work_tokens": min(wl) if wl else 0,
        "max_work_tokens": max(wl) if wl else 0,
        "min_total_tokens": min(tl) if tl else 0,
        "max_total_tokens": max(tl) if tl else 0,
        "avg_input_tokens": sum(il) // len(il) if il else 0,
        "avg_output_tokens": sum(ol) // len(ol) if ol else 0,
        "first_seen": ts[0] if ts else "", "last_seen": ts[-1] if ts else "",
        "sample_descriptions": descs,
    }, indent=2))


def action_unused(cutoff, since_label):
    """Find agents on disk that have no evidence of invocation.

    Matching signals (checked in order, any match = agent is considered used):
    1. agent_type from parent JSONL's subagent_type field (e.g. "fasciculus", "Explore")
    2. agent_name from parent's input.name field (often empty for ad-hoc Agent calls)
    3. Agent filename stem appearing as a substring in any invocation description

    Signal 3 catches cases where an agent is referenced in the prompt description
    (e.g. "Ask the office-manager to..." or "office-manager-checkpoint") but the
    explicit type/name fields don't match the file stem exactly.
    """
    invocations, _, _ = scan_all(cutoff, project_filter=None)
    disk_agents = scan_disk_agents()

    # Signals 1 & 2: explicit type/name fields
    invoked = {i["agent_type"].lower() for i in invocations}
    invoked |= {i["agent_name"].lower() for i in invocations if i["agent_name"]}

    # Signal 3: description substring match
    descriptions = [i["description"].lower() for i in invocations if i.get("description")]

    unused = []
    for a in disk_agents:
        name_lower = a["name"].lower()
        if name_lower in invoked:
            continue
        # Also check if the agent name appears in any invocation description
        if any(name_lower in d for d in descriptions):
            continue
        unused.append(a)

    print(json.dumps({
        "period": since_label,
        "total_agents_on_disk": len(disk_agents),
        "total_invoked": len(disk_agents) - len(unused),
        "total_unused": len(unused),
        "unused_agents": unused,
        "matching_signals": ["subagent_type", "input.name", "description substring"],
    }, indent=2))


def main():
    parser = argparse.ArgumentParser(
        description="Level Up — Agent Usage Stats. Identity from parent JSONL, costs from subagent JSONL.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --action summary                         Last 7 days
  %(prog)s --action summary --since 30d             Last 30 days
  %(prog)s --action detail --agent-type fasciculus   Deep dive
  %(prog)s --action unused --since all               All-time unused

Note: Per-agent token costs are approximate. Agent identity comes from the
parent session JSONL, token costs come from subagent JSONL files, matched by
timestamp proximity (<60s). There is no direct link between the two in the
Claude Code JSONL format. Totals and invocation counts are accurate; per-agent
cost attribution should be treated as best-effort.
        """)
    parser.add_argument("--action", required=True, choices=["summary", "detail", "unused"])
    parser.add_argument("--agent-type", help="Agent type for detail action")
    parser.add_argument("--since", default="7d", help="7d (default), 30d, all, or ISO date")
    parser.add_argument("--project", help="Filter to one project")
    args = parser.parse_args()
    cutoff = parse_since(args.since)
    since_label = f"last {args.since}" if args.since != "all" else "all time"
    if args.action == "summary":
        action_summary(cutoff, args.project, since_label)
    elif args.action == "detail":
        if not args.agent_type:
            print(json.dumps({"error": "--agent-type required"}), file=sys.stderr)
            sys.exit(1)
        action_detail(args.agent_type, cutoff, args.project, since_label)
    elif args.action == "unused":
        action_unused(cutoff, since_label)


if __name__ == "__main__":
    main()

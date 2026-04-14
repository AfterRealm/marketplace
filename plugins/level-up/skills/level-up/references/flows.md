# Level Up v1.1.0 — Extended Flows

Load this file only if SKILL.md references it for additional detail. The primary flows are fully described in SKILL.md itself — this file exists for edge cases and the granular merge fallback.

## Granular Merge (fallback — only if user requests control)

If the user doesn't like the smart-merged result and wants granular control:

1. Present the section comparison from merge-prep JSON:
   - Common sections (present in both)
   - Unique sections (only in one)
   - Frontmatter differences
2. For each common section, ask in plain text: "Keep from Agent 1, Agent 2, or combine?"
3. For unique sections, ask: "Include or skip?"
4. Assemble the result, ask for name + scope, save, verify

## Stats — Detail Drill-Down

If the user wants to drill into a specific agent after seeing the summary:

```
Agent(description: "Agent detail stats", prompt: "Run: python \"<STATS_PATH>\" --action detail --agent-type \"TYPE\" --since PERIOD
Parse the JSON. Show: invocation count, avg/min/max work tokens, avg total tokens, per-project breakdown, first/last seen, sample task descriptions.")
```

## Stats — Period Change

If the user wants a different time window, re-run the summary subagent with `--since 30d` or `--since all`. No pickers needed — the user just says "show me all time" or "last 30 days."

## Versioning (not in menu — available via script)

The `scan_agents.py` script still supports `--action version`, `--action list-versions`, and `--action version --restore`. These are available if a user asks directly ("snapshot my agent", "rollback fasciculus"). They just aren't in the 4-option menu. Handle them via plain text if triggered.

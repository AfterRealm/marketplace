# Changelog

## v1.1.0 — 2026-04-13

### Added
- **Merge action** — Combine two agents into one via `scan_agents.py --action merge-prep` and a smart-merge subagent flow (granular merge available as fallback)
- **Stats action** — New `agent_stats.py` script scans subagent JSONL files for real token costs with work/cache breakdown, turn counts, and weekly budget context from Anthropic's usage API
- **Optimization audit flow** — After Stats, offer to audit any agent's definition against its usage patterns and suggest reductions in turns, cache growth, or redundant work

### Changed
- **Intent-first routing** — Skip scan+menu when user's intent is clear from the trigger; fall back to scan+menu only for ambiguous prompts
- **One AskUserQuestion per invocation** — Action menu only; all follow-ups are plain chat messages. Every picker is a full context re-read; keep them minimal
- **Merge flow redesigned** — Smart merge by default (auto-combine everything, present result for approval); granular section-by-section merge is a fallback option
- **SKILL.md consolidated** — Single `## Rules` section, glossary at top, changelog extracted to this file

### Fixed
- **Hardcoded username in `decode_project_name`** — Now derived dynamically from `Path.home()`
- **Inspect subagent prompt missing `--project`** — Could match wrong agent when names duplicated across projects
- **Description field in skill** — Replaced "JSONL session files" with "session history" (user-facing language)
- **Order-based parent/subagent matching** — Replaced with timestamp proximity matching (<60s window)
- **Silent under-counting of unmatched invocations** — Summary output now exposes `unmatched_invocations` count and flags it in caveats
- **Unused agent detection matching** — Now uses three signals (subagent_type, input.name, description substring) for better coverage
- **Caveat note format** — Replaced single prose string with a `caveats` array for cleaner rendering

### Removed from menu
- **Create** — Claude handles agent creation natively; no skill needed. Trigger description now documents this explicitly.
- **Version** — Niche feature; `scan_agents.py` still supports `--action version`, `--action list-versions`, and `--action version --restore` if a user asks directly. Just not surfaced in the 4-option menu.

### Output format additions
- `sessions_scanned` — Count of JSONL files walked
- `unmatched_invocations` — Count of parent invocations that couldn't be paired to a subagent file
- `weekly_usage` — Object with `weekly_utilization_pct` and `weekly_resets_at` (when Anthropic OAuth token is available)
- `caveats` — Array of short caveats replacing the previous single note string
- Per-agent `avg_turns`, `avg_work_tokens`, `avg_cache_tokens`, `avg_total_tokens` — Broken out so users can see the difference between what an agent actually does and what it costs

## v1.0.0 — Initial release

- Scan all agents across global + Desktop project `.claude/agents/` directories
- Inspect agent source
- Promote & Adapt agents from project scope to global
- Create new agents via walkthrough

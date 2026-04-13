---
name: level-up
description: >-
  Use this skill when the user wants to manage, inspect, create, promote, or organize their Claude Code agents.
  IMPORTANT: You cannot discover what agents exist across projects without this skill — it contains
  scanner scripts that search all .claude/agents/ directories across every project and global scope.
  Triggers: "list my agents", "show agents", "create an agent", "promote agent to global",
  "copy agent", "what agents do I have", "agent manager", "level up", "manage agents",
  "move agent to global", "make this agent available everywhere", "which agents are where",
  or any follow-up like "move that one to global" when agents are being discussed.
  Do NOT trigger for: running an existing agent (/agents), debugging agent errors,
  asking about agent capabilities, or general questions about what agents are.
license: MIT
compatibility: Requires Python 3.x for the scanner script
metadata:
  author: AfterRealm
  version: "1.0.0"
---

# Level Up — An Agent Promotion Skill

Manage, inspect, create, and promote your Claude Code agents across projects and global scope.

## Architecture

This skill uses a **split approach** to save context:

- **Heavy work** (scanning, inspecting, adapting) runs in a **subagent** so the large JSON payloads and file contents stay out of the main session context
- **User interaction** (menus, approval) stays in the **main thread** since AskUserQuestion only works there
- The subagent returns a compact summary; the main thread presents it and handles navigation

## Path Resolution

Before any action, resolve the scanner script path once. The script lives at:
`SKILL_DIR/scripts/scan_agents.py`

Where `SKILL_DIR` is this skill's base directory. Store the resolved absolute path and pass it into ALL subagent prompts as a concrete path — subagents cannot resolve `SKILL_DIR` themselves.

Example: if the skill is at `C:\Users\me\.claude\skills\level-up`, the scanner is `C:\Users\me\.claude\skills\level-up\scripts\scan_agents.py`. Use that full path in every subagent prompt.

## Flow

### Step 1: Scan (subagent)

Resolve the scanner path, then spawn an Agent:

```
Agent(description: "Scan agents", prompt: "Run: python \"<RESOLVED_SCANNER_PATH>\" --action list
Parse the JSON. Return ONLY a compact summary in this format:
GLOBAL: agent1, agent2
PROJECT_NAME (count): agent1, agent2, agent3
...one line per project, agents comma-separated. Include model in parens if set. Nothing else.")
```

If the scan returns zero agents, skip the action menu entirely and offer: "No agents found anywhere. Want to create your first one?" Then go directly to the Create flow.

Present the summary to the user in this format:

```
**GLOBAL** — agent1, agent2
**Ark Claude** (14) — Accountant (sonnet), BP Architect (sonnet), ...
**Vox Memori** (4) — Architect (opus), Neurologist (opus), ...
```

Bold project names, agent count in parens, comma-separated agents with model.

### Step 2: Action Menu

AskUserQuestion with 4 options:

1. **Inspect** — View the full source of an agent
2. **Promote & Adapt** — Copy or adapt an agent to a different scope
3. **Create** — Build a new agent from scratch

### Agent Picker (used by ALL actions except Create)

Always use the two-step picker — project first, then agent. This prevents ambiguity with duplicate names (e.g., "Architect" exists in 3 projects).

**Step A — Pick the project.** Show up to 3 projects per page. If more than 3, the 4th option is "More projects..." for the next page.

**Step B — Pick the agent.** List that project's agents. Show up to 3 per page with descriptions. If more than 3, the 4th option is "More agents..." to paginate.

Never skip Step A, even for Inspect. Duplicate agent names across projects are common.

### If Inspect (subagent)

After agent picker, spawn a subagent with the resolved scanner path:

```
Agent(description: "Inspect agent", prompt: "Run: python \"<RESOLVED_SCANNER_PATH>\" --action inspect --name \"AGENT_NAME\"
Show the full agent markdown content. Format it readably.")
```

### If Promote & Adapt

After agent picker, AskUserQuestion:

1. **Direct copy** — Promote as-is
2. **Template & adapt** — Rewrite for the new scope

**Direct copy** — spawn subagent:
```
Agent(description: "Promote agent", prompt: "Run: python \"<RESOLVED_SCANNER_PATH>\" --action promote --name \"AGENT_NAME\" --project \"PROJECT\"
Report the result.")
```

**Template & adapt** — spawn subagent:
```
Agent(description: "Adapt agent", prompt: "Run: python \"<RESOLVED_SCANNER_PATH>\" --action inspect --name \"AGENT_NAME\"
Read the full agent source. Identify project-specific references (hardcoded paths, project names, project-specific tools, data references). Rewrite the agent to be generic — replace specific paths with general instructions, broaden scope, keep core role and personality. If the agent has no project-specific references, state that clearly before returning the content unchanged. Return ONLY the adapted markdown content (or the no-changes notice + original content), nothing else.")
```

Show the adapted version to the user. AskUserQuestion: Save it / Edit first. If approved, write to `~/.claude/agents/AGENT_NAME.md`.

### If Create

Walk the user through building a new agent (main thread — needs user input at each step):

1. Ask what the agent should do (role, personality, tools, restrictions)
2. AskUserQuestion for scope: Global / pick a project (use project picker if needed)
3. Ask for a name
4. Write the `.md` file using the agent template below
5. Save to the appropriate `.claude/agents/` directory
6. Run the scanner to verify it appears

**Agent template:**
```markdown
---
name: agent-name
description: One-line description of what this agent does
model: sonnet
tools:
  - Read
  - Glob
  - Grep
  - Bash
---

# Agent Name

You are [role description]. When invoked, you [what the agent does].

## What You Do

[Specific instructions for the agent's behavior]

## Rules

- [Key constraints and guidelines]
```

**Example agents for reference** — show these to the user if they're unsure:

- **Simple reviewer:** Reads code files, checks for issues, reports findings
- **Subagent worker:** Runs scripts, processes output, returns compact results
- **Project specialist:** Deep knowledge of one project, handles project-specific tasks

## Important Notes

- Global agents: `~/.claude/agents/` — available in every project
- Project agents: `<project>/.claude/agents/` — only work in that project
- Agent files are `.md` with YAML frontmatter
- Never delete an agent without explicit user confirmation
- Always check for name collisions before promoting
- Always use the project picker before the agent picker — never skip project selection
- AskUserQuestion max 4 options — paginate with "More..." as 4th when needed
- Heavy operations go to subagents to preserve main session context
- Pass resolved absolute paths to subagents, never SKILL_DIR placeholders

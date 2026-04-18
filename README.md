# AfterRealm Marketplace

Claude Code plugins by [AfterRealm](https://github.com/AfterRealm).

## Install the Marketplace

```bash
claude marketplace add AfterRealm/marketplace
```

## Available Plugins

### Blunt Cake

Brutal, funny code reviewer with 8 modes and 6 personalities. Every finding is real, every roast comes with a fix.

```bash
claude plugin add afterrealm/blunt-cake
```

**Modes:** Standard Roast, Panel Roast (multi-agent), Skill Roast, Eval Mode, Diff Roast, Batter Battle, Roast-a-thon, Roast Challenge

**Personalities:** Chef, Disappointed Grandma, Passive-Aggressive PR Reviewer, Simon Cowell, Snoop Dogg, Pirate, Custom

[Full README](https://github.com/AfterRealm/blunt-cake) | v2.4.0

---

### Father Time

Session-aware time management for Claude Code. Tracks session duration, context usage, and helps you work with your schedule instead of against it.

```bash
claude plugin add afterrealm/father-time
```

**Skills:** Time Menu, Session Timer, Session Health, Peak Hours, Daily Brief, Focus Mode, Pace Check, Context Budget, Activity Patterns

[Full README](https://github.com/AfterRealm/father-time) | v1.8.3

---

### Curb Cut

WCAG 2.2 Level AA accessibility auditor. Scans HTML, JSX, Vue, and Svelte for violations — explains what's wrong, who's affected, and how to fix it.

```bash
claude plugin add afterrealm/curb-cut
```

**Modes:** Quick Scan, Full Audit, Component Check, Report

**Features:** Auto-fix (prefers semantic HTML over ARIA), per-pillar scoring, CI/CD GitHub Action, WAI-ARIA component pattern checks

[Full README](https://github.com/AfterRealm/curb-cut) | v1.1.0

---

### Level Up

Agent management for Claude Code. Inspect, promote, merge, and analyze usage of agents across projects and global scope. One picker, plain-chat follow-ups, heavy work delegated to subagents.

```bash
claude plugin add afterrealm/level-up
```

**Actions:** Inspect, Promote & Adapt, Merge, Stats (with turn counts + weekly budget context), Optimization Audit

**Features:** Real subagent token counting via timestamp matching, work-vs-cache breakdown, unused agent detection, AI-generated optimization suggestions

[Full README](https://github.com/AfterRealm/level-up) | v1.1.0

---

### Claude Voice

Multilingual-first voice input for the **Claude Desktop App** (not the Code CLI). Hold a hotkey, speak any of 99 Whisper languages, transcript pastes into the chat. Lightweight plugin — no MCP, no TTS. Fills the gap while official voice mode is English-only.

```bash
claude plugin add afterrealm/claude-voice
```

**Flow:** `/voice` → pick language + Whisper model + hotkey → hold F8 → speak → release → transcript pastes into Claude.

**Features:** Local `faster-whisper` STT (99 languages), focus safety (only pastes into Claude windows), plugin-local venv install, configurable hotkey + recording cap, first-run macOS/Linux platform warnings.

**Status:** Windows-tested end-to-end. macOS/Linux code paths implemented; [feedback welcome](https://github.com/AfterRealm/claude-voice/issues).

[Full README](https://github.com/AfterRealm/claude-voice) | v0.1.0

## License

MIT

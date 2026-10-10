# AfterRealm Marketplace

Claude Code plugins and Claude-adjacent desktop tools by [AfterRealm](https://github.com/AfterRealm).

## Install the Marketplace

In Claude Code:

```
/plugin marketplace add AfterRealm/marketplace
```

Or from a terminal: `claude plugin marketplace add AfterRealm/marketplace`. Then install any plugin below.

## Available Plugins

### Blunt Cake

Brutal, funny code reviewer with 8 modes and 6 personalities. Every finding is real, every roast comes with a fix.

```
/plugin install blunt-cake@afterrealm
```

**Modes:** Standard Roast, Panel Roast (multi-agent), Skill Roast, Eval Mode, Diff Roast, Batter Battle, Roast-a-thon, Roast Challenge

**Personalities:** Chef, Disappointed Grandma, Passive-Aggressive PR Reviewer, Simon Cowell, Snoop Dogg, Pirate, Custom

[Full README](https://github.com/AfterRealm/blunt-cake) | v2.4.0

---

### Father Time

Session-aware time management for Claude Code. Tracks session duration, context usage, and helps you work with your schedule instead of against it.

```
/plugin install father-time@afterrealm
```

**Skills:** Time Menu, Session Timer, Session Health, Peak Hours, Daily Brief, Focus Mode, Pace Check, Context Budget, Activity Patterns

[Full README](https://github.com/AfterRealm/father-time) | v1.9.0

---

### Curb Cut

WCAG 2.2 Level AA accessibility auditor. Scans HTML, JSX, Vue, and Svelte for violations — explains what's wrong, who's affected, and how to fix it.

```
/plugin install curb-cut@afterrealm
```

**Modes:** Quick Scan, Full Audit, Component Check, Report

**Features:** Auto-fix (prefers semantic HTML over ARIA), per-pillar scoring, CI/CD GitHub Action, WAI-ARIA component pattern checks

[Full README](https://github.com/AfterRealm/curb-cut) | v1.1.1

---

### Level Up

Agent management for Claude Code. Inspect, promote, merge, and analyze usage of agents across projects and global scope. One picker, plain-chat follow-ups, heavy work delegated to subagents.

```
/plugin install level-up@afterrealm
```

**Actions:** Inspect, Promote & Adapt, Merge, Stats (with turn counts + weekly budget context), Optimization Audit

**Features:** Real subagent token counting via timestamp matching, work-vs-cache breakdown, unused agent detection, AI-generated optimization suggestions

[Full README](https://github.com/AfterRealm/level-up) | v1.1.0

---

### Open Voice

Multilingual-first voice input for anywhere you type into Claude — **Desktop App, Claude Code Desktop, or regular Claude Code terminals**. Hold a hotkey, speak any of 99 Whisper languages, transcript pastes into whatever Claude window has focus. Lightweight plugin — no MCP, no TTS. Fills the gap while official voice mode is English-only.

```
/plugin install open-voice@afterrealm
```

**Flow:** `/voice` → pick language + Whisper model + hotkey → hold F8 → speak → release → transcript pastes into Claude.

**Features:** Local `faster-whisper` STT (99 languages), focus safety (only pastes into Claude windows), plugin-local venv install, configurable hotkey + recording cap, first-run macOS/Linux platform warnings.

**Status:** Windows-tested end-to-end. macOS/Linux code paths implemented; [feedback welcome](https://github.com/AfterRealm/open-voice/issues).

[Full README](https://github.com/AfterRealm/open-voice) | v0.3.1

---

### Session Continuity

Detects prior session history for any project at startup and offers to name or rename the session for you automatically, so picking work back up starts with the right name.

```
/plugin install session-continuity@afterrealm
```

[Full README](https://github.com/AfterRealm/session-continuity) | v2.1.2

---

### UE5 Blueprint Skills

Blueprint analysis for Unreal Engine 5. Export Blueprints from a running editor, detect 25+ anti-patterns, and get beginner-friendly fix instructions, all from your terminal.

```
/plugin install ue5-blueprints@afterrealm
```

**Commands:** `/ue5-blueprints:setup`, `blueprint-export`, `blueprint-check`, `blueprint-audit`, `blueprint-fix`

**Requires:** Python 3 with `upyrc`, Node.js, UE5 Editor with the Python Editor Script Plugin enabled.

[Full README](https://github.com/AfterRealm/ue5-blueprint-skills) | v0.1.2

---

## Desktop Apps

Standalone desktop tools that live alongside Claude — not installed as plugins. Download installers directly from each project's GitHub Releases page.

### Image Center

Standalone desktop image processor — no login, no cloud, no Claude required. Drag images in and run **resize**, **compress**, **convert**, **rotate / flip / blur / sharpen / grayscale / invert / trim / crop**, **adjust brightness/contrast/saturation**, **add text**, **remove background** (local ONNX model), chain operations into reusable **macros**, and export individually or as a zip.

Everything runs locally — your images never leave your machine.

**Download:** [latest release](https://github.com/AfterRealm/image-center/releases/latest) — `.exe` for Windows, `.dmg` for macOS (Intel + Apple Silicon).

[Full README](https://github.com/AfterRealm/image-center) | v1.0.0

## License

MIT

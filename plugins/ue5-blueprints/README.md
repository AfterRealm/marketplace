# UE5 Blueprint Skills for Claude Code

The AI-powered Blueprint analysis toolkit for Unreal Engine 5. Export Blueprints from a running editor, detect 25+ anti-patterns, and get beginner-friendly fix instructions — all from your terminal.

## What It Does

**Claude Code gains the ability to see inside your Blueprints.** No more describing your node graph in chat. Export directly from UE5, and Claude reads the actual wiring.

- **Export** Blueprints from a running UE5 Editor via Python remote execution
- **Detect** 25 known anti-patterns (BreakStruct copy bugs, null crashes, memory leaks, performance killers)
- **Audit** entire Blueprint graphs with heuristic health checks
- **Fix** issues with step-by-step instructions written for visual learners, not programmers
- **Reference** 1,864 node cards scraped from Epic's official UE5 Blueprint API docs

## Skills

| Skill | What It Does |
|-------|-------------|
| `/ue5-blueprints:setup` | One-time setup — enables Python remote execution in your UE5 project |
| `/ue5-blueprints:blueprint-export` | Export Blueprints as T3D text or structured JSON from a running editor |
| `/ue5-blueprints:blueprint-check` | Paste Blueprint data and get an instant analysis |
| `/ue5-blueprints:blueprint-audit` | Deep audit of exported data — full pattern scan + graph health checks |
| `/ue5-blueprints:blueprint-fix` | Step-by-step fix instructions for detected bugs |

## Anti-Patterns Detected

**Critical:**
- P-001: BreakStruct Copy Bug — writing to a disconnected copy instead of the original
- P-002: Missing Write-Back — struct modifications that never propagate
- P-013: Latent Node in ForEachLoop — Delay/MoveTo inside loops that silently break

**High:**
- P-003: Uninitialized Variable Read
- P-004: Missing IsValid Check (null crash)
- P-007: Modifying an array while iterating it
- P-011: Pure node re-evaluation in loops
- P-012: Delegate memory leak
- P-014: Delay on Tick (60 pending delays per second)
- P-015: FlipFlop sharing state across all instances
- P-017: GetAllActorsOfClass on Tick
- P-018: Unguarded Array Get (crash)
- P-019: Timer string mismatch (silent failure)
- P-020: Sequence + Latent Node (doesn't wait)
- P-023: Multicast without RepNotify
- P-025: Widget leak (Create Widget without existence check)

**Medium/Low:**
- P-005, P-006, P-008, P-009, P-010, P-016, P-021, P-022, P-024

Plus 15+ heuristic graph health checks for dead-end execution, orphaned nodes, variable safety, and cross-function consistency.

## The Pipeline

```
UE5 Editor
    |
    | Python Remote Execution (upyrc)
    v
T3D Export / JSON Snapshot
    |
    | Wiring Map Generator (Node.js)
    v
Compact Wiring Maps (.md)
    |
    | Pattern Detection + Heuristic Analysis
    v
Findings + Fix Instructions
```

No copy-pasting screenshots. No describing your graph in chat. Claude reads the actual Blueprint data.

## Requirements

- **Claude Code** v2.1.70+
- **Python 3** with `pip install upyrc`
- **Node.js** (for wiring map generation)
- **UE5 Editor** with Python Editor Script Plugin enabled

## Quick Start

```bash
# Install the plugin
claude plugin marketplace add AfterRealm/ue5-blueprint-skills
claude plugin install ue5-blueprints@ue5-blueprint-skills

# One-time setup
/ue5-blueprints:setup

# Export your Blueprint
/ue5-blueprints:blueprint-export

# Analyze it
/ue5-blueprints:blueprint-audit

# Fix what's broken
/ue5-blueprints:blueprint-fix
```

## Knowledge Base

### Node Cards (1,864)
Scraped from Epic's official UE5 Blueprint API documentation. Organized into 52 categories:

Actor, Array, Blueprint, Class, Collision, Components, Data, DataTable, Debug, DynamicMesh, Event, EventDispatchers, Game, Gameplay, GameState, General, Input, Interaction, Level, Material, Math, Mesh, Naming, Pawn, Physics, PlayerController, Rendering, Set, SkeletalMesh, Spawning, StaticMesh, String, Struct, Tick, Transformation, UMG, UserInterface, Utilities, Variables, Widget, and more.

Each card includes: node name, category, search term, target class, inputs/outputs with pin types, and description.

### Language System
All instructions follow strict Blueprint-native rules:
- Pin colors and sides always specified
- Exact search terms for node placement
- Sequential steps only (never forward references)
- Beginner-friendly terminology (node, pin, wire — not block, port, line)

## License

MIT

## Move Component To
**Category:** Components
**Search:** "Move Component To"
**Target:** Kismet System Library

**Inputs:**
- Move (exec) — Move to target over specified time.
- Stop (exec) — If currently moving, stop.
- Return (exec) — If currently moving, return to where you started, over the time elapsed so far.
- Component (object) — Component to interpolate *
- Target Relative Location (vector) — Relative target location *
- Target Relative Rotation (rotator) — Relative target rotation *
- Ease Out (boolean) — if true we will ease out (ie end slowly) during interpolation *
- Ease In (boolean) — if true we will ease in (ie start slowly) during interpolation *
- Over Time (real) — duration of interpolation *
- Force Shortest Rotation Path (boolean) — if true we will always use the shortest path for rotation *

**Outputs:**
- Completed (exec)

**Description:** Interpolate a component to the specified relative location and rotation over the course of OverTime seconds. *
---

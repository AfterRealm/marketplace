## Suggest Projectile Velocity Custom Arc
**Category:** Game
**Search:** "Suggest Projectile Velocity Custom Arc"
**Target:** Gameplay Statics

**Inputs:**
- In (exec)
- Start Pos (vector) — Start position of the simulation
- End Pos (vector) — Desired end location for the simulation
- Override Gravity Z (real) — Optional override of WorldGravityZ
- Arc Param (real) — Change height of arc between 0.0-1.0 where 0.5 is the default medium arc, 0 is up, and 1 is directly toward EndPos.

**Outputs:**
- Out (exec)
- Out Launch Velocity (vector) — Returns the launch velocity required to reach the EndPos
- Return Value (boolean)

**Description:** Returns the launch velocity needed for a projectile at rest at StartPos to land on EndPos. Assumes a medium arc (e.g. 45 deg on level ground). Projectile velocity is variable and unconstrained. Does no tracing.
---

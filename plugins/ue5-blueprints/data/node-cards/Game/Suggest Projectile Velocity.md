## Suggest Projectile Velocity
**Category:** Game
**Search:** "Suggest Projectile Velocity"
**Target:** Gameplay Statics

**Inputs:**
- In (exec)
- Start Location (vector) — Intended launch location
- End Location (vector) — Desired landing location
- Launch Speed (real) — Desired launch speed
- Override Gravity Z (real) — Optional gravity override. 0 means "do not override".
- Trace Option (enum) — Controls whether or not to validate a clear path by tracing along the calculated arc
- Collision Radius (real) — Radius of the projectile (assumed spherical), used when tracing
- Favor High Arc (boolean) — If true and there are 2 valid solutions, will return the higher arc. If false, will favor the lower arc.
- Draw Debug (boolean) — When true, a debug arc is drawn (red for an invalid arc, green for a valid arc)
- Accept Closest on No Solutions (boolean) — If target is unreachable and no solutions are possible, provide a velocity that gets as close to the target as possible given this launch speed

**Outputs:**
- Out (exec)
- Toss Velocity (vector) — (output) Result launch velocity.
- Return Value (boolean) — Returns false if there is no valid solution or the valid solutions are blocked. Returns true otherwise.

**Description:** Calculates an launch velocity for a projectile to hit a specified point.
---

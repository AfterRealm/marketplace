## Predict Projectile Path (Advanced)
**Category:** Game
**Search:** "Predict Projectile Path (Advanced)"
**Target:** Gameplay Statics

**Inputs:**
- In (exec)
- Predict Params (struct) — Input params to the trace (start location, velocity, time to simulate, etc).

**Outputs:**
- Out (exec)
- Predict Result (struct) — Output result of the trace (Hit result, array of location/velocity/times for each trace step, etc).
- Return Value (boolean) — True if hit something along the path (if tracing with collision).

**Description:** Predict the arc of a virtual projectile affected by gravity with collision checks along the arc. Returns true if it hit something.
---

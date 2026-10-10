## Predict Projectile Path By TraceChannel
**Category:** Game
**Search:** "Predict Projectile Path By TraceChannel"
**Target:** Gameplay Statics

**Inputs:**
- In (exec)
- Start Pos (vector) — First start trace location
- Launch Velocity (vector) — Velocity the "virtual projectile" is launched at
- Trace Path (boolean) — Trace along the entire path to look for blocking hits
- Projectile Radius (real) — Radius of the virtual projectile to sweep against the environment
- Trace Channel (enum) — TraceChannel to trace against, if bTracePath is true.
- Trace Complex (boolean) — Use TraceComplex (trace against triangles not primitives)
- Actors to Ignore (object) — Actors to exclude from the traces
- Draw Debug Type (enum) — Debug type (one-frame, duration, persistent)
- Draw Debug Time (real) — Duration of debug lines (only relevant for DrawDebugType::Duration)
- Sim Frequency (real) — Determines size of each sub-step in the simulation (chopping up MaxSimTime)
- Max Sim Time (real) — Maximum simulation time for the virtual projectile.
- Override Gravity Z (real) — Optional override of Gravity (if 0, uses WorldGravityZ)

**Outputs:**
- Out (exec)
- Out Hit (struct) — Predicted hit result, if the projectile will hit something
- Out Path Positions (vector) — Predicted projectile path. Ordered series of positions from StartPos to the end. Includes location at point of impact if it hit something.
- Out Last Trace Destination (vector) — Goal position of the final trace it did. Will not be in the path if there is a hit.
- Return Value (boolean) — True if hit something along the path (if tracing with collision).

**Description:** Predict the arc of a virtual projectile affected by gravity with collision checks along the arc. Returns a list of positions of the simulated arc and the destination reached by the simulation. Returns true if it hit something (if tracing with collision).
---

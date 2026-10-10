## Sphere Trace Component
**Category:** Collision
**Search:** "Sphere Trace Component"
**Target:** Primitive Component

**Inputs:**
- In (exec)
- Target (object)
- Trace Start (vector) — The start of the trace in world-space
- Trace End (vector) — The end of the trace in world-space
- Sphere Radius (real) — Radius of the sphere to trace against the component
- Trace Complex (boolean) — Whether or not to trace the complex physics representation or just the simple representation
- Show Trace (boolean) — Whether or not to draw the trace in the world (for debugging)
- Persistent Show Trace (boolean) — Whether or not to make the debugging draw stay in the world permanently

**Outputs:**
- Out (exec)
- Hit Location (vector)
- Hit Normal (vector)
- Bone Name (name)
- Out Hit (struct)
- Return Value (boolean)

**Description:** Perform a sphere trace against a single component
---

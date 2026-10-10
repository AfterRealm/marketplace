## Sphere Overlap Component
**Category:** Collision
**Search:** "Sphere Overlap Component"
**Target:** Primitive Component

**Inputs:**
- In (exec)
- Target (object)
- In Sphere Centre (vector) — The centre of the sphere to overlap with the component
- In Sphere Radius (real) — The Radius of the sphere to overlap with the component
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

**Description:** Perform a sphere overlap against a single component
---

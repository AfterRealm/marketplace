## Box Overlap Component
**Category:** Collision
**Search:** "Box Overlap Component"
**Target:** Primitive Component

**Inputs:**
- In (exec)
- Target (object)
- In Box Centre (vector) — The centre of the box to overlap with the component
- In Box (struct) — Description of the box to use in the overlap
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

**Description:** Perform a box overlap against a single component as an AABB (No rotation)
---

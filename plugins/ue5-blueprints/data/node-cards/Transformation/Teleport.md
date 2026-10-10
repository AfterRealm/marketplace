## Teleport
**Category:** Transformation
**Search:** "Teleport"
**Target:** Actor

**Inputs:**
- In (exec)
- Target (object)
- Dest Location (vector) — The target destination point
- Dest Rotation (rotator) — The target rotation at the destination

**Outputs:**
- Out (exec)
- Return Value (boolean) — true if the actor has been successfully moved, or false if it couldn't fit.

**Description:** Teleport this actor to a new location. If the actor doesn't fit exactly at the location specified, tries to slightly move it out of walls and such.
---

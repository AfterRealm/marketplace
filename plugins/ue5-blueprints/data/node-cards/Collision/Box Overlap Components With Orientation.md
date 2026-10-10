## Box Overlap Components With Orientation
**Category:** Collision
**Search:** "Box Overlap Components With Orientation"
**Target:** Kismet System Library

**Inputs:**
- In (exec)
- Box Pos (vector) — Center of box.
- Extent (vector) — Extents of box.
- Orientation (rotator) — Orientation of the box.
- Object Types (enum)
- Component Class Filter (class)
- Actors to Ignore (object) — Ignore these actors in the list

**Outputs:**
- Out (exec)
- Out Components (object)
- Return Value (boolean) — true if there was an overlap that passed the filters, false otherwise.

**Description:** Returns an array of components that overlap the given box.
---

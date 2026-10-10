## Box Overlap Actors With Orientation
**Category:** Collision
**Search:** "Box Overlap Actors With Orientation"
**Target:** Kismet System Library

**Inputs:**
- In (exec)
- Box Pos (vector) — Center of box.
- Box Extent (vector) — Extents of box.
- Orientation (rotator) — Orientation of the box.
- Object Types (enum)
- Actor Class Filter (class)
- Actors to Ignore (object) — Ignore these actors in the list

**Outputs:**
- Out (exec)
- Out Actors (object) — Returned array of actors. Unsorted.
- Return Value (boolean) — true if there was an overlap that passed the filters, false otherwise.

**Description:** Returns an array of actors that overlap the given axis-aligned box.
---

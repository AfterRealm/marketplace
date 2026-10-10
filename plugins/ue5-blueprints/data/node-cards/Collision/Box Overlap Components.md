## Box Overlap Components
**Category:** Collision
**Search:** "Box Overlap Components"
**Target:** Kismet System Library

**Inputs:**
- In (exec)
- Box Pos (vector) — Center of box.
- Extent (vector)
- Object Types (enum)
- Component Class Filter (class)
- Actors to Ignore (object) — Ignore these actors in the list

**Outputs:**
- Out (exec)
- Out Components (object)
- Return Value (boolean) — true if there was an overlap that passed the filters, false otherwise.

**Description:** Returns an array of components that overlap the given axis-aligned box.
---

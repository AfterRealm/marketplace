## Sphere Overlap Components
**Category:** Collision
**Search:** "Sphere Overlap Components"
**Target:** Kismet System Library

**Inputs:**
- In (exec)
- Sphere Pos (vector) — Center of sphere.
- Sphere Radius (real) — Size of sphere.
- Object Types (enum)
- Component Class Filter (class)
- Actors to Ignore (object) — Ignore these actors in the list

**Outputs:**
- Out (exec)
- Out Components (object)
- Return Value (boolean) — true if there was an overlap that passed the filters, false otherwise.

**Description:** Returns an array of components that overlap the given sphere.
---

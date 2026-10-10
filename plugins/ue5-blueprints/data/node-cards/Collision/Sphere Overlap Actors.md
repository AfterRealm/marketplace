## Sphere Overlap Actors
**Category:** Collision
**Search:** "Sphere Overlap Actors"
**Target:** Kismet System Library

**Inputs:**
- In (exec)
- Sphere Pos (vector) — Center of sphere.
- Sphere Radius (real) — Size of sphere.
- Object Types (enum)
- Actor Class Filter (class)
- Actors to Ignore (object) — Ignore these actors in the list

**Outputs:**
- Out (exec)
- Out Actors (object) — Returned array of actors. Unsorted.
- Return Value (boolean) — true if there was an overlap that passed the filters, false otherwise.

**Description:** Returns an array of actors that overlap the given sphere.
---

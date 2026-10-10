## Component Overlap Actors
**Category:** Collision
**Search:** "Component Overlap Actors"
**Target:** Kismet System Library

**Inputs:**
- In (exec)
- Component (object) — Component to test with.
- Component Transform (transform) — Defines where to place the component for overlap testing.
- Object Types (enum)
- Actor Class Filter (class)
- Actors to Ignore (object) — Ignore these actors in the list

**Outputs:**
- Out (exec)
- Out Actors (object) — Returned array of actors. Unsorted.
- Return Value (boolean) — true if there was an overlap that passed the filters, false otherwise.

**Description:** Returns an array of actors that overlap the given component.
---

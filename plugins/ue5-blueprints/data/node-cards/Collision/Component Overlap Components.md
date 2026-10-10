## Component Overlap Components
**Category:** Collision
**Search:** "Component Overlap Components"
**Target:** Kismet System Library

**Inputs:**
- In (exec)
- Component (object) — Component to test with.
- Component Transform (transform) — Defines where to place the component for overlap testing.
- Object Types (enum)
- Component Class Filter (class)
- Actors to Ignore (object) — Ignore these actors in the list

**Outputs:**
- Out (exec)
- Out Components (object)
- Return Value (boolean) — true if there was an overlap that passed the filters, false otherwise.

**Description:** Returns an array of components that overlap the given component.
---

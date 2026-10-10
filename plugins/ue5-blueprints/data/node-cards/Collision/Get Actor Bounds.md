## Get Actor Bounds
**Category:** Collision
**Search:** "Get Actor Bounds"
**Target:** Actor

**Inputs:**
- Target (object)
- Only Colliding Components (boolean) — If true, will only return the bounding box for components with collision enabled.
- Include from Child Actors (boolean) — If true then recurse in to ChildActor components

**Outputs:**
- Origin (vector) — Set to the center of the actor in world space
- Box Extent (vector) — Set to half the actor's size in 3d space

**Description:** Returns the bounding box of all components that make up this Actor (excluding ChildActorComponents).
---

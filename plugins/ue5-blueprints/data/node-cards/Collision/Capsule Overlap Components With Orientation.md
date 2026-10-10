## Capsule Overlap Components With Orientation
**Category:** Collision
**Search:** "Capsule Overlap Components With Orientation"
**Target:** Kismet System Library

**Inputs:**
- In (exec)
- Capsule Pos (vector) — Center of the capsule.
- Radius (real) — Radius of capsule hemispheres and radius of center cylinder portion.
- Half Height (real) — Half-height of the capsule (from center of capsule to tip of hemisphere.
- Orientation (rotator) — Orientation of the box.
- Object Types (enum)
- Component Class Filter (class)
- Actors to Ignore (object) — Ignore these actors in the list

**Outputs:**
- Out (exec)
- Out Components (object)
- Return Value (boolean) — true if there was an overlap that passed the filters, false otherwise.

**Description:** Returns an array of components that overlap the given capsule.
---

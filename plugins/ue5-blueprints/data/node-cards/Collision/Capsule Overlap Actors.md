## Capsule Overlap Actors
**Category:** Collision
**Search:** "Capsule Overlap Actors"
**Target:** Kismet System Library

**Inputs:**
- In (exec)
- Capsule Pos (vector) — Center of the capsule.
- Radius (real) — Radius of capsule hemispheres and radius of center cylinder portion.
- Half Height (real) — Half-height of the capsule (from center of capsule to tip of hemisphere.
- Object Types (enum)
- Actor Class Filter (class)
- Actors to Ignore (object) — Ignore these actors in the list

**Outputs:**
- Out (exec)
- Out Actors (object) — Returned array of actors. Unsorted.
- Return Value (boolean) — true if there was an overlap that passed the filters, false otherwise.

**Description:** Returns an array of actors that overlap the given capsule.
---

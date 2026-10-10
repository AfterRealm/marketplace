## Capsule Trace For Objects
**Category:** Collision
**Search:** "Capsule Trace For Objects"
**Target:** Kismet System Library

**Inputs:**
- In (exec)
- Start (vector) — Start of line segment.
- End (vector) — End of line segment.
- Radius (real) — Radius of the capsule to sweep
- Half Height (real) — Distance from center of capsule to tip of hemisphere endcap.
- Object Types (enum) — Array of Object Types to trace
- Trace Complex (boolean) — True to test against complex collision, false to test against simplified collision.
- Actors to Ignore (object)
- Draw Debug Type (enum)
- Ignore Self (boolean)
- Trace Color (linearcolor)
- Trace Hit Color (linearcolor)
- Draw Time (real)

**Outputs:**
- Out (exec)
- Out Hit (struct) — Properties of the trace hit.
- Return Value (boolean) — True if there was a hit, false otherwise.

**Description:** Sweeps a capsule along the given line and returns the first hit encountered. This only finds objects that are of a type specified by ObjectTypes.
---

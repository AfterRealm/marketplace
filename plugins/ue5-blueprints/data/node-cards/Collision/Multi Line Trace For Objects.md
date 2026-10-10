## Multi Line Trace For Objects
**Category:** Collision
**Search:** "Multi Line Trace For Objects"
**Target:** Kismet System Library

**Inputs:**
- In (exec)
- Start (vector) — Start of line segment.
- End (vector) — End of line segment.
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
- Out Hits (struct)
- Return Value (boolean) — True if there was a hit, false otherwise.

**Description:** Does a collision trace along the given line and returns all hits encountered. This only finds objects that are of a type specified by ObjectTypes.
---

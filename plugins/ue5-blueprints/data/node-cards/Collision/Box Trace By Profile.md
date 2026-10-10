## Box Trace By Profile
**Category:** Collision
**Search:** "Box Trace By Profile"
**Target:** Kismet System Library

**Inputs:**
- In (exec)
- Start (vector) — Start of line segment.
- End (vector) — End of line segment.
- Half Size (vector) — Distance from the center of box along each axis
- Orientation (rotator) — Orientation of the box
- Profile Name (name) — The 'profile' used to determine which components to hit
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

**Description:** Sweep a box against the world and return the first blocking hit using a specific profile
---

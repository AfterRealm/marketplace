## Line Trace By Profile
**Category:** Collision
**Search:** "Line Trace By Profile"
**Target:** Kismet System Library

**Inputs:**
- In (exec)
- Start (vector) — Start of line segment.
- End (vector) — End of line segment.
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

**Description:** Trace a ray against the world using a specific profile and return the first blocking hit
---

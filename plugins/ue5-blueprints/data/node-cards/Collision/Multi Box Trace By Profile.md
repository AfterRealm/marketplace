## Multi Box Trace By Profile
**Category:** Collision
**Search:** "Multi Box Trace By Profile"
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
- Out Hits (struct) — A list of hits, sorted along the trace from start to finish. The blocking hit will be the last hit, if there was one.
- Return Value (boolean) — True if there was a blocking hit, false otherwise.

**Description:** Sweep a box against the world and return all initial overlaps using a specific profile, then overlapping hits and then first blocking hit Results are sorted, so a blocking hit (if found) will be the last element of the array Only the single closest blocking result will be generated, no tests will be done after that
---

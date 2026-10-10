## Multi Line Trace By Profile
**Category:** Collision
**Search:** "Multi Line Trace By Profile"
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
- Out Hits (struct)
- Return Value (boolean) — True if there was a blocking hit, false otherwise.

**Description:** Trace a ray against the world using a specific profile and return overlapping hits and then first blocking hit Results are sorted, so a blocking hit (if found) will be the last element of the array Only the single closest blocking result will be generated, no tests will be done after that
---

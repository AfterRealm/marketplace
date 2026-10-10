## Multi Line Trace By Channel
**Category:** Collision
**Search:** "Multi Line Trace By Channel"
**Target:** Kismet System Library

**Inputs:**
- In (exec)
- Start (vector) — Start of line segment.
- End (vector) — End of line segment.
- Trace Channel (enum) — The channel to trace
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

**Description:** Does a collision trace along the given line and returns all hits encountered up to and including the first blocking hit. This trace finds the objects that RESPOND to the given TraceChannel
---

## Multi Capsule Trace By Channel
**Category:** Collision
**Search:** "Multi Capsule Trace By Channel"
**Target:** Kismet System Library

**Inputs:**
- In (exec)
- Start (vector) — Start of line segment.
- End (vector) — End of line segment.
- Radius (real) — Radius of the capsule to sweep
- Half Height (real) — Distance from center of capsule to tip of hemisphere endcap.
- Trace Channel (enum)
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

**Description:** Sweeps a capsule along the given line and returns all hits encountered up to and including the first blocking hit. This trace finds the objects that RESPOND to the given TraceChannel
---

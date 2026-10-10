## Box Trace By Channel
**Category:** Collision
**Search:** "Box Trace By Channel"
**Target:** Kismet System Library

**Inputs:**
- In (exec)
- Start (vector) — Start of line segment.
- End (vector) — End of line segment.
- Half Size (vector) — Distance from the center of box along each axis
- Orientation (rotator) — Orientation of the box
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
- Out Hit (struct) — Properties of the trace hit.
- Return Value (boolean) — True if there was a hit, false otherwise.

**Description:** Sweeps a box along the given line and returns the first blocking hit encountered. This trace finds the objects that RESPONDS to the given TraceChannel
---

## Get Actor Eyes View Point
**Category:** Actor
**Search:** "Get Actor Eyes View Point"
**Target:** Actor

**Inputs:**
- Target (object)

**Outputs:**
- Out Location (vector) — location of view point
- Out Rotation (rotator) — view rotation of actor.

**Description:** Returns the point of view of the actor. Note that this doesn't mean the camera, but the 'eyes' of the actor. For example, for a Pawn, this would define the eye height location, and view rotation (which is different from the pawn rotation which has a zeroed pitch component). A camera first person view will typically use this view point. Most traces (weapon, AI) will be done from this view point.
---

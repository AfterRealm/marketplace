## Add Local Rotation
**Category:** Transformation
**Search:** "Add Local Rotation"
**Target:** Scene Component

**Inputs:**
- In (exec)
- Target (object)
- Delta Rotation (rotator) — Change in rotation of the component in its local reference frame.
- Sweep (boolean) — Whether we sweep to the destination (currently not supported for rotation).
- Teleport (boolean) — Whether we teleport the physics state (if physics collision is enabled for this object). If true, physics velocity for this object is unchanged (so ragdoll parts are not affected by change in location). If false, physics velocity is updated based on the change in position (affecting ragdoll parts).

**Outputs:**
- Out (exec)
- Sweep Hit Result (struct) — Hit result from any impact if sweep is true.

**Description:** Adds a delta to the rotation of the component in its local reference frame
---

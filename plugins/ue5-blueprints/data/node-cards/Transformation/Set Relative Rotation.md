## Set Relative Rotation
**Category:** Transformation
**Search:** "Set Relative Rotation"
**Target:** Scene Component

**Inputs:**
- In (exec)
- Target (object)
- New Rotation (rotator) — New rotation of the component relative to its parent
- Sweep (boolean) — Whether we sweep to the destination (currently not supported for rotation).
- Teleport (boolean) — Whether we teleport the physics state (if physics collision is enabled for this object). If true, physics velocity for this object is unchanged (so ragdoll parts are not affected by change in location). If false, physics velocity is updated based on the change in position (affecting ragdoll parts).

**Outputs:**
- Out (exec)
- Sweep Hit Result (struct) — Hit result from any impact if sweep is true.

**Description:** Set the rotation of the component relative to its parent
---

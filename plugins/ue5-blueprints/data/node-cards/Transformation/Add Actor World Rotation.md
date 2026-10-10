## Add Actor World Rotation
**Category:** Transformation
**Search:** "Add Actor World Rotation"
**Target:** Actor

**Inputs:**
- In (exec)
- Target (object)
- Delta Rotation (rotator) — The change in rotation.
- Sweep (boolean) — Whether to sweep to the target rotation (not currently supported for rotation).
- Teleport (boolean) — Whether we teleport the physics state (if physics collision is enabled for this object). If true, physics velocity for this object is unchanged (so ragdoll parts are not affected by change in location). If false, physics velocity is updated based on the change in position (affecting ragdoll parts). If CCD is on and not teleporting, this will affect objects along the entire swept volume. Note that when teleporting, any child/attached components will be teleported too, maintaining their current offset even if they are being simulated. Setting the rotation without teleporting will not update the rotation of simulated child/attached components.

**Outputs:**
- Out (exec)
- Sweep Hit Result (struct) — The hit result from the move if swept.

**Description:** Adds a delta to the rotation of this actor in world space.
---

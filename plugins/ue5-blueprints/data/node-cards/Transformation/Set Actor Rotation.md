## Set Actor Rotation
**Category:** Transformation
**Search:** "Set Actor Rotation"
**Target:** Actor

**Inputs:**
- In (exec)
- Target (object)
- New Rotation (rotator) — The new rotation for the Actor.
- Teleport Physics (boolean) — Whether we teleport the physics state (if physics collision is enabled for this object). If true, physics velocity for this object is unchanged (so ragdoll parts are not affected by change in location). If false, physics velocity is updated based on the change in position (affecting ragdoll parts). Note that when teleporting, any child/attached components will be teleported too, maintaining their current offset even if they are being simulated. Setting the rotation without teleporting will not update the rotation of simulated child/attached components.

**Outputs:**
- Out (exec)
- Return Value (boolean) — Whether the rotation was successfully set.

**Description:** Set the Actor's rotation instantly to the specified rotation.
---

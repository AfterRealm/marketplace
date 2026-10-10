## Set Actor Location And Rotation
**Category:** Transformation
**Search:** "Set Actor Location And Rotation"
**Target:** Actor

**Inputs:**
- In (exec)
- Target (object)
- New Location (vector) — The new location to teleport the Actor to.
- New Rotation (rotator) — The new rotation for the Actor.
- Sweep (boolean) — Whether we sweep to the destination location, triggering overlaps along the way and stopping short of the target if blocked by something. Only the root component is swept and checked for blocking collision, child components move without sweeping. If collision is off, this has no effect.
- Teleport (boolean) — Whether we teleport the physics state (if physics collision is enabled for this object). If true, physics velocity for this object is unchanged (so ragdoll parts are not affected by change in location). If false, physics velocity is updated based on the change in position (affecting ragdoll parts). If CCD is on and not teleporting, this will affect objects along the entire swept volume. Note that when teleporting, any child/attached components will be teleported too, maintaining their current offset even if they are being simulated. Setting the location without teleporting will not update the location of simulated child/attached components.

**Outputs:**
- Out (exec)
- Sweep Hit Result (struct) — The hit result from the move if swept.
- Return Value (boolean) — Whether the rotation was successfully set.

**Description:** Move the actor instantly to the specified location and rotation.
---

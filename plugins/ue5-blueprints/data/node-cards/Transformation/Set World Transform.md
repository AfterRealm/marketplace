## Set World Transform
**Category:** Transformation
**Search:** "Set World Transform"
**Target:** Scene Component

**Inputs:**
- In (exec)
- Target (object)
- New Transform (transform) — New transform in world space for the component.
- Sweep (boolean) — Whether we sweep to the destination location, triggering overlaps along the way and stopping short of the target if blocked by something. Only the root component is swept and checked for blocking collision, child components move without sweeping. If collision is off, this has no effect.
- Teleport (boolean) — Whether we teleport the physics state (if physics collision is enabled for this object). If true, physics velocity for this object is unchanged (so ragdoll parts are not affected by change in location). If false, physics velocity is updated based on the change in position (affecting ragdoll parts). If CCD is on and not teleporting, this will affect objects along the entire sweep volume.

**Outputs:**
- Out (exec)
- Sweep Hit Result (struct) — Hit result from any impact if sweep is true.

**Description:** Set the transform of the component in world space.
---

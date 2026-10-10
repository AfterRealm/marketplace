## Set Physics Angular Velocity in Radians
**Category:** Physics
**Search:** "Set Physics Angular Velocity in Radians"
**Target:** Primitive Component

**Inputs:**
- In (exec)
- Target (object)
- New Ang Vel (vector) — New angular velocity to apply to body, in radians per second.
- Add to Current (boolean) — If true, NewAngVel is added to the existing angular velocity of the body.
- Bone Name (name) — If a SkeletalMeshComponent, name of body to modify angular velocity of. 'None' indicates root body.

**Outputs:**
- Out (exec)

**Description:** Set the angular velocity of a single body. This should be used cautiously - it may be better to use AddTorque or AddImpulse.
---

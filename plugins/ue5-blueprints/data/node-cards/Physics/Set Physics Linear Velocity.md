## Set Physics Linear Velocity
**Category:** Physics
**Search:** "Set Physics Linear Velocity"
**Target:** Primitive Component

**Inputs:**
- In (exec)
- Target (object)
- New Vel (vector) — New linear velocity to apply to physics.
- Add to Current (boolean) — If true, NewVel is added to the existing velocity of the body.
- Bone Name (name) — If a SkeletalMeshComponent, name of body to modify velocity of. 'None' indicates root body.

**Outputs:**
- Out (exec)

**Description:** Set the linear velocity of a single body. This should be used cautiously - it may be better to use AddForce or AddImpulse.
---

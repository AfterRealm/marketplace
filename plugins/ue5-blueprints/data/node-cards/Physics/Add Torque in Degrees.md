## Add Torque in Degrees
**Category:** Physics
**Search:** "Add Torque in Degrees"
**Target:** Primitive Component

**Inputs:**
- In (exec)
- Target (object)
- Torque (vector) — Torque to apply. Direction is axis of rotation and magnitude is strength of torque.
- Bone Name (name) — If a SkeletalMeshComponent, name of body to apply torque to. 'None' indicates root body.
- Accel Change (boolean) — If true, Torque is taken as a change in angular acceleration instead of a physical torque (i.e. mass will have no effect).

**Outputs:**
- Out (exec)

**Description:** Add a torque to a single rigid body.
---

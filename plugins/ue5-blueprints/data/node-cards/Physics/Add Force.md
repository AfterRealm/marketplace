## Add Force
**Category:** Physics
**Search:** "Add Force"
**Target:** Primitive Component

**Inputs:**
- In (exec)
- Target (object)
- Force (vector) — Force vector to apply. Magnitude indicates strength of force.
- Bone Name (name) — If a SkeletalMeshComponent, name of body to apply force to. 'None' indicates root body.
- Accel Change (boolean) — If true, Force is taken as a change in acceleration instead of a physical force (i.e. mass will have no effect).

**Outputs:**
- Out (exec)

**Description:** Add a force to a single rigid body. This is like a 'thruster'. Good for adding a burst over some (non zero) time. Should be called every frame for the duration of the force.
---

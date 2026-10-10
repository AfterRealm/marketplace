## Add Force at Location
**Category:** Physics
**Search:** "Add Force at Location"
**Target:** Primitive Component

**Inputs:**
- In (exec)
- Target (object)
- Force (vector) — Force vector to apply. Magnitude indicates strength of force.
- Location (vector) — Location to apply force, in world space.
- Bone Name (name) — If a SkeletalMeshComponent, name of body to apply force to. 'None' indicates root body.

**Outputs:**
- Out (exec)

**Description:** Add a force to a single rigid body at a particular location in world space. This is like a 'thruster'. Good for adding a burst over some (non zero) time. Should be called every frame for the duration of the force.
---

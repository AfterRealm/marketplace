## Set Max Depenetration Velocity
**Category:** Physics
**Search:** "Set Max Depenetration Velocity"
**Target:** Primitive Component

**Inputs:**
- In (exec)
- Target (object)
- Bone Name (name)
- In Max Depenetration Velocity (real)

**Outputs:**
- Out (exec)

**Description:** The maximum velocity used to depenetrate this object from others when spawned or teleported with initial overlaps (does not affect overlaps as a result of normal movement). A value of zero will allow objects that are spawned overlapping to go to sleep without moving rather than pop out of each other. E.g., use zero if you spawn dynamic rocks partially embedded in the ground and want them to be interactive but not pop out of the ground when touched. A negative value means that the config setting CollisionInitialOverlapDepenetrationVelocity will be used.
---

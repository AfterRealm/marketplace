## Add Force
**Category:** Utilities
**Search:** "Add Force"
**Target:** Physics Thread Library

**Inputs:**
- In (exec)
- Handle (struct)
- Force (vector) — Force vector to apply. Magnitude indicates strength of force.
- Accel Change (boolean) — If true, Force is taken as a change in acceleration instead of a physical force (i.e. mass will have no effect).

**Outputs:**
- Out (exec)

**Description:** Add a force to a single rigid body. This is like a 'thruster'. Good for adding a burst over some (non zero) time. Should be called every frame for the duration of the force.
---

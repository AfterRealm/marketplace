## Add Radial Force
**Category:** Physics
**Search:** "Add Radial Force"
**Target:** Primitive Component

**Inputs:**
- In (exec)
- Target (object)
- Origin (vector) — Origin of force in world space.
- Radius (real) — Radius within which to apply the force.
- Strength (real) — Strength of force to apply.
- Falloff (enum) — Allows you to control the strength of the force as a function of distance from Origin.
- Accel Change (boolean) — If true, Strength is taken as a change in acceleration instead of a physical force (i.e. mass will have no effect).

**Outputs:**
- Out (exec)

**Description:** Add a force to all bodies in this component, originating from the supplied world-space location.
---

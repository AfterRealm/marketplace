## Add Radial Impulse
**Category:** Physics
**Search:** "Add Radial Impulse"
**Target:** Primitive Component

**Inputs:**
- In (exec)
- Target (object)
- Origin (vector) — Point of origin for the radial impulse blast, in world space
- Radius (real) — Size of radial impulse. Beyond this distance from Origin, there will be no affect.
- Strength (real) — Maximum strength of impulse applied to body.
- Falloff (enum) — Allows you to control the strength of the impulse as a function of distance from Origin.
- Vel Change (boolean) — If true, the Strength is taken as a change in velocity instead of an impulse (ie. mass will have no effect).

**Outputs:**
- Out (exec)

**Description:** Add an impulse to all rigid bodies in this component, radiating out from the specified position.
---

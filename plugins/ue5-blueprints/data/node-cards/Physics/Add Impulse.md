## Add Impulse
**Category:** Physics
**Search:** "Add Impulse"
**Target:** Primitive Component

**Inputs:**
- In (exec)
- Target (object)
- Impulse (vector) — Magnitude and direction of impulse to apply.
- Bone Name (name) — If a SkeletalMeshComponent, name of body to apply impulse to. 'None' indicates root body.
- Vel Change (boolean) — If true, the Strength is taken as a change in velocity instead of an impulse (ie. mass will have no effect).

**Outputs:**
- Out (exec)

**Description:** Add an impulse to a single rigid body. Good for one time instant burst.
---

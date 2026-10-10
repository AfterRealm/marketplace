## Add Impulse to All Bodies Below
**Category:** Physics
**Search:** "Add Impulse to All Bodies Below"
**Target:** Skeletal Mesh Component

**Inputs:**
- In (exec)
- Target (object)
- Impulse (vector) — Magnitude and direction of impulse to apply.
- Bone Name (name) — If a SkeletalMeshComponent, name of body to apply impulse to. 'None' indicates root body.
- Vel Change (boolean) — If true, the Strength is taken as a change in velocity instead of an impulse (ie. mass will have no effect).
- Include Self (boolean) — If false, Force is only applied to bodies below but not given bone name.

**Outputs:**
- Out (exec)

**Description:** Add impulse to all single rigid bodies below. Good for one time instant burst.
---

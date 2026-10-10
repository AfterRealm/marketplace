## Get Center Of Mass
**Category:** Physics
**Search:** "Get Center Of Mass"
**Target:** Primitive Component

**Inputs:**
- Target (object)
- Bone Name (name) — If a SkeletalMeshComponent, name of body to get center of mass of. 'None' indicates root body.

**Outputs:**
- Return Value (vector)

**Description:** Get the center of mass of a single body. In the case of a welded body this will return the center of mass of the entire welded body (including its parent and children) Objects that are not simulated return (0,0,0) as they do not have COM
---

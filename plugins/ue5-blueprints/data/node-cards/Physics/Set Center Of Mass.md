## Set Center Of Mass
**Category:** Physics
**Search:** "Set Center Of Mass"
**Target:** Primitive Component

**Inputs:**
- In (exec)
- Target (object)
- Center Of Mass Offset (vector) — User specified offset for the center of mass of this object, from the calculated location.
- Bone Name (name) — If a SkeletalMeshComponent, name of body to set center of mass of. 'None' indicates root body.

**Outputs:**
- Out (exec)

**Description:** Set the center of mass of a single body. This will offset the physx-calculated center of mass. Note that in the case where multiple bodies are attached together, the center of mass will be set for the entire group.
---

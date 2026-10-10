## Get Skeletal Mesh Embedded Positions
**Category:** Physics
**Search:** "Get Skeletal Mesh Embedded Positions"
**Target:** Deformable Tetrahedral Component

**Inputs:**
- Target (object)
- Format (enum)
- Target Deformation Skeleton Offset (transform)
- Target Bone (name)
- Simulation Blend Weight (real)

**Outputs:**
- Return Value (vector)

**Description:** Get the current positions of the transformation hierarchy from \c TargetDeformationSkeleton, deformed by the tetrahedral mesh. Results can be in world space postions/deltas, component space positions/deltas, or bone space positions/deltas. If a bone space is desired \p TargetBone must indicate which bone to use. TargetDeformationSkeletonOffset is an offset transform that moves the \c TargetDeformationSkeleton to be co-located with the flesh mesh.
---

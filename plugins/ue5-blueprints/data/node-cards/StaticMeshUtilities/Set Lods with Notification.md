## Set Lods with Notification
**Category:** StaticMeshUtilities
**Search:** "Set Lods with Notification"
**Target:** Static Mesh Editor Subsystem

**Inputs:**
- In (exec)
- Target (object)
- Static Mesh (object) — Mesh to process.
- Reduction Options (struct) — Options on how to generate LODs on the mesh.
- Apply Changes (boolean) — Indicates if change must be notified.

**Outputs:**
- Out (exec)
- Return Value (integer) — the number of LODs generated on the input mesh. An negative value indicates that the reduction could not be performed. See log for explanation. No action will be performed if ReductionOptions.ReductionSettings is empty

**Description:** Remove then add LODs on a static mesh. The static mesh must have at least LOD 0. The LOD 0 of the static mesh is kept after removal. The build settings of LOD 0 will be applied to all subsequent LODs.
---

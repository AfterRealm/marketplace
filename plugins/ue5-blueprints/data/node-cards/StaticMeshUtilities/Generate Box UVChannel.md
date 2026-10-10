## Generate Box UVChannel
**Category:** StaticMeshUtilities
**Search:** "Generate Box UVChannel"
**Target:** Static Mesh Editor Subsystem

**Inputs:**
- In (exec)
- Target (object)
- Static Mesh (object) — Static mesh on which to generate the UV mapping.
- LODIndex (integer) — Index of the StaticMesh LOD.
- UVChannel Index (integer) — Channel where to save the UV mapping.
- Position (vector) — Position of the center of the projection gizmo.
- Orientation (rotator) — Rotation to apply to the projection gizmo.
- Size (vector) — The size of the box projection gizmo.

**Outputs:**
- Out (exec)
- Return Value (boolean) — true if the UV mapping was generated.

**Description:** Generates box UV mapping in the specified UV channel on the given LOD of a StaticMesh.
---

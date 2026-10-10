## Generate Cylindrical UVChannel
**Category:** StaticMeshUtilities
**Search:** "Generate Cylindrical UVChannel"
**Target:** Static Mesh Editor Subsystem

**Inputs:**
- In (exec)
- Target (object)
- Static Mesh (object) — Static mesh on which to generate the UV mapping.
- LODIndex (integer) — Index of the StaticMesh LOD.
- UVChannel Index (integer) — Channel where to save the UV mapping.
- Position (vector) — Position of the center of the projection gizmo.
- Orientation (rotator) — Rotation to apply to the projection gizmo.
- Tiling (vector2d struct) — The UV tiling to use to generate the UV mapping.

**Outputs:**
- Out (exec)
- Return Value (boolean) — true if the UV mapping was generated.

**Description:** Generates cylindrical UV mapping in the specified UV channel on the given LOD of a StaticMesh.
---

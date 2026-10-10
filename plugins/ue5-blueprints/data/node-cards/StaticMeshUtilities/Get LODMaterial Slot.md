## Get LODMaterial Slot
**Category:** StaticMeshUtilities
**Search:** "Get LODMaterial Slot"
**Target:** Static Mesh Editor Subsystem

**Inputs:**
- In (exec)
- Target (object)
- Static Mesh (object) — Static mesh to get the material index from.
- LODIndex (integer) — Index of the StaticMesh LOD.
- Section Index (integer) — Index of the StaticMesh Section.

**Outputs:**
- Out (exec)
- Return Value (integer) — MaterialSlotIndex Index of the material slot used by the section or INDEX_NONE in case of error.

**Description:** Gets the material slot used for a specific LOD section.
---

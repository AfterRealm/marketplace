## Set Lod from Static Mesh
**Category:** StaticMeshUtilities
**Search:** "Set Lod from Static Mesh"
**Target:** Static Mesh Editor Subsystem

**Inputs:**
- In (exec)
- Target (object)
- Destination Static Mesh (object) — The static mesh to set the LOD in.
- Destination Lod Index (integer) — The index of the LOD to set.
- Source Static Mesh (object) — The static mesh to get the LOD from.
- Source Lod Index (integer) — The index of the LOD to get.
- Reuse Existing Material Slots (boolean) — If true, sections from SourceStaticMesh will be remapped to match the material slots of DestinationStaticMesh when they have the same material assigned. If false, all material slots of SourceStaticMesh will be appended in DestinationStaticMesh.

**Outputs:**
- Out (exec)
- Return Value (integer) — The index of the LOD that was set. It can be different than DestinationLodIndex if it wasn't a valid index. A negative value indicates that the LOD was not set. See log for explanation.

**Description:** Adds or create a LOD at DestinationLodIndex using the geometry from SourceStaticMesh SourceLodIndex
---

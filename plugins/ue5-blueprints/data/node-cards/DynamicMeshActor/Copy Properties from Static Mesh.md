## Copy Properties from Static Mesh
**Category:** DynamicMeshActor
**Search:** "Copy Properties from Static Mesh"
**Target:** Generated Dynamic Mesh Actor

**Inputs:**
- In (exec)
- Target (object)
- Static Mesh Actor (object)
- Copy Component Materials (boolean)

**Outputs:**
- Out (exec)

**Description:** Attempt to copy Actor Properties from a StaticMeshActor. Optionally copy DynamicMeshComponent material list to the StaticMeshComponent. This function is useful when (eg) swapping from a StaticMeshActor to a DynamicMeshActor as it will allow many configured Actor settings to be preserved (like assigned DataLayers, etc)
---

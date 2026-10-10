## Copy Properties to Static Mesh
**Category:** DynamicMeshActor
**Search:** "Copy Properties to Static Mesh"
**Target:** Generated Dynamic Mesh Actor

**Inputs:**
- In (exec)
- Target (object)
- Static Mesh Actor (object)
- Copy Component Materials (boolean)

**Outputs:**
- Out (exec)

**Description:** Attempt to copy Actor Properties to a StaticMeshActor. Optionally copy DynamicMeshComponent material list to the StaticMeshComponent. This function is useful when (eg) swapping from a DynamicMeshActor to a StaticMeshActor as it will allow many configured Actor settings to be preserved (like assigned DataLayers, etc)
---

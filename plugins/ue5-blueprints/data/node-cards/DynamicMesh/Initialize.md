## Initialize
**Category:** DynamicMesh
**Search:** "Initialize"
**Target:** PCGDynamic Mesh Data

**Inputs:**
- In (exec)
- Target (object)
- In Mesh (object)
- In Materials (object)
- Can Take Ownership (boolean)

**Outputs:**
- Out (exec)

**Description:** Initialize the dynamic mesh data from an input dynamic mesh object. If the input dynamic mesh is not meant to be re-used after this initialization, you can set Can Take Ownership to true. Be careful as it will put the previous object in an invalid state. You can also pass an array of materials that correspond to the referenced materials in the dynamic mesh.
---

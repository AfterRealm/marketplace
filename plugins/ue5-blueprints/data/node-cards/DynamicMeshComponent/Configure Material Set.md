## Configure Material Set
**Category:** DynamicMeshComponent
**Search:** "Configure Material Set"
**Target:** Dynamic Mesh Component

**Inputs:**
- In (exec)
- Target (object)
- New Material Set (object)
- Delete Extra Slots (boolean) — if true, extra Material Slots beyond max NewMaterialSet.Num() are removed

**Outputs:**
- Out (exec)

**Description:** Set new list of Materials for the Mesh. Dynamic Mesh Component does not have Slot Names, so the size of the Material Set should be the same as the number of different Material IDs on the mesh MaterialID attribute
---

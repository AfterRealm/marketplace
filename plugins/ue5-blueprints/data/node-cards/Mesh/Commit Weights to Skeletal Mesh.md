## Commit Weights to Skeletal Mesh
**Category:** Mesh
**Search:** "Commit Weights to Skeletal Mesh"
**Target:** Skin Weight Modifier

**Inputs:**
- In (exec)
- Target (object)

**Outputs:**
- Out (exec)
- Return Value (boolean) — true if weights were applied to a skeletal mesh, false otherwise

**Description:** Actually applies the weight modifications to the skeletal mesh. This action creates an undo transaction. The skeletal mesh asset will be dirtied, but it is up to the user to save the asset if required.
---

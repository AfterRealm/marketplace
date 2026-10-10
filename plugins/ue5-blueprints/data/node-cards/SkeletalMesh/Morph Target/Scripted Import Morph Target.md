## Scripted Import Morph Target
**Category:** SkeletalMesh > Morph Target
**Search:** "Scripted Import Morph Target"
**Target:** Interchange Mesh Utilities

**Inputs:**
- Target (object)
- Skeletal Mesh (object) — The target skeletal mesh we want to add the morph targets
- Lod Index (integer) — The index of the LOD we want to replace or add the morph targets
- Source Data (object) — The source to import the morph targets
- Morph Target Name (string) — If not empty we will use this name to create the morph target, if there is already an existing morph target it will be re-import

**Outputs:**
- Return Value (boolean) — return true if it successfully add or replace the skeletal mesh morph target at LodIndex, flase otherwise.

**Description:** This function import a morph target from the source data and add/replace the skeletal mesh morph target.
---

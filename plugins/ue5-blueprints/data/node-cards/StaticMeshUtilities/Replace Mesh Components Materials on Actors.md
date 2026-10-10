## Replace Mesh Components Materials on Actors
**Category:** StaticMeshUtilities
**Search:** "Replace Mesh Components Materials on Actors"
**Target:** Static Mesh Editor Subsystem

**Inputs:**
- In (exec)
- Target (object)
- Actors (object) — List of Actors to search from.
- Material to be Replaced (object) — Material we want to replace.
- New Material (object) — Material to replace MaterialToBeReplaced by.

**Outputs:**
- Out (exec)

**Description:** Find the references of the material MaterialToReplaced on all the MeshComponents of all the Actors provided and replace it by NewMaterial.
---

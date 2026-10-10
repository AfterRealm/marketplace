## Add Simple Collisions with Notification
**Category:** StaticMeshUtilities
**Search:** "Add Simple Collisions with Notification"
**Target:** Static Mesh Editor Subsystem

**Inputs:**
- In (exec)
- Target (object)
- Static Mesh (object) — Mesh to generate simple collision for.
- Shape Type (enum) — Options on which simple collision to add to the mesh.
- Apply Changes (boolean) — Indicates if changes must be apply or not.

**Outputs:**
- Out (exec)
- Return Value (integer) — An integer indicating the index of the collision newly created. A negative value indicates the addition failed.

**Description:** Add simple collisions to a static mesh. This method replicates what is done when invoking menu entries "Collision > Add [...] Simplified Collision" in the Mesh Editor.
---

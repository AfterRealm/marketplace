## Set Convex Decomposition Collisions with Notification
**Category:** StaticMeshUtilities
**Search:** "Set Convex Decomposition Collisions with Notification"
**Target:** Static Mesh Editor Subsystem

**Inputs:**
- In (exec)
- Target (object)
- Static Mesh (object) — Static mesh to add convex collision on.
- Hull Count (integer) — Maximum number of convex pieces that will be created. Must be positive.
- Max Hull Verts (integer) — Maximum number of vertices allowed for any generated convex hull.
- Hull Precision (integer) — Number of voxels to use when generating collision. Must be positive.
- Apply Changes (boolean) — Indicates if changes must be apply or not.

**Outputs:**
- Out (exec)
- Return Value (boolean) — A boolean indicating if the addition was successful or not.

**Description:** Add a convex collision to a static mesh. Any existing collisions will be removed from the static mesh. This method replicates what is done when invoking menu entry "Collision > Auto Convex Collision" in the Mesh Editor.
---

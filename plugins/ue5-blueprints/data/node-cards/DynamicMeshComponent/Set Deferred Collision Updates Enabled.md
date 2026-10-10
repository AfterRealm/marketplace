## Set Deferred Collision Updates Enabled
**Category:** DynamicMeshComponent
**Search:** "Set Deferred Collision Updates Enabled"
**Target:** Dynamic Mesh Component

**Inputs:**
- In (exec)
- Target (object)
- Enabled (boolean)
- Immediate Update (boolean) — if true, UpdateCollision(true) is called if bEnabled=false, ie to force a collision rebuild

**Outputs:**
- Out (exec)

**Description:** Set value of bDeferCollisionUpdates, when enabled, collision is not automatically recomputed each time the mesh changes.
---

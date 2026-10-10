## Spawn Actor from Class
**Category:** Game
**Search:** "Spawn Actor from Class"

**Inputs:**
- In (exec)
- Class (class) — Actor Class Reference ClassThe object class you want to construct
- Spawn Transform (transform) — The transform to spawn the Actor with
- Collision Handling Override (enum) — Specifies how to handle collisions at the spawn point. If undefined, uses actor class settings.
- Transform Scale Method (enum)
- Owner (object) — Can be left empty; primarily used for replication (bNetUseOwnerRelevancy and bOnlyRelevantToOwner), or visibility (PrimitiveComponent's bOwnerNoSee/bOnlyOwnerSee)

**Outputs:**
- Out (exec)
- Return Value (object) — Actor Object Reference Return ValueThe constructed object

**Description:** Attempts to spawn a new Actor with the specified transform
---

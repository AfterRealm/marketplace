## Create Local Player For Platform User
**Category:** Game
**Search:** "Create Local Player For Platform User"
**Target:** Gameplay Statics

**Inputs:**
- In (exec)
- User Id (struct) — The platform user id that should control the newly created player. A valude of PLATFRMUSERID_NONE specifies to use the next available ID
- Spawn Player Controller (boolean) — Whether a player controller should be spawned immediately for this player. If false a player controller will not be created automatically until transition to the next map.

**Outputs:**
- Out (exec)
- Return Value (object) — The created player controller if one is created.

**Description:** Create a new local player for this game, for cases like local multiplayer.
---

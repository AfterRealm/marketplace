## Create Local Player
**Category:** Game
**Search:** "Create Local Player"
**Target:** Gameplay Statics

**Inputs:**
- In (exec)
- Controller Id (integer) — The ID of the physical controller that the should control the newly created player. A value of -1 specifies to use the next available ID
- Spawn Player Controller (boolean) — Whether a player controller should be spawned immediately for this player. If false a player controller will not be created automatically until transition to the next map.

**Outputs:**
- Out (exec)
- Return Value (object) — The created player controller if one is created.

**Description:** Create a new local player for this game, for cases like local multiplayer.
---

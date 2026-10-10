## Get Player State
**Category:** Game
**Search:** "Get Player State"
**Target:** Gameplay Statics

**Inputs:**
- Player State Index (integer) — Index into the game state's PlayerArray

**Outputs:**
- Return Value (object)

**Description:** Returns the player state at the given index in the game state's PlayerArray. This will work on both the client and server and the index will be consistent. After initial replication, all clients and the server will have access to PlayerStates for all connected players.
---

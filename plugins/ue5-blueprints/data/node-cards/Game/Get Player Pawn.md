## Get Player Pawn
**Category:** Game
**Search:** "Get Player Pawn"
**Target:** Gameplay Statics

**Inputs:**
- Player Index (integer) — Index in the player controller list, starting first with local players and then available remote ones

**Outputs:**
- Return Value (object)

**Description:** Returns the pawn for the player controller at the specified player index. This will not include pawns of remote clients with no available player controller, you can use the player states list for that.
---

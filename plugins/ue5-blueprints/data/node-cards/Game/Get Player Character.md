## Get Player Character
**Category:** Game
**Search:** "Get Player Character"
**Target:** Gameplay Statics

**Inputs:**
- Player Index (integer) — Index in the player controller list, starting first with local players and then available remote ones

**Outputs:**
- Return Value (object)

**Description:** Returns the pawn for the player controller at the specified player index, will return null if the pawn is not a character. This will not include characters of remote clients with no available player controller, you can iterate the PlayerStates list for that.
---

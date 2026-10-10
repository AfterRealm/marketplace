## Get Player Controller
**Category:** Game
**Search:** "Get Player Controller"
**Target:** Gameplay Statics

**Inputs:**
- Player Index (integer) — Index in the player controller list, starting first with local players and then available remote ones

**Outputs:**
- Return Value (object)

**Description:** Returns the player controller found while iterating through the local and available remote player controllers. On a network client, this will only include local players as remote player controllers are not available. The index will be consistent as long as no new players join or leave, but it will not be the same across different clients and servers.
---

## FindPlayerStart
**Category:** Game
**Search:** "FindPlayerStart"
**Target:** Game Mode Base

**Inputs:**
- Target (object)
- Player (object) — The AController for whom we are choosing a Player Start
- Incoming Name (string) — Specifies the tag of a Player Start to use

**Outputs:**
- Return Value (object) — Actor chosen as player start (usually a PlayerStart)

**Description:** Return the specific player start actor that should be used for the next spawn This will either use a previously saved startactor, or calls ChoosePlayerStart
---

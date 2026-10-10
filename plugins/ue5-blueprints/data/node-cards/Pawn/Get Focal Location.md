## Get Focal Location
**Category:** Pawn
**Search:** "Get Focal Location"
**Target:** Player Controller

**Inputs:**
- Target (object)

**Outputs:**
- Return Value (vector)

**Description:** Returns the location the PlayerController is focused on. If there is a possessed Pawn, returns the Pawn's location. If there is a spectator Pawn, returns that Pawn's location. Otherwise, returns the PlayerController's spawn location (usually the last known Pawn location after it has died).
---

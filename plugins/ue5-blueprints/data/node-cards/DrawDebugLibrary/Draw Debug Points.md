## Draw Debug Points
**Category:** DrawDebugLibrary
**Search:** "Draw Debug Points"
**Target:** Draw Debug Library

**Inputs:**
- In (exec)
- Drawer (struct)
- Locations (vector)
- Point Style (struct)
- Depth Test (boolean)

**Outputs:**
- Out (exec)

**Description:** Debug Draw points. These should be preferred over DrawDebugPoint where possible as it will batch drawing when required such as when using the visual logger.
---

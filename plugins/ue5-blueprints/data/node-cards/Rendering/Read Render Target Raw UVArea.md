## Read Render Target Raw UVArea
**Category:** Rendering
**Search:** "Read Render Target Raw UVArea"
**Target:** Kismet Rendering Library

**Inputs:**
- In (exec)
- Texture Render Target (object)
- Area (struct)
- Normalize (boolean)

**Outputs:**
- Out (exec)
- Return Value (linearcolor)

**Description:** Incredibly inefficient and slow operation! Read an area of values as-is from a render target using a rectangle defined by UV [0,1]x[0,1] coordinates.
---

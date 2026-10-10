## Read Render Target Raw Pixel Area
**Category:** Rendering
**Search:** "Read Render Target Raw Pixel Area"
**Target:** Kismet Rendering Library

**Inputs:**
- In (exec)
- Texture Render Target (object)
- Min X (integer)
- Min Y (integer)
- Max X (integer)
- Max Y (integer)
- Normalize (boolean)

**Outputs:**
- Out (exec)
- Return Value (linearcolor)

**Description:** Incredibly inefficient and slow operation! Read an area of values as-is from a render target using a rectangle defined by integer pixel coordinates.
---

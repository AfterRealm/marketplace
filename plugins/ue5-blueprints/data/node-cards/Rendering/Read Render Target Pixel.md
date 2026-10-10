## Read Render Target Pixel
**Category:** Rendering
**Search:** "Read Render Target Pixel"
**Target:** Kismet Rendering Library

**Inputs:**
- In (exec)
- Texture Render Target (object)
- X (integer)
- Y (integer)

**Outputs:**
- Out (exec)
- Return Value (struct)

**Description:** Incredibly inefficient and slow operation! Read a value as sRGB color from a render target using integer pixel coordinates. LDR render targets are assumed to be in sRGB space. HDR ones are assumed to be in linear space. Result is 8-bit per channel [0,255] BGRA in sRGB space.
---

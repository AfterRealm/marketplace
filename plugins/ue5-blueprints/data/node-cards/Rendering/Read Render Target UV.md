## Read Render Target UV
**Category:** Rendering
**Search:** "Read Render Target UV"
**Target:** Kismet Rendering Library

**Inputs:**
- In (exec)
- Texture Render Target (object)
- U (real)
- V (real)

**Outputs:**
- Out (exec)
- Return Value (struct)

**Description:** Incredibly inefficient and slow operation! Read a value as sRGB color from a render target using UV [0,1]x[0,1] coordinates. LDR render targets are assumed to be in sRGB space. HDR ones are assumed to be in linear space. Result is 8-bit per channel [0,255] BGRA in sRGB space.
---

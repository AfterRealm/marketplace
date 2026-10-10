## Read Render Target
**Category:** Rendering
**Search:** "Read Render Target"
**Target:** Kismet Rendering Library

**Inputs:**
- In (exec)
- Texture Render Target (object)
- Normalize (boolean)

**Outputs:**
- Out (exec)
- Out Samples (struct)
- Return Value (boolean)

**Description:** Incredibly inefficient and slow operation! Reads entire render target as sRGB color and returns a linear array of sRGB colors. LDR render targets are assumed to be in sRGB space. HDR ones are assumed to be in linear space. Result whether the operation succeeded. If successful, OutSamples will an entry per pixel, where each is 8-bit per channel [0,255] BGRA in sRGB space.
---

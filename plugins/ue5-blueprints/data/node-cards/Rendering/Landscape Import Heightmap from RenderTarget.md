## Landscape Import Heightmap from RenderTarget
**Category:** Rendering
**Search:** "Landscape Import Heightmap from RenderTarget"
**Target:** Landscape Proxy

**Inputs:**
- In (exec)
- Target (object)
- In Render Target (object) — Valid render target with a format of RTF_RGBA16f, RTF_RGBA32f or RTF_RGBA8
- In Import Height from RGChannel (boolean) — Only relevant when using format RTF_RGBA16f or RTF_RGBA32f, and will tell us if we should import the height data from the R channel only of the Render target or from R & G. Note that using RTF_RGBA16f with InImportHeightFromRGChannel == false, could have precision loss Only works in the editor
- In Edit Layer Index (integer)

**Outputs:**
- Out (exec)
- Return Value (boolean)

**Description:** Overwrites a landscape heightmap with render target data
---

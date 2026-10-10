## Landscape Export Heightmap to RenderTarget
**Category:** Rendering
**Search:** "Landscape Export Heightmap to RenderTarget"
**Target:** Landscape Proxy

**Inputs:**
- In (exec)
- Target (object)
- In Render Target (object) — Valid render target with a format of RTF_RGBA16f, RTF_RGBA32f or RTF_RGBA8
- In Export Height Into RGChannel (boolean) — Tell us if we should export the height that is internally stored as R & G (for 16 bits) to a single R channel of the render target (the format need to be RTF_RGBA16f or RTF_RGBA32f) Note that using RTF_RGBA16f with InExportHeightIntoRGChannel == false, could have precision loss.
- In Export Landscape Proxies (boolean) — Option to also export components of all proxies of Landscape actor (if LandscapeProxy is the Landscape Actor)

**Outputs:**
- Out (exec)
- Return Value (boolean)

**Description:** Output a landscape heightmap to a render target
---

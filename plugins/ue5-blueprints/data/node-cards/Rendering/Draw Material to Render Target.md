## Draw Material to Render Target
**Category:** Rendering
**Search:** "Draw Material to Render Target"
**Target:** Kismet Rendering Library

**Inputs:**
- In (exec)
- Texture Render Target (object)
- Material (object)

**Outputs:**
- Out (exec)

**Description:** Renders a quad with the material applied to the specified render target. This sets the render target even if it is already set, which is an expensive operation. Use BeginDrawCanvasToRenderTarget / EndDrawCanvasToRenderTarget instead if rendering multiple primitives to the same render target.
---

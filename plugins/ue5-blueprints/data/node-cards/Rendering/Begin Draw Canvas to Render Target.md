## Begin Draw Canvas to Render Target
**Category:** Rendering
**Search:** "Begin Draw Canvas to Render Target"
**Target:** Kismet Rendering Library

**Inputs:**
- In (exec)
- Texture Render Target (object)

**Outputs:**
- Out (exec)
- Canvas (object)
- Size (vector2d struct)
- Context (struct)

**Description:** Returns a Canvas object that can be used to draw to the specified render target. Canvas has functions like DrawMaterial with size parameters that can be used to draw to a specific area of a render target. Be sure to call EndDrawCanvasToRenderTarget to complete the rendering!
---

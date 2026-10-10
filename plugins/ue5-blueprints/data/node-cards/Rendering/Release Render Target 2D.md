## Release Render Target 2D
**Category:** Rendering
**Search:** "Release Render Target 2D"
**Target:** Kismet Rendering Library

**Inputs:**
- In (exec)
- Texture Render Target (object)

**Outputs:**
- Out (exec)

**Description:** Manually releases GPU resources of a render target. This is useful for blueprint creating a lot of render target that would normally be released too late by the garbage collector that can be problematic on platforms that have tight GPU memory constrains.
---

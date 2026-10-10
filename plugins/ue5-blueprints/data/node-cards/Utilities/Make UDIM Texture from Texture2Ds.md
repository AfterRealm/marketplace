## Make UDIM Texture from Texture2Ds
**Category:** Utilities
**Search:** "Make UDIM Texture from Texture2Ds"
**Target:** UDIMTexture Function Library

**Inputs:**
- In (exec)
- Output Path Name (string) — Path name of the UDIM texture (e.g. /Game/MyTexture)
- Source Textures (object) — List of regular 2D textures to be packed into the atlas
- Block Coords (struct) — Coordinates of the corresponding texture in the atlas
- Keep Existing Settings (boolean) — Whether to keep existing settings if a texture with the same path name exists. Otherwise, settings will be copied from the first source texture
- Check Out and Save (boolean) — Whether to check out and save the UDIM texture

**Outputs:**
- Out (exec)
- Return Value (object) — UTexture2D* Pointer to the UDIM texture or null if failed

**Description:** Make a UDIM virtual texture from a list of regular 2D textures
---

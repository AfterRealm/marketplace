## Prestream Textures
**Category:** Rendering
**Search:** "Prestream Textures"
**Target:** Actor

**Inputs:**
- In (exec)
- Target (object)
- Seconds (real) — Number of seconds to force all mip-levels to be resident
- Enable Streaming (boolean) — Whether to start (true) or stop (false) streaming
- Cinematic Texture Groups (integer) — Bitfield indicating which texture groups that use extra high-resolution mips

**Outputs:**
- Out (exec)

**Description:** Calls PrestreamTextures() for all the actor's meshcomponents.
---

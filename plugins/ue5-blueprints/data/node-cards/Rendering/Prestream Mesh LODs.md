## Prestream Mesh LODs
**Category:** Rendering
**Search:** "Prestream Mesh LODs"
**Target:** Mesh Component

**Inputs:**
- In (exec)
- Target (object)
- Seconds (real) — Number of seconds to force all LODs to be resident

**Outputs:**
- Out (exec)
- Return Value (boolean) — bool True if streaming was successfully requested

**Description:** Tell the streaming system to start streaming in all LODs for the mesh. Note: this function may set bIgnoreStreamingMipBias on this component enable the FastForceResident system.
---

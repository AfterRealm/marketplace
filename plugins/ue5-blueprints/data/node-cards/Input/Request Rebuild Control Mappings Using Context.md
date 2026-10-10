## Request Rebuild Control Mappings Using Context
**Category:** Input
**Search:** "Request Rebuild Control Mappings Using Context"
**Target:** Enhanced Input Library

**Inputs:**
- In (exec)
- Context (object) — Mappings will be rebuilt for all subsystems utilizing this context.
- Force Immediately (boolean) — The mapping changes will be applied synchronously, rather than at the end of the frame, making them available to the input system on the same frame.

**Outputs:**
- Out (exec)

**Description:** Flag all enhanced input subsystems making use of the mapping context for reapplication of all control mappings at the end of this frame.
---

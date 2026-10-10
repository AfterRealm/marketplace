## Get Attach Parent Actor
**Category:** Actor
**Search:** "Get Attach Parent Actor"
**Target:** Actor

**Inputs:**
- Target (object)

**Outputs:**
- Return Value (object)

**Description:** Walk up the attachment chain from RootComponent until we encounter a different actor, and return it. If we are not attached to a component in a different actor, returns nullptr
---

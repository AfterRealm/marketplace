## Get Attach Parent Socket Name
**Category:** Actor
**Search:** "Get Attach Parent Socket Name"
**Target:** Actor

**Inputs:**
- Target (object)

**Outputs:**
- Return Value (name)

**Description:** Walk up the attachment chain from RootComponent until we encounter a different actor, and return the socket name in the component. If we are not attached to a component in a different actor, returns NAME_None
---

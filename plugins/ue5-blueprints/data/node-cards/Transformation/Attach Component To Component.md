## Attach Component To Component
**Category:** Transformation
**Search:** "Attach Component To Component"
**Target:** Scene Component

**Inputs:**
- In (exec)
- Target (object)
- Parent (object) — Parent to attach to.
- Socket Name (name) — Optional socket to attach to on the parent.
- Location Rule (enum) — How to handle translation when attaching.
- Rotation Rule (enum) — How to handle rotation when attaching.
- Scale Rule (enum) — How to handle scale when attaching.
- Weld Simulated Bodies (boolean) — Whether to weld together simulated physics bodies. This transfers the shapes in the welded object into the parent (if simulated), which can result in permanent changes that persist even after subsequently detaching.

**Outputs:**
- Out (exec)
- Return Value (boolean) — True if attachment is successful (or already attached to requested parent/socket), false if attachment is rejected and there is no change in AttachParent.

**Description:** Attach this component to another scene component, optionally at a named socket. It is valid to call this on components whether or not they have been Registered.
---

## Attach Actor To Component
**Category:** Transformation
**Search:** "Attach Actor To Component"
**Target:** Actor

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
- Return Value (boolean) — Whether the attachment was successful or not

**Description:** Attaches the RootComponent of this Actor to the supplied component, optionally at a named socket. It is not valid to call this on components that are not Registered.
---

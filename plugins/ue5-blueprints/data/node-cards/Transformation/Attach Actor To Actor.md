## Attach Actor To Actor
**Category:** Transformation
**Search:** "Attach Actor To Actor"
**Target:** Actor

**Inputs:**
- In (exec)
- Target (object)
- Parent Actor (object) — Actor to attach this actor's RootComponent to
- Socket Name (name) — Socket name to attach to, if any
- Location Rule (enum) — How to handle translation when attaching.
- Rotation Rule (enum) — How to handle rotation when attaching.
- Scale Rule (enum) — How to handle scale when attaching.
- Weld Simulated Bodies (boolean) — Whether to weld together simulated physics bodies.This transfers the shapes in the welded object into the parent (if simulated), which can result in permanent changes that persist even after subsequently detaching.

**Outputs:**
- Out (exec)
- Return Value (boolean) — Whether the attachment was successful or not

**Description:** Attaches the RootComponent of this Actor to the supplied actor, optionally at a named socket.
---

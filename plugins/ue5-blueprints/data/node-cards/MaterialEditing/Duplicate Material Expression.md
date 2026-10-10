## Duplicate Material Expression
**Category:** MaterialEditing
**Search:** "Duplicate Material Expression"
**Target:** Material Editing Library

**Inputs:**
- In (exec)
- Material (object) — Material asset to add an expression to
- Material Function (object) — Specified if adding an expression to a MaterialFunction, used as Outer for new expression object
- Expression (object)

**Outputs:**
- Out (exec)
- Return Value (object)

**Description:** Duplicates the provided material expression adding it to the same material / material function, and copying parameters. Note: Does not duplicate transient properties (Ex: GraphNode).
---

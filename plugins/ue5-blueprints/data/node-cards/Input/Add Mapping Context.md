## Add Mapping Context
**Category:** Input
**Search:** "Add Mapping Context"
**Target:** Enhanced Input Subsystem Interface

**Inputs:**
- In (exec)
- Target (interface)
- Mapping Context (object) — A set of key to action mappings to apply to this player
- Priority (integer) — Higher priority mappings will be applied first and, if they consume input, will block lower priority mappings.
- Options (struct) — Options to consider when adding this mapping context.

**Outputs:**
- Out (exec)

**Description:** Add a control mapping context.
---

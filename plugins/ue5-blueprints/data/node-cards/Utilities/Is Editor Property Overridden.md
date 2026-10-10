## Is Editor Property Overridden
**Category:** Utilities
**Search:** "Is Editor Property Overridden"
**Target:** Kismet System Library

**Inputs:**
- In (exec)
- Object (object) — The object you want to query a property value on.
- Property Name (name) — The name of the object property to query the value of.

**Outputs:**
- Out (exec)
- Return Value (enum) — What state the requested property is in.

**Description:** Attempts to query whether the value of a named property on the given object overrides the value of its archetype (ie, would ResetEditorProperty do anything?).
---

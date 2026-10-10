## Reset Editor Property
**Category:** Utilities
**Search:** "Reset Editor Property"
**Target:** Kismet System Library

**Inputs:**
- In (exec)
- Object (object) — The object you want to reset a property value on.
- Property Name (name) — The name of the object property to reset the value of.
- Change Notify Mode (enum) — When to emit property change notifications.

**Outputs:**
- Out (exec)
- Return Value (boolean) — Whether the property value was found and correctly reset.

**Description:** Attempts to reset the value of a named property on the given object so that it matches the value of the archetype.
---

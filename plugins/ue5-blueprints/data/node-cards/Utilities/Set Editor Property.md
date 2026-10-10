## Set Editor Property
**Category:** Utilities
**Search:** "Set Editor Property"
**Target:** Kismet System Library

**Inputs:**
- In (exec)
- Object (object) — The object you want to set a property value on.
- Property Name (name) — The name of the object property to set the value of.
- Property Value (wildcard) — The property value to set.
- Change Notify Mode (enum) — When to emit property change notifications.

**Outputs:**
- Out (exec)
- Success? (boolean) — Whether the property value was found and correctly set.

**Description:** Attempts to set the value of a named property on the given object.
---

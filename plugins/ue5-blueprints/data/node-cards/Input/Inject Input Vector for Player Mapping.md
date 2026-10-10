## Inject Input Vector for Player Mapping
**Category:** Input
**Search:** "Inject Input Vector for Player Mapping"
**Target:** Enhanced Input Subsystem Interface

**Inputs:**
- In (exec)
- Target (interface)
- Mapping Name (name) — The name of the player mapping that can be used for look up an associated UInputAction object.
- Value (vector) — The value to set the action to (the type will be controlled by the Action)
- Modifiers (object) — The modifiers to apply to the injected input.
- Triggers (object) — The triggers to apply to the injected input.

**Outputs:**
- Out (exec)

**Description:** Input simulation via injection. Runs modifiers and triggers delegates as if the input had come through the underlying input system as FKeys. Applies action modifiers and triggers on top.
---

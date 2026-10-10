## Start Continuous Input Injection for Player Mapping
**Category:** Input
**Search:** "Start Continuous Input Injection for Player Mapping"
**Target:** Enhanced Input Subsystem Interface

**Inputs:**
- In (exec)
- Target (interface)
- Mapping Name (name) — The name of the player mapping that can be used for look up an associated UInputAction object.
- Raw Value (struct) — The value to set the action to (the type will be controlled by the Action)
- Modifiers (object) — The modifiers to apply to the injected input.
- Triggers (object) — The triggers to apply to the injected input.

**Outputs:**
- Out (exec)

**Description:** Starts simulation of input via injection. This injects the given input every tick until it is stopped with StopContinuousInputInjectionForAction.
---

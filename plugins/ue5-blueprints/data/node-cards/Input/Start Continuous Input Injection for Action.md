## Start Continuous Input Injection for Action
**Category:** Input
**Search:** "Start Continuous Input Injection for Action"
**Target:** Enhanced Input Subsystem Interface

**Inputs:**
- In (exec)
- Target (interface)
- Action (object) — The Input Action to set inject input for
- Raw Value (struct) — The value to set the action to (the type will be controlled by the Action)
- Modifiers (object) — The modifiers to apply to the injected input.
- Triggers (object) — The triggers to apply to the injected input.

**Outputs:**
- Out (exec)

**Description:** Starts simulation of input via injection. This injects the given input every tick until it is stopped with StopContinuousInputInjectionForAction.
---

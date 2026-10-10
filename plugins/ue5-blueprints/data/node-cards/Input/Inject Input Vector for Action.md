## Inject Input Vector for Action
**Category:** Input
**Search:** "Inject Input Vector for Action"
**Target:** Enhanced Input Subsystem Interface

**Inputs:**
- In (exec)
- Target (interface)
- Action (object) — The Input Action to set inject input for
- Value (vector) — The value to set the action to (the type will be controlled by the Action)
- Modifiers (object) — The modifiers to apply to the injected input.
- Triggers (object) — The triggers to apply to the injected input.

**Outputs:**
- Out (exec)

**Description:** Input simulation via injection. Runs modifiers and triggers delegates as if the input had come through the underlying input system as FKeys. Applies action modifiers and triggers on top.
---

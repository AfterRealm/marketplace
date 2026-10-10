## Set Ignore Move Input
**Category:** Input
**Search:** "Set Ignore Move Input"
**Target:** Controller

**Inputs:**
- In (exec)
- Target (object)
- New Move Input (boolean) — If true, move input is ignored. If false, input is not ignored.

**Outputs:**
- Out (exec)

**Description:** Locks or unlocks movement input, consecutive calls stack up and require the same amount of calls to undo, or can all be undone using ResetIgnoreMoveInput.
---

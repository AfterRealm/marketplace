## Possess
**Category:** Pawn
**Search:** "Possess"
**Target:** Controller

**Inputs:**
- In (exec)
- Target (object)
- In Pawn (object) — The Pawn to be possessed.

**Outputs:**
- Out (exec)

**Description:** Handles attaching this controller to the specified pawn. Only runs on the network authority (where HasAuthority() returns true). Derived native classes can override OnPossess to filter the specified pawn. When possessed pawn changed, blueprint class gets notified by ReceivePossess and OnNewPawn delegate is broadcasted.
---

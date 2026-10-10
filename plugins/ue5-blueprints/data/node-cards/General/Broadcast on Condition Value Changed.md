## Broadcast on Condition Value Changed
**Category:** General
**Search:** "Broadcast on Condition Value Changed"
**Target:** Day Sequence Condition Tag

**Inputs:**
- In (exec)
- Target (object)

**Outputs:**
- Out (exec)

**Description:** Derived classes should call this function to notify listeners that the underlying condition may have changed. This will only trigger a broadcast if Evaluate() returns a different value than the last invocation of this function.
---

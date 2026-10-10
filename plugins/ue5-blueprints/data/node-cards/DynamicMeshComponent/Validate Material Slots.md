## Validate Material Slots
**Category:** DynamicMeshComponent
**Search:** "Validate Material Slots"
**Target:** Dynamic Mesh Component

**Inputs:**
- In (exec)
- Target (object)
- Create if Missing (boolean) — if true, add extra (empty) Material Slots to match max MaterialID
- Delete Extra Slots (boolean) — if true, extra Material Slots beyond max MaterialID are removed

**Outputs:**
- Out (exec)
- Return Value (boolean) — true if at the end of this function, Material Slot Count == Max MaterialID

**Description:** Compute the maximum MaterialID on the DynamicMesh, and ensure that Material Slots match. Pass both arguments as false to just do a check.
---

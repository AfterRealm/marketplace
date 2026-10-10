## Detach From Component
**Category:** Transformation
**Search:** "Detach From Component"
**Target:** Scene Component

**Inputs:**
- In (exec)
- Target (object)
- Location Rule (enum) — How to handle translations when detaching.
- Rotation Rule (enum) — How to handle rotation when detaching.
- Scale Rule (enum) — How to handle scales when detaching.
- Call Modify (boolean) — If true, call Modify() on the component and the current attach parent component

**Outputs:**
- Out (exec)

**Description:** Detach this component from whatever it is attached to. Automatically unwelds components that are welded together (see AttachToComponent), though note that some effects of welding may not be undone.
---

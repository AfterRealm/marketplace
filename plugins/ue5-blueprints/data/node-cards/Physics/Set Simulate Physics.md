## Set Simulate Physics
**Category:** Physics
**Search:** "Set Simulate Physics"
**Target:** Primitive Component

**Inputs:**
- In (exec)
- Target (object)
- Simulate (boolean) — New simulation state for the single body or multiple bodies

**Outputs:**
- Out (exec)

**Description:** When this component is a simple/single body, this will enable or disable simulation on that body. In addition, if this component is currently attached to something, beginning simulation will detach it. Note that stopping simulation will not reattach the component - that would need to be done explicitly. For more complex components (e.g. skeletal meshes), simulation will apply to the bodies contained by the component (e.g. using a physics asset). Since these bodies will be free to move independently of the component, the component will not be automatically detached. If detachment is required, then that can be done by calling DetachFromComponent.
---

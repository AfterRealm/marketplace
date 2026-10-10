## Set Notify Rigid Body Collision Below
**Category:** Physics
**Search:** "Set Notify Rigid Body Collision Below"
**Target:** Skeletal Mesh Component

**Inputs:**
- In (exec)
- Target (object)
- New Notify Rigid Body Collision (boolean) — The value to assign to bNotifyRigidBodyCollision
- Bone Name (name) — Name of the body to turn hit notifies on (and below)
- Include Self (boolean) — Whether to modify the given body (useful for roots with multiple children)

**Outputs:**
- Out (exec)

**Description:** Changes the value of bNotifyRigidBodyCollision on all bodies below a given bone
---

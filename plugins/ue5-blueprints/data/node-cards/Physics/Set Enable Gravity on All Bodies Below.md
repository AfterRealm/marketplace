## Set Enable Gravity on All Bodies Below
**Category:** Physics
**Search:** "Set Enable Gravity on All Bodies Below"
**Target:** Skeletal Mesh Component

**Inputs:**
- In (exec)
- Target (object)
- Enable Gravity (boolean) — Whether gravity should be enabled or disabled.
- Bone Name (name) — The name of the top most bone.
- Include Self (boolean) — Whether the bone specified should be edited.

**Outputs:**
- Out (exec)

**Description:** Enables or disables gravity to all bodies below the given bone. NAME_None indicates all bodies will be edited. In that case, consider using UPrimitiveComponent::EnableGravity.
---

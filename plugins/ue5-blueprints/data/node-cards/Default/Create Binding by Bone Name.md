## Create Binding by Bone Name
**Category:** Default
**Search:** "Create Binding by Bone Name"
**Target:** Nanite Assembly Skeletal Mesh Builder

**Inputs:**
- In (exec)
- Target (object)
- Bone Name (name)
- Weight (real)
- Transform (transform)
- Transform Space (enum)

**Outputs:**
- Out (exec)
- Out Binding (struct)
- Success (boolean)

**Description:** Attempts to create a new skeletal mesh part binding from the specified bone's name. For multiple bone influence, use AddBoneInfluenceByName for each additional bone.
---

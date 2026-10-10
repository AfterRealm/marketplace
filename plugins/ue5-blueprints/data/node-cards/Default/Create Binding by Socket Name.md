## Create Binding by Socket Name
**Category:** Default
**Search:** "Create Binding by Socket Name"
**Target:** Nanite Assembly Skeletal Mesh Builder

**Inputs:**
- In (exec)
- Target (object)
- Socket Name (name)
- Transform (transform)
- Transform Space (enum)

**Outputs:**
- Out (exec)
- Out Binding (struct)
- Success (boolean)

**Description:** Attempts to create a new skeletal mesh part binding from a socket's name. WARNING: Don't add additional bone influences to the binding when creating from a socket, or the attachment won't look right.
---

## Rename Material Function Parameter Group
**Category:** MaterialEditing
**Search:** "Rename Material Function Parameter Group"
**Target:** Material Editing Library

**Inputs:**
- In (exec)
- Material Function (object) — The material function asset in which the parameter group resides.
- Old Group Name (name) — The current name of the parameter group to rename.
- New Group Name (name) — The new name to assign to the parameter group.

**Outputs:**
- Out (exec)
- Return Value (boolean) — true if the rename operation was successful; false otherwise.

**Description:** Renames a material parameter group within the specified material function. This function allows you to rename an existing parameter group in a material function. It iterates all parameters within the material function, finds all the one belonging to the OldGroupName group and switches those parameters to be in the NewGroupName group. This function only affects parameters that belong to the specified group. To remove the groups from the parameters the new group name can be 'None'. If the OldGroupName does not exist in the material, the function will return false. If the NewGroupName already exists, the parameters will be "merged" into the existing group.
---

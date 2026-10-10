## Get Scalar Parameter Source
**Category:** MaterialEditing
**Search:** "Get Scalar Parameter Source"
**Target:** Material Editing Library

**Inputs:**
- In (exec)
- Material (object) — The material or material instance you want to look up a parameter from
- Parameter Name (name) — The parameter name

**Outputs:**
- Out (exec)
- Parameter Source (struct) — The soft object path of the asset the parameter originates in
- Return Value (boolean) — Whether or not the parameter was found in this material

**Description:** Returns the path of the asset where the parameter originated, as well as true/false if it was found
---

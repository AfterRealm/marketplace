## Get Constraints from Body
**Category:** Physics
**Search:** "Get Constraints from Body"
**Target:** Skeletal Mesh Component

**Inputs:**
- In (exec)
- Target (object)
- Body Name (name) — name of the body to get the attached constraints from
- Parent Constraints (boolean) — return constraints where BodyName is the child of the constraint
- Child Constraints (boolean) — return constraints where BodyName is the parent of the constraint
- Includes Terminated (boolean)

**Outputs:**
- Out (exec)
- Out Constraints (struct) — returned list of constraints matching the parameters

**Description:** Gets all the constraints attached to a body
---

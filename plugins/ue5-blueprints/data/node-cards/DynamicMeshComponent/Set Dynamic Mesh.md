## Set Dynamic Mesh
**Category:** DynamicMeshComponent
**Search:** "Set Dynamic Mesh"
**Target:** Dynamic Mesh Component

**Inputs:**
- In (exec)
- Target (object)
- New Mesh (object)

**Outputs:**
- Out (exec)

**Description:** Replace the current UDynamicMesh with a new one, and transfer ownership of NewMesh to this Component. This can be used to (eg) assign a UDynamicMesh created with NewObject in the Transient Package to this Component. @warning If NewMesh is owned/Outer'd to another DynamicMeshComponent, a GLEO error may occur if that Component is serialized.
---

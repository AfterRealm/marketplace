## Get Body Instance Async Physics Tick Handle
**Category:** Physics
**Search:** "Get Body Instance Async Physics Tick Handle"
**Target:** Primitive Component

**Inputs:**
- Target (object)
- Bone Name (name) — Used to get body associated with specific bone. NAME_None automatically gets the root most body
- Get Welded (boolean) — If the component has been welded to another component and bGetWelded is true we return the single welded BodyInstance that is used in the simulation
- Index (integer) — Index used in Components with multiple body instances

**Outputs:**
- Return Value (struct) — Returns the BodyInstanceAsyncPhysicsTickHandle based on various states (does component have multiple bodies? Is the body welded to another body?)

**Description:** Returns BodyInstanceAsyncPhysicsTickHandle of the component. For use in the Async Physics Tick event
---

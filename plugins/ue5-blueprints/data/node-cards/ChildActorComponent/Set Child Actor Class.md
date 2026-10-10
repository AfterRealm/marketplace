## Set Child Actor Class
**Category:** ChildActorComponent
**Search:** "Set Child Actor Class"
**Target:** Child Actor Component

**Inputs:**
- In (exec)
- Target (object)
- In Class (class) — The Actor subclass to spawn as a child actor

**Outputs:**
- Out (exec)

**Description:** Sets the class to use for the child actor. If called on a template component (owned by a CDO), the properties of any existing child actor template will be copied as best possible to the template. If called on a component instance in a world (and the class is changing), the created ChildActor will use the class defaults as template.
---

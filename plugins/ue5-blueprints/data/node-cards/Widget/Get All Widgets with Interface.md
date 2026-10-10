## Get All Widgets with Interface
**Category:** Widget
**Search:** "Get All Widgets with Interface"
**Target:** Widget Blueprint Library

**Inputs:**
- In (exec)
- Interface (class) — The interface to find. Must be specified or result array will be empty.
- Top Level Only (boolean) — Only the widgets that are direct children of the viewport will be returned.

**Outputs:**
- Out (exec)
- Found Widgets (object) — Output array of widgets that implement the specified interface.

**Description:** Find all widgets in the world with the specified interface. This is a slow operation, use with caution e.g. do not use every frame.
---

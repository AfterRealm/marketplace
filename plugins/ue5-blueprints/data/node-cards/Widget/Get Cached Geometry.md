## Get Cached Geometry
**Category:** Widget
**Search:** "Get Cached Geometry"
**Target:** Widget

**Inputs:**
- Target (object)

**Outputs:**
- Return Value (struct)

**Description:** Gets the last geometry used to Tick the widget. This data may not exist yet if this call happens prior to the widget having been ticked/painted, or it may be out of date, or a frame behind. We recommend not to use this data unless there's no other way to solve your problem. Normally in Slate we try and handle these issues by making a dependent widget part of the hierarchy, as to avoid frame behind or what are referred to as hysteresis problems, both caused by depending on geometry from the previous frame being used to advise how to layout a dependent object the current frame.
---

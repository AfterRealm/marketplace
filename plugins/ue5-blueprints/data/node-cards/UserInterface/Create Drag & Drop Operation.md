## Create Drag & Drop Operation
**Category:** UserInterface
**Search:** "Create Drag & Drop Operation"

**Inputs:**
- In (exec)
- Class (class) — Drag Drop Operation Class Reference ClassThe object class you want to construct
- Tag (string) — A simple string tag you can optionally use to provide extra metadata about the operation.
- Payload (object) — The payload of the drag operation. This can be any UObject that you want to pass along as dragged data. If youwere building an inventory screen this would be the UObject representing the item being moved to another slot.
- Default Drag Visual (object) — The Drag Visual is the widget to display when dragging the item. Normally people create a new widget to represent thetemporary drag.
- Pivot (enum) — Controls where the drag widget visual will appear when dragged relative to the pointer performingthe drag operation.
- Offset (vector2d struct) — A percentage offset (-1..+1) from the Pivot location, the percentage is of the desired size of the dragged visual.

**Outputs:**
- Out (exec)
- Return Value (object) — Drag Drop Operation Object Reference Return ValueThe constructed object

**Description:** Creates a new drag drop operation
---

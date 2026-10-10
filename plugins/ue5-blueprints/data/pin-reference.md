# UE5 Blueprint Pin Quick Reference

## Pin Types by Color

| Color | Type | Notes |
|-------|------|-------|
| **White arrow** | Execution | Controls flow order. Left = input, right = output. |
| **Bright green** | Boolean | True/False |
| **Cyan / teal** | Integer | Whole numbers |
| **Light green** | Float / Double | Decimal numbers |
| **Dark teal** | Array | Any array type — hover to see element type |
| **Blue** | Object reference | Actor, Component, Widget, etc. |
| **Purple** | Class reference | A class itself, not an instance |
| **Red / dark red** | Byte / Enum | Enum values show as dropdown |
| **Magenta / pink** | String | Text data |
| **Salmon / light pink** | Name | FName — used for lookups and tags |
| **Light purple** | Text | FText — localized display text |
| **Gold / yellow** | Struct | Compound data (Vector, Rotator, Transform, etc.) |
| **Gray** | Wildcard | Adapts to whatever you connect |
| **Dark gray** | Delegate | Event dispatcher bindings |

## Pin Sides

- **Left side** = Input (data flows IN, execution enters)
- **Right side** = Output (data flows OUT, execution exits)

## Execution Pins (White Arrows)

Every node that does something has at least one exec pin:
- **Input exec** (left) = "when this node should fire"
- **Output exec** (right) = "what fires next"

Some nodes have multiple output exec pins:
- **Branch**: True (top) and False (bottom)
- **ForEachLoop**: Loop Body (top), Completed (bottom)
- **Sequence**: Then 0, Then 1, Then 2...
- **Switch**: One output per case + Default
- **Cast**: Success (top) and Cast Failed (bottom)

## Data Pins (Colored Circles)

- **Solid circle** = connected
- **Hollow circle** = disconnected (may have default value)
- **Small triangle on pin** = pass-by-reference (writes go through to source)

## Common Pin Names

| Pin Name | What It Does |
|----------|-------------|
| **self / Target** | The object this node operates on |
| **Return Value** | The result of a function call |
| **Array Element** | Current item in a ForEachLoop |
| **Array Index** | Current index in a ForEachLoop |
| **Index** | Which element to access in an array |
| **Condition** | Boolean input for Branch nodes |
| **Exec** / **then** | Standard execution output |
| **Completed** | Fires when a loop finishes all iterations |
| **Loop Body** | Fires once per loop iteration |

## Wire Rules

- **One output → many inputs**: OK (fan out)
- **Many outputs → one input**: NOT OK (only one wire per input)
- **Exec wires** (white): only connect to other exec pins
- **Data wires** (colored): only connect to matching types (or auto-converts)
- **Dragging from output to empty space**: opens search filtered to compatible nodes

# UE5 Blueprint Language Rules

When communicating Blueprint instructions to users, follow these rules strictly. They exist because Blueprint users are often visual thinkers, not programmers, and ambiguous instructions cause real mistakes in the editor.

## Terminology — Always Use

- **"node"** not "block", "box", or "element"
- **"pin"** not "port", "connector", or "slot"
- **"wire"** not "line", "connection", or "link"
- **"execution pin"** (white arrow) not "flow pin" or "exec pin"
- **"data pin"** (colored circle) not "value pin" or "input/output"
- **"search [NodeName]"** when telling users to place a node (they use the right-click search)

## Pin Colors

Always include the pin color when referencing pins:
- **White arrow** = Execution (controls flow order)
- **Green** = Boolean / Integer (context-dependent)
- **Dark green** = Float / Double
- **Dark teal / turquoise** = Array
- **Blue** = Object reference
- **Red / pink** = Boolean
- **Magenta / pink** = String / Name
- **Gold / yellow** = Struct
- **Purple** = Enum

Include the **side** (left = input, right = output):
"the green output pin on the right side of the Add node"

## Step Writing Rules

### Required
- Pin descriptions include COLOR and SIDE
- Exact search terms for placing nodes: "right-click and search **Set Material**"
- Number duplicate nodes: "Get ReadPos (1)", "Get ReadPos (2)"
- Parenthetical identifiers: "the Subtract node (the one connected to PlayerIndex)"
- Strictly sequential steps — each step only references nodes from prior steps
- When setting values: "click the pin and type **8801**"
- When checking boxes: "check the box next to **Client Side Only**"

### Forbidden
- X/Y coordinates or position numbers
- "Inner loop" / "outer loop" — use "first ForLoop", "second ForLoop"
- Vague references like "connect the output to the input" — WHICH output? WHICH input?
- Forward references — never say "wire to the node from step 12" in step 5
- Jargon without definition — first time a term appears, explain it
- "The loop" when there are multiple loops — specify WHICH one
- Internal class names (K2Node_CallFunction) — use the searchable name
- Steps that place AND wire more than one node (in complex sections)

### Formatting
- Number all steps: 1, 2, 3
- Bold all node names: **Branch**, **ForLoop**, **Set Array Elem**
- Bold all pin names: **Use Index**, **Target Array**
- One blank line between steps for readability
- Group related steps under headers for long sequences

## Press Key
**Category:** Interaction
**Search:** "Press Key"
**Target:** Widget Interaction Component

**Inputs:**
- In (exec)
- Target (object)
- Key (struct)
- Repeat (boolean)

**Outputs:**
- Out (exec)
- Return Value (boolean)

**Description:** Press a key as if it had come from the keyboard. Avoid using this for 'a-z|A-Z', things like the Editable Textbox in Slate expect OnKeyChar to be called to signal a specific character being send to the widget. So for those cases you should use SendKeyChar.
---

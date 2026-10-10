## Set Input Mode Game And UI
**Category:** Input
**Search:** "Set Input Mode Game And UI"
**Target:** Widget Blueprint Library

**Inputs:**
- In (exec)
- Player Controller (object)
- In Widget to Focus (object)
- In Mouse Lock Mode (enum)
- Hide Cursor During Capture (boolean)
- Flush Input (boolean)

**Outputs:**
- Out (exec)

**Description:** Setup an input mode that allows only the UI to respond to user input, and if the UI doesn't handle it player input / player controller gets a chance. Note: This means that any bound Input events in the widget will be called.
---

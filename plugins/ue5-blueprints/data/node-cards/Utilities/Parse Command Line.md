## Parse Command Line
**Category:** Utilities
**Search:** "Parse Command Line"
**Target:** Kismet System Library

**Inputs:**
- In (exec)
- In Cmd Line (string) — The the string to parse (ie '-foo -bar=/game/baz testtoken' ) *

**Outputs:**
- Out (exec)
- Out Tokens (string)
- Out Switches (string)
- Out Params (string)

**Description:** Parses the given string into loose tokens, switches (arguments that begin with - or /) and parameters (-mySwitch=myVar)
---

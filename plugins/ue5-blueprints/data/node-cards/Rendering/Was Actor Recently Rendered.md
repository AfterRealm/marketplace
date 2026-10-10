## Was Actor Recently Rendered
**Category:** Rendering
**Search:** "Was Actor Recently Rendered"
**Target:** Actor

**Inputs:**
- Target (object)
- Tolerance (real) — How many seconds ago the actor last render time can be and still count as having been "recently" rendered.

**Outputs:**
- Return Value (boolean) — Whether this actor was recently rendered.

**Description:** Returns true if this actor has been rendered "recently", with a tolerance in seconds to define what "recent" means. e.g.: If a tolerance of 0.1 is used, this function will return true only if the actor was rendered in the last 0.1 seconds of game time.
---

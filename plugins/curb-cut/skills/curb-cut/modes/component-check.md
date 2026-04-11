# Mode: Component Check

Deep dive on a single interactive widget. This mode checks the component against WAI-ARIA Authoring Practices — the specific keyboard, focus, and ARIA patterns expected for each widget type.

Scoring, severity levels, rules, and auto-fix all come from the router (`SKILL.md`). This file defines the process, the widget patterns, and the output format.

## Process

1. **Identify the widget type.** If the filename makes it obvious (e.g., `Modal.jsx`, `Tabs.vue`, `Dropdown.svelte`), infer it. If the file contains multiple widgets or the type is ambiguous, ask the user which widget to check before proceeding.
2. Read the component code completely.
3. Look up the matching pattern below (or apply WAI-ARIA Authoring Practices if the type isn't listed).
4. Check three dimensions: **Keyboard Interaction**, **Focus Management**, **State & Properties**.
5. Report findings with the Component Check output format.
6. Offer auto-fix.

## Component Patterns

### Modal / Dialog

**Keyboard:**
| Key | Expected |
|-----|----------|
| Tab / Shift+Tab | Cycles focus within the modal (focus trap) |
| Escape | Closes the modal |

**Focus:**
- On open: focus moves into the modal (to first focusable element, or the dialog itself)
- On close: focus returns to the element that triggered the modal
- Background content does not receive focus while modal is open

**ARIA:**
- `role="dialog"` or native `<dialog>` element
- `aria-modal="true"`
- `aria-labelledby` pointing to the modal's heading
- Background content marked with `inert` attribute or `aria-hidden="true"`

---

### Tabs

**Keyboard:**
| Key | Expected |
|-----|----------|
| Arrow Left/Right | Move between tabs (horizontal) |
| Arrow Up/Down | Move between tabs (vertical) |
| Tab | Move focus from active tab into tab panel |
| Home / End | Move to first / last tab |

**Focus:**
- Active tab: `tabindex="0"`
- Inactive tabs: `tabindex="-1"`
- Arrow keys move focus and optionally activate (automatic activation) or just move (manual activation with Enter/Space)

**ARIA:**
- Container: `role="tablist"`
- Each tab: `role="tab"`
- Each panel: `role="tabpanel"`
- Active tab: `aria-selected="true"`
- Tab → panel: `aria-controls`
- Panel → tab: `aria-labelledby`

---

### Form

**Structure:**
- Every input has a `<label>` with matching `for`/`id` — not just a placeholder
- Related inputs grouped with `<fieldset>` and `<legend>` (e.g., radio groups, address fields)
- Required fields: `aria-required="true"` or `required` attribute, plus visible indicator
- Personal data fields: `autocomplete` attribute set

**Errors:**
- Error messages in text, not just color/icon
- Error linked to input via `aria-describedby`
- `aria-invalid="true"` on invalid fields
- On submission error: focus moves to first invalid field or error summary

**ARIA:**
- Help text linked via `aria-describedby`
- Dynamic validation announced via `aria-live` or `role="alert"`

---

### Dropdown / Menu

**Keyboard:**
| Key | Expected |
|-----|----------|
| Enter / Space | Opens menu (on trigger button) |
| Arrow Down | Moves to next item / opens menu |
| Arrow Up | Moves to previous item |
| Escape | Closes menu |
| Home / End | First / last item |
| Letter keys | Jump to item starting with that letter |

**Focus:**
- On open: focus moves to first menu item
- On close: focus returns to trigger button
- Arrow keys move focus between items

**ARIA:**
- Trigger: `aria-haspopup="true"`, `aria-expanded`
- Container: `role="menu"`
- Items: `role="menuitem"`
- Disabled items: `aria-disabled="true"`

---

### Accordion

**Keyboard:**
| Key | Expected |
|-----|----------|
| Enter / Space | Toggle section open/closed |
| Arrow Up/Down | Move between accordion headers (optional) |
| Home / End | First / last header (optional) |

**Structure:**
- Headers are `<button>` elements (or have `role="button"`) inside heading elements
- Each header has `aria-expanded` indicating open/closed state
- `aria-controls` pointing to the panel

---

### Navigation

**Structure:**
- `<nav>` element with `aria-label` (required if multiple `<nav>` elements exist)
- Skip navigation link as the first focusable element on the page
- Current page indicated with `aria-current="page"`
- Logical tab order matching visual order

---

### Other Widget Types

For components not listed above (combobox, tooltip, tree view, carousel, listbox, slider, etc.), apply the corresponding WAI-ARIA Authoring Practices pattern. Check the same three dimensions: keyboard interaction, focus management, and ARIA state/properties.

## Output Format

```
♿ CURB CUT — Component Check
[filename] → [Component Type]
Pattern: WAI-ARIA [pattern name]

Keyboard Interaction
  ✅ [Key] — [Expected behavior]
  ❌ [Key] — [Expected behavior] → [What's actually happening or missing]
  ...

Focus Management
  ✅ [Expectation met]
  ❌ [Expectation] → [What's wrong]
  ...

State & Properties
  ✅ [ARIA attribute/role present and correct]
  ❌ [ARIA attribute/role] → [What's wrong or missing]
  ...

---

Findings

[Severity emoji] [LEVEL] — [Title]
**WCAG [X.X.X]** [Criterion Name]
**What:** [explanation]
**Who:** [affected users]
**Fix:**
\```[language]
[code fix]
\```

[repeat per finding]

---

Component Score: [X]/[Y] checks passing
Auto-fix available for [X] of [Y] findings.
```

After delivering the component check, return control to the router for Auto-Fix handling.

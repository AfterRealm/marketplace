# Mode: Full Audit

Comprehensive WCAG 2.2 Level AA check. Every applicable criterion, every severity level.

Scoring, severity levels, rules, and auto-fix all come from the router (`SKILL.md`). This file defines the process, the full WCAG 2.2 AA checklist, and the output format.

## Process

1. Read the code thoroughly. Understand the full page or component.
2. Check ALL applicable criteria from the Full Audit Checklist below. Skip criteria that don't apply to the content (e.g., skip audio/video criteria if there's no media).
3. Report findings at every severity level (CRITICAL through LOW).
4. Score overall and per pillar (use the scoring table from the router).
5. List passing criteria.
6. Offer auto-fix.

**Multiple files or directories:** audit each file individually, report per-file scores, then add an aggregate summary. For projects with 10+ files, suggest Quick Scan to stay within context limits.

## Full Audit Checklist

### Perceivable — Can all users perceive the content?

| WCAG | Criterion | What to check |
|------|-----------|---------------|
| 1.1.1 | Non-text Content | Every `<img>`, `<svg>`, icon font, `<canvas>`, and `<video>` has a text alternative. Decorative content has `alt=""` or `aria-hidden="true"`. |
| 1.3.1 | Info and Relationships | Semantic HTML throughout: headings, landmarks, lists, tables with headers, form labels, fieldset/legend for groups. Relationships conveyed visually are also conveyed in markup. |
| 1.3.2 | Meaningful Sequence | DOM order matches visual reading order. CSS doesn't reorder content in a way that breaks meaning. |
| 1.3.4 | Orientation | No CSS or JS that locks display to portrait or landscape only. |
| 1.3.5 | Identify Input Purpose | Personal data fields (`name`, `email`, `tel`, `address`, etc.) have `autocomplete` attributes. |
| 1.4.1 | Use of Color | Information is not conveyed by color alone. Errors, required fields, statuses have text/icon indicators alongside color. |
| 1.4.3 | Contrast (Minimum) | Normal text: 4.5:1. Large text (18pt / 14pt bold): 3:1. Check CSS colors, Tailwind classes, inline styles. |
| 1.4.4 | Resize Text | Font sizes use relative units (`rem`, `em`, `%`), not fixed `px`. No content loss at 200% zoom. |
| 1.4.5 | Images of Text | Real text is used instead of images of text, except logos. |
| 1.4.10 | Reflow | Content works at 320px viewport width without horizontal scrolling. Check for fixed widths, overflow issues. |
| 1.4.11 | Non-text Contrast | UI components (buttons, inputs, icons) and meaningful graphics have 3:1 contrast against adjacent colors. |
| 1.4.12 | Text Spacing | No content loss or overlap when line-height is 1.5×, letter-spacing 0.12em, word-spacing 0.16em, paragraph spacing 2×. Check for fixed-height containers that would clip. |
| 1.4.13 | Content on Hover/Focus | Hover/focus-triggered content (tooltips, dropdowns) is dismissible (Escape), hoverable (mouse can move to it), and persistent (doesn't vanish on its own). |

### Operable — Can all users operate the interface?

| WCAG | Criterion | What to check |
|------|-----------|---------------|
| 2.1.1 | Keyboard | Every interactive element works with keyboard. No `onClick` without keyboard equivalent on non-interactive elements. |
| 2.1.2 | No Keyboard Trap | Focus can always move away from any component. Modals have escape. Custom widgets don't trap Tab. |
| 2.1.4 | Character Key Shortcuts | If single-character shortcuts exist, they can be turned off or remapped. |
| 2.4.1 | Bypass Blocks | Skip navigation link or proper landmark regions (`<main>`, `<nav>`, `<header>`). |
| 2.4.2 | Page Titled | Descriptive `<title>` element. For SPAs: title updates on route change. |
| 2.4.3 | Focus Order | Tab order is logical and predictable. No positive `tabindex` values. DOM order matches visual order. |
| 2.4.4 | Link Purpose | Every link's purpose is clear from its text (or text + surrounding context). No bare "click here" or "read more". |
| 2.4.5 | Multiple Ways | More than one way to reach pages: navigation + search, sitemap, or other. (Page-level check.) |
| 2.4.6 | Headings and Labels | Headings are descriptive and don't skip levels. Labels describe their input's purpose. |
| 2.4.7 | Focus Visible | Clear visible focus indicator on all interactive elements. No `outline: none` without replacement. |
| 2.4.11 | Focus Not Obscured | Focused elements are not fully covered by sticky headers, footers, or overlays. |
| 2.5.1 | Pointer Gestures | Multi-finger or path-based gestures have single-pointer alternatives. |
| 2.5.2 | Pointer Cancellation | Actions fire on `click`/`pointerup`, not `mousedown`/`pointerdown`. |
| 2.5.3 | Label in Name | Visible text label is contained within the accessible name (important for voice control). |
| 2.5.4 | Motion Actuation | Shake/tilt/motion-triggered actions have a button alternative and can be disabled. |
| 2.5.7 | Dragging Movements | Drag-and-drop has a click-based alternative (e.g., buttons to reorder). |
| 2.5.8 | Target Size | Interactive targets are at least 24×24 CSS pixels, with adequate spacing if smaller. |

### Understandable — Can all users understand the content?

| WCAG | Criterion | What to check |
|------|-----------|---------------|
| 3.1.1 | Language of Page | `<html>` has a `lang` attribute with valid language code. |
| 3.1.2 | Language of Parts | Content in a different language than the page has its own `lang` attribute. |
| 3.2.1 | On Focus | Moving focus doesn't trigger unexpected changes (page navigation, form submission, modal opening). |
| 3.2.2 | On Input | Changing a form value doesn't trigger unexpected changes without warning. |
| 3.2.3 | Consistent Navigation | Navigation appears in the same order across pages. (Multi-page check — flag if evidence suggests inconsistency.) |
| 3.2.4 | Consistent Identification | Same functions are labeled the same way across pages. |
| 3.2.6 | Consistent Help | Help mechanisms appear in the same location across pages. |
| 3.3.1 | Error Identification | Errors are described in text, not just color or icon. The field in error is identified. |
| 3.3.2 | Labels or Instructions | Form fields have visible labels (not just placeholders). Required fields are indicated. |
| 3.3.3 | Error Suggestion | Error messages suggest how to fix the problem when possible. |
| 3.3.4 | Error Prevention | Forms handling legal, financial, or user data: submissions are reversible, confirmed, or reviewable. |
| 3.3.7 | Redundant Entry | Don't require users to re-enter information already provided in the same process. |
| 3.3.8 | Accessible Authentication | No cognitive function test for login. Support paste, autofill, and password managers. |

### Robust — Is the code compatible with assistive technology?

| WCAG | Criterion | What to check |
|------|-----------|---------------|
| 4.1.2 | Name, Role, Value | Every interactive element has an accessible name, correct role, and programmatically determinable state. Custom widgets use appropriate ARIA. |
| 4.1.3 | Status Messages | Dynamic content updates (success, error, progress, results) use `aria-live`, `role="alert"`, or `role="status"` so screen readers announce them without focus change. |

## Output Format

```
♿ CURB CUT — Full Audit
[filename]
WCAG 2.2 Level AA

Score: [XX]/100 | [Compliance Badge]

| Pillar | Score | Findings |
|--------|:-----:|:--------:|
| Perceivable | [XX]/25 | [X] |
| Operable | [XX]/25 | [X] |
| Understandable | [XX]/25 | [X] |
| Robust | [XX]/25 | [X] |

---

🔴 CRITICAL ([X])

### [Title]
**WCAG [X.X.X]** [Criterion Name]  
**What:** [plain English]
**Who:** [affected users]
**Fix:**
\```[language]
[code fix]
\```

---

🟠 HIGH ([X])
[same format per finding]

🟡 MEDIUM ([X])
[same format per finding]

🔵 LOW ([X])
[same format per finding]

---

✅ Passing ([X] criteria)
- [Criterion] — [what's working]
- [Criterion] — [what's working]
- ...

---

[If 2+ findings at HIGH or CRITICAL, include this section:]

User Experience Walkthrough
A screen reader user arriving at this [page/component] would experience:
[3-5 factual sentences describing the concrete experience of navigating this
code with assistive technology. Grounded in the specific findings above.
No drama — just what happens.]

---

Auto-fix available for [X] of [Y] findings.
```

After delivering the audit, return control to the router for Auto-Fix handling.

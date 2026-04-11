# Mode: Quick Scan

Fast check. **CRITICAL and HIGH issues only.** This is the everyday tool — run it before a commit, during a PR, whenever.

Scoring, severity levels, rules, and auto-fix all come from the router (`SKILL.md`). This file defines the process, the checklist, and the output format.

## Process

1. Read the code. Understand what it does and what type of content it is.
2. Check all 15 items on the Quick Scan Checklist below. Only report **CRITICAL** and **HIGH** findings.
3. Report findings with the Quick Scan output format.
4. Give the score (based on all 15 checks, even though only failures are detailed).
5. In the Passing section, list which of the 15 checks passed.
6. Offer auto-fix if fixable issues exist.

## Quick Scan Checklist (Top 15)

These are the highest-impact criteria — the ones that, when violated, block or seriously impair access.

| # | Check | WCAG | What to look for |
|---|-------|------|-----------------|
| 1 | Images have text alternatives | 1.1.1 | `<img>` without `alt`. Decorative images should have `alt=""`, not missing alt. |
| 2 | Form inputs have labels | 1.3.1, 3.3.2 | `<input>` without a `<label>`, `aria-label`, or `aria-labelledby`. Placeholder is NOT a label. |
| 3 | Semantic structure exists | 1.3.1 | Content in plain `<div>`s without landmarks (`<nav>`, `<main>`, `<header>`, etc.) or heading hierarchy. |
| 4 | Color is not the sole indicator | 1.4.1 | Error states, required fields, or status shown only with color (red text, green icon). |
| 5 | Text contrast meets minimum | 1.4.3 | Text below 4.5:1 ratio against background. Large text (18pt+): 3:1. Check CSS/Tailwind values. |
| 6 | All interactions are keyboard accessible | 2.1.1 | `onClick` on non-interactive elements (`<div>`, `<span>`) without `onKeyDown`/`onKeyUp` and `tabIndex`. |
| 7 | No keyboard traps | 2.1.2 | Focus enters a component (modal, menu) and cannot leave via Tab or Escape. |
| 8 | Heading hierarchy is logical | 2.4.6 | Skipped heading levels (h1 → h3), multiple h1s, headings used for styling not structure. |
| 9 | Focus is visible | 2.4.7 | `outline: none` or `outline: 0` without a replacement focus style. `:focus-visible` removal. |
| 10 | Links and buttons have clear text | 2.4.4 | "Click here", "Read more", "Link" without context. Empty `<a>` or `<button>` with only an icon and no accessible name. |
| 11 | Page language is set | 3.1.1 | Missing `lang` attribute on `<html>`. |
| 12 | Custom elements have ARIA roles | 4.1.2 | Custom interactive widgets (`<div>` acting as button, tab, menu) without `role`, `aria-label`, or other ARIA. |
| 13 | Dynamic content announces updates | 4.1.3 | Content that changes (notifications, errors, live data) without `aria-live`, `role="alert"`, or `role="status"`. |
| 14 | Touch targets meet minimum size | 2.5.8 | Interactive elements smaller than 24×24 CSS pixels. Check inline links, icon buttons, close buttons. |
| 15 | Focus order matches visual order | 2.4.3 | `tabindex` values > 0 that override natural order. DOM order doesn't match visual layout. |

## Output Format

```
♿ CURB CUT — Quick Scan
[filename]

Score: [XX]/100 | [Compliance Badge]

---

🔴 CRITICAL ([X])

### [Title]
**WCAG [X.X.X]** [Criterion Name]
**What:** [plain English — what's wrong and where]
**Who:** [who is affected — e.g., "Screen reader users cannot identify this input's purpose"]
**Fix:**
\```[language]
[concrete code fix]
\```

---

🟠 HIGH ([X])

### [Title]
[same format]

---

✅ Passing ([X] criteria checked, [Y] passing)
[Brief list of what's working well]

---

Auto-fix available for [X] of [Y] findings.
```

After delivering the scan, return control to the router for Auto-Fix handling.

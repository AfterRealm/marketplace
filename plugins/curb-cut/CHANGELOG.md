# Changelog

## v1.1.0 — 2026-04-11

The biggest Curb Cut refactor yet. The monolithic `SKILL.md` has been split into a thin router and four lazy-loaded mode files, the description was systematically optimized against a 20-query eval set, and several quality issues from a pre-ship full-pass review were fixed.

### Progressive Disclosure Architecture

`SKILL.md` went from **698 lines → 210 lines** (-70%). Per-invocation context drops roughly **50%** because only the mode the user picks is loaded, not all four modes plus every WCAG pillar table plus every WAI-ARIA pattern plus every output format on every call.

**New structure:**

| File | Lines | Contents |
|------|------:|----------|
| `SKILL.md` | 210 | Router — Rules, Severity Levels, Scoring, Step 1 picker, Step 1.5 confirm-something-to-audit, Step 2 mode dispatch, Auto-Fix, CI/CD |
| `modes/quick-scan.md` | 76 | Quick Scan process, top-15 checklist, output format |
| `modes/full-audit.md` | 147 | Full Audit process, all 4 WCAG 2.2 AA pillar tables (Perceivable / Operable / Understandable / Robust), output format |
| `modes/component-check.md` | 182 | Component Check process, all 6 WAI-ARIA patterns (Modal / Tabs / Form / Dropdown / Accordion / Navigation), output format |
| `modes/report.md` | 136 | Report process, writing guidance, formal report output format |

The router still carries the universal pieces — Rules, Severity, Scoring, Auto-Fix — because they apply to every mode regardless of which file is loaded. `modes/*.md` are mutually exclusive and enforced by the router: "Only load ONE mode file per invocation."

### Added

- **Step 1.5: Confirm There's Something to Audit** — after mode selection, the router checks that the user actually provided code, a file path, or a directory before loading a mode file. Prompts for input if missing. Prevents dead-ends where a mode file loads without anything to audit.
- **Step 1.5: Multi-file handling** — directories and multi-file audits are now handled uniformly in the router for every mode, with a recommendation to prefer Quick Scan on projects with 10+ files to stay within context limits.
- **AskUserQuestion guidance** — the router documents how to use the interactive 4-option picker cleanly (Curb Cut has exactly 4 modes, so no gateway pattern is needed) and falls back to the markdown menu for headless contexts.

### Changed

- **Description optimized** via Anthropic's `skill-creator` systematic optimization loop — see Optimization below.
- **Rules are now explicitly "applies to every mode"** — previously implicit, now documented in the router so every mode file inherits them.
- **Component Check widget-type detection** moved from the mode-agnostic Step 1.5 into `modes/component-check.md` where it belongs. Filename-based inference (e.g., `Modal.jsx` → modal pattern) is the first step of the Component Check process now.
- **Stale `## Trigger` section removed** from `SKILL.md`. The old hand-written keyword list contradicted the new optimized frontmatter description. Frontmatter is what actually drives skill triggering — the body section was dead weight.
- **Manual install instructions updated** in `README.md` and `PROMO.md`. The old `curl` instructions only downloaded the router, which would fail at runtime when it tried to load `modes/*.md`. Install is now `git clone` into `~/.claude/skills/curb-cut`.

### Optimization

Ran the full `skill-creator` description loop end-to-end: **5 iterations, 20 queries** (10 should-trigger with inline code, 10 near-miss should-nots), **60/40 train/test split**, 3 trials per query, 4 parallel workers.

| Iter | Train (per-query) | Test (per-query) | Train recall (trial) | Test recall (trial) |
|------|:-----------------:|:----------------:|:--------------------:|:-------------------:|
| 1 (baseline) | 6/12 | 5/8 | 22% | 25% |
| 2 | 7/12 | 5/8 | 22% | 25% |
| 3 | 6/12 | 5/8 | 28% | 33% |
| **4 ⭐ winner** | **7/12** | **5/8** | **28%** | **42%** |
| 5 | 7/12 | 5/8 | 33% | 17% *(regressed)* |

**Precision held at 100% across every iteration** — nothing false-triggered on the near-miss queries (write new accessible components, explain `aria-live`, color-contrast library recommendation, broken CSS hover, JSX→Vue translation, React performance profiling, unit-test authoring, smaller-components refactor).

Per-query test stayed tied at 5/8 across all iterations, so the loop's greedy tiebreaker would have kept the baseline. **Iter 4 was selected manually on trial-level reliability** — 42% of held-out positive queries trip all 3 trials under iter 4, versus 25% under the baseline. Same number of flipped queries, but iter 4 triggers more *reliably* when it does trigger.

The winning description trades the old exact-phrase trigger list (`"accessibility check"`, `"a11y scan"`, `"WCAG audit"`, `"curb cut"`) for pattern-based implicit phrasing (`"does this pass WCAG"`, `"audit before I ship"`, `"compliance report for a client"`) plus explicit non-triggers (write new components, explain concepts, find libraries, write tests).

Curb Cut is a manually-invoked skill — the description is discoverability gravy for first-time users, not the primary access path. Users who know the skill exists will invoke it directly.

### Internal

- All five files (`SKILL.md` + 4 mode files) are byte-identical across source, AfterRealm marketplace, and `~/.claude/skills/curb-cut/` — md5-verified.
- No changes to the eval suite format — existing `evals/evals.json` prompts still work unchanged because the router's Step 1 / Step 1.5 / Step 2 flow correctly handles the prompt style they use.

---

## v1.0.1 — 2026-04-09

### Added
- YAML frontmatter (`name`, `description`) for Agent Skills spec compliance and cross-platform discoverability (skills.sh, etc.)

## v1.0.0 — 2026-04-05

### Added
- **Quick Scan** mode — fast check for critical and high issues (top 15 criteria)
- **Full Audit** mode — comprehensive WCAG 2.2 Level AA check with per-pillar scoring
- **Component Check** mode — deep dive on interactive widgets against WAI-ARIA Authoring Practices
  - Patterns: Modal, Tabs, Form, Dropdown/Menu, Accordion, Navigation
- **Report** mode — formal compliance report for stakeholders and legal
- **Auto-Fix** — applies fixes after any mode, prefers semantic HTML over ARIA
- **Scoring system** — 0-100 scale with AA Compliant / Partial AA / Non-Compliant levels
- **CI/CD GitHub Action** — accessibility checks on PRs touching frontend files
- Eval suite: test files covering forms, modals, dropdowns, navigation, and accessible components

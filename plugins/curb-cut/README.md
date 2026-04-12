# Curb Cut

Web accessibility auditing for Claude Code. Scans your HTML, JSX, Vue, and Svelte components for WCAG 2.2 Level AA violations — explains what's wrong, who it affects, and how to fix it.

Named after the [curb cut effect](https://ssir.org/articles/entry/the_curb_cut_effect): accessibility improvements designed for people with disabilities end up benefiting everyone.

## Modes

**Quick Scan** — Critical and high issues only. Fast enough to run before every commit.

**Full Audit** — Comprehensive WCAG 2.2 AA check across all four pillars (Perceivable, Operable, Understandable, Robust) with per-pillar scoring.

**Component Check** — Deep dive on a single interactive widget (modal, form, tabs, dropdown, accordion, navigation) against WAI-ARIA Authoring Practices. Tests keyboard interaction, focus management, and ARIA state/properties.

**Report** — Formal compliance report suitable for clients, stakeholders, or legal. Includes executive summary, remediation plan with effort estimates, and methodology notes.

## What It Catches That Lighthouse Doesn't

- Custom components missing ARIA roles and keyboard support
- Focus management issues in modals, menus, and tab panels
- Keyboard traps and missing escape handlers
- Non-interactive elements with click handlers but no keyboard equivalent
- Placeholder-only form inputs (no real labels)
- Missing live regions for dynamic content
- Color-only error indicators
- Broken heading hierarchy
- Missing skip navigation and landmark regions

## Auto-Fix

After any scan, Curb Cut offers to fix what it found — all at once, critical only, or pick individually. Prefers semantic HTML over ARIA. Re-scans after fixes so you can watch your score improve.

## Scoring

| Score | Compliance |
|-------|-----------|
| 90-100 | AA Compliant (zero critical, zero high) |
| 70-89 | Partial AA (zero critical) |
| Below 70 | Non-Compliant |

Scores break down by WCAG pillar: Perceivable, Operable, Understandable, Robust (25 points each).

## Install

### From the AfterRealm Marketplace

```bash
claude plugin marketplace add AfterRealm/marketplace
claude plugin install curb-cut@afterrealm
```

### Manual Install

Curb Cut uses progressive disclosure — the skill is a router plus lazy-loaded mode files under `modes/`. Clone the repo directly into your skills directory:

```bash
git clone https://github.com/AfterRealm/curb-cut.git ~/.claude/skills/curb-cut
```

Or clone anywhere and symlink:

```bash
git clone https://github.com/AfterRealm/curb-cut.git
ln -s "$(pwd)/curb-cut" ~/.claude/skills/curb-cut
```

## CI/CD

Drop the included GitHub Action into your repo to run accessibility checks on every PR that touches frontend files. See `SKILL.md` for the workflow configuration.

## WCAG Coverage

Curb Cut checks against WCAG 2.2 Level AA success criteria through static code analysis. This includes criteria new in WCAG 2.2:

- 2.4.11 Focus Not Obscured
- 2.5.7 Dragging Movements
- 2.5.8 Target Size (Minimum)
- 3.2.6 Consistent Help
- 3.3.7 Redundant Entry
- 3.3.8 Accessible Authentication

Static analysis cannot replace runtime testing with screen readers and assistive technology. Curb Cut identifies structural and semantic issues in your source code — pair it with manual testing for full compliance.

## Links

- **Marketplace:** [AfterRealm/marketplace](https://github.com/AfterRealm/marketplace)
- **Also by AfterRealm:** [Blunt Cake](https://github.com/AfterRealm/blunt-cake) (code review) | [Father Time](https://github.com/AfterRealm/father-time) (time management)
- **WCAG 2.2:** [W3C Specification](https://www.w3.org/TR/WCAG22/)
- **WAI-ARIA Practices:** [Authoring Practices Guide](https://www.w3.org/WAI/ARIA/apg/)

## License

MIT

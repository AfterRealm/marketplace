# Changelog

All notable changes to this project are documented here. This project follows [Semantic Versioning](https://semver.org/).

## [0.1.2] - 2026-10-10

### Fixed
- Marketplace install now works: added `.claude-plugin/marketplace.json`. Install with `claude plugin marketplace add AfterRealm/ue5-blueprint-skills` then `claude plugin install ue5-blueprints@ue5-blueprint-skills`.
- README Quick Start uses the marketplace install instead of `--plugin-dir`.
- Plugin author URL now points to github.com/AfterRealm.

## [0.1.1] - 2026-10-10

### Fixed
- Node cards no longer show a YAML parse error banner on GitHub. Removed the leading `---` line from all 1,864 cards so GitHub stops treating it as frontmatter.

### Changed
- README tagline reworded ("The AI-powered Blueprint analysis toolkit…").

### Removed
- Promo files (`PROMO.md`, `PROMO_DISCORD.txt`) from the repo.

## [0.1.0] - 2026-03-27

Initial release.

[0.1.2]: https://github.com/AfterRealm/ue5-blueprint-skills/compare/v0.1.1...v0.1.2
[0.1.1]: https://github.com/AfterRealm/ue5-blueprint-skills/compare/v0.1.0...v0.1.1
[0.1.0]: https://github.com/AfterRealm/ue5-blueprint-skills/releases/tag/v0.1.0

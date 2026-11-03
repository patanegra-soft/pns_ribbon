# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [1.0.9] — 2026-11-01

### Changed
- README: bugs, ideas and questions go through CONTRIBUTING. It no longer says «Patches»: pull requests are switched off.

## [1.0.8] — 2026-11-01

### Fixed
- 35 Odoo tests (colour parsing, booleans, hex to rgba, history keys) were plain `unittest` classes, which the Odoo test runner skips. They are `TransactionCase` now and run with `--test-enable`.

## [1.0.7] — 2026-11-01

### Changed
- The Apps page has a *Source code* card: the GitHub repository, what `main` is (one tree, one stack per OWL generation) and how the flat branches are built. The Apps Store only reads a flat branch.

## [1.0.6] — 2026-10-31

### Changed
- Supported series: Odoo 14.0 and later (tested: 14.0 and 19.0; 15.0 to 18.0 coming soon). Odoo 13 and older are not supported; README, *Odoo versions*.

## [1.0.5] — 2026-10-31

### Changed
- The banner text is plain text. Line breaks are drawn as breaks; other tags are shown as text.
- Only a Settings administrator can save the ribbon.

## [1.0.4] — 2026-10-31

### Changed
- The corner banner is drawn when the page is ready, without waiting one second.
- Apps page, README, and license notices for the public tree.

## [1.0.3] — 2026-10-31

### Changed
- Technical menu renamed to *PNS Ribbon*.
- New module icon.
- The Apps page is the local `static/description/index.html`; the manifest `website` points to it and there is no outbound website button.
- Published from a multi-version tree: `main` holds every Odoo version, one tag per release, and one installable branch per tested series.

### Added
- Unit tests that need no Odoo database (`unit_tests/`).

## [1.0.0] — 2025-12-01

### Added
- Diagonal corner ribbon with configurable text, colors and opacity.
- Configuration wizard at *Settings > Technical > Ribbon* (admin only).
- Native `<input type="color">` picker with synchronized opacity slider and pasteable `rgba(...)` field.
- Live preview of text + colors while editing.
- History grid of the last 20 color combinations (click to reuse, × to remove).
- Variables: `{dbname}`, `{db_name}`, `{user}`, `{company}`.
- Master on/off switch (`pns_ribbon.enabled`) to hide the ribbon without uninstalling.
- Shadow toggle (`pns_ribbon.shadow`) for a flatter look.
- Framework-agnostic ribbon injection: a plain script, no asset bundler.
- OWL1 stack (Odoo 14) and OWL2 stack (Odoo 15 and later).

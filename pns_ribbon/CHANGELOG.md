# Changelog

What changes for people who use this module, one section per published version, newest first. The heading is the git tag.

## owl1-1.0.18_owl2-1.0.18_owl3-1.0.18 (2026-11-12)

- Odoo 16: the colour picker and the ribbon history load again; their screen templates were missing there.
- Apps page and README: each Odoo version links to its branch on GitHub, and the store cover is easier to read in the grid.

## owl1-1.0.17_owl2-1.0.17_owl3-1.0.17 (2026-11-09)

- Banners (Apps store, README and site) show the seven supported series, 14.0 to 20.0; the old ones still said 14 and 19. Images only.

## owl1-1.0.16_owl2-1.0.16_owl3-1.0.16 (2026-11-09)

- Odoo 15, 16, 17, 18 and 20 join 14 and 19: every series from 14.0 to 20.0 is tested and has its own flat branch.
- On Odoo 20 the module also needs `pns_base`, which brings back the access-rights file and `get_param` that Odoo 20 removed. On 14 to 19 it still depends only on `web`.

## owl1-1.0.12_owl2-1.0.12 (2026-11-04)

- Store page: a new 2:1 thumbnail, so the Odoo Apps listing no longer crops the sides of the banner.

## owl1-1.0.11_owl2-1.0.11 (2026-11-03)

- Store page and README: the banner shows the ribbon in the top-left corner, where Odoo draws it.

## owl1-1.0.10_owl2-1.0.10 (2026-11-03)

- Store page and README: a new banner with an example Odoo window wearing the ribbon.

## owl1-1.0.9_owl2-1.0.9 (2026-11-01)

- First public release. A diagonal ribbon in the backend corner, so a test or staging database is not mistaken for production. Configure it at Settings → Technical → PNS Ribbon: text with `{dbname}`, `{user}` and `{company}`, colours, and the last 20 colour pairs.
- The ribbon is a plain script, outside the asset bundler, and shows as soon as the page is ready. Tested on Odoo 14.0 and 19.0; 15.0 to 18.0 coming soon; 13.0 and older not supported.
- Security: the ribbon text is plain text (only line breaks are kept), and only Settings administrators can open or save the configuration.
- Store page: a Source code card with the GitHub repository and the installable branches.

## Before the first public release

- 1.0.8 (2026-11-01): 35 Odoo tests (colour parsing, booleans, hex to rgba, history keys) were plain `unittest` classes, which the Odoo test runner skips. They are `TransactionCase` now.
- 1.0.3 (2026-10-31): technical menu renamed to *PNS Ribbon*; new module icon; the Apps page is the local `static/description/index.html`; unit tests that need no Odoo database (`unit_tests/`).
- 1.0.0 (2025-12-01): diagonal corner ribbon with configurable text, colours and opacity; configuration wizard (admin only) with colour picker, opacity slider and live preview; history of the last 20 colour pairs; variables `{dbname}`, `{db_name}`, `{user}`, `{company}`; on/off switch (`pns_ribbon.enabled`) and shadow toggle (`pns_ribbon.shadow`); OWL1 stack (Odoo 14) and OWL2 stack (Odoo 15 and later).

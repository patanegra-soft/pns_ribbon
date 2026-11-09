# Contributing

This repository is generated from our internal tree on every release. Pull requests are switched off: a merge here would be overwritten by the next release.

| You have | Where it goes |
| :--- | :--- |
| A bug | An issue, with the bug form |
| An idea or a question | Discussions |
| A security problem | A private report, see [SECURITY.md](SECURITY.md) |

If we take your idea, we implement it internally and credit you in the release notes. Do not paste secrets, API keys or customer data anywhere.

The code is Apache-2.0: you are free to fork it and keep your changes.
## If you fork

`common/` is shared. `stacks/owl1/` is Odoo 14 and 15 (15 reads `__manifest_o15__.py`). `stacks/owl2/` is Odoo 16 to 19. `stacks/owl3/` is Odoo 20 and later, and also needs `pns_base`.
`ribbon.js` and `ribbon.css` are the same file in every stack. Tests: README, "Tests".

Comments and docstrings in English. `ribbon.js` stays free of `odoo.define`,
OWL, and jQuery: it is injected outside the asset bundler.

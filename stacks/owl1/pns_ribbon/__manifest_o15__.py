# -*- coding: utf-8 -*-
# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2025-2026 Patanegra Soft <https://patanegra.com>
# Odoo reads this file with ast.literal_eval — no module docstring before `{`.
# Odoo 15: the owl1 module with this manifest (i.sh, t.sh and install_flat.sh
# install it as __manifest__.py). Assets go here; 15 has no web.assets_backend
# template to inherit. The rest matches __manifest__.py.

{
    'name': 'PNS Ribbon',
    'version': '1.0.18',
    'category': 'Web',
    'summary': 'Visual ribbon (TEST/DEV banner) to identify non-production instances.',
    'description': """
Lightweight module that shows a configurable ribbon/banner in the corner
to clearly identify non-production instances (TEST/DEV).

Odoo 14.0 and later. Tested series: README, "Odoo versions".

Where to configure (administrators only):
Settings > Technical > Ribbon

- Text (one line per row; variables {dbname}, {user}, {company}).
- Text and background color in a single rgba(r, g, b, a) format: color
  picker plus opacity control plus pasteable rgba field, with validation
  and live preview.
- History of the last 20 color combinations (no duplicates), shown as a
  grid, reusable with one click and removable with an "x".

Or via Settings > Technical > Parameters > System Parameters:

- pns_ribbon.html : text to show ({dbname} = database name).
- pns_ribbon.textColor : text color, e.g. rgba(255, 255, 255, 1).
- pns_ribbon.backgroundColor : background color, e.g. rgba(255, 0, 0, 0.5).

Part of Patanegra Soft Suite.
""",
    'author': 'PATANEGRA Soft',
    'website': '/pns_ribbon/static/description/index.html',
    'depends': ['web'],
    'assets': {
        'web.assets_backend': [
            'pns_ribbon/static/src/js/pns_color_field_v14.js',
            'pns_ribbon/static/src/js/pns_ribbon_history_v14.js',
        ],
    },
    'data': [
        'security/ir.model.access.csv',
        'data/parameters.xml',
        'views/ribbon_config_views.xml',
        'views/layout.xml',
    ],
    # Apache License 2.0 — see LICENSE file
    'license': 'Other OSI approved licence',
    'installable': True,
    'auto_install': False,
}

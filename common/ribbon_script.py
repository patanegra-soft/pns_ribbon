# -*- coding: utf-8 -*-
# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2025-2026 Patanegra Soft <https://patanegra.com>
"""JSON safe to drop inside an HTML script element. No Odoo import."""

import json


def script_json(payload):
    """Serialize *payload* for a raw ``<script>`` assignment.

    ``json.dumps`` leaves ``<`` as is. An HTML parser would end the script
    at ``</script>`` before JavaScript sees the text. The replacements are
    JSON escapes, so ``json.loads`` returns the original characters.
    """
    text = json.dumps(payload, ensure_ascii=True, separators=(',', ':'))
    return (
        text.replace('<', '\\u003c')
            .replace('>', '\\u003e')
            .replace('&', '\\u0026')
    )

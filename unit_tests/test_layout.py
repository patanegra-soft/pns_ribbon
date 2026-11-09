# -*- coding: utf-8 -*-
# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2025-2026 Patanegra Soft <https://patanegra.com>
"""Checks on the multi-version tree that need no Odoo database."""
from __future__ import annotations

import ast
import re
import xml.etree.ElementTree as ET
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
STACKS = tuple(sorted(p.name for p in (ROOT / 'stacks').iterdir() if p.is_dir()))


def _module(stack):
    return ROOT / 'stacks' / stack / 'pns_ribbon'


def _manifest(stack):
    path = _module(stack) / '__manifest__.py'
    return ast.literal_eval(path.read_text(encoding='utf-8'))


def _exists(stack, rel):
    """A module file comes from the stack or from common/ (install layering)."""
    return (_module(stack) / rel).is_file() or (ROOT / 'common' / rel).is_file()


@pytest.mark.parametrize('stack', STACKS)
def test_manifest_is_a_literal(stack):
    info = _manifest(stack)
    assert info['name']
    assert info['version']
    # Odoo 20 has no ir.model.access nor get_param; pns_base brings them back.
    expected = ['web', 'pns_base'] if stack == 'owl3' else ['web']
    assert info['depends'] == expected


def test_every_stack_ships_the_same_version():
    assert len({_manifest(stack)['version'] for stack in STACKS}) == 1


@pytest.mark.parametrize('stack', STACKS)
def test_manifest_data_files_exist(stack):
    missing = [rel for rel in _manifest(stack)['data'] if not _exists(stack, rel)]
    assert not missing


@pytest.mark.parametrize('stack', STACKS)
def test_asset_paths_exist(stack):
    xml = ''.join(p.read_text(encoding='utf-8') for p in (_module(stack) / 'views').glob('*.xml'))
    paths = set(re.findall(r'/?pns_ribbon/(static/[^\'"?<\s]+)', xml))
    assert paths
    missing = [rel for rel in sorted(paths) if not _exists(stack, rel)]
    assert not missing


@pytest.mark.parametrize('stack', STACKS)
def test_views_are_well_formed(stack):
    for path in (_module(stack) / 'views').glob('*.xml'):
        ET.parse(path)


def test_ribbon_is_the_same_on_every_version():
    for rel in ('static/src/js/ribbon.js', 'static/src/css/ribbon.css'):
        owl1 = (_module('owl1') / rel).read_bytes()
        owl2 = (_module('owl2') / rel).read_bytes()
        assert owl1 == owl2, rel


def test_ribbon_js_uses_no_framework():
    """ribbon.js loads outside the asset bundler, so it cannot rely on one."""
    src = (_module('owl2') / 'static' / 'src' / 'js' / 'ribbon.js').read_text(encoding='utf-8')
    code = re.sub(r'/\*.*?\*/|//[^\n]*', '', src, flags=re.S)
    for token in (
        'odoo.define', '@odoo/', 'require(', 'jQuery', '$(',
        'setTimeout', 'setInterval', 'innerHTML',
    ):
        assert token not in code, token


def _ribbon_script():
    import importlib.util
    path = ROOT / 'common' / 'ribbon_script.py'
    spec = importlib.util.spec_from_file_location('ribbon_script', path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_script_json_cannot_close_the_script_tag():
    text = _ribbon_script().script_json({
        'html': '</script><img onerror="alert(1)">',
        'note': 'a`b${c}&',
    })
    assert '<' not in text
    assert '>' not in text
    assert '&' not in text
    import json
    data = json.loads(text)
    assert data['html'] == '</script><img onerror="alert(1)">'
    assert data['note'] == 'a`b${c}&'


def test_head_script_is_json():
    owl1 = (_module('owl1') / 'views' / 'layout.xml').read_text(encoding='utf-8')
    owl2 = (_module('owl2') / 'views' / 'assets.xml').read_text(encoding='utf-8')
    assert "t-raw=\"request.env['pns.ribbon.config']._ribbon_client_json()" in owl1
    assert "t-out=\"request.env['pns.ribbon.config']._ribbon_client_json()" in owl2
    for xml in (owl1, owl2):
        script = xml.split('<script', 1)[1].split('</script>', 1)[0]
        assert '`' not in script
        assert 'sudo' not in script


def test_wizard_checks_the_group_and_stores_plain_text():
    for stack in STACKS:
        src = (_module(stack) / 'models' / 'ribbon_config.py').read_text(encoding='utf-8')
        assert '_require_settings' in src
        assert "_NL_RE.sub('<br>'" not in src


def test_license_ships_with_the_module():
    assert 'Apache License' in (ROOT / 'common' / 'LICENSE').read_text(encoding='utf-8')
    for rel in ('LICENSE', 'NOTICE', 'SECURITY.md', 'CONTRIBUTING.md'):
        assert (ROOT / rel).is_file(), rel
    index = (ROOT / 'common' / 'static' / 'description' / 'index.html').read_text(encoding='utf-8')
    assert 'name="tdm-reservation" content="0"' in index
    assert 'https://patanegra.com' in index

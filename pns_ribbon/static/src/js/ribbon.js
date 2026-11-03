// SPDX-License-Identifier: Apache-2.0
// Copyright (C) 2025-2026 Patanegra Soft <https://patanegra.com>
/**
 * Corner banner for a non-production database.
 *
 * Reads window.pns_ribbon_data (rendered in the page head) and appends
 * a fixed div. No Odoo module loader, OWL, or jQuery.
 */
(function() {
    "use strict";

    // -----------------------------------------------------------------------
    // ribbon.js — PNS Ribbon environment indicator (client-side).
    //
    // This script is injected into every page via a QWeb ``web.layout``
    // inheritance.  It reads its configuration from ``window.pns_ribbon_data``
    // (server-rendered in the ``<head>``) and creates a fixed-position
    // ``<div id="pns-ribbon">`` in the top-left corner.
    //
    // The script is **framework-agnostic**: no dependency on ``odoo.define``,
    // OWL, jQuery or any bundler.  It works the same on every supported series (14.0 and later).
    //
    // Configuration object (``window.pns_ribbon_data``):
    //   db         — database name (fallback: ``odoo.session_info.db``)
    //   user       — current user's display name
    //   company    — current company's name
    //   html       — plain text; newlines and a literal br tag start a new line
    //   color      — CSS text color  (e.g. ``rgba(255,255,255,1)``)
    //   background — CSS background  (e.g. ``rgba(255,0,0,0.5)``)
    //   enabled    — master switch   (``'0'`` / ``'False'`` = hidden)
    //   shadow     — shadow toggle   (``'0'`` = flat, no shadow/border)
    // -----------------------------------------------------------------------

    /**
     * Return ``true`` if *v* represents a falsy/"off" value.
     * Recognized: ``'0'``, ``'False'``, ``'false'``, boolean ``false``.
     */
    function isOff(v) {
        return v === '0' || v === 'False' || v === 'false' || v === false;
    }

    /** Replace **all** occurrences of *needle* in *haystack* with *value*. */
    function replaceAll(haystack, needle, value) {
        return (haystack || '').split(needle).join(value || '');
    }

    /** Color we will assign to a CSS property. Anything else is ignored. */
    function safeColor(value) {
        var v = String(value || '').trim();
        if (!v || v === 'False') {
            return '';
        }
        if (/^#(?:[0-9a-f]{3}|[0-9a-f]{6})$/i.test(v)) {
            return v;
        }
        if (/^rgba?\(\s*(?:\d{1,3}\s*,\s*){2}\d{1,3}\s*(?:,\s*(?:0|1|0?\.\d+)\s*)?\)$/i.test(v)) {
            return v;
        }
        return '';
    }

    /**
     * Append *text* as text nodes. Newlines and a literal br tag become
     * a br element. Nothing else is parsed as HTML.
     */
    function appendLines(parent, text) {
        var parts = String(text).split(/\r\n|\r|\n|<br\s*\/?>/i);
        for (var i = 0; i < parts.length; i++) {
            if (i) {
                parent.appendChild(document.createElement('br'));
            }
            parent.appendChild(document.createTextNode(parts[i]));
        }
    }

    /**
     * Build (or rebuild) the ribbon ``<div>`` from a configuration object.
     *
     * If the ribbon is disabled (``data.enabled`` is falsy) or has already
     * been injected, it is removed first — this allows live rebuilds.
     */
    function buildRibbon(data) {
        data = data || {};

        // Remove any existing ribbon to allow live rebuilds.
        var existing = document.getElementById('pns-ribbon');
        if (existing && existing.parentNode) {
            existing.parentNode.removeChild(existing);
        }

        // Master switch: when disabled, nothing is rendered.
        if (isOff(data.enabled)) {
            return;
        }

        var dbName = data.db || "";
        if (!dbName && window.odoo && window.odoo.session_info && window.odoo.session_info.db) {
            dbName = window.odoo.session_info.db;
        }

        var html = data.html;
        if (html === 'False') html = '';

        var ribbonText = html || "TEST\n{dbname}";
        ribbonText = replaceAll(ribbonText, '{dbname}', dbName);
        ribbonText = replaceAll(ribbonText, '{db_name}', dbName);
        ribbonText = replaceAll(ribbonText, '{user}', data.user);
        ribbonText = replaceAll(ribbonText, '{company}', data.company);

        var ribbon = document.createElement('div');
        ribbon.id = 'pns-ribbon';
        appendLines(ribbon, ribbonText);

        var color = safeColor(data.color);
        var background = safeColor(data.background);
        if (color) {
            ribbon.style.color = color;
        }
        if (background) {
            ribbon.style.backgroundColor = background;
        }

        // Optional shadow: removing box-shadow AND the dashed border makes
        // the ribbon flat and discreet.
        if (isOff(data.shadow)) {
            ribbon.style.setProperty('box-shadow', 'none', 'important');
            ribbon.style.setProperty('border', 'none', 'important');
        }

        document.body.appendChild(ribbon);
    }

    /** Initial injection: read server-rendered data from ``<head>``. */
    function injectRibbon() {
        buildRibbon(window.pns_ribbon_data || {});
    }

    if (document.body) {
        injectRibbon();
    } else {
        document.addEventListener('DOMContentLoaded', injectRibbon);
    }
})();

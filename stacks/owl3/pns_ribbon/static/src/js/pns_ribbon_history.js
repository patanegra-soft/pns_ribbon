/** @odoo-module **/
// SPDX-License-Identifier: Apache-2.0
// Copyright (C) 2025-2026 Patanegra Soft <https://patanegra.com>
// ---------------------------------------------------------------------------
// pns_ribbon_history — Owl 3 history widget (Odoo 20 and later).
//
// Displays a flex-wrap grid of colored cards, one per recent color
// combination stored in the ``pns_ribbon.history`` system parameter.
// Each card shows the ribbon text with the corresponding foreground and
// background colors.
//
// Interactions:
//   • **Click** on a card → fills the form fields with that entry.
//   • **Click "×"** on a card → deletes that entry from the history
//     (server-side, no confirmation dialog).
// ---------------------------------------------------------------------------

import { registry } from "@web/core/registry";
import { Component, proxy, useProps } from "@odoo/owl";
import { standardFieldProps } from "@web/views/fields/standard_field_props";
import { useService } from "@web/core/utils/hooks";

class PnsRibbonHistory extends Component {
    static template = "pns_ribbon.PnsRibbonHistory";
    props = useProps(standardFieldProps);

    setup() {
        this.orm = useService("orm");
        this.state = proxy({ entries: this._read() });
    }

    /** Parse the JSON value from the record into an array of entries. */
    _read() {
        const raw = this.props.record.data[this.props.name] || "[]";
        try {
            const data = JSON.parse(raw);
            return Array.isArray(data) ? data : [];
        } catch (e) {
            return [];
        }
    }

    /** Apply a history entry to the wizard form fields. */
    apply(entry) {
        this.props.record.update({
            ribbon_text: entry.text || "",
            text_color: entry.fg || "",
            bg_color: entry.bg || "",
        });
    }

    /** Remove a history entry server-side and refresh the local state. */
    async remove(entry, ev) {
        ev.stopPropagation();
        const rec = this.props.record;
        let json;
        try {
            json = await this.orm.call(rec.resModel, "action_remove_history", [entry.fg, entry.bg]);
        } catch (e) {
            json = JSON.stringify(this.state.entries.filter((e2) => e2 !== entry));
        }
        this.state.entries = JSON.parse(json || "[]");
        // Sync the field value: prevents a re-render / re-mount of the form
        // from reviving the just-deleted entry by reading stale JSON.
        await rec.update({ [this.props.name]: json });
    }
}

const pnsRibbonHistory = {
    component: PnsRibbonHistory,
    supportedTypes: ["char", "text"],
};

registry.category("fields").add("pns_ribbon_history", pnsRibbonHistory);

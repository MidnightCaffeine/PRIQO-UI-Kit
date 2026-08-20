"""`FilterBar` — a configurable row of filters above an `AppDataTable`.

Filter definitions are data (a list of dicts), so callers can compose a
bar without writing bespoke layout code for every screen.
"""
from __future__ import annotations

from typing import Callable, Mapping, Optional, Sequence

import flet as ft

from prisqo_ui.theme import Theme
from prisqo_ui.components.forms.fields import SearchField, AppDropdown
from prisqo_ui.components.buttons.buttons import GhostButton


def FilterBar(
    theme: Theme,
    page: ft.Page,
    filters: Sequence[Mapping],
    on_change: Optional[Callable[[dict], None]] = None,
    on_clear: Optional[Callable] = None,
) -> ft.Row:
    """
    filters: sequence of filter definitions, e.g.
        {"key": "search", "type": "search", "label": "Search", "placeholder": "Search items..."}
        {"key": "status", "type": "dropdown", "label": "Status", "options": ["Active", "Inactive"]}
        {"key": "category", "type": "dropdown", "label": "Category", "options": [...]}
    Supported types: search, status, date_range, category, store, location, vendor, customer
    (the latter render as a plain dropdown keyed by their `options`).
    """
    state: dict = {}
    controls: list[ft.Control] = []

    def _emit() -> None:
        if on_change:
            on_change(dict(state))

    for f in filters:
        key = f["key"]
        ftype = f.get("type", "dropdown")
        if ftype == "search":
            field = SearchField(
                theme,
                hint=f.get("placeholder", "Search..."),
                width=f.get("width", 240),
                on_change=lambda e, k=key: (state.update({k: e.control.value}), _emit()),
            )
            controls.append(field)
        else:
            field = AppDropdown(
                theme,
                label=f.get("label"),
                options=f.get("options", []),
                width=f.get("width", 180),
                on_change=lambda e, k=key: (state.update({k: e.control.value}), _emit()),
            )
            controls.append(field)

    def _clear(e: ft.ControlEvent) -> None:
        state.clear()
        if on_clear:
            on_clear()

    controls.append(GhostButton(theme, "Clear filters", icon=ft.Icons.FILTER_ALT_OFF, on_click=_clear))

    return ft.Row(controls=controls, spacing=theme.spacing.SM, wrap=True, run_spacing=theme.spacing.SM)

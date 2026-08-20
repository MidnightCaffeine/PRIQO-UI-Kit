"""`Menu` — a themed popup menu (context menus, row action menus, ...)."""
from __future__ import annotations

from typing import Callable, Mapping, Optional, Sequence

import flet as ft

from prisqo_ui.theme import Theme


def Menu(
    theme: Theme,
    trigger_icon: str = None,
    items: Sequence[Mapping] = (),
    tooltip: str = "More options",
) -> ft.PopupMenuButton:
    """
    items: sequence of {"label": str, "icon": IconData (optional),
           "on_click": Callable, "danger": bool (optional)} or {} for a divider.
    """
    menu_items = []
    for it in items:
        if not it:
            menu_items.append(ft.PopupMenuItem())
            continue
        color = theme.danger if it.get("danger") else theme.text_primary
        row = [ft.Icon(it["icon"], size=16, color=color)] if it.get("icon") else []
        row.append(ft.Text(it["label"], style=theme.typography.body_small(color)))
        menu_items.append(
            ft.PopupMenuItem(content=ft.Row(controls=row, spacing=theme.spacing.SM), on_click=it.get("on_click"))
        )
    return ft.PopupMenuButton(
        icon=trigger_icon or ft.Icons.MORE_VERT,
        icon_color=theme.text_secondary,
        tooltip=tooltip,
        items=menu_items,
    )

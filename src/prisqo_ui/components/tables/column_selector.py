"""`ColumnSelector` — lets users toggle which table columns are visible."""
from __future__ import annotations

from typing import Callable, Mapping, Optional, Sequence

import flet as ft

from prisqo_ui.theme import Theme
from prisqo_ui.components.liquid.toggles import BOUNCE, QUICK


def _liquid_checkbox_visual(theme: Theme, checked: bool, size: int = 20) -> ft.Container:
    """A non-interactive liquid-style checkbox visual — the popup menu item
    itself owns the tap handling, so this only renders the elastic-bounce
    checked state; `_toggle` below mutates it directly.
    """
    check_icon = ft.Icon(
        ft.Icons.CHECK_ROUNDED,
        size=size * 0.7,
        color="#FFFFFF",
        scale=1.0 if checked else 0.0,
        animate_scale=BOUNCE,
    )
    return ft.Container(
        width=size,
        height=size,
        border_radius=theme.radius.SM,
        bgcolor=theme.primary if checked else theme.surface,
        border=ft.Border.all(2, theme.primary if checked else theme.border),
        alignment=ft.Alignment(0, 0),
        content=check_icon,
        animate=QUICK,
    )


def ColumnSelector(
    theme: Theme,
    columns: Sequence[Mapping],
    visible_keys: set,
    on_change: Optional[Callable[[set], None]] = None,
) -> ft.PopupMenuButton:
    """
    columns: sequence of {"key": str, "label": str}
    """
    state = set(visible_keys)
    boxes: dict[str, ft.Container] = {}

    def _toggle(key: str) -> Callable:
        def _handler(e: ft.ControlEvent) -> None:
            if key in state:
                state.discard(key)
            else:
                state.add(key)
            checked = key in state
            box = boxes[key]
            box.bgcolor = theme.primary if checked else theme.surface
            box.border = ft.Border.all(2, theme.primary if checked else theme.border)
            box.content.scale = 1.0 if checked else 0.0
            box.update()
            if on_change:
                on_change(set(state))

        return _handler

    items = []
    for col in columns:
        box = _liquid_checkbox_visual(theme, col["key"] in state)
        boxes[col["key"]] = box
        items.append(
            ft.PopupMenuItem(
                content=ft.Row(
                    controls=[box, ft.Text(col["label"], style=theme.typography.body_small(theme.text_primary))],
                    spacing=theme.spacing.SM,
                ),
                on_click=_toggle(col["key"]),
            )
        )

    return ft.PopupMenuButton(
        icon=ft.Icons.VIEW_COLUMN,
        tooltip="Choose columns",
        items=items,
    )

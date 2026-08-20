"""`BulkActionBar` — appears only when one or more rows are selected."""
from __future__ import annotations

from typing import Callable, Mapping, Optional, Sequence

import flet as ft

from prisqo_ui.theme import Theme
from prisqo_ui.components.buttons.buttons import GhostButton, DangerButton, SecondaryButton


def BulkActionBar(
    theme: Theme,
    selected_count: int,
    actions: Sequence[Mapping],
    on_clear: Optional[Callable] = None,
) -> ft.Container:
    """
    actions: sequence of {"label": str, "icon": IconData (optional),
             "on_click": Callable, "danger": bool (optional)}
    Returns an (invisible when selected_count == 0) container so callers
    can keep it mounted in the layout without conditional rendering.
    """
    action_buttons = []
    for a in actions:
        if a.get("danger"):
            action_buttons.append(DangerButton(theme, a["label"], icon=a.get("icon"), on_click=a["on_click"]))
        else:
            action_buttons.append(SecondaryButton(theme, a["label"], icon=a.get("icon"), on_click=a["on_click"]))

    return ft.Container(
        content=ft.Row(
            controls=[
                ft.Row(
                    controls=[
                        ft.Text(f"{selected_count} selected", style=theme.typography.body(theme.text_primary)),
                        GhostButton(theme, "Clear", on_click=on_clear) if on_clear else ft.Container(),
                    ],
                    spacing=theme.spacing.SM,
                ),
                ft.Row(controls=action_buttons, spacing=theme.spacing.SM),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        ),
        bgcolor=theme.primary_light,
        border=ft.Border.all(1, theme.primary),
        border_radius=theme.radius.MD,
        padding=ft.Padding.symmetric(horizontal=theme.spacing.LG, vertical=theme.spacing.SM),
        visible=selected_count > 0,
    )

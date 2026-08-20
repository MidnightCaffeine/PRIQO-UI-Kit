"""Alert -- an inline, persistent status banner (Bootstrap's `.alert
.alert-{variant}`), distinct from `Toast`/`Snackbar` which are transient
and float over the page.

Use `Alert` for things that should stay visible until the user acts or
dismisses them (form-level validation summaries, "this record is
locked", banner-style warnings above a table) -- use `Toast`/`Snackbar`
for one-shot confirmations ("Saved.").
"""
from __future__ import annotations

from typing import Callable, Optional

import flet as ft

from prisqo_ui.theme import Theme
from prisqo_ui.components.core.variants import VariantName, resolve_variant

_ICONS = {
    "primary": ft.Icons.INFO,
    "secondary": ft.Icons.INFO_OUTLINE,
    "success": ft.Icons.CHECK_CIRCLE,
    "danger": ft.Icons.ERROR,
    "warning": ft.Icons.WARNING_AMBER,
    "info": ft.Icons.INFO,
    "neutral": ft.Icons.INFO_OUTLINE,
    "light": ft.Icons.INFO_OUTLINE,
    "dark": ft.Icons.INFO_OUTLINE,
}


def Alert(
    theme: Theme,
    message: str,
    variant: VariantName = "info",
    title: Optional[str] = None,
    icon: Optional[str] = None,
    dismissible: bool = False,
    on_dismiss: Optional[Callable] = None,
) -> ft.Container:
    """`.alert .alert-{variant}` -- a soft-background banner with an icon,
    optional bold title line, body text, and an optional close button.
    """
    colors = resolve_variant(theme, variant)
    resolved_icon = icon or _ICONS.get(variant, ft.Icons.INFO)

    text_children = []
    if title:
        text_children.append(ft.Text(title, style=theme.typography.label(colors.text)))
    text_children.append(ft.Text(message, style=theme.typography.body_small(colors.text)))

    row_children = [
        ft.Icon(resolved_icon, color=colors.text, size=18),
        ft.Column(controls=text_children, spacing=2, tight=True, expand=True),
    ]

    if dismissible:
        close_btn = ft.IconButton(
            icon=ft.Icons.CLOSE,
            icon_size=16,
            icon_color=colors.text,
            on_click=(lambda e: on_dismiss(e)) if on_dismiss else None,
            style=ft.ButtonStyle(padding=ft.Padding.all(4)),
        )
        row_children.append(close_btn)

    return ft.Container(
        content=ft.Row(
            controls=row_children,
            spacing=theme.spacing.SM,
            vertical_alignment=ft.CrossAxisAlignment.START,
        ),
        bgcolor=colors.soft_bg,
        border=ft.Border.all(1, colors.border),
        border_radius=theme.radius.MD,
        padding=ft.Padding.symmetric(horizontal=14, vertical=12),
    )

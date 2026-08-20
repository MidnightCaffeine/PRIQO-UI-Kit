"""`PageContainer` — the scrollable content wrapper for every ERP page."""
from __future__ import annotations

from typing import Optional

import flet as ft

from prisqo_ui.theme import Theme


def PageContainer(theme: Theme, content: ft.Control, max_width: Optional[float] = None) -> ft.Container:
    inner = content
    if max_width:
        inner = ft.Container(content=content, width=max_width, alignment=ft.Alignment(0, -1))
    return ft.Container(
        content=ft.Column(controls=[inner], scroll=ft.ScrollMode.AUTO, expand=True, horizontal_alignment=ft.CrossAxisAlignment.STRETCH),
        bgcolor=theme.background,
        padding=theme.spacing.XL,
        expand=True,
    )

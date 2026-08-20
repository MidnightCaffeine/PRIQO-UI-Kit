"""`Breadcrumb` — hierarchical page location indicator."""
from __future__ import annotations

from typing import Callable, Optional, Sequence

import flet as ft

from prisqo_ui.theme import Theme


def Breadcrumb(theme: Theme, items: Sequence[str], on_click: Optional[Callable[[int], None]] = None) -> ft.Row:
    controls: list[ft.Control] = []
    for i, label in enumerate(items):
        is_last = i == len(items) - 1
        color = theme.text_primary if is_last else theme.text_muted
        text = ft.Text(label, style=theme.typography.body_small(color))
        if not is_last and on_click:
            controls.append(
                ft.Container(content=text, ink=True, on_click=lambda e, idx=i: on_click(idx), border_radius=theme.radius.SM)
            )
        else:
            controls.append(text)
        if not is_last:
            controls.append(ft.Icon(ft.Icons.CHEVRON_RIGHT, size=14, color=theme.text_muted))
    return ft.Row(controls=controls, spacing=6)

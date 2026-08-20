"""`ChartCard` — a card wrapping a lightweight bar chart.

Flet 0.85.3 does not ship native chart controls, so this renders a
simple, dependency-free bar chart out of styled `Container`s. It's
intentionally minimal — swap in a real charting library inside the
PRISQO ERP app later if richer charts are needed.
"""
from __future__ import annotations

from typing import Mapping, Optional, Sequence

import flet as ft

from prisqo_ui.theme import Theme


def ChartCard(
    theme: Theme,
    title: str,
    data: Sequence[Mapping],
    subtitle: Optional[str] = None,
    max_value: Optional[float] = None,
    bar_color: Optional[str] = None,
    height: int = 160,
) -> ft.Container:
    """
    data: sequence of {"label": str, "value": float}
    """
    color = bar_color or theme.primary
    values = [d["value"] for d in data] or [0]
    top = max_value or max(values) or 1

    bars = []
    for d in data:
        bar_height = max(4, (d["value"] / top) * height)
        bars.append(
            ft.Column(
                controls=[
                    ft.Container(expand=True),
                    ft.Container(
                        width=28,
                        height=bar_height,
                        bgcolor=color,
                        border_radius=ft.BorderRadius(top_left=4, top_right=4, bottom_left=0, bottom_right=0),
                    ),
                    ft.Text(d["label"], style=theme.typography.caption(theme.text_muted), text_align=ft.TextAlign.CENTER),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=6,
                height=height + 28,
            )
        )

    chart = ft.Row(controls=bars, spacing=theme.spacing.LG, alignment=ft.MainAxisAlignment.SPACE_EVENLY)

    header = [ft.Text(title, style=theme.typography.card_title(theme.text_primary))]
    if subtitle:
        header.append(ft.Text(subtitle, style=theme.typography.body_small(theme.text_muted)))

    return ft.Container(
        content=ft.Column(
            controls=[ft.Column(controls=header, spacing=2, tight=True), chart],
            spacing=theme.spacing.MD,
            tight=True,
        ),
        bgcolor=theme.surface,
        border=ft.Border.all(1, theme.border),
        border_radius=theme.radius.LG,
        padding=theme.spacing.LG,
        shadow=theme.shadows.card,
    )

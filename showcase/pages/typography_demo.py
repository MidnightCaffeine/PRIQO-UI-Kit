"""Typography showcase — including the responsive scale.

Resize the window (or, on the web, the browser tab) to see every text
role below resize with it: `ThemeManager` recomputes the active
breakpoint from the page width and rebuilds the whole app with a
rescaled `Typography`, the same way Bootstrap's type scale reads
differently on a phone than a desktop.
"""
from __future__ import annotations

import flet as ft

from prisqo_ui.theme import Theme, BREAKPOINTS
from prisqo_ui.components.cards import SectionCard, AppCard
from prisqo_ui.components.status import StatusChip

_ROLES = [
    ("page_title", "Page Title", "24px @ lg baseline"),
    ("section_title", "Section Title", "18px @ lg baseline"),
    ("card_title", "Card Title", "15px @ lg baseline"),
    ("body", "Body", "14px @ lg baseline"),
    ("body_small", "Body Small", "13px @ lg baseline"),
    ("label", "LABEL", "12px @ lg baseline"),
    ("caption", "Caption", "12px @ lg baseline"),
    ("kpi", "\u20b1125,450.00", "26px @ lg baseline"),
]


def build(theme: Theme, page: ft.Page) -> ft.Control:
    current_bp = theme.breakpoint
    scale = theme.typography.scale

    status = ft.Row(
        controls=[
            StatusChip(theme, f"Breakpoint: {current_bp}", variant="primary"),
            StatusChip(theme, f"Scale: {scale:.2f}\u00d7", variant="info"),
            StatusChip(theme, f"Page width: {int(page.width or 0)}px", variant="neutral"),
        ],
        spacing=8,
        wrap=True,
    )

    scale_rows = []
    for bp in BREAKPOINTS:
        active = bp.name == current_bp
        scale_rows.append(
            ft.Container(
                content=ft.Row(
                    controls=[
                        ft.Text(bp.name, style=theme.typography.label(theme.primary if active else theme.text_secondary), width=40),
                        ft.Text(f">= {bp.min_width}px", style=theme.typography.body_small(theme.text_secondary), width=90),
                        ft.Text(f"{bp.typography_scale:.2f}\u00d7", style=theme.typography.body_small(theme.text_secondary)),
                        ft.Text("\u25c0 current", style=theme.typography.caption(theme.primary)) if active else ft.Container(),
                    ],
                    spacing=12,
                ),
                bgcolor=theme.primary_light if active else None,
                padding=ft.Padding.symmetric(horizontal=10, vertical=6),
                border_radius=theme.radius.SM,
            )
        )

    scale_table = ft.Column(controls=scale_rows, spacing=4, tight=True)

    role_rows = []
    for method_name, sample, note in _ROLES:
        style = getattr(theme.typography, method_name)(theme.text_primary)
        role_rows.append(
            ft.Row(
                controls=[
                    ft.Text(method_name, style=theme.typography.caption(theme.text_muted), width=110),
                    ft.Text(sample, style=style, expand=True),
                    ft.Text(f"{style.size}px now \u00b7 {note}", style=theme.typography.caption(theme.text_muted)),
                ],
                spacing=12,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            )
        )

    role_scale = ft.Column(controls=role_rows, spacing=14, tight=True)

    return ft.Column(
        controls=[
            SectionCard(
                theme,
                "Responsive State",
                status,
                subtitle="Resize the window to watch these change",
            ),
            SectionCard(
                theme,
                "Breakpoint \u2192 Typography Scale",
                scale_table,
                subtitle="theme/breakpoints.py \u2014 Bootstrap's grid breakpoints, each with a type-scale multiplier",
            ),
            SectionCard(
                theme,
                "Type Scale at Current Breakpoint",
                role_scale,
                subtitle="theme.typography.<role>() \u2014 every size below scales together",
            ),
        ],
        spacing=16,
        tight=True,
    )

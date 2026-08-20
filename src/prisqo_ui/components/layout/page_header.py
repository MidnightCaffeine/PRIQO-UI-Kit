"""`PageHeader` — standard title + subtitle + actions block for pages."""
from __future__ import annotations

from typing import Optional, Sequence

import flet as ft

from prisqo_ui.theme import Theme


def PageHeader(
    theme: Theme,
    title: str,
    subtitle: Optional[str] = None,
    actions: Optional[Sequence[ft.Control]] = None,
    breadcrumb: Optional[ft.Control] = None,
) -> ft.Column:
    header_children = []
    if breadcrumb:
        header_children.append(breadcrumb)
    header_children.append(
        ft.Row(
            controls=[
                ft.Column(
                    controls=[
                        ft.Text(title, style=theme.typography.page_title(theme.text_primary)),
                        ft.Text(subtitle, style=theme.typography.body_small(theme.text_muted)) if subtitle else ft.Container(),
                    ],
                    spacing=2,
                    tight=True,
                ),
                ft.Row(controls=list(actions or []), spacing=theme.spacing.SM),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.START,
        )
    )
    return ft.Column(controls=header_children, spacing=theme.spacing.SM, tight=True)

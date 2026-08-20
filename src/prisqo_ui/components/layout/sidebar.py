"""`Sidebar` + `SidebarItem` — the primary ERP navigation surface.

The sidebar keeps its own dark-ish palette (`theme.sidebar_*` tokens) in
both light and dark app themes, matching common ERP/SaaS conventions
(Dynamics 365, Linear) where the nav rail stays visually distinct from
the content area.
"""
from __future__ import annotations

from typing import Callable, Mapping, Optional, Sequence

import flet as ft

from prisqo_ui.theme import Theme


def SidebarItem(
    theme: Theme,
    label: str,
    icon: Optional[str] = None,
    active: bool = False,
    collapsed: bool = False,
    badge: Optional[str] = None,
    on_click: Optional[Callable] = None,
    indent: bool = False,
) -> ft.Container:
    text_color = "#FFFFFF" if active else theme.sidebar_text
    row_controls = []
    if icon:
        row_controls.append(ft.Icon(icon, size=18, color=text_color))
    if not collapsed:
        row_controls.append(ft.Text(label, style=theme.typography.body_small(text_color), expand=True))
        if badge:
            row_controls.append(
                ft.Container(
                    content=ft.Text(badge, style=theme.typography.caption("#FFFFFF")),
                    bgcolor=theme.primary,
                    padding=ft.Padding.symmetric(horizontal=6, vertical=1),
                    border_radius=theme.radius.ROUND,
                )
            )
    return ft.Container(
        content=ft.Row(controls=row_controls, spacing=theme.spacing.SM),
        bgcolor=theme.sidebar_active_bg if active else None,
        border_radius=theme.radius.MD,
        padding=ft.Padding.symmetric(horizontal=12 + (16 if indent and not collapsed else 0), vertical=9),
        ink=True,
        on_click=on_click,
        tooltip=label if collapsed else None,
        animate=ft.Animation(100, ft.AnimationCurve.EASE_OUT),
    )


def Sidebar(
    theme: Theme,
    groups: Sequence[Mapping],
    active_key: Optional[str] = None,
    collapsed: bool = False,
    on_navigate: Optional[Callable[[str], None]] = None,
    header: Optional[ft.Control] = None,
    footer: Optional[ft.Control] = None,
    width_expanded: int = 240,
    width_collapsed: int = 72,
    on_close: Optional[Callable] = None,
) -> ft.Container:
    """
    groups: sequence of {"title": Optional[str], "items": [{"key": str,
            "label": str, "icon": IconData, "badge": Optional[str]}]}

    `on_close`, if given, renders a close (X) button at the top of the
    sidebar -- pass it when rendering the sidebar as a mobile drawer (see
    `AppShell`) so the user has an explicit way to dismiss it besides
    tapping the scrim behind it.
    """
    body: list[ft.Control] = []
    if on_close:
        body.append(
            ft.Row(
                controls=[
                    ft.IconButton(
                        icon=ft.Icons.CLOSE,
                        icon_color=theme.sidebar_text,
                        icon_size=20,
                        tooltip="Close menu",
                        on_click=on_close,
                    )
                ],
                alignment=ft.MainAxisAlignment.END,
            )
        )
    if header:
        body.append(header)
        body.append(ft.Divider(height=1, color=theme.sidebar_active_bg))

    for group in groups:
        if group.get("title") and not collapsed:
            body.append(
                ft.Container(
                    content=ft.Text(
                        group["title"].upper(),
                        style=theme.typography.caption(theme.sidebar_text_muted),
                    ),
                    padding=ft.Padding.only(left=12, top=theme.spacing.MD, bottom=4),
                )
            )
        for item in group.get("items", []):
            body.append(
                SidebarItem(
                    theme,
                    label=item["label"],
                    icon=item.get("icon"),
                    active=item["key"] == active_key,
                    collapsed=collapsed,
                    badge=item.get("badge"),
                    indent=group.get("title") is not None,
                    on_click=(lambda e, k=item["key"]: on_navigate(k)) if on_navigate else None,
                )
            )

    column = ft.Column(controls=body, spacing=2, scroll=ft.ScrollMode.AUTO, expand=True)

    content_children = [column]
    if footer:
        content_children.append(ft.Divider(height=1, color=theme.sidebar_active_bg))
        content_children.append(footer)

    return ft.Container(
        content=ft.Column(controls=content_children, spacing=0, expand=True),
        width=width_collapsed if collapsed else width_expanded,
        bgcolor=theme.sidebar_bg,
        padding=ft.Padding.symmetric(horizontal=8, vertical=theme.spacing.MD),
        animate=ft.Animation(150, ft.AnimationCurve.EASE_OUT),
    )

"""`Navbar` — top app bar with page title, search, and user actions."""
from __future__ import annotations

from typing import Callable, Optional, Sequence

import flet as ft

from prisqo_ui.theme import Theme
from prisqo_ui.components.buttons.buttons import AppIconButton


def Navbar(
    theme: Theme,
    title: Optional[str] = None,
    actions: Optional[Sequence[ft.Control]] = None,
    on_menu_click: Optional[Callable] = None,
    user_menu: Optional[ft.Control] = None,
) -> ft.Container:
    left_controls: list[ft.Control] = []
    if on_menu_click:
        left_controls.append(AppIconButton(theme, ft.Icons.MENU, "Toggle menu", on_click=on_menu_click))
    if title:
        left_controls.append(
            ft.Text(
                title,
                style=theme.typography.section_title(theme.text_primary),
                max_lines=1,
                overflow=ft.TextOverflow.ELLIPSIS,
                expand=True,
            )
        )

    right_controls = list(actions or [])
    if user_menu:
        right_controls.append(user_menu)

    return ft.Container(
        content=ft.Row(
            controls=[
                ft.Row(controls=left_controls, spacing=theme.spacing.SM, expand=True),
                ft.Row(controls=right_controls, spacing=theme.spacing.SM, wrap=True, run_spacing=4),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        ),
        bgcolor=theme.surface,
        border=ft.Border(bottom=ft.BorderSide(1, theme.border)),
        padding=ft.Padding.symmetric(horizontal=theme.spacing.LG, vertical=theme.spacing.MD),
        height=64,
    )


def UserMenu(theme: Theme, name: str, role: Optional[str] = None, avatar_initials: Optional[str] = None) -> ft.PopupMenuButton:
    initials = avatar_initials or "".join([p[0] for p in name.split()[:2]]).upper()
    avatar = ft.CircleAvatar(
        content=ft.Text(initials, style=theme.typography.caption("#FFFFFF")),
        bgcolor=theme.primary,
        radius=16,
    )
    return ft.PopupMenuButton(
        content=ft.Row(
            controls=[
                avatar,
                ft.Column(
                    controls=[
                        ft.Text(name, style=theme.typography.body_small(theme.text_primary)),
                        ft.Text(role or "", style=theme.typography.caption(theme.text_muted)) if role else ft.Container(),
                    ],
                    spacing=0,
                    tight=True,
                ),
                ft.Icon(ft.Icons.EXPAND_MORE, size=16, color=theme.text_muted),
            ],
            spacing=theme.spacing.SM,
        ),
        items=[
            ft.PopupMenuItem(content=ft.Text("Profile")),
            ft.PopupMenuItem(content=ft.Text("Settings")),
            ft.PopupMenuItem(),
            ft.PopupMenuItem(content=ft.Text("Sign out")),
        ],
    )


def NotificationMenu(theme: Theme, count: int = 0) -> ft.Stack:
    icon_btn = AppIconButton(theme, ft.Icons.NOTIFICATIONS_NONE, "Notifications")
    if count <= 0:
        return ft.Stack(controls=[icon_btn], width=40, height=40)
    badge = ft.Container(
        content=ft.Text(str(count), style=theme.typography.caption("#FFFFFF")),
        bgcolor=theme.danger,
        width=16,
        height=16,
        border_radius=theme.radius.ROUND,
        alignment=ft.Alignment(0, 0),
        right=4,
        top=4,
    )
    return ft.Stack(controls=[icon_btn, badge], width=40, height=40)

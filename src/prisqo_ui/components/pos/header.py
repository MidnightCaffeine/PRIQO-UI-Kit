"""The POS screen's top bar — search, store/terminal context, connection
status, and the signed-in cashier. Distinct from the generic ERP
`Navbar`: it's brand-colored and carries store/session context a
touchscreen cashier needs at a glance.
"""
from __future__ import annotations

from typing import Callable, Optional

import flet as ft

from prisqo_ui.theme import Theme
from prisqo_ui.components.buttons.buttons import AppIconButton


def SearchBar(theme: Theme, hint: str = "Search item, barcode, SKU, or scan...", shortcut: Optional[str] = "F2", on_change: Optional[Callable] = None) -> ft.Container:
    field = ft.TextField(
        hint_text=hint,
        hint_style=ft.TextStyle(color=ft.Colors.with_opacity(0.7, theme.text_on_primary), font_family=theme.typography.font_family, size=14),
        text_style=ft.TextStyle(color=theme.text_on_primary, font_family=theme.typography.font_family, size=14),
        prefix_icon=ft.Icons.SEARCH,
        border=ft.InputBorder.NONE,
        content_padding=ft.Padding.symmetric(horizontal=4, vertical=10),
        cursor_color=theme.text_on_primary,
        on_change=on_change,
        expand=True,
    )
    controls: list[ft.Control] = [field]
    if shortcut:
        controls.append(
            ft.Container(
                content=ft.Text(shortcut, style=theme.typography.caption(theme.text_on_primary)),
                bgcolor=ft.Colors.with_opacity(0.18, "#FFFFFF"),
                padding=ft.Padding.symmetric(horizontal=8, vertical=3),
                border_radius=theme.radius.SM,
            )
        )
    return ft.Container(
        content=ft.Row(controls=controls, vertical_alignment=ft.CrossAxisAlignment.CENTER, spacing=8),
        bgcolor=ft.Colors.with_opacity(0.15, "#FFFFFF"),
        border_radius=theme.radius.MD,
        padding=ft.Padding.symmetric(horizontal=12),
        width=420,
        height=42,
    )


def InfoBadge(theme: Theme, icon: str, title: str, subtitle: str) -> ft.Row:
    """Store 01 / Main Branch, Terminal 03 / Front Counter, etc."""
    return ft.Row(
        controls=[
            ft.Icon(icon, size=18, color=theme.text_on_primary),
            ft.Column(
                controls=[
                    ft.Text(title, style=theme.typography.body_small(theme.text_on_primary)),
                    ft.Text(subtitle, style=theme.typography.caption(ft.Colors.with_opacity(0.75, theme.text_on_primary))),
                ],
                spacing=0,
                tight=True,
            ),
        ],
        spacing=8,
    )


def OnlineStatus(theme: Theme, online: bool = True) -> ft.Row:
    color = theme.success if online else theme.danger
    return ft.Row(
        controls=[
            ft.Container(width=8, height=8, bgcolor=color, border_radius=theme.radius.ROUND),
            ft.Text("Online" if online else "Offline", style=theme.typography.body_small(theme.text_on_primary)),
        ],
        spacing=6,
    )


def CashierProfile(theme: Theme, name: str, role: str, avatar_initials: Optional[str] = None) -> ft.Row:
    initials = avatar_initials or "".join(p[0] for p in name.split()[:2]).upper()
    return ft.Row(
        controls=[
            ft.CircleAvatar(content=ft.Text(initials, style=theme.typography.caption(theme.primary)), bgcolor="#FFFFFF", radius=16),
            ft.Column(
                controls=[
                    ft.Text(name, style=theme.typography.body_small(theme.text_on_primary)),
                    ft.Text(role, style=theme.typography.caption(ft.Colors.with_opacity(0.75, theme.text_on_primary))),
                ],
                spacing=0,
                tight=True,
            ),
            ft.Icon(ft.Icons.EXPAND_MORE, size=16, color=theme.text_on_primary),
        ],
        spacing=8,
    )


def POSHeader(
    theme: Theme,
    store_name: str,
    store_branch: str,
    terminal_name: str,
    terminal_type: str,
    cashier_name: str,
    cashier_role: str,
    online: bool = True,
    search_hint: str = "Search item, barcode, SKU, or scan...",
    on_menu_click: Optional[Callable] = None,
    on_search_change: Optional[Callable] = None,
) -> ft.Container:
    """The full brand-colored POS top bar."""
    left: list[ft.Control] = []
    if on_menu_click:
        left.append(AppIconButton(theme, ft.Icons.MENU, "Toggle menu", on_click=on_menu_click))
    left.append(SearchBar(theme, hint=search_hint, on_change=on_search_change))

    right = ft.Row(
        controls=[
            InfoBadge(theme, ft.Icons.STOREFRONT, store_name, store_branch),
            InfoBadge(theme, ft.Icons.POINT_OF_SALE, terminal_name, terminal_type),
            OnlineStatus(theme, online=online),
            CashierProfile(theme, cashier_name, cashier_role),
        ],
        spacing=theme.spacing.XL,
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
    )

    return ft.Container(
        content=ft.Row(
            controls=[ft.Row(controls=left, spacing=theme.spacing.MD, expand=True), right],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        bgcolor=theme.primary,
        padding=ft.Padding.symmetric(horizontal=theme.spacing.LG, vertical=theme.spacing.MD),
        height=68,
    )

"""Navigation showcase — Sidebar, Navbar, Breadcrumb, Tabs, Menu."""
from __future__ import annotations

import flet as ft

from prisqo_ui.theme import Theme
from prisqo_ui.components.cards import SectionCard
from prisqo_ui.components.layout import Sidebar, Navbar, UserMenu, NotificationMenu, Breadcrumb
from prisqo_ui.components.navigation import AppTabs, Menu

DEMO_GROUPS = [
    {
        "title": "Sales",
        "items": [
            {"key": "pos", "label": "POS", "icon": ft.Icons.POINT_OF_SALE},
            {"key": "orders", "label": "Orders", "icon": ft.Icons.RECEIPT_LONG, "badge": "3"},
            {"key": "invoices", "label": "Invoices", "icon": ft.Icons.DESCRIPTION_OUTLINED},
        ],
    },
    {
        "title": "Inventory",
        "items": [
            {"key": "items", "label": "Items", "icon": ft.Icons.INVENTORY_2_OUTLINED},
            {"key": "stock", "label": "Stock", "icon": ft.Icons.WAREHOUSE_OUTLINED},
        ],
    },
]


def build(theme: Theme, page: ft.Page) -> ft.Control:
    sidebar_preview = ft.Container(
        content=Sidebar(theme, DEMO_GROUPS, active_key="orders", width_expanded=220),
        height=340,
        border_radius=theme.radius.LG,
        clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
    )
    sidebar_collapsed_preview = ft.Container(
        content=Sidebar(theme, DEMO_GROUPS, active_key="items", collapsed=True),
        height=340,
        border_radius=theme.radius.LG,
        clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
    )

    navbar_preview = Navbar(
        theme,
        title="Inventory",
        actions=[NotificationMenu(theme, 4)],
        user_menu=UserMenu(theme, "Maria Santos", "Cashier"),
    )

    breadcrumb = Breadcrumb(theme, ["Home", "Inventory", "Items", "Coca-Cola 1L"])

    tabs = AppTabs(
        theme,
        tabs=[
            {"label": "Details", "content": ft.Container(content=ft.Text("Item details go here.", style=theme.typography.body(theme.text_secondary)), padding=16)},
            {"label": "Stock History", "content": ft.Container(content=ft.Text("Stock movement history.", style=theme.typography.body(theme.text_secondary)), padding=16)},
            {"label": "Pricing", "content": ft.Container(content=ft.Text("Pricing tiers.", style=theme.typography.body(theme.text_secondary)), padding=16)},
        ],
        height=140,
    )

    menu = Menu(
        theme,
        items=[
            {"label": "Duplicate", "icon": ft.Icons.CONTENT_COPY, "on_click": lambda e: None},
            {"label": "Export", "icon": ft.Icons.DOWNLOAD, "on_click": lambda e: None},
            {},
            {"label": "Delete", "icon": ft.Icons.DELETE_OUTLINE, "danger": True, "on_click": lambda e: None},
        ],
    )

    return ft.Column(
        controls=[
            SectionCard(
                theme,
                "Sidebar (Expanded / Collapsed)",
                ft.Row(controls=[sidebar_preview, sidebar_collapsed_preview], spacing=16),
            ),
            SectionCard(theme, "Navbar", navbar_preview),
            SectionCard(theme, "Breadcrumb", breadcrumb),
            SectionCard(theme, "Tabs", tabs),
            SectionCard(theme, "Popup Menu", menu),
        ],
        spacing=16,
        tight=True,
    )

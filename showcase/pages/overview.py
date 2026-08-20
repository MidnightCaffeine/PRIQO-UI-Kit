"""Overview — the showcase landing page."""
from __future__ import annotations

import flet as ft

from prisqo_ui.theme import Theme
from prisqo_ui.components.cards import AppCard, StatCard
from prisqo_ui.components.status import StatusChip

CATEGORIES = [
    ("Buttons", "7 variants \u00b7 all states", ft.Icons.SMART_BUTTON),
    ("Cards", "5 surfaces for grouping content", ft.Icons.DASHBOARD_CUSTOMIZE_OUTLINED),
    ("Forms", "12 field types + layout helpers", ft.Icons.EDIT_NOTE),
    ("Lookups", "Generic + 5 ERP-specific lookups", ft.Icons.SEARCH),
    ("Tables", "Data table, filters, pagination", ft.Icons.TABLE_CHART_OUTLINED),
    ("Dialogs", "5 dialog patterns", ft.Icons.CHAT_BUBBLE_OUTLINE),
    ("Feedback", "Toasts, skeletons, empty/error states", ft.Icons.NOTIFICATIONS_NONE),
    ("Status", "Chips, badges, dots", ft.Icons.LABEL_OUTLINE),
    ("Financial", "Amounts, totals, payment summary", ft.Icons.PAYMENTS_OUTLINED),
    ("Navigation", "Sidebar, navbar, tabs, breadcrumbs", ft.Icons.MENU_OPEN),
    ("POS", "Touch-friendly checkout components", ft.Icons.POINT_OF_SALE),
    ("ERP Components", "Inventory + approval status", ft.Icons.BUSINESS_CENTER_OUTLINED),
]


def build(theme: Theme, page: ft.Page) -> ft.Control:
    hero = ft.Container(
        content=ft.Column(
            controls=[
                ft.Text("PRISQO UI KIT", style=theme.typography.page_title(theme.text_primary)),
                ft.Text(
                    "A standalone, modern ERP component library built for Flet 0.85.3.",
                    style=theme.typography.body(theme.text_secondary),
                ),
                ft.Row(
                    controls=[
                        StatusChip(theme, "70+ Components", status="info"),
                        StatusChip(theme, "Light + Dark", status="success"),
                        StatusChip(theme, "Flet 0.85.3", status="info"),
                        StatusChip(theme, "Zero Dependencies", status="neutral"),
                    ],
                    spacing=theme.spacing.SM,
                    wrap=True,
                    run_spacing=theme.spacing.SM,
                ),
            ],
            spacing=theme.spacing.SM,
            tight=True,
        ),
        padding=theme.spacing.XL,
        bgcolor=theme.surface,
        border=ft.Border.all(1, theme.border),
        border_radius=theme.radius.LG,
    )

    stats_row = ft.Row(
        controls=[
            StatCard(theme, "Design Tokens", "6 categories", icon=ft.Icons.PALETTE_OUTLINED),
            StatCard(theme, "Component Groups", "13 categories", icon=ft.Icons.WIDGETS_OUTLINED),
            StatCard(theme, "Theme Modes", "Light / Dark / System", icon=ft.Icons.CONTRAST),
            StatCard(theme, "ERP Modules Ready", "Inventory, POS, Purchasing", icon=ft.Icons.BUSINESS_CENTER_OUTLINED),
        ],
        spacing=theme.spacing.MD,
        wrap=True,
        run_spacing=theme.spacing.MD,
    )

    category_cards = ft.Row(
        controls=[
            ft.Container(
                content=AppCard(
                    theme,
                    content=ft.Text(desc, style=theme.typography.body_small(theme.text_muted)),
                    title=title,
                    icon=icon,
                ),
                width=360,
            )
            for title, desc, icon in CATEGORIES
        ],
        wrap=True,
        spacing=theme.spacing.MD,
        run_spacing=theme.spacing.MD,
    )

    return ft.Column(
        controls=[
            hero,
            stats_row,
            ft.Text("Component Categories", style=theme.typography.section_title(theme.text_primary)),
            category_cards,
        ],
        spacing=theme.spacing.LG,
        tight=True,
    )

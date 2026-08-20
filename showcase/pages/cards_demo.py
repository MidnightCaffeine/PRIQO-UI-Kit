"""Cards showcase."""
from __future__ import annotations

import flet as ft

from prisqo_ui.theme import Theme
from prisqo_ui.components.cards import AppCard, SectionCard, KPICard, StatCard, MetricCard
from prisqo_ui.components.buttons import GhostButton, PrimaryButton


def build(theme: Theme, page: ft.Page) -> ft.Control:
    kpis = ft.Row(
        controls=[
            KPICard(theme, "Today's Sales", "\u20b1125,450.00", trend="+12.5%", trend_label="vs yesterday", icon=ft.Icons.TRENDING_UP),
            KPICard(theme, "Open Orders", "38", trend="-4.2%", trend_label="vs last week", icon=ft.Icons.RECEIPT_LONG),
            KPICard(theme, "Low Stock Items", "6", icon=ft.Icons.WARNING_AMBER),
        ],
        spacing=16,
        wrap=True,
        run_spacing=16,
    )

    stats = ft.Row(
        controls=[
            StatCard(theme, "Total Customers", "1,204", icon=ft.Icons.GROUPS_OUTLINED),
            StatCard(theme, "Active Vendors", "58", icon=ft.Icons.LOCAL_SHIPPING_OUTLINED, color=theme.info),
            StatCard(theme, "Pending Approvals", "12", icon=ft.Icons.PENDING_ACTIONS, color=theme.warning),
        ],
        spacing=16,
        wrap=True,
        run_spacing=16,
    )

    metrics = ft.Row(
        controls=[
            MetricCard(theme, "Gross Margin", "34.2%", delta="+1.1%", delta_positive=True, footer_note="Last 30 days"),
            MetricCard(theme, "Return Rate", "2.4%", delta="+0.3%", delta_positive=False, footer_note="Last 30 days"),
        ],
        spacing=16,
        wrap=True,
        run_spacing=16,
    )

    app_card = AppCard(
        theme,
        title="Recent Activity",
        subtitle="Last updated 5 minutes ago",
        icon=ft.Icons.HISTORY,
        content=ft.Column(
            controls=[
                ft.Text("Invoice INV-1042 posted by Ana Lim", style=theme.typography.body_small(theme.text_secondary)),
                ft.Text("PO-2201 approved by Juan Dela Cruz", style=theme.typography.body_small(theme.text_secondary)),
            ],
            spacing=6,
            tight=True,
        ),
        actions=[GhostButton(theme, "View all")],
        footer=ft.Row(controls=[PrimaryButton(theme, "Refresh", icon=ft.Icons.REFRESH)], alignment=ft.MainAxisAlignment.END),
    )

    section = SectionCard(
        theme,
        "Shipping Details",
        subtitle="Grouped form fields inside a card",
        content=ft.Text("Section cards are used to group related form fields.", style=theme.typography.body_small(theme.text_muted)),
    )

    return ft.Column(
        controls=[
            ft.Text("KPI Cards", style=theme.typography.section_title(theme.text_primary)),
            kpis,
            ft.Text("Stat Cards", style=theme.typography.section_title(theme.text_primary)),
            stats,
            ft.Text("Metric Cards", style=theme.typography.section_title(theme.text_primary)),
            metrics,
            ft.Text("App Card & Section Card", style=theme.typography.section_title(theme.text_primary)),
            ft.Row(controls=[ft.Container(content=app_card, width=420), ft.Container(content=section, width=420)], spacing=16, wrap=True, run_spacing=16),
        ],
        spacing=16,
        tight=True,
    )

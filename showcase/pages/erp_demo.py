"""ERP components showcase — InventoryStatus, ApprovalStatus, and a combined
mini inventory table using several ERP components together.
"""
from __future__ import annotations

import flet as ft

from prisqo_ui.theme import Theme
from prisqo_ui.components.cards import SectionCard, AppCard
from prisqo_ui.components.erp import InventoryStatus, ApprovalStatus
from prisqo_ui.components.tables import AppDataTable
from prisqo_ui.mock_data import ITEMS


def build(theme: Theme, page: ft.Page) -> ft.Control:
    inventory_row = ft.Row(
        controls=[
            InventoryStatus(theme, 0),
            InventoryStatus(theme, 8),
            InventoryStatus(theme, 120),
        ],
        spacing=12,
    )

    approval_row = ft.Row(
        controls=[
            ApprovalStatus(theme, "Draft"),
            ApprovalStatus(theme, "Pending"),
            ApprovalStatus(theme, "Approved"),
            ApprovalStatus(theme, "Rejected"),
            ApprovalStatus(theme, "Posted"),
            ApprovalStatus(theme, "Cancelled"),
        ],
        spacing=8,
        wrap=True,
        run_spacing=8,
    )

    columns = [
        {"key": "name", "label": "Item"},
        {"key": "category", "label": "Category"},
        {"key": "stock", "label": "Stock", "numeric": True},
        {"key": "status", "label": "Status", "render": lambda r: InventoryStatus(theme, r["stock"])},
    ]
    combined_table = AppDataTable(theme, columns, ITEMS, row_id_field="sku", page=page)

    module_cards = ft.Row(
        controls=[
            AppCard(theme, title="Inventory", icon=ft.Icons.INVENTORY_2_OUTLINED, content=ft.Text("Item, Stock, Transfers, Adjustments", style=theme.typography.body_small(theme.text_muted))),
            AppCard(theme, title="POS", icon=ft.Icons.POINT_OF_SALE, content=ft.Text("Touch-friendly checkout flow", style=theme.typography.body_small(theme.text_muted))),
            AppCard(theme, title="Purchasing", icon=ft.Icons.LOCAL_SHIPPING_OUTLINED, content=ft.Text("Vendors, Purchase Orders, Receiving", style=theme.typography.body_small(theme.text_muted))),
        ],
        spacing=16,
        wrap=True,
        run_spacing=16,
    )

    return ft.Column(
        controls=[
            SectionCard(theme, "Inventory Status", inventory_row, subtitle="Derived from stock count \u2014 In Stock / Low Stock / Out of Stock"),
            SectionCard(theme, "Approval Status", approval_row),
            SectionCard(theme, "Combined: Table + Inventory Status", combined_table),
            SectionCard(theme, "Future PRISQO Modules", module_cards, subtitle="These components are ready to be composed into real ERP pages"),
        ],
        spacing=16,
        tight=True,
    )

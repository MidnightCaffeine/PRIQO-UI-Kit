"""Tables showcase — AppDataTable, FilterBar, Pagination, BulkActionBar, ColumnSelector."""
from __future__ import annotations

import flet as ft

from prisqo_ui.theme import Theme
from prisqo_ui.components.cards import SectionCard
from prisqo_ui.components.buttons import PrimaryButton
from prisqo_ui.components.status import StatusChip
from prisqo_ui.components.tables import AppDataTable, FilterBar, Pagination, BulkActionBar, ColumnSelector
from prisqo_ui.mock_data import ITEMS

COLUMNS = [
    {"key": "name", "label": "Item"},
    {"key": "category", "label": "Category"},
    {"key": "stock", "label": "Stock", "numeric": True},
    {"key": "price", "label": "Price", "numeric": True, "render": lambda r: ft.Text(f"\u20b1{r['price']:,.2f}")},
    {"key": "status", "label": "Status"},
]


def build(theme: Theme, page: ft.Page) -> ft.Control:
    columns = [dict(c) for c in COLUMNS]
    columns[-1]["render"] = lambda r: StatusChip(theme, r["status"])

    toolbar = ft.Row(
        controls=[
            FilterBar(
                theme,
                page,
                filters=[
                    {"key": "search", "type": "search", "label": "Search", "placeholder": "Search items..."},
                    {"key": "status", "type": "dropdown", "label": "Status", "options": ["In Stock", "Low Stock", "Out of Stock"]},
                    {"key": "category", "type": "dropdown", "label": "Category", "options": ["Beverage", "Grocery", "Dairy"]},
                ],
            ),
            ft.Row(
                controls=[
                    ColumnSelector(theme, columns, visible_keys={c["key"] for c in columns}),
                    PrimaryButton(theme, "New Item", icon=ft.Icons.ADD),
                ],
                spacing=8,
            ),
        ],
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
    )

    normal_table = AppDataTable(
        theme,
        columns,
        ITEMS,
        row_id_field="sku",
        selectable=True,
        row_actions=[
            {"icon": ft.Icons.EDIT_OUTLINED, "tooltip": "Edit", "on_click": lambda r: None},
            {"icon": ft.Icons.DELETE_OUTLINE, "tooltip": "Delete", "on_click": lambda r: None, "danger": True},
        ],
        page=page,
    )

    bulk_bar = BulkActionBar(
        theme,
        selected_count=2,
        actions=[
            {"label": "Archive", "icon": ft.Icons.ARCHIVE_OUTLINED, "on_click": lambda e: None},
            {"label": "Delete", "icon": ft.Icons.DELETE_OUTLINE, "on_click": lambda e: None, "danger": True},
        ],
        on_clear=lambda e: None,
    )

    pagination = Pagination(theme, current_page=1, total_pages=8, total_records=len(ITEMS) * 8, on_page_change=lambda p: None)

    loading_table = AppDataTable(theme, columns, ITEMS, loading=True)
    empty_table = AppDataTable(theme, columns, [])

    return ft.Column(
        controls=[
            SectionCard(theme, "Items Table", ft.Column(controls=[toolbar, bulk_bar, normal_table, pagination], spacing=16, tight=True)),
            SectionCard(theme, "Loading State", loading_table),
            SectionCard(theme, "Empty State", empty_table),
        ],
        spacing=16,
        tight=True,
    )

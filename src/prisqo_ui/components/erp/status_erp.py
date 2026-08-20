"""ERP-specific status indicators: `InventoryStatus`, `ApprovalStatus`.

Both compose the generic `StatusChip` from `components.status`.
"""
from __future__ import annotations

import flet as ft

from prisqo_ui.theme import Theme
from prisqo_ui.components.status.status import StatusChip


def InventoryStatus(theme: Theme, stock: int, low_stock_threshold: int = 15) -> ft.Container:
    if stock <= 0:
        return StatusChip(theme, "Out of Stock", status="out of stock")
    if stock <= low_stock_threshold:
        return StatusChip(theme, "Low Stock", status="low stock")
    return StatusChip(theme, "In Stock", status="in stock")


def ApprovalStatus(theme: Theme, status: str) -> ft.Container:
    """status: one of Draft, Pending, Approved, Rejected, Posted, Cancelled."""
    return StatusChip(theme, status, status=status)

"""Status showcase — StatusChip, StatusBadge, StatusDot across all statuses."""
from __future__ import annotations

import flet as ft

from prisqo_ui.theme import Theme
from prisqo_ui.components.cards import SectionCard
from prisqo_ui.components.status import StatusChip, StatusBadge, StatusDot

DOCUMENT_STATUSES = ["Draft", "Pending", "Approved", "Rejected", "Posted", "Cancelled"]
RECORD_STATUSES = ["Active", "Inactive"]
PAYMENT_STATUSES = ["Paid", "Unpaid", "Partially Paid"]
STOCK_STATUSES = ["In Stock", "Low Stock", "Out of Stock"]


def _chip_row(theme: Theme, statuses: list[str]) -> ft.Row:
    return ft.Row(controls=[StatusChip(theme, s) for s in statuses], spacing=8, wrap=True, run_spacing=8)


def _badge_row(theme: Theme, statuses: list[str]) -> ft.Row:
    return ft.Row(controls=[StatusBadge(theme, s) for s in statuses], spacing=8, wrap=True, run_spacing=8)


def _dot_row(theme: Theme, statuses: list[str]) -> ft.Row:
    return ft.Row(controls=[StatusDot(theme, s) for s in statuses], spacing=16, wrap=True, run_spacing=8)


def build(theme: Theme, page: ft.Page) -> ft.Control:
    all_statuses = DOCUMENT_STATUSES + RECORD_STATUSES + PAYMENT_STATUSES + STOCK_STATUSES

    return ft.Column(
        controls=[
            SectionCard(theme, "Status Chips", _chip_row(theme, all_statuses), subtitle="Document, record, payment, and stock statuses"),
            SectionCard(theme, "Status Badges", _badge_row(theme, all_statuses)),
            SectionCard(theme, "Status Dots", _dot_row(theme, all_statuses), subtitle="Paired with text \u2014 color is never the only indicator"),
        ],
        spacing=16,
        tight=True,
    )

"""Financial showcase — AmountDisplay, TotalsSummary, PaymentSummary."""
from __future__ import annotations

import flet as ft

from prisqo_ui.theme import Theme
from prisqo_ui.components.cards import SectionCard
from prisqo_ui.components.erp import AmountDisplay, TotalsSummary, PaymentSummary


def build(theme: Theme, page: ft.Page) -> ft.Control:
    amounts = ft.Row(
        controls=[
            AmountDisplay(theme, 125450.00, size="lg"),
            AmountDisplay(theme, 10640.00, size="md"),
            AmountDisplay(theme, 75.00, size="sm"),
            AmountDisplay(theme, -500.00, size="md"),
        ],
        spacing=24,
        vertical_alignment=ft.CrossAxisAlignment.END,
    )

    totals = TotalsSummary(
        theme,
        subtotal=10000.00,
        discount=500.00,
        vat=1140.00,
        grand_total=10640.00,
    )

    payment = PaymentSummary(
        theme,
        amount_due=500.00,
        amount_tendered=1000.00,
        payment_method="Cash",
    )

    return ft.Column(
        controls=[
            SectionCard(theme, "Amount Display", amounts, subtitle="Sizes: lg, md, sm \u2014 negative amounts in danger color"),
            SectionCard(
                theme,
                "Totals Summary & Payment Summary",
                ft.Row(controls=[totals, payment], spacing=16, wrap=True, run_spacing=16),
                subtitle="Display-only \u2014 values are pre-computed by the caller",
            ),
        ],
        spacing=16,
        tight=True,
    )

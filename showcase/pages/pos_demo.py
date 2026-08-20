"""POS showcase — touch-friendly checkout components."""
from __future__ import annotations

import flet as ft

from prisqo_ui.theme import Theme
from prisqo_ui.components.cards import SectionCard
from prisqo_ui.components.pos import LargeButton, NumericInput, QuantityControl, CartSummary, TenderButton

CART_ITEMS = [
    {"name": "Coca-Cola 1L", "quantity": 2, "unit_price": 75.00, "line_total": 150.00},
    {"name": "Lucky Me Pancit Canton", "quantity": 5, "unit_price": 15.00, "line_total": 75.00},
]


def build(theme: Theme, page: ft.Page) -> ft.Control:
    large_buttons = ft.Row(
        controls=[
            LargeButton(theme, "Cash", icon=ft.Icons.PAYMENTS),
            LargeButton(theme, "Card", icon=ft.Icons.CREDIT_CARD, primary=False),
            LargeButton(theme, "GCash", icon=ft.Icons.QR_CODE, primary=False),
        ],
        spacing=16,
        wrap=True,
        run_spacing=12,
    )

    numeric_and_qty = ft.Row(
        controls=[
            NumericInput(theme, label="Cash Tendered", value="1000", width=200),
            ft.Column(
                controls=[ft.Text("Quantity", style=theme.typography.label(theme.text_secondary)), QuantityControl(theme, quantity=3)],
                spacing=8,
            ),
        ],
        spacing=32,
        vertical_alignment=ft.CrossAxisAlignment.END,
    )

    cart = CartSummary(theme, CART_ITEMS, subtotal=225.00, vat=27.00, grand_total=252.00)

    tender = TenderButton(theme, amount=252.00)

    return ft.Column(
        controls=[
            SectionCard(theme, "Large Touch Buttons", large_buttons, subtitle="Minimum 56px tall for touchscreen use"),
            SectionCard(theme, "Numeric Input & Quantity Control", numeric_and_qty),
            SectionCard(theme, "Cart Summary", ft.Column(controls=[cart, tender], spacing=16, tight=True)),
        ],
        spacing=16,
        tight=True,
    )

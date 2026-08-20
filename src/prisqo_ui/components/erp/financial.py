"""Financial display components.

IMPORTANT: these components only DISPLAY pre-computed values. They do
not perform any accounting, tax, or discount calculations — all
totals/amounts must be computed by the caller and passed in.
"""
from __future__ import annotations

from typing import Optional, Sequence

import flet as ft

from prisqo_ui.theme import Theme

PESO = "\u20b1"


def _format_amount(amount: float, currency_symbol: str) -> str:
    negative = amount < 0
    formatted = f"{currency_symbol}{abs(amount):,.2f}"
    return f"-{formatted}" if negative else formatted


def AmountDisplay(
    theme: Theme,
    amount: float,
    currency_symbol: str = PESO,
    size: str = "md",
    color: Optional[str] = None,
) -> ft.Text:
    """size: 'sm' | 'md' | 'lg' — controls text weight/size only."""
    style_fn = {"sm": theme.typography.body_small, "md": theme.typography.currency, "lg": theme.typography.kpi}.get(
        size, theme.typography.currency
    )
    resolved_color = color or (theme.danger if amount < 0 else theme.text_primary)
    return ft.Text(_format_amount(amount, currency_symbol), style=style_fn(resolved_color))


def TotalsSummary(
    theme: Theme,
    subtotal: float,
    discount: float = 0.0,
    vat: float = 0.0,
    other_charges: float = 0.0,
    withholding_tax: float = 0.0,
    grand_total: Optional[float] = None,
    currency_symbol: str = PESO,
) -> ft.Container:
    """Displays a standard ERP totals breakdown. `grand_total` should be
    supplied by the caller (pre-computed) — this component never adds
    the numbers up itself.
    """
    rows: list[tuple[str, float]] = [("Subtotal", subtotal)]
    if discount:
        rows.append(("Discount", -abs(discount)))
    if vat:
        rows.append(("VAT", vat))
    if other_charges:
        rows.append(("Other Charges", other_charges))
    if withholding_tax:
        rows.append(("Withholding Tax", -abs(withholding_tax)))

    line_controls = [
        ft.Row(
            controls=[
                ft.Text(label, style=theme.typography.body_small(theme.text_secondary)),
                AmountDisplay(theme, value, currency_symbol, size="sm"),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        )
        for label, value in rows
    ]

    total_value = grand_total if grand_total is not None else subtotal - discount + vat + other_charges - withholding_tax

    return ft.Container(
        content=ft.Column(
            controls=[
                *line_controls,
                ft.Divider(height=1, color=theme.divider),
                ft.Row(
                    controls=[
                        ft.Text("TOTAL", style=theme.typography.card_title(theme.text_primary)),
                        AmountDisplay(theme, total_value, currency_symbol, size="lg"),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                ),
            ],
            spacing=theme.spacing.SM,
            tight=True,
        ),
        bgcolor=theme.surface,
        border=ft.Border.all(1, theme.border),
        border_radius=theme.radius.LG,
        padding=theme.spacing.LG,
        width=320,
    )


def PaymentSummary(
    theme: Theme,
    amount_due: float,
    amount_tendered: float,
    change: Optional[float] = None,
    payment_method: Optional[str] = None,
    currency_symbol: str = PESO,
) -> ft.Container:
    """POS/AR payment recap. `change` should be pre-computed by the caller."""
    resolved_change = change if change is not None else amount_tendered - amount_due
    rows = [
        ("Amount Due", amount_due),
        ("Amount Tendered", amount_tendered),
    ]
    line_controls = [
        ft.Row(
            controls=[
                ft.Text(label, style=theme.typography.body_small(theme.text_secondary)),
                AmountDisplay(theme, value, currency_symbol, size="sm"),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        )
        for label, value in rows
    ]
    if payment_method:
        line_controls.insert(
            0,
            ft.Row(
                controls=[
                    ft.Text("Payment Method", style=theme.typography.body_small(theme.text_secondary)),
                    ft.Text(payment_method, style=theme.typography.body_small(theme.text_primary)),
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            ),
        )
    return ft.Container(
        content=ft.Column(
            controls=[
                *line_controls,
                ft.Divider(height=1, color=theme.divider),
                ft.Row(
                    controls=[
                        ft.Text("CHANGE", style=theme.typography.card_title(theme.text_primary)),
                        AmountDisplay(
                            theme,
                            resolved_change,
                            currency_symbol,
                            size="lg",
                            color=theme.success if resolved_change >= 0 else theme.danger,
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                ),
            ],
            spacing=theme.spacing.SM,
            tight=True,
        ),
        bgcolor=theme.surface,
        border=ft.Border.all(1, theme.border),
        border_radius=theme.radius.LG,
        padding=theme.spacing.LG,
        width=320,
    )

"""POS-friendly components — larger touch targets, simple hierarchy,
fast interaction. Back-office components elsewhere in the library stay
compact; these are specifically for touchscreen checkout flows.
"""
from __future__ import annotations

from typing import Callable, Mapping, Optional, Sequence

import flet as ft

from prisqo_ui.theme import Theme
from prisqo_ui.components.erp.financial import AmountDisplay, TotalsSummary
from prisqo_ui.components.buttons.buttons import AppIconButton

PESO = "\u20b1"


def LargeButton(
    theme: Theme,
    text: str,
    icon: Optional[str] = None,
    on_click: Optional[Callable] = None,
    disabled: bool = False,
    primary: bool = True,
    width: Optional[float] = None,
) -> ft.Button:
    """A large, touch-friendly button for POS screens (min 56px tall)."""
    style = ft.ButtonStyle(
        bgcolor={
            ft.ControlState.DEFAULT: theme.primary if primary else theme.surface_variant,
            ft.ControlState.DISABLED: theme.primary_disabled if primary else theme.surface_variant,
        },
        color={
            ft.ControlState.DEFAULT: theme.text_on_primary if primary else theme.text_primary,
            ft.ControlState.DISABLED: theme.text_muted,
        },
        shape=ft.RoundedRectangleBorder(radius=theme.radius.LG),
        text_style=ft.TextStyle(size=16, weight=ft.FontWeight.W_600, font_family=theme.typography.font_family),
        padding=ft.Padding.symmetric(horizontal=theme.spacing.XL, vertical=theme.spacing.LG),
    )
    return ft.Button(
        content=ft.Text(text),
        icon=icon,
        on_click=on_click,
        disabled=disabled,
        style=style,
        width=width,
        height=56,
    )


def NumericInput(
    theme: Theme,
    label: Optional[str] = None,
    value: str = "0",
    width: Optional[float] = None,
    on_change: Optional[Callable] = None,
) -> ft.TextField:
    """A large-text numeric field sized for touch entry (POS quantity/cash)."""
    return ft.TextField(
        label=label,
        value=value,
        width=width,
        height=64,
        text_align=ft.TextAlign.RIGHT,
        text_style=ft.TextStyle(size=22, weight=ft.FontWeight.W_600, font_family=theme.typography.font_family, color=theme.text_primary),
        keyboard_type=ft.KeyboardType.NUMBER,
        input_filter=ft.InputFilter(regex_string=r"^\d*\.?\d*$", allow=True, replacement_string=""),
        border=ft.InputBorder.OUTLINE,
        border_radius=theme.radius.MD,
        border_color=theme.border,
        focused_border_color=theme.primary,
        bgcolor=theme.surface,
        content_padding=ft.Padding.symmetric(horizontal=16, vertical=14),
        on_change=on_change,
    )


def QuantityControl(
    theme: Theme,
    quantity: int = 1,
    min_quantity: int = 1,
    max_quantity: int = 9999,
    on_change: Optional[Callable[[int], None]] = None,
) -> ft.Row:
    """A [-] qty [+] control with large touch targets."""
    qty_text = ft.Text(str(quantity), style=ft.TextStyle(size=18, weight=ft.FontWeight.W_700, color=theme.text_primary))
    state = {"qty": quantity}

    def _update(delta: int) -> Callable:
        def _handler(e: ft.ControlEvent) -> None:
            new_qty = max(min_quantity, min(max_quantity, state["qty"] + delta))
            state["qty"] = new_qty
            qty_text.value = str(new_qty)
            qty_text.update()
            if on_change:
                on_change(new_qty)

        return _handler

    def _btn(icon: str, delta: int) -> ft.Container:
        return ft.Container(
            content=ft.Icon(icon, size=20, color=theme.primary),
            width=40,
            height=40,
            bgcolor=theme.primary_light,
            border_radius=theme.radius.MD,
            alignment=ft.Alignment(0, 0),
            ink=True,
            on_click=_update(delta),
        )

    return ft.Row(
        controls=[
            _btn(ft.Icons.REMOVE, -1),
            ft.Container(content=qty_text, width=40, alignment=ft.Alignment(0, 0)),
            _btn(ft.Icons.ADD, 1),
        ],
        spacing=theme.spacing.SM,
    )


def CartItem(
    theme: Theme,
    name: str,
    quantity: int,
    unit_price: float,
    line_total: float,
    on_quantity_change: Optional[Callable[[int], None]] = None,
    on_remove: Optional[Callable] = None,
) -> ft.Container:
    """A single line in the POS cart: name, qty control, price, remove."""
    return ft.Container(
        content=ft.Row(
            controls=[
                ft.Column(
                    controls=[
                        ft.Text(name, style=theme.typography.body(theme.text_primary)),
                        ft.Text(f"{PESO}{unit_price:,.2f} each", style=theme.typography.caption(theme.text_muted)),
                    ],
                    spacing=2,
                    tight=True,
                    expand=True,
                ),
                QuantityControl(theme, quantity=quantity, on_change=on_quantity_change),
                ft.Container(
                    content=AmountDisplay(theme, line_total),
                    width=90,
                    alignment=ft.Alignment(1, 0),
                ),
                AppIconButton(theme, ft.Icons.DELETE_OUTLINE, "Remove", danger=True, on_click=on_remove),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        padding=ft.Padding.symmetric(horizontal=theme.spacing.MD, vertical=theme.spacing.SM),
        border=ft.Border(bottom=ft.BorderSide(1, theme.divider)),
    )


def CartSummary(
    theme: Theme,
    items: Sequence[Mapping],
    subtotal: float,
    discount: float = 0.0,
    vat: float = 0.0,
    grand_total: Optional[float] = None,
) -> ft.Container:
    """The full cart panel: item list + totals breakdown."""
    cart_rows = [
        CartItem(
            theme,
            name=it["name"],
            quantity=it["quantity"],
            unit_price=it["unit_price"],
            line_total=it["line_total"],
            on_quantity_change=it.get("on_quantity_change"),
            on_remove=it.get("on_remove"),
        )
        for it in items
    ]
    return ft.Container(
        content=ft.Column(
            controls=[
                ft.Text(f"Cart ({len(items)} items)", style=theme.typography.section_title(theme.text_primary)),
                ft.Column(controls=cart_rows, spacing=0, scroll=ft.ScrollMode.AUTO, height=240)
                if cart_rows
                else ft.Text("Cart is empty", style=theme.typography.body_small(theme.text_muted)),
                TotalsSummary(theme, subtotal=subtotal, discount=discount, vat=vat, grand_total=grand_total),
            ],
            spacing=theme.spacing.MD,
            tight=True,
        ),
        bgcolor=theme.surface,
        border=ft.Border.all(1, theme.border),
        border_radius=theme.radius.LG,
        padding=theme.spacing.LG,
        width=380,
    )


def TenderButton(
    theme: Theme,
    label: str = "Tender / Pay",
    amount: Optional[float] = None,
    on_click: Optional[Callable] = None,
    disabled: bool = False,
) -> ft.Button:
    """The primary POS checkout action — large and unmistakable."""
    display_label = f"{label}  {PESO}{amount:,.2f}" if amount is not None else label
    return LargeButton(theme, display_label, icon=ft.Icons.PAYMENTS, on_click=on_click, disabled=disabled, primary=True)

"""The right-hand cart/checkout panel for the POS screen: toolbar,
itemized cart lines, charges & discounts, VAT totals, and the payment
method grid.
"""
from __future__ import annotations

from typing import Callable, Mapping, Optional, Sequence

import flet as ft

from prisqo_ui.theme import Theme
from prisqo_ui.components.pos.pos import LargeButton
from prisqo_ui.components.buttons.buttons import AppIconButton
from prisqo_ui.components.liquid._liquid_core import LiquidPressable

PESO = "\u20b1"

# Shared column widths for the cart table (header + line items must match
# exactly, column for column, including the trailing remove-button column).
_COL_PRICE = 60
_COL_QTY = 84
_COL_DISC = 40
_COL_TOTAL = 68
_COL_REMOVE = 36
_COL_SPACING = 8


def KeyBadge(theme: Theme, key: str) -> ft.Container:
    """A small outlined key-shortcut hint, e.g. 'F8'."""
    return ft.Container(
        content=ft.Text(key, style=theme.typography.caption(theme.text_muted)),
        border=ft.Border.all(1, theme.border),
        border_radius=theme.radius.SM,
        padding=ft.Padding.symmetric(horizontal=6, vertical=2),
    )


def CartToolbar(
    theme: Theme,
    on_hold: Optional[Callable] = None,
    on_recall: Optional[Callable] = None,
    on_clear: Optional[Callable] = None,
) -> ft.Container:
    """The Hold / Recall / Clear Cart row above the cart list."""

    def _action(label: str, icon: str, key: Optional[str], color: str, on_click: Optional[Callable]) -> ft.Container:
        controls = [
            ft.Icon(icon, size=16, color=color),
            ft.Text(label, style=theme.typography.button(color)),
        ]
        if key:
            controls.append(KeyBadge(theme, key))
        return ft.Container(
            content=ft.Row(controls=controls, spacing=8, tight=True, alignment=ft.MainAxisAlignment.CENTER),
            padding=ft.Padding.symmetric(vertical=10),
            ink=True,
            on_click=on_click,
            expand=True,
            border_radius=theme.radius.MD,
        )

    return ft.Container(
        content=ft.Row(
            controls=[
                _action("Hold", ft.Icons.PAUSE_CIRCLE_OUTLINE, "F8", theme.text_secondary, on_hold),
                ft.VerticalDivider(width=1, color=theme.divider),
                _action("Recall", ft.Icons.REFRESH, "F9", theme.text_secondary, on_recall),
                ft.VerticalDivider(width=1, color=theme.divider),
                _action("Clear Cart", ft.Icons.DELETE_OUTLINE, None, theme.danger, on_clear),
            ],
            spacing=0,
        ),
        border=ft.Border.all(1, theme.border),
        border_radius=theme.radius.LG,
        height=44,
    )


def CompactQuantityControl(
    theme: Theme,
    quantity: int = 1,
    min_quantity: int = 1,
    max_quantity: int = 9999,
    on_change: Optional[Callable[[int], None]] = None,
) -> ft.Row:
    """A [-] qty [+] stepper sized to fit inside a cart table cell — the
    Qty column of `CartLineItem` (unlike `QuantityControl`, which is
    sized for full-size POS touch targets elsewhere on the screen)."""
    qty_text = ft.Text(str(quantity), style=ft.TextStyle(size=13, weight=ft.FontWeight.W_600, color=theme.text_primary))
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
            content=ft.Icon(icon, size=13, color=theme.primary),
            width=22,
            height=22,
            bgcolor=theme.primary_light,
            border_radius=theme.radius.SM,
            alignment=ft.Alignment(0, 0),
            ink=True,
            on_click=_update(delta),
        )

    return ft.Row(
        controls=[
            _btn(ft.Icons.REMOVE, -1),
            ft.Container(content=qty_text, width=20, alignment=ft.Alignment(0, 0)),
            _btn(ft.Icons.ADD, 1),
        ],
        spacing=4,
        tight=True,
        alignment=ft.MainAxisAlignment.CENTER,
    )


def CartTableHeader(theme: Theme) -> ft.Row:
    """Column labels above the cart line items — six columns, matching
    `CartLineItem` width-for-width: Item / Price / Qty / Disc. / Total /
    (remove-button column)."""
    label = lambda t, align=ft.TextAlign.LEFT: ft.Text(t, style=theme.typography.label(theme.text_muted), text_align=align)
    return ft.Row(
        controls=[
            ft.Container(content=label("ITEM"), expand=True),
            ft.Container(content=label("PRICE", ft.TextAlign.RIGHT), width=_COL_PRICE),
            ft.Container(content=label("QTY", ft.TextAlign.CENTER), width=_COL_QTY, alignment=ft.Alignment(0, 0)),
            ft.Container(content=label("DISC.", ft.TextAlign.RIGHT), width=_COL_DISC),
            ft.Container(content=label("TOTAL", ft.TextAlign.RIGHT), width=_COL_TOTAL),
            ft.Container(width=_COL_REMOVE),
        ],
        spacing=_COL_SPACING,
    )


def CartLineItem(
    theme: Theme,
    name: str,
    unit_price: float,
    quantity: int,
    line_total: float,
    discount_pct: float = 0.0,
    vat_label: str = "VAT Excl.",
    currency_symbol: str = PESO,
    on_quantity_change: Optional[Callable[[int], None]] = None,
    on_remove: Optional[Callable] = None,
) -> ft.Container:
    """A single line in the cart: name + VAT tag, unit price, qty stepper,
    discount %, line total, remove — six columns aligned to
    `CartTableHeader`."""
    return ft.Container(
        content=ft.Row(
            controls=[
                ft.Column(
                    controls=[
                        ft.Text(name, style=theme.typography.body(theme.text_primary), max_lines=2),
                        ft.Text(vat_label, style=theme.typography.caption(theme.success)),
                    ],
                    spacing=1,
                    tight=True,
                    expand=True,
                ),
                ft.Container(
                    content=ft.Text(
                        f"{currency_symbol}{unit_price:,.2f}",
                        style=theme.typography.body_small(theme.text_secondary),
                        text_align=ft.TextAlign.RIGHT,
                    ),
                    width=_COL_PRICE,
                ),
                ft.Container(
                    content=CompactQuantityControl(theme, quantity=quantity, on_change=on_quantity_change),
                    width=_COL_QTY,
                    alignment=ft.Alignment(0, 0),
                ),
                ft.Container(
                    content=ft.Text(
                        f"{discount_pct:.0f}%" if discount_pct else "0%",
                        style=theme.typography.body_small(theme.success if discount_pct else theme.text_muted),
                        text_align=ft.TextAlign.RIGHT,
                    ),
                    width=_COL_DISC,
                ),
                ft.Container(
                    content=ft.Text(
                        f"{currency_symbol}{line_total:,.2f}",
                        style=theme.typography.card_title(theme.text_primary),
                        text_align=ft.TextAlign.RIGHT,
                    ),
                    width=_COL_TOTAL,
                ),
                ft.Container(
                    content=AppIconButton(theme, ft.Icons.CLOSE, "Remove item", danger=True, on_click=on_remove),
                    width=_COL_REMOVE,
                    alignment=ft.Alignment(1, 0),
                ),
            ],
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=_COL_SPACING,
        ),
        padding=ft.Padding.symmetric(vertical=theme.spacing.SM),
        border=ft.Border(bottom=ft.BorderSide(1, theme.divider)),
    )


_ADJ_ROW_SPACING = 4  # tighter than _COL_SPACING (used by cart line items) on purpose


def _AdjustmentRemoveButton(theme: Theme, tooltip: str, on_click: Optional[Callable] = None) -> ft.GestureDetector:
    """Compact 20x20 remove (x) control for charge/discount line items.

    AppIconButton is a fixed 36x36 touch target — fine for the main cart
    rows, but it forces every Charges/Discounts row to be at least 36px
    tall no matter how tight the surrounding Column spacing is. This is
    a smaller version scoped to AdjustmentRow so those lists can sit
    genuinely close together.
    """
    return LiquidPressable(
        theme,
        content=ft.Icon(ft.Icons.CLOSE, size=13, color=theme.danger),
        bgcolor=ft.Colors.TRANSPARENT,
        hover_bgcolor=theme.surface_variant,
        on_click=on_click,
        width=20,
        height=20,
        tooltip=tooltip,
        radius=theme.radius.SM,
    )


def AdjustmentRow(theme: Theme, label: str, amount: float, tone_color: str, on_remove: Optional[Callable] = None, currency_symbol: str = PESO) -> ft.Row:
    """A single itemized row inside a Charges/Discounts section — label,
    amount, and a remove (x) button, always present after the amount."""
    sign = "-" if amount < 0 else ""
    return ft.Row(
        controls=[
            ft.Text(label, style=theme.typography.body_small(theme.text_secondary), expand=True),
            ft.Text(f"{sign}{currency_symbol}{abs(amount):,.2f}", style=theme.typography.body_small(tone_color)),
            _AdjustmentRemoveButton(theme, f"Remove {label}", on_click=on_remove),
        ],
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        spacing=_ADJ_ROW_SPACING,
    )


def AdjustmentSection(
    theme: Theme,
    title: str,
    icon: str,
    tone: str,
    total: float,
    items: Sequence[Mapping],
    add_label: str,
    currency_symbol: str = PESO,
    on_add: Optional[Callable] = None,
    expanded: bool = True,
) -> ft.Container:
    """Generic collapsible-looking section used for both 'Charges' (tone=
    'warning') and 'Discounts Applied' (tone='success').

    items: sequence of {"label": str, "amount": float, "on_remove": Callable?}
    """
    color = theme.warning if tone == "warning" else theme.success
    bg = theme.warning_bg if tone == "warning" else theme.success_bg
    sign = "-" if tone == "success" else ""

    item_rows: list[ft.Control] = []
    if expanded:
        if items:
            item_rows.extend(
                AdjustmentRow(theme, it["label"], it["amount"], theme.text_primary, on_remove=it.get("on_remove"), currency_symbol=currency_symbol)
                for it in items
            )
        else:
            item_rows.append(ft.Text("None added yet", style=theme.typography.caption(theme.text_muted)))

    add_row = ft.Container(
        content=ft.Row(
            controls=[ft.Icon(ft.Icons.ADD, size=14, color=theme.primary), ft.Text(add_label, style=theme.typography.body_small(theme.primary))],
            spacing=4,
        ),
        on_click=on_add,
        ink=True,
        border_radius=theme.radius.SM,
    )

    header = ft.Row(
        controls=[
            ft.Row(
                controls=[ft.Icon(icon, size=16, color=color), ft.Text(title, style=theme.typography.card_title(color))],
                spacing=8,
            ),
            ft.Text(f"{sign}{currency_symbol}{abs(total):,.2f}", style=theme.typography.card_title(color)),
        ],
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
    )

    # item_rows get their own tight column (2px) so the individual charge/
    # discount lines sit close together, independent of the looser gap
    # between the header and the list, and between the list and "Add".
    body: list[ft.Control] = []
    if expanded:
        body.append(ft.Column(controls=item_rows, spacing=2, tight=True))
        body.append(add_row)

    return ft.Container(
        content=ft.Column(controls=[header, *body], spacing=theme.spacing.XS, tight=True),
        bgcolor=bg,
        border_radius=theme.radius.MD,
        padding=theme.spacing.SM,
    )


def POSTotalsBreakdown(
    theme: Theme,
    vatable_sales: float,
    vat_amount: float,
    vat_exempt_sales: float,
    grand_total: float,
    currency_symbol: str = PESO,
) -> ft.Container:
    """VATable Sales / VAT Amount / VAT Exempt Sales, then a bold TOTAL —
    the tax-compliant breakdown shown at the bottom of a PH POS receipt."""

    def _row(label: str, value: float) -> ft.Row:
        return ft.Row(
            controls=[
                ft.Text(label, style=theme.typography.body_small(theme.text_secondary)),
                ft.Text(f"{currency_symbol}{value:,.2f}", style=theme.typography.body_small(theme.text_primary)),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        )

    return ft.Container(
        content=ft.Column(
            controls=[
                _row("VATable Sales", vatable_sales),
                _row("VAT Amount", vat_amount),
                _row("VAT Exempt Sales", vat_exempt_sales),
                ft.Divider(height=1, color=theme.divider),
                ft.Row(
                    controls=[
                        ft.Text("TOTAL", style=theme.typography.section_title(theme.text_primary)),
                        ft.Text(f"{currency_symbol}{grand_total:,.2f}", style=theme.typography.kpi(theme.primary)),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                ),
            ],
            spacing=theme.spacing.SM,
            tight=True,
        ),
    )


def PaymentMethodGrid(
    theme: Theme,
    methods: Sequence[Mapping],
    on_select: Optional[Callable[[str], None]] = None,
    columns: int = 2,
) -> ft.Row:
    """A grid of large tender buttons — Cash, GCash, PayMaya, Credit Card,
    Debit Card, Other. methods: {"key", "label", "icon", "primary"?}"""
    buttons = [
        LargeButton(
            theme,
            m["label"],
            icon=m.get("icon"),
            primary=m.get("primary", False),
            on_click=(lambda e, k=m["key"]: on_select(k)) if on_select else None,
            width=None,
        )
        for m in methods
    ]
    rows = [
        ft.Row(controls=buttons[i : i + columns], spacing=theme.spacing.SM)
        for i in range(0, len(buttons), columns)
    ]
    for row in rows:
        for btn in row.controls:
            btn.expand = True
    return ft.Column(controls=rows, spacing=theme.spacing.SM, tight=True)


def BottomActionBar(theme: Theme, actions: Sequence[Mapping]) -> ft.Row:
    """The Discount / Charges / Hold / Recall / More strip under the item
    grid. actions: {"label", "icon", "key"?, "on_click"?}"""

    def _tile(a: Mapping) -> ft.Container:
        content_controls = [
            ft.Icon(a["icon"], size=18, color=theme.text_secondary),
            ft.Text(a["label"], style=theme.typography.body_small(theme.text_primary)),
        ]
        col = [ft.Row(controls=content_controls, spacing=6, alignment=ft.MainAxisAlignment.CENTER)]
        if a.get("key"):
            col.append(ft.Row(controls=[KeyBadge(theme, a["key"])], alignment=ft.MainAxisAlignment.CENTER))
        return ft.Container(
            content=ft.Column(controls=col, spacing=4, horizontal_alignment=ft.CrossAxisAlignment.CENTER, tight=True),
            border=ft.Border.all(1, theme.border),
            border_radius=theme.radius.MD,
            padding=theme.spacing.SM,
            bgcolor=theme.surface,
            ink=True,
            on_click=a.get("on_click"),
            expand=True,
        )

    return ft.Row(controls=[_tile(a) for a in actions], spacing=theme.spacing.SM)


def CartPanel(
    theme: Theme,
    cart_items: Sequence[Mapping],
    charges: Sequence[Mapping] = (),
    discounts: Sequence[Mapping] = (),
    vatable_sales: float = 0.0,
    vat_amount: float = 0.0,
    vat_exempt_sales: float = 0.0,
    grand_total: float = 0.0,
    payment_methods: Sequence[Mapping] = (),
    transaction_title: Optional[str] = None,
    on_hold: Optional[Callable] = None,
    on_recall: Optional[Callable] = None,
    on_clear: Optional[Callable] = None,
    on_add_charge: Optional[Callable] = None,
    on_add_discount: Optional[Callable] = None,
    on_add_note: Optional[Callable] = None,
    on_pay: Optional[Callable[[str], None]] = None,
    width: Optional[float] = 440,
) -> ft.Container:
    """The full right-hand checkout panel, composed from the pieces above.

    Responsive by default: pass `width=None` (instead of a fixed pixel
    width) to have the panel flex-fill whatever space its parent gives
    it — the right choice on tablet, where the panel sits in a `Row`
    alongside the catalog and screen width varies. The cart's own line-
    item list always flex-grows to fill the space between the header and
    the totals/payment section below, rather than scrolling inside a
    fixed pixel height, so it adapts to the panel's actual height too.
    Charges and Discounts sections are always shown (even with zero
    items) since carts are empty far more often than not — each just
    collapses to its header + 'Add' prompt when there's nothing in it.
    """
    charges_total = sum(c["amount"] for c in charges)
    discounts_total = sum(d["amount"] for d in discounts)

    lines = [
        CartLineItem(
            theme,
            name=it["name"],
            unit_price=it["unit_price"],
            quantity=it["quantity"],
            line_total=it["line_total"],
            discount_pct=it.get("discount_pct", 0.0),
            on_quantity_change=it.get("on_quantity_change"),
            on_remove=it.get("on_remove"),
        )
        for it in cart_items
    ]

    top_controls: list[ft.Control] = [CartToolbar(theme, on_hold=on_hold, on_recall=on_recall, on_clear=on_clear)]
    if transaction_title:
        top_controls.append(ft.Text(transaction_title, style=theme.typography.card_title(theme.text_primary)))
    top_controls.append(CartTableHeader(theme))
    top_section = ft.Column(controls=top_controls, spacing=theme.spacing.MD, tight=True)

    items_section: ft.Control = (
        ft.Column(controls=lines, spacing=0, scroll=ft.ScrollMode.AUTO, expand=True)
        if lines
        else ft.Container(
            content=ft.Text("Cart is empty", style=theme.typography.body_small(theme.text_muted)),
            alignment=ft.Alignment(0, 0),
            expand=True,
        )
    )

    bottom_controls: list[ft.Control] = [
        ft.Container(
            content=ft.Row(
                controls=[ft.Icon(ft.Icons.ADD, size=14, color=theme.primary), ft.Text("Add Note", style=theme.typography.body_small(theme.primary))],
                spacing=4,
                tight=True,
            ),
            on_click=on_add_note,
            ink=True,
            border_radius=theme.radius.SM,
        ),
        ft.Column(
            controls=[
                AdjustmentSection(theme, "Charges", ft.Icons.STAR_OUTLINE, "warning", charges_total, charges, "Add Charge", on_add=on_add_charge),
                AdjustmentSection(
                    theme, "Discounts Applied", ft.Icons.LOCAL_OFFER_OUTLINED, "success", discounts_total, discounts, "Add Discount", on_add=on_add_discount
                ),
            ],
            spacing=theme.spacing.XS,
            tight=True,
        ),
        POSTotalsBreakdown(theme, vatable_sales, vat_amount, vat_exempt_sales, grand_total),
        PaymentMethodGrid(theme, payment_methods, on_select=on_pay),
    ]
    bottom_section = ft.Column(controls=bottom_controls, spacing=theme.spacing.MD, tight=True)

    return ft.Container(
        content=ft.Column(controls=[top_section, items_section, bottom_section], spacing=theme.spacing.MD, expand=True),
        bgcolor=theme.background,
        border=ft.Border(left=ft.BorderSide(1, theme.border)),
        padding=theme.spacing.LG,
        width=width,
        expand=width is None,
    )

"""Full POS screen — assembles the sidebar, header, item catalog (image
and no-image variants), and the checkout panel into the complete
touchscreen layout from the mockups.
"""
from __future__ import annotations

import flet as ft

from prisqo_ui.theme import Theme
from prisqo_ui.components.layout import Sidebar
from prisqo_ui.components.pos import (
    ItemGrid,
    CategoryFilterBar,
    BottomActionBar,
    CartPanel,
    POSHeader,
)

ITEMS = [
    {"name": "Paracetamol 500mg Tablet", "brand": "Generic Pharma", "price": 60.00, "stock": 120, "rx": False},
    {"name": "Amoxicillin 500mg Capsule", "brand": "Rx Pharma", "price": 80.00, "stock": 85, "rx": True},
    {"name": "Loratadine 10mg Tablet", "brand": "Generic Pharma", "price": 45.00, "stock": 200, "rx": False},
    {"name": "Cetirizine 10mg Tablet", "brand": "Rx Pharma", "price": 50.00, "stock": 150, "rx": True},
    {"name": "Ascorbic Acid 500mg Tablet", "brand": "Generic Pharma", "price": 35.00, "stock": 300, "rx": False},
    {"name": "Omeprazole 20mg Capsule", "brand": "Rx Pharma", "price": 90.00, "stock": 60, "rx": True},
    {"name": "Salbutamol Inhaler 100mcg", "brand": "Generic Pharma", "price": 120.00, "stock": 40, "sku_icon": ft.Icons.AIR},
    {"name": "Ibuprofen 400mg Tablet", "brand": "Generic Pharma", "price": 55.00, "stock": 180},
    {"name": "Multivitamins Tablet", "brand": "Generic Pharma", "price": 75.00, "stock": 90},
    {"name": "Zinc Sulfate 20mg Tablet", "brand": "Generic Pharma", "price": 25.00, "stock": 250},
    {"name": "Vitamin C 500mg Tablet", "brand": "Generic Pharma", "price": 40.00, "stock": 210},
    {"name": "Azithromycin 500mg Tablet", "brand": "Rx Pharma", "price": 110.00, "stock": 35, "rx": True},
]

CATEGORIES = [
    {"key": "all", "label": "All Items"},
    {"key": "vaccine", "label": "Vaccine", "icon": ft.Icons.VACCINES_OUTLINED},
    {"key": "medicine", "label": "Medicine", "icon": ft.Icons.MEDICATION_OUTLINED},
    {"key": "supplies", "label": "Medical Supplies", "icon": ft.Icons.MEDICAL_SERVICES_OUTLINED},
    {"key": "personal_care", "label": "Personal Care", "icon": ft.Icons.SPA_OUTLINED},
    {"key": "others", "label": "Others"},
]

CART_ITEMS = [
    {"name": "Paracetamol 500mg Tablet", "unit_price": 60.00, "quantity": 2, "discount_pct": 20, "line_total": 96.00},
    {"name": "Amoxicillin 500mg Capsule", "unit_price": 80.00, "quantity": 1, "discount_pct": 0, "line_total": 80.00},
    {"name": "Loratadine 10mg Tablet", "unit_price": 45.00, "quantity": 1, "discount_pct": 0, "line_total": 45.00},
]

CHARGES = [
    {"label": "Professional Fee", "amount": 500.00},
    {"label": "Delivery Charge", "amount": 50.00},
]

DISCOUNTS = [
    {"label": "Senior Citizen Discount (20%)", "amount": 96.00},
    {"label": "Employee Discount (10%)", "amount": 12.00},
]

PAYMENT_METHODS = [
    {"key": "cash", "label": "Cash", "icon": ft.Icons.PAYMENTS_OUTLINED, "primary": True},
    {"key": "gcash", "label": "GCash", "icon": ft.Icons.QR_CODE, "primary": True},
    {"key": "paymaya", "label": "PayMaya", "icon": ft.Icons.ACCOUNT_BALANCE_WALLET_OUTLINED, "primary": True},
    {"key": "credit", "label": "Credit Card", "icon": ft.Icons.CREDIT_CARD, "primary": True},
    {"key": "debit", "label": "Debit Card", "icon": ft.Icons.CREDIT_CARD_OUTLINED, "primary": True},
    {"key": "other", "label": "Other", "icon": ft.Icons.MORE_HORIZ, "primary": True},
]

SIDEBAR_GROUPS = [
    {
        "items": [
            {"key": "dashboard", "label": "Dashboard", "icon": ft.Icons.DASHBOARD_OUTLINED},
            {"key": "pos", "label": "POS", "icon": ft.Icons.POINT_OF_SALE},
            {"key": "inventory", "label": "Inventory", "icon": ft.Icons.INVENTORY_2_OUTLINED},
            {"key": "sales", "label": "Sales", "icon": ft.Icons.BAR_CHART},
            {"key": "customers", "label": "Customers", "icon": ft.Icons.PEOPLE_OUTLINE},
            {"key": "reports", "label": "Reports", "icon": ft.Icons.DESCRIPTION_OUTLINED},
        ]
    }
]

BOTTOM_ACTIONS = [
    {"label": "Discount", "icon": ft.Icons.SELL_OUTLINED, "key": "F6"},
    {"label": "Charges", "icon": ft.Icons.RECEIPT_LONG_OUTLINED, "key": "F7"},
    {"label": "More", "icon": ft.Icons.MORE_HORIZ, "key": None},
]


def _pos_screen(theme: Theme, show_image: bool) -> ft.Control:
    sidebar = Sidebar(
        theme,
        SIDEBAR_GROUPS,
        active_key="pos",
        header=ft.Row(
            controls=[
                ft.Container(content=ft.Icon(ft.Icons.HEXAGON, color=theme.primary, size=20), bgcolor="#FFFFFF", padding=6, border_radius=theme.radius.MD),
                ft.Text("PRISQO POS", style=theme.typography.card_title("#FFFFFF")),
            ],
            spacing=theme.spacing.SM,
        ),
        width_expanded=220,
    )

    header = POSHeader(
        theme,
        store_name="Store 01",
        store_branch="Main Branch",
        terminal_name="Terminal 03",
        terminal_type="Front Counter",
        cashier_name="Jobert Simbre",
        cashier_role="Cashier",
    )

    catalog = ft.Container(
        content=ft.Column(
            controls=[
                CategoryFilterBar(theme, CATEGORIES, selected_key="all"),
                ItemGrid(theme, ITEMS, show_image=show_image, card_width=172),
                BottomActionBar(theme, BOTTOM_ACTIONS),
            ],
            spacing=theme.spacing.MD,
            expand=True,
        ),
        padding=theme.spacing.LG,
        expand=3,
    )

    cart = CartPanel(
        theme,
        cart_items=CART_ITEMS,
        charges=CHARGES,
        discounts=DISCOUNTS,
        vatable_sales=107.14,
        vat_amount=12.86,
        vat_exempt_sales=171.42,
        grand_total=733.42,
        payment_methods=PAYMENT_METHODS,
        width=None,
    )
    cart.expand = 2

    return ft.Container(
        content=ft.Row(
            controls=[
                sidebar,
                ft.Column(
                    controls=[header, ft.Row(controls=[catalog, cart], spacing=0, expand=True)],
                    spacing=0,
                    expand=True,
                ),
            ],
            spacing=0,
            expand=True,
        ),
        bgcolor=theme.background,
        border=ft.Border.all(1, theme.border),
        border_radius=theme.radius.LG,
        height=980,
        clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
    )


def build(theme: Theme, page: ft.Page) -> ft.Control:
    state = {"show_image": True}
    frame = ft.Container(content=_pos_screen(theme, True), expand=True)

    def _set_variant(show_image: bool):
        def handler(e: ft.ControlEvent) -> None:
            state["show_image"] = show_image
            frame.content = _pos_screen(theme, show_image)
            frame.update()
            _sync_toggle()

        return handler

    def _toggle_btn(label: str, show_image: bool) -> ft.Container:
        active = state["show_image"] == show_image
        return ft.Container(
            content=ft.Text(label, style=theme.typography.button("#FFFFFF" if active else theme.text_secondary)),
            bgcolor=theme.primary if active else theme.surface_variant,
            padding=ft.Padding.symmetric(horizontal=14, vertical=8),
            border_radius=theme.radius.MD,
            ink=True,
            on_click=_set_variant(show_image),
            data=show_image,
        )

    toggle_row = ft.Row(controls=[_toggle_btn("With item image", True), _toggle_btn("Without item image", False)], spacing=8)

    def _sync_toggle() -> None:
        toggle_row.controls = [_toggle_btn("With item image", True), _toggle_btn("Without item image", False)]
        toggle_row.update()

    return ft.Column(
        controls=[
            ft.Row(
                controls=[ft.Text("Catalog variant:", style=theme.typography.body_small(theme.text_muted)), toggle_row],
                spacing=12,
            ),
            frame,
        ],
        spacing=theme.spacing.MD,
        expand=True,
    )

"""POS product-grid components — the item catalog tiles a cashier taps to
add to the cart, and the category filter bar above them.

`ItemCard` has a single `show_image` switch rather than being two
separate components: the two mockups (with photos vs. text-only) are the
*same* card, just with the image block toggled off for catalogs that
don't have product photography (e.g. a pharmacy that only photographs
some SKUs). Toggle it once for the whole `ItemGrid` via `show_image`.
"""
from __future__ import annotations

from typing import Callable, Mapping, Optional, Sequence

import flet as ft

from prisqo_ui.theme import Theme

PESO = "\u20b1"


def StockIndicator(theme: Theme, stock: int, low_stock_threshold: int = 15) -> ft.Row:
    """Small colored dot + 'Stock: N' label — in/low/out of stock tone."""
    if stock <= 0:
        color = theme.danger
        label = "Out of stock"
    elif stock <= low_stock_threshold:
        color = theme.warning
        label = f"Stock: {stock}"
    else:
        color = theme.success
        label = f"Stock: {stock}"
    return ft.Row(
        controls=[
            ft.Container(width=7, height=7, bgcolor=color, border_radius=theme.radius.ROUND),
            ft.Text(label, style=theme.typography.caption(theme.text_muted)),
        ],
        spacing=6,
        tight=True,
    )


def ItemCard(
    theme: Theme,
    name: str,
    brand: str,
    price: float,
    stock: int,
    image_url: Optional[str] = None,
    sku_icon: str = ft.Icons.MEDICATION_OUTLINED,
    rx: bool = False,
    show_image: bool = True,
    currency_symbol: str = PESO,
    on_click: Optional[Callable] = None,
    width: Optional[float] = 168,
) -> ft.Container:
    """A single product tile for the POS grid.

    Set `show_image=False` for the text-only catalog variant (no product
    photography) — it's the same card, just without the image block and
    with a little more breathing room for the name.
    """
    disabled = stock <= 0
    brand_color = theme.info if rx else theme.text_muted

    children: list[ft.Control] = []

    if show_image:
        image_block: ft.Control
        if image_url:
            image_block = ft.Image(src=image_url, fit=ft.ImageFit.CONTAIN, width=float("inf"), height=88)
        else:
            image_block = ft.Icon(sku_icon, size=32, color=theme.text_muted)
        children.append(
            ft.Container(
                content=image_block,
                bgcolor=theme.surface_variant,
                border_radius=theme.radius.MD,
                height=96,
                alignment=ft.Alignment(0, 0),
            )
        )

    children.extend(
        [
            ft.Column(
                controls=[
                    ft.Text(
                        name,
                        style=theme.typography.card_title(theme.text_muted if disabled else theme.text_primary),
                        max_lines=2,
                        overflow=ft.TextOverflow.ELLIPSIS,
                    ),
                    ft.Text(brand, style=theme.typography.caption(brand_color)),
                ],
                spacing=2,
                tight=True,
            ),
            ft.Text(
                f"{currency_symbol}{price:,.2f}",
                style=theme.typography.section_title(theme.text_muted if disabled else theme.text_primary),
            ),
            StockIndicator(theme, stock),
        ]
    )

    return ft.Container(
        content=ft.Column(controls=children, spacing=theme.spacing.SM, tight=True),
        width=width,
        bgcolor=theme.surface,
        border=ft.Border.all(1, theme.border),
        border_radius=theme.radius.LG,
        padding=theme.spacing.MD,
        ink=not disabled,
        on_click=None if disabled else on_click,
        opacity=0.55 if disabled else 1,
        animate=ft.Animation(120, ft.AnimationCurve.EASE_OUT),
        shadow=theme.shadows.card,
    )


def ItemGrid(
    theme: Theme,
    items: Sequence[Mapping],
    show_image: bool = True,
    card_width: float = 168,
    on_item_click: Optional[Callable[[Mapping], None]] = None,
    scroll: bool = True,
) -> ft.Control:
    """Wraps `ItemCard`s into a responsive, wrapping grid.

    items: sequence of {name, brand, price, stock, image_url?, sku_icon?, rx?}

    `scroll=True` (default) makes the grid vertically scrollable and lets
    it fill available height — the right behavior when it sits below a
    category bar and above a fixed bottom action bar, as in the POS
    screen. Pass `scroll=False` if the caller already provides its own
    scrolling container.
    """
    cards = [
        ItemCard(
            theme,
            name=it["name"],
            brand=it.get("brand", ""),
            price=it["price"],
            stock=it.get("stock", 0),
            image_url=it.get("image_url"),
            sku_icon=it.get("sku_icon", ft.Icons.MEDICATION_OUTLINED),
            rx=it.get("rx", False),
            show_image=show_image,
            width=card_width,
            on_click=(lambda e, it=it: on_item_click(it)) if on_item_click else None,
        )
        for it in items
    ]
    wrap_row = ft.Row(controls=cards, wrap=True, spacing=theme.spacing.MD, run_spacing=theme.spacing.MD)
    if not scroll:
        return wrap_row
    return ft.Column(controls=[wrap_row], scroll=ft.ScrollMode.AUTO, expand=True)


def CategoryChip(
    theme: Theme,
    label: str,
    icon: Optional[str] = None,
    selected: bool = False,
    on_click: Optional[Callable] = None,
) -> ft.Container:
    """A single pill in the category filter bar."""
    color = theme.text_on_primary if selected else theme.text_secondary
    row_controls = []
    if icon:
        row_controls.append(ft.Icon(icon, size=16, color=color))
    row_controls.append(ft.Text(label, style=theme.typography.button(color)))
    return ft.Container(
        content=ft.Row(controls=row_controls, spacing=6, tight=True),
        bgcolor=theme.primary if selected else theme.surface,
        border=ft.Border.all(1, theme.primary if selected else theme.border),
        border_radius=theme.radius.MD,
        padding=ft.Padding.symmetric(horizontal=14, vertical=10),
        ink=True,
        on_click=on_click,
        animate=ft.Animation(100, ft.AnimationCurve.EASE_OUT),
    )


def CategoryFilterBar(
    theme: Theme,
    categories: Sequence[Mapping],
    selected_key: Optional[str] = None,
    on_change: Optional[Callable[[str], None]] = None,
    show_more: bool = True,
) -> ft.Row:
    """categories: sequence of {"key": str, "label": str, "icon": Optional[str]}"""
    chips = [
        CategoryChip(
            theme,
            label=c["label"],
            icon=c.get("icon"),
            selected=c["key"] == selected_key,
            on_click=(lambda e, k=c["key"]: on_change(k)) if on_change else None,
        )
        for c in categories
    ]
    if show_more:
        chips.append(CategoryChip(theme, "\u2022\u2022\u2022", selected=False, on_click=None))
    return ft.Row(controls=chips, spacing=theme.spacing.SM, wrap=True, run_spacing=theme.spacing.SM)

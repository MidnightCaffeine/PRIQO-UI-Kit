"""Button components -- Bootstrap-style base component + variant modifiers.

Bootstrap doesn't ship a separate hand-written CSS block for `.btn-primary`,
`.btn-success`, `.btn-danger`, etc. -- it has ONE `.btn` base class plus a
`button-variant()` mixin that stamps out each `.btn-{variant}` from the
shared `$theme-colors` map. `Button()` below is that pattern in Flet:
one base component that reads its colors from
`core.variants.resolve_variant()` and its sizing from
`core.variants.resolve_size()`.

`PrimaryButton`, `SecondaryButton`, `DangerButton`, etc. still exist and
still have the exact same call signature as before -- they are now just
`Button(variant="...")` one-liners, the same way Bootstrap's `.btn-primary`
is "just" `.btn` plus a modifier class, not a separately maintained
component. Every existing call site in this library (dialogs, tables,
POS, forms, ...) keeps working unmodified.

Every button is still built on `LiquidPressable`: it squishes down on
press and bounces back with an elastic overshoot on release.
"""
from __future__ import annotations

from typing import Callable, Optional

import flet as ft

from prisqo_ui.theme import Theme
from prisqo_ui.components.liquid._liquid_core import LiquidPressable
from prisqo_ui.components.core.variants import (
    SizeName,
    VariantName,
    resolve_size,
    resolve_variant,
)


def _content_row(theme: Theme, text: Optional[str], icon: Optional[str], color: str, loading: bool, icon_size: int, spacing: int) -> ft.Control:
    if loading:
        return ft.Row(
            controls=[
                ft.ProgressRing(width=16, height=16, stroke_width=2, color=color),
                ft.Text(text or "Loading...", style=theme.typography.button(color)),
            ],
            spacing=spacing,
            alignment=ft.MainAxisAlignment.CENTER,
            tight=True,
        )
    row_children = []
    if icon:
        row_children.append(ft.Icon(icon, size=icon_size, color=color))
    row_children.append(ft.Text(text, style=theme.typography.button(color)))
    return ft.Row(controls=row_children, spacing=spacing, alignment=ft.MainAxisAlignment.CENTER, tight=True)


def Button(
    theme: Theme,
    text: str,
    variant: VariantName = "primary",
    size: SizeName = "md",
    outline: bool = False,
    ghost: bool = False,
    icon: Optional[str] = None,
    on_click: Optional[Callable] = None,
    disabled: bool = False,
    loading: bool = False,
    tooltip: Optional[str] = None,
    width: Optional[float] = None,
    height: Optional[float] = None,
) -> ft.GestureDetector:
    """The base liquid button -- every other button in this module is a
    thin `variant=`/`size=` preset of this one call, mirroring Bootstrap's
    `.btn .btn-{variant} .btn-{size}` class composition.

    - `outline=True`: transparent fill, colored border + text (like
      `.btn-outline-{variant}`).
    - `ghost=True`: transparent fill, no border, muted-to-variant text on
      hover (like a borderless `.btn-link`/toolbar button). `ghost` wins
      if both `outline` and `ghost` are set.
    """
    colors = resolve_variant(theme, variant)
    spec = resolve_size(theme, size)
    is_disabled = disabled or loading
    h = height or spec.height
    padding = ft.Padding.symmetric(horizontal=spec.padding_h, vertical=spec.padding_v)

    if ghost:
        fg = theme.text_muted if is_disabled else colors.text
        content = _content_row(theme, text, icon, fg, loading, spec.icon_size, spec.padding_v // 2 or 6)
        return LiquidPressable(
            theme, content=content, bgcolor=ft.Colors.TRANSPARENT,
            hover_bgcolor=theme.surface_variant, on_click=None if is_disabled else on_click,
            disabled=is_disabled, width=width, height=h, tooltip=tooltip,
            radius=spec.radius, padding=padding,
        )

    if outline:
        fg = theme.text_muted if is_disabled else colors.text
        content = _content_row(theme, text, icon, fg, loading, spec.icon_size, spec.padding_v // 2 or 6)
        return LiquidPressable(
            theme, content=content, bgcolor=ft.Colors.TRANSPARENT,
            hover_bgcolor=colors.soft_bg, border=ft.Border.all(1, theme.border if is_disabled else colors.border),
            on_click=None if is_disabled else on_click, disabled=is_disabled, width=width, height=h,
            tooltip=tooltip, radius=spec.radius, padding=padding,
        )

    # Solid/filled -- the default, like `.btn-{variant}` with no modifier.
    fg = theme.text_muted if is_disabled else colors.on_solid
    content = _content_row(theme, text, icon, fg, loading, spec.icon_size, spec.padding_v // 2 or 6)
    return LiquidPressable(
        theme, content=content, bgcolor=colors.solid, hover_bgcolor=colors.solid_hover,
        on_click=None if is_disabled else on_click, disabled=is_disabled, width=width, height=h,
        tooltip=tooltip, radius=spec.radius, padding=padding,
    )


# -- Variant presets -----------------------------------------------------
# Each of these is intentionally a one-line call into `Button()`. They
# exist so existing/obvious call sites read naturally (`PrimaryButton(...)`)
# without every caller needing to know or pass `variant=`.

def PrimaryButton(
    theme: Theme, text: str, icon: Optional[str] = None, on_click: Optional[Callable] = None,
    disabled: bool = False, loading: bool = False, tooltip: Optional[str] = None,
    width: Optional[float] = None, height: Optional[float] = None, size: SizeName = "md",
) -> ft.GestureDetector:
    """The main call-to-action liquid button (Save, Submit, Create, ...)."""
    return Button(theme, text, variant="primary", size=size, icon=icon, on_click=on_click,
                  disabled=disabled, loading=loading, tooltip=tooltip, width=width, height=height)


def SecondaryButton(
    theme: Theme, text: str, icon: Optional[str] = None, on_click: Optional[Callable] = None,
    disabled: bool = False, loading: bool = False, tooltip: Optional[str] = None,
    width: Optional[float] = None, height: Optional[float] = None, size: SizeName = "md",
) -> ft.GestureDetector:
    """A lower-emphasis liquid button used alongside a PrimaryButton (e.g. Cancel)."""
    return Button(theme, text, variant="secondary", size=size, icon=icon, on_click=on_click,
                  disabled=disabled, loading=loading, tooltip=tooltip, width=width, height=height)


def OutlineButton(
    theme: Theme, text: str, icon: Optional[str] = None, on_click: Optional[Callable] = None,
    disabled: bool = False, tooltip: Optional[str] = None,
    width: Optional[float] = None, height: Optional[float] = None, size: SizeName = "md",
    variant: VariantName = "primary",
) -> ft.GestureDetector:
    """`.btn-outline-{variant}` -- defaults to primary, like before."""
    return Button(theme, text, variant=variant, size=size, outline=True, icon=icon, on_click=on_click,
                  disabled=disabled, tooltip=tooltip, width=width, height=height)


def GhostButton(
    theme: Theme, text: str, icon: Optional[str] = None, on_click: Optional[Callable] = None,
    disabled: bool = False, tooltip: Optional[str] = None,
    width: Optional[float] = None, height: Optional[float] = None, size: SizeName = "md",
) -> ft.GestureDetector:
    """A minimal, borderless, low-emphasis liquid button (table row actions, links)."""
    return Button(theme, text, variant="secondary", size=size, ghost=True, icon=icon, on_click=on_click,
                  disabled=disabled, tooltip=tooltip, width=width, height=height or 40)


def DangerButton(
    theme: Theme, text: str, icon: Optional[str] = None, on_click: Optional[Callable] = None,
    disabled: bool = False, loading: bool = False, tooltip: Optional[str] = None,
    width: Optional[float] = None, height: Optional[float] = None, size: SizeName = "md",
) -> ft.GestureDetector:
    """Destructive-action liquid button (Delete, Void, Cancel Order)."""
    return Button(theme, text, variant="danger", size=size, icon=icon, on_click=on_click,
                  disabled=disabled, loading=loading, tooltip=tooltip, width=width, height=height)


def SuccessButton(
    theme: Theme, text: str, icon: Optional[str] = None, on_click: Optional[Callable] = None,
    disabled: bool = False, loading: bool = False, tooltip: Optional[str] = None,
    width: Optional[float] = None, height: Optional[float] = None, size: SizeName = "md",
) -> ft.GestureDetector:
    """Confirmation/positive-action liquid button (Approve, Confirm, Mark Paid)."""
    return Button(theme, text, variant="success", size=size, icon=icon, on_click=on_click,
                  disabled=disabled, loading=loading, tooltip=tooltip, width=width, height=height)


def WarningButton(
    theme: Theme, text: str, icon: Optional[str] = None, on_click: Optional[Callable] = None,
    disabled: bool = False, loading: bool = False, tooltip: Optional[str] = None,
    width: Optional[float] = None, height: Optional[float] = None, size: SizeName = "md",
) -> ft.GestureDetector:
    """Caution liquid button (Void, Hold, Override)."""
    return Button(theme, text, variant="warning", size=size, icon=icon, on_click=on_click,
                  disabled=disabled, loading=loading, tooltip=tooltip, width=width, height=height)


def InfoButton(
    theme: Theme, text: str, icon: Optional[str] = None, on_click: Optional[Callable] = None,
    disabled: bool = False, loading: bool = False, tooltip: Optional[str] = None,
    width: Optional[float] = None, height: Optional[float] = None, size: SizeName = "md",
) -> ft.GestureDetector:
    """Informational liquid button (View Details, Learn More)."""
    return Button(theme, text, variant="info", size=size, icon=icon, on_click=on_click,
                  disabled=disabled, loading=loading, tooltip=tooltip, width=width, height=height)


def AppIconButton(
    theme: Theme,
    icon: str,
    tooltip: str,
    on_click: Optional[Callable] = None,
    disabled: bool = False,
    selected: bool = False,
    danger: bool = False,
) -> ft.GestureDetector:
    """Icon-only liquid button. `tooltip` is required for accessibility."""
    icon_color = theme.text_muted if disabled else (theme.danger if danger else (theme.primary if selected else theme.text_secondary))
    return LiquidPressable(
        theme,
        content=ft.Icon(icon, size=18, color=icon_color),
        bgcolor=theme.primary_light if selected else ft.Colors.TRANSPARENT,
        hover_bgcolor=theme.surface_variant,
        on_click=on_click,
        disabled=disabled,
        width=36,
        height=36,
        tooltip=tooltip,
        radius=theme.radius.MD,
    )


def LoadingButton(
    theme: Theme,
    text: str,
    loading: bool,
    on_click: Optional[Callable] = None,
    icon: Optional[str] = None,
    disabled: bool = False,
    width: Optional[float] = None,
    height: Optional[float] = None,
) -> ft.GestureDetector:
    """A PrimaryButton with a built-in loading spinner state."""
    return PrimaryButton(
        theme=theme,
        text=text,
        icon=icon,
        on_click=on_click,
        disabled=disabled,
        loading=loading,
        width=width,
        height=height,
    )

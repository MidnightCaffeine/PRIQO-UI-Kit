"""Utility helpers -- the Python equivalent of Bootstrap's utility classes
(`.mt-3`, `.p-2`, `.d-flex`, `.text-primary`, `.rounded-lg`, `.shadow`, ...).

Bootstrap lets you skip writing custom CSS for one-off spacing/color/layout
tweaks by composing small utility classes on any element. Flet has no
classes to compose, but the same idea works as small functions that return
plain values (ints, `ft.Padding`, colors, `ft.TextStyle`) you compose when
building a control -- or wrap with `Box()` for the fully declarative,
class-like version.

Spacing scale (mirrors Bootstrap's 0-5 spacer scale, mapped onto this
kit's `Spacing` tokens so it stays themeable):

    0   -> 0px            (theme.spacing has no "0" token, so this is literal)
    1   -> theme.spacing.XS   (4px)
    2   -> theme.spacing.SM   (8px)
    3   -> theme.spacing.MD   (12px)
    4   -> theme.spacing.LG   (16px)
    5   -> theme.spacing.XL   (24px)
    6   -> theme.spacing.XXL  (32px)

Usage:

    from prisqo_ui.components.core import helpers as u

    ft.Container(content=my_control, padding=u.p(theme, 3), margin=u.mt(theme, 4))

    u.Box(theme, content=my_control, p=3, bg="surface", rounded="lg", shadow="card")

    u.row(theme, [a, b, c], gap=2, justify="between", align="center")
"""
from __future__ import annotations

from typing import Iterable, Literal, Optional, Sequence

import flet as ft

from prisqo_ui.theme import Theme
from prisqo_ui.theme.breakpoints import breakpoint_at_least, breakpoint_at_most

from .variants import VariantName, resolve_variant

SpacingStep = Literal[0, 1, 2, 3, 4, 5, 6]

_SPACING_SCALE_ATTR = {1: "XS", 2: "SM", 3: "MD", 4: "LG", 5: "XL", 6: "XXL"}


def spacing_value(theme: Theme, step: SpacingStep) -> int:
    """Resolve a Bootstrap-style 0-6 spacing step against `theme.spacing`."""
    if step == 0:
        return 0
    attr = _SPACING_SCALE_ATTR.get(step)
    if attr is None:
        raise ValueError("Spacing step must be 0-6 (like Bootstrap's spacer scale).")
    return getattr(theme.spacing, attr)


# -- margin / padding, Bootstrap-style shorthands ---------------------------
# m/p = all sides, t/b/s/e = top/bottom/start(left)/end(right), x = start+end, y = top+bottom

def m(theme: Theme, step: SpacingStep) -> ft.Margin:
    v = spacing_value(theme, step)
    return ft.Margin.all(v)


def mt(theme: Theme, step: SpacingStep) -> ft.Margin:
    return ft.Margin.only(top=spacing_value(theme, step))


def mb(theme: Theme, step: SpacingStep) -> ft.Margin:
    return ft.Margin.only(bottom=spacing_value(theme, step))


def ms(theme: Theme, step: SpacingStep) -> ft.Margin:
    return ft.Margin.only(left=spacing_value(theme, step))


def me(theme: Theme, step: SpacingStep) -> ft.Margin:
    return ft.Margin.only(right=spacing_value(theme, step))


def mx(theme: Theme, step: SpacingStep) -> ft.Margin:
    v = spacing_value(theme, step)
    return ft.Margin.symmetric(horizontal=v)


def my(theme: Theme, step: SpacingStep) -> ft.Margin:
    v = spacing_value(theme, step)
    return ft.Margin.symmetric(vertical=v)


def p(theme: Theme, step: SpacingStep) -> ft.Padding:
    v = spacing_value(theme, step)
    return ft.Padding.all(v)


def pt(theme: Theme, step: SpacingStep) -> ft.Padding:
    return ft.Padding.only(top=spacing_value(theme, step))


def pb(theme: Theme, step: SpacingStep) -> ft.Padding:
    return ft.Padding.only(bottom=spacing_value(theme, step))


def ps(theme: Theme, step: SpacingStep) -> ft.Padding:
    return ft.Padding.only(left=spacing_value(theme, step))


def pe(theme: Theme, step: SpacingStep) -> ft.Padding:
    return ft.Padding.only(right=spacing_value(theme, step))


def px(theme: Theme, step: SpacingStep) -> ft.Padding:
    v = spacing_value(theme, step)
    return ft.Padding.symmetric(horizontal=v)


def py(theme: Theme, step: SpacingStep) -> ft.Padding:
    v = spacing_value(theme, step)
    return ft.Padding.symmetric(vertical=v)


def gap(theme: Theme, step: SpacingStep) -> int:
    """Spacing value for `ft.Row`/`ft.Column(spacing=...)` -- Bootstrap's `.gap-*`."""
    return spacing_value(theme, step)


# -- color utilities ---------------------------------------------------------
# Equivalent of `.text-primary`, `.bg-success-subtle`, `.border-danger`.

def text_color(theme: Theme, variant: VariantName) -> str:
    return resolve_variant(theme, variant).text


def bg_color(theme: Theme, variant: VariantName, soft: bool = True) -> str:
    colors = resolve_variant(theme, variant)
    return colors.soft_bg if soft else colors.solid


def border_color(theme: Theme, variant: VariantName) -> str:
    return resolve_variant(theme, variant).border


def text_style(
    theme: Theme,
    variant: Optional[VariantName] = None,
    size: Literal["caption", "small", "body", "label", "title"] = "body",
    color: Optional[str] = None,
) -> ft.TextStyle:
    """Bootstrap's `.text-{variant} .fs-*` combo, as one call."""
    resolved_color = color or (text_color(theme, variant) if variant else theme.text_primary)
    getter = {
        "caption": theme.typography.caption,
        "small": theme.typography.body_small,
        "body": theme.typography.body,
        "label": theme.typography.label,
        "title": theme.typography.page_title,
    }[size]
    return getter(resolved_color)


# -- radius / shadow ----------------------------------------------------------

def rounded(theme: Theme, size: Literal["sm", "md", "lg", "xl", "round"] = "md") -> int:
    """Bootstrap's `.rounded-{size}`."""
    return {
        "sm": theme.radius.SM,
        "md": theme.radius.MD,
        "lg": theme.radius.LG,
        "xl": theme.radius.XL,
        "round": theme.radius.ROUND,
    }[size]


def shadow(theme: Theme, level: Literal["card", "raised", "dropdown"] = "card") -> ft.BoxShadow:
    """Bootstrap's `.shadow` / `.shadow-sm` / `.shadow-lg`."""
    return {
        "card": theme.shadows.card,
        "raised": theme.shadows.raised,
        "dropdown": theme.shadows.dropdown,
    }[level]


# Stable references to the functions above, captured before `Box()` reuses
# their names as keyword arguments (so `Box(m=..., p=..., rounded=..., shadow=...)`
# can read like Bootstrap's utility-class names without shadowing bugs).
_m_fn, _p_fn, _rounded_fn, _shadow_fn = m, p, rounded, shadow


# -- flex/layout helpers -------------------------------------------------------
# Equivalent of `.d-flex`, `.justify-content-*`, `.align-items-*`, `.gap-*`.

_JUSTIFY = {
    "start": ft.MainAxisAlignment.START,
    "end": ft.MainAxisAlignment.END,
    "center": ft.MainAxisAlignment.CENTER,
    "between": ft.MainAxisAlignment.SPACE_BETWEEN,
    "around": ft.MainAxisAlignment.SPACE_AROUND,
    "evenly": ft.MainAxisAlignment.SPACE_EVENLY,
}

_ALIGN = {
    "start": ft.CrossAxisAlignment.START,
    "end": ft.CrossAxisAlignment.END,
    "center": ft.CrossAxisAlignment.CENTER,
    "stretch": ft.CrossAxisAlignment.STRETCH,
    "baseline": ft.CrossAxisAlignment.BASELINE,
}

JustifyName = Literal["start", "end", "center", "between", "around", "evenly"]
AlignName = Literal["start", "end", "center", "stretch", "baseline"]


def row(
    theme: Theme,
    controls: Sequence[ft.Control],
    gap: SpacingStep = 2,
    justify: JustifyName = "start",
    align: AlignName = "center",
    wrap: bool = False,
    tight: bool = False,
) -> ft.Row:
    """Bootstrap's `.d-flex .gap-* .justify-content-* .align-items-*`."""
    return ft.Row(
        controls=list(controls),
        spacing=spacing_value(theme, gap),
        alignment=_JUSTIFY[justify],
        vertical_alignment=_ALIGN[align],
        wrap=wrap,
        tight=tight,
    )


def stack(
    theme: Theme,
    controls: Sequence[ft.Control],
    gap: SpacingStep = 2,
    justify: JustifyName = "start",
    align: AlignName = "stretch",
    tight: bool = False,
) -> ft.Column:
    """Vertical equivalent of `row()` -- `.d-flex .flex-column`."""
    return ft.Column(
        controls=list(controls),
        spacing=spacing_value(theme, gap),
        alignment=_JUSTIFY[justify],
        horizontal_alignment=_ALIGN[align],
        tight=tight,
    )


# -- the "utility div" -------------------------------------------------------

def Box(
    theme: Theme,
    content: ft.Control,
    m: Optional[SpacingStep] = None,
    p: Optional[SpacingStep] = None,
    bg: Optional[VariantName] = None,
    bg_solid: bool = False,
    rounded: Literal["sm", "md", "lg", "xl", "round"] = "md",  # noqa: A002 (shadow name reuse ok, module-level fns not in scope here)
    border: Optional[VariantName] = None,
    shadow: Optional[Literal["card", "raised", "dropdown"]] = None,
    width: Optional[float] = None,
    height: Optional[float] = None,
    alignment: Optional[ft.Alignment] = None,
) -> ft.Container:
    """A single-call `ft.Container` builder using the same spacing/color/
    radius/shadow vocabulary as every other helper here -- the Flet analog
    of slapping `class="p-3 mt-4 bg-primary-subtle rounded-lg shadow-sm"`
    on a `<div>`.
    """
    return ft.Container(
        content=content,
        margin=_m_fn(theme, m) if m is not None else None,
        padding=_p_fn(theme, p) if p is not None else None,
        bgcolor=bg_color(theme, bg, soft=not bg_solid) if bg else None,
        border_radius=_rounded_fn(theme, rounded),
        border=ft.Border.all(1, border_color(theme, border)) if border else None,
        shadow=_shadow_fn(theme, shadow) if shadow else None,
        width=width,
        height=height,
        alignment=alignment,
    )


# -- responsive utilities -----------------------------------------------
# Equivalent of Bootstrap's `.d-none .d-md-block` (show/hide per
# breakpoint) and its responsive prop overrides. `theme.breakpoint` is
# kept in sync with the page width by `ThemeManager` -- these just read
# it, they don't measure anything themselves.

BreakpointName = Literal["xs", "sm", "md", "lg", "xl", "xxl"]


def is_mobile(theme: Theme) -> bool:
    """True below `md` (phones, narrow POS screens) -- `.d-md-none` territory."""
    return breakpoint_at_most(theme.breakpoint, "sm")


def is_tablet(theme: Theme) -> bool:
    """True at `md`/`lg` -- tablets and small laptops."""
    return breakpoint_at_least(theme.breakpoint, "md") and breakpoint_at_most(theme.breakpoint, "lg")


def is_desktop(theme: Theme) -> bool:
    """True at `xl` and above -- wide back-office monitors."""
    return breakpoint_at_least(theme.breakpoint, "xl")


def responsive(theme: Theme, xs=None, sm=None, md=None, lg=None, xl=None, xxl=None):
    """Pick a value for the current breakpoint, falling back to the
    nearest smaller breakpoint that was given a value -- the same
    cascade Bootstrap's responsive utility classes use (a value set at
    `md` also applies at `lg`/`xl`/`xxl` unless overridden).

    Example -- collapse a form from 3 columns to 1 as the screen narrows:

        columns = u.responsive(theme, xs=1, sm=1, md=2, lg=3)
    """
    values = {"xs": xs, "sm": sm, "md": md, "lg": lg, "xl": xl, "xxl": xxl}
    order = ["xs", "sm", "md", "lg", "xl", "xxl"]
    current_index = order.index(theme.breakpoint)
    chosen = None
    for name in order[: current_index + 1]:
        if values[name] is not None:
            chosen = values[name]
    return chosen

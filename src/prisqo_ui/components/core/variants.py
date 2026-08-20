"""The variant/size engine — the Python equivalent of Bootstrap's
`$theme-colors` Sass map + `button-variant()` / `badge-variant()` mixins.

Bootstrap doesn't hand-write `.btn-primary`, `.btn-success`, `.badge-danger`,
etc. one at a time. It defines ONE map of semantic names -> colors, and ONE
mixin per component family that turns `(name, color)` into the right CSS.
Every `.btn-{name}` / `.badge-{name}` / `.alert-{name}` class is generated
from that single source.

This module is that map + those mixins, translated to Flet:

- `VARIANTS` is the map (semantic name -> which `Theme` tokens to pull from).
- `resolve_variant(theme, name)` is the mixin: given a `Theme` and a variant
  name, it returns a `VariantColors` bundle (bg / hover / text / border /
  soft-bg) that any component can use, so a new component family (e.g. a
  future `Tag` or `Callout`) gets the full color set for free just by
  calling this function -- no copy-pasted color logic.
- `SIZES` is the equivalent of Bootstrap's `.btn-sm` / `.btn-lg` scale.

Components should never hand-roll `if variant == "success": ...` color
lookups -- call `resolve_variant` instead, the same way every Bootstrap
component defers to the shared color map.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from prisqo_ui.theme import Theme

VariantName = Literal[
    "primary",
    "secondary",
    "success",
    "danger",
    "warning",
    "info",
    "neutral",
    "light",
    "dark",
]

SizeName = Literal["sm", "md", "lg"]

# Canonical list, mainly for showcase/demo iteration and validation.
VARIANTS: tuple[VariantName, ...] = (
    "primary",
    "secondary",
    "success",
    "danger",
    "warning",
    "info",
    "neutral",
    "light",
    "dark",
)

SIZES: tuple[SizeName, ...] = ("sm", "md", "lg")


@dataclass(frozen=True)
class VariantColors:
    """The full color bundle for one variant, resolved against a `Theme`.

    - `solid` / `solid_hover` / `on_solid`: for filled/solid usage
      (PrimaryButton-style: colored background, light text on top).
    - `text`: the variant's "ink" color, for outline/ghost/link usage and
      for text-only utilities (Bootstrap's `.text-{variant}`).
    - `soft_bg`: a pale background tint, for chips/badges/alerts
      (Bootstrap's `.bg-{variant}-subtle` / `.alert-{variant}`).
    - `border`: border color for outline variants.
    """

    solid: str
    solid_hover: str
    on_solid: str
    text: str
    soft_bg: str
    border: str


# Component-family size scales. Mirrors Bootstrap's font-size + padding
# bump for `.btn-sm` / `.btn-lg`, expressed once and reused everywhere a
# `size` kwarg is accepted (buttons, badges, inputs, ...).
@dataclass(frozen=True)
class SizeSpec:
    height: float
    padding_h: int
    padding_v: int
    font_size: int
    icon_size: int
    radius: int


def resolve_variant(theme: Theme, variant: VariantName = "primary") -> VariantColors:
    """The single source of truth every component family reads from.

    Equivalent to calling Bootstrap's `button-variant($color)` /
    `badge-variant($color)` mixins for a given `$theme-colors` entry.
    """
    table = {
        "primary": VariantColors(
            solid=theme.primary,
            solid_hover=theme.primary_hover,
            on_solid=theme.text_on_primary,
            text=theme.primary,
            soft_bg=theme.primary_light,
            border=theme.primary,
        ),
        "secondary": VariantColors(
            solid=theme.surface_variant,
            solid_hover=theme.border,
            on_solid=theme.text_primary,
            text=theme.text_primary,
            soft_bg=theme.surface_variant,
            border=theme.border,
        ),
        "success": VariantColors(
            solid=theme.success,
            solid_hover=theme.success,
            on_solid="#FFFFFF",
            text=theme.success,
            soft_bg=theme.success_bg,
            border=theme.success,
        ),
        "danger": VariantColors(
            solid=theme.danger,
            solid_hover=theme.danger,
            on_solid="#FFFFFF",
            text=theme.danger,
            soft_bg=theme.danger_bg,
            border=theme.danger,
        ),
        "warning": VariantColors(
            solid=theme.warning,
            solid_hover=theme.warning,
            on_solid="#FFFFFF",
            text=theme.warning,
            soft_bg=theme.warning_bg,
            border=theme.warning,
        ),
        "info": VariantColors(
            solid=theme.info,
            solid_hover=theme.info,
            on_solid="#FFFFFF",
            text=theme.info,
            soft_bg=theme.info_bg,
            border=theme.info,
        ),
        "neutral": VariantColors(
            solid=theme.neutral_bg,
            solid_hover=theme.border,
            on_solid=theme.neutral_text,
            text=theme.neutral_text,
            soft_bg=theme.neutral_bg,
            border=theme.border,
        ),
        "light": VariantColors(
            solid=theme.surface,
            solid_hover=theme.surface_variant,
            on_solid=theme.text_primary,
            text=theme.text_secondary,
            soft_bg=theme.surface,
            border=theme.border,
        ),
        "dark": VariantColors(
            solid=theme.text_primary,
            solid_hover=theme.text_primary,
            on_solid=theme.background,
            text=theme.text_primary,
            soft_bg=theme.surface_variant,
            border=theme.text_primary,
        ),
    }
    if variant not in table:
        raise ValueError(
            f"Unknown variant {variant!r}. Valid variants: {', '.join(VARIANTS)}"
        )
    return table[variant]  # type: ignore[index]


def resolve_size(theme: Theme, size: SizeName = "md") -> SizeSpec:
    """Equivalent to Bootstrap's `.btn-sm` / `.btn` / `.btn-lg` scale.

    Reads radii from `theme.radius` so the scale stays themeable, but
    keeps height/padding/font-size ratios consistent across every
    component family that accepts `size=`.
    """
    table = {
        "sm": SizeSpec(
            height=32, padding_h=14, padding_v=6, font_size=13,
            icon_size=14, radius=theme.radius.MD,
        ),
        "md": SizeSpec(
            height=44, padding_h=20, padding_v=10, font_size=14,
            icon_size=17, radius=theme.radius.LG,
        ),
        "lg": SizeSpec(
            height=52, padding_h=26, padding_v=14, font_size=16,
            icon_size=19, radius=theme.radius.LG,
        ),
    }
    if size not in table:
        raise ValueError(f"Unknown size {size!r}. Valid sizes: {', '.join(SIZES)}")
    return table[size]  # type: ignore[index]

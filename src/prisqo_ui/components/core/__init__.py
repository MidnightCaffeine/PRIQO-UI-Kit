"""The Bootstrap-style foundation layer for PRISQO UI KIT.

This is the one place a variant/size/spacing decision gets made -- every
component family (buttons, badges, alerts, cards, ...) should build on top
of `variants.resolve_variant` / `variants.resolve_size` and the
`helpers` utility functions instead of re-deriving colors or spacing
locally, the same way every Bootstrap component defers to
`$theme-colors` and the shared spacing scale instead of hardcoding hex
values.
"""
from . import helpers
from .variants import (
    SIZES,
    VARIANTS,
    SizeName,
    SizeSpec,
    VariantColors,
    VariantName,
    resolve_size,
    resolve_variant,
)

__all__ = [
    "helpers",
    "VARIANTS",
    "SIZES",
    "VariantName",
    "SizeName",
    "VariantColors",
    "SizeSpec",
    "resolve_variant",
    "resolve_size",
]

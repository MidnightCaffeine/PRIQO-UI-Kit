"""Responsive breakpoint scale — the Python equivalent of Bootstrap's
`$grid-breakpoints` (`xs`, `sm`, `md`, `lg`, `xl`, `xxl`).

Bootstrap doesn't just use breakpoints for the grid: its `$font-size-base`
and heading sizes are tuned so text reads comfortably from a phone up to
a wide desktop, and utilities like `.fs-1`–`.fs-6` and `.display-*` scale
with them. `BREAKPOINTS` here plays the same role for this kit — each
breakpoint carries a `typography_scale` multiplier that `Typography`
applies to every text-style size, so `theme.typography.page_title()` is
one size on a POS tablet in portrait and a larger size on a wide desktop
monitor, without any component needing to know about screen width itself.
"""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Breakpoint:
    name: str
    min_width: int
    typography_scale: float


# Same names/min-widths as Bootstrap 5's grid breakpoints. `typography_scale`
# is this kit's addition: text shrinks slightly below `md` (phones/narrow
# POS screens) and grows slightly above `xl` (wide back-office monitors),
# with `lg` (a typical laptop) as the 1.0 baseline the existing type scale
# was designed at.
BREAKPOINTS: tuple[Breakpoint, ...] = (
    Breakpoint("xs", 0, 0.88),
    Breakpoint("sm", 576, 0.92),
    Breakpoint("md", 768, 0.96),
    Breakpoint("lg", 992, 1.0),
    Breakpoint("xl", 1200, 1.04),
    Breakpoint("xxl", 1400, 1.08),
)

_ORDER = ["xs", "sm", "md", "lg", "xl", "xxl"]


def resolve_breakpoint(width: float | None) -> Breakpoint:
    """The widest breakpoint whose `min_width` the given width satisfies.

    Mirrors how Bootstrap's `min-width` media queries cascade: a 1000px
    viewport matches `lg` (>=992), not `md`, even though it also
    technically satisfies `md`/`sm`/`xs`.

    `width=None` (page not laid out yet, or running headless) falls back
    to `lg` — a reasonable desktop default that matches this type scale's
    original, pre-responsive sizing.
    """
    if not width:
        return BREAKPOINTS[3]  # "lg"
    current = BREAKPOINTS[0]
    for bp in BREAKPOINTS:
        if width >= bp.min_width:
            current = bp
        else:
            break
    return current


def breakpoint_at_least(current: str, floor: str) -> bool:
    """`breakpoint_at_least(theme.breakpoint, "md")` — Bootstrap's
    `.d-md-block` idea: true from `floor` and up.
    """
    return _ORDER.index(current) >= _ORDER.index(floor)


def breakpoint_at_most(current: str, ceiling: str) -> bool:
    """True at `ceiling` and below — Bootstrap's `.d-md-none` idea."""
    return _ORDER.index(current) <= _ORDER.index(ceiling)

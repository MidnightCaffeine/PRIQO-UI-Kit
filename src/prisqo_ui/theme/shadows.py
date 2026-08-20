"""Elevation / shadow presets.

Shadows are intentionally subtle, matching the "modern enterprise SaaS"
design philosophy (Linear / Stripe Dashboard) rather than heavy skeuomorphic
drop shadows.
"""
from dataclasses import dataclass, field
from typing import List

import flet as ft


@dataclass(frozen=True)
class Shadows:
    """A set of BoxShadow presets for a given theme mode."""

    card: List[ft.BoxShadow] = field(default_factory=list)
    raised: List[ft.BoxShadow] = field(default_factory=list)
    dropdown: List[ft.BoxShadow] = field(default_factory=list)


def light_shadows() -> Shadows:
    return Shadows(
        card=[
            ft.BoxShadow(
                spread_radius=0,
                blur_radius=8,
                color=ft.Colors.with_opacity(0.06, "#111827"),
                offset=ft.Offset(0, 1),
            )
        ],
        raised=[
            ft.BoxShadow(
                spread_radius=0,
                blur_radius=16,
                color=ft.Colors.with_opacity(0.10, "#111827"),
                offset=ft.Offset(0, 4),
            )
        ],
        dropdown=[
            ft.BoxShadow(
                spread_radius=0,
                blur_radius=24,
                color=ft.Colors.with_opacity(0.14, "#111827"),
                offset=ft.Offset(0, 8),
            )
        ],
    )


def dark_shadows() -> Shadows:
    return Shadows(
        card=[
            ft.BoxShadow(
                spread_radius=0,
                blur_radius=8,
                color=ft.Colors.with_opacity(0.35, "#000000"),
                offset=ft.Offset(0, 1),
            )
        ],
        raised=[
            ft.BoxShadow(
                spread_radius=0,
                blur_radius=16,
                color=ft.Colors.with_opacity(0.45, "#000000"),
                offset=ft.Offset(0, 4),
            )
        ],
        dropdown=[
            ft.BoxShadow(
                spread_radius=0,
                blur_radius=24,
                color=ft.Colors.with_opacity(0.55, "#000000"),
                offset=ft.Offset(0, 8),
            )
        ],
    )

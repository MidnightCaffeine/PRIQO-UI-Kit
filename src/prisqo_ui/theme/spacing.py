"""Spacing scale used throughout PRISQO UI Kit.

Centralizing spacing avoids arbitrary pixel values scattered across
components and keeps the visual rhythm of the design system consistent.
"""
from dataclasses import dataclass


@dataclass(frozen=True)
class Spacing:
    XS: int = 4
    SM: int = 8
    MD: int = 12
    LG: int = 16
    XL: int = 24
    XXL: int = 32


SPACING = Spacing()

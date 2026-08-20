"""Raw color palettes for the Light and Dark themes.

These are the ONLY places raw hex values should live. Every component in
`prisqo_ui.components` must consume colors through semantic theme tokens
(see `theme.py`) rather than referencing these palettes directly.
"""
from dataclasses import dataclass


@dataclass(frozen=True)
class LightPalette:
    PRIMARY: str = "#4F46E5"
    PRIMARY_LIGHT: str = "#E0E7FF"
    PRIMARY_DARK: str = "#312E81"

    BACKGROUND: str = "#F9FAFB"
    SURFACE: str = "#FFFFFF"
    SURFACE_VARIANT: str = "#F3F4F6"

    SIDEBAR_BG: str = "#111827"
    SIDEBAR_TEXT: str = "#D1D5DB"
    SIDEBAR_TEXT_MUTED: str = "#6B7280"
    SIDEBAR_ACTIVE_BG: str = "#1F2937"

    TEXT_PRIMARY: str = "#111827"
    TEXT_SECONDARY: str = "#4B5563"
    TEXT_MUTED: str = "#6B7280"
    TEXT_ON_PRIMARY: str = "#FFFFFF"

    BORDER: str = "#E5E7EB"
    DIVIDER: str = "#E5E7EB"

    SUCCESS: str = "#16A34A"
    SUCCESS_BG: str = "#DCFCE7"
    WARNING: str = "#D97706"
    WARNING_BG: str = "#FEF3C7"
    DANGER: str = "#DC2626"
    DANGER_BG: str = "#FEE2E2"
    INFO: str = "#2563EB"
    INFO_BG: str = "#DBEAFE"

    NEUTRAL_BG: str = "#F3F4F6"
    NEUTRAL_TEXT: str = "#374151"


@dataclass(frozen=True)
class DarkPalette:
    PRIMARY: str = "#6366F1"
    PRIMARY_LIGHT: str = "#818CF8"
    PRIMARY_DARK: str = "#4F46E5"

    BACKGROUND: str = "#0F1117"
    SURFACE: str = "#171A21"
    SURFACE_VARIANT: str = "#1E232D"

    SIDEBAR_BG: str = "#0B0D12"
    SIDEBAR_TEXT: str = "#C3C8D1"
    SIDEBAR_TEXT_MUTED: str = "#6B7280"
    SIDEBAR_ACTIVE_BG: str = "#1E232D"

    TEXT_PRIMARY: str = "#F9FAFB"
    TEXT_SECONDARY: str = "#D1D5DB"
    TEXT_MUTED: str = "#9CA3AF"
    TEXT_ON_PRIMARY: str = "#FFFFFF"

    BORDER: str = "#2D3340"
    DIVIDER: str = "#252A34"

    SUCCESS: str = "#22C55E"
    SUCCESS_BG: str = "#123321"
    WARNING: str = "#F59E0B"
    WARNING_BG: str = "#3A2A0D"
    DANGER: str = "#EF4444"
    DANGER_BG: str = "#3A1414"
    INFO: str = "#3B82F6"
    INFO_BG: str = "#122540"

    NEUTRAL_BG: str = "#1E232D"
    NEUTRAL_TEXT: str = "#D1D5DB"


LIGHT_PALETTE = LightPalette()
DARK_PALETTE = DarkPalette()

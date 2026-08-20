"""Buttons showcase."""
from __future__ import annotations

import flet as ft

from prisqo_ui.theme import Theme
from prisqo_ui.components.cards import SectionCard
from prisqo_ui.components.buttons import (
    Button,
    PrimaryButton,
    SecondaryButton,
    OutlineButton,
    GhostButton,
    DangerButton,
    SuccessButton,
    WarningButton,
    InfoButton,
    AppIconButton,
    LoadingButton,
)
from prisqo_ui.components.liquid import LiquidSwitch, LiquidCheckbox, LiquidRadioGroup
from prisqo_ui.components.core.variants import VARIANTS, SIZES


def _row(*controls: ft.Control) -> ft.Row:
    return ft.Row(controls=list(controls), spacing=16, wrap=True, run_spacing=12)


def build(theme: Theme, page: ft.Page) -> ft.Control:
    normal = _row(
        PrimaryButton(theme, "Save", icon=ft.Icons.SAVE),
        SecondaryButton(theme, "Cancel"),
        OutlineButton(theme, "Export", icon=ft.Icons.DOWNLOAD),
        GhostButton(theme, "View details"),
        DangerButton(theme, "Delete", icon=ft.Icons.DELETE_OUTLINE),
        AppIconButton(theme, ft.Icons.EDIT, "Edit"),
    )

    disabled = _row(
        PrimaryButton(theme, "Save", disabled=True),
        SecondaryButton(theme, "Cancel", disabled=True),
        OutlineButton(theme, "Export", disabled=True),
        GhostButton(theme, "View details", disabled=True),
        DangerButton(theme, "Delete", disabled=True),
        AppIconButton(theme, ft.Icons.EDIT, "Edit", disabled=True),
    )

    loading = _row(
        LoadingButton(theme, "Saving...", loading=True),
        DangerButton(theme, "Deleting...", loading=True),
    )

    selected = _row(
        AppIconButton(theme, ft.Icons.FORMAT_BOLD, "Bold", selected=True),
        AppIconButton(theme, ft.Icons.FORMAT_ITALIC, "Italic", selected=False),
        AppIconButton(theme, ft.Icons.DELETE, "Delete", danger=True),
    )

    sizes = _row(
        PrimaryButton(theme, "Full width action", width=280),
        PrimaryButton(theme, "Compact", height=32),
    )

    # Bootstrap-style base component: one `Button()` call, `variant=` /
    # `size=` do the rest -- this is what every named button above
    # actually resolves to under the hood.
    full_palette = _row(*[Button(theme, v.capitalize(), variant=v) for v in VARIANTS])

    new_variants = _row(
        SuccessButton(theme, "Approve", icon=ft.Icons.CHECK),
        WarningButton(theme, "Hold", icon=ft.Icons.PAUSE),
        InfoButton(theme, "View details", icon=ft.Icons.INFO_OUTLINE),
    )

    size_scale = _row(*[Button(theme, s.upper(), variant="primary", size=s) for s in SIZES])

    toggles = _row(
        LiquidSwitch(theme, value=True, label="Notifications"),
        LiquidSwitch(theme, value=False, label="Auto-sync"),
        LiquidCheckbox(theme, value=True, label="Remember me"),
        LiquidCheckbox(theme, value=False, label="Send receipt"),
    )
    radio_group = LiquidRadioGroup(
        theme,
        options=[
            {"key": "cash", "label": "Cash"},
            {"key": "card", "label": "Card"},
            {"key": "gcash", "label": "GCash"},
        ],
        value="cash",
        vertical=False,
    )

    return ft.Column(
        controls=[
            SectionCard(theme, "Normal State", normal, subtitle="Primary, Secondary, Outline, Ghost, Danger, Icon \u2014 press and release for the liquid squish + bounce"),
            SectionCard(theme, "Disabled State", disabled),
            SectionCard(theme, "Loading State", loading),
            SectionCard(theme, "Selected / Danger Icon Buttons", selected),
            SectionCard(theme, "Sizing", sizes, subtitle="width / height overrides"),
            SectionCard(
                theme,
                "Full Variant Palette",
                full_palette,
                subtitle="Button(theme, text, variant=...) \u2014 the base component every named button below resolves to",
            ),
            SectionCard(theme, "Success / Warning / Info", new_variants),
            SectionCard(theme, "Size Scale", size_scale, subtitle="Button(theme, text, size=\"sm\"|\"md\"|\"lg\")"),
            SectionCard(
                theme,
                "Liquid Switches & Checkboxes",
                toggles,
                subtitle="Thumb/checkmark drop into place with an elastic overshoot",
            ),
            SectionCard(theme, "Liquid Radio Group", radio_group, subtitle="Payment method selector"),
        ],
        spacing=16,
        tight=True,
    )

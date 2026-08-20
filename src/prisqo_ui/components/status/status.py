"""Status components — badges, chips and dots used to communicate record
state (Draft, Approved, Active, In Stock, ...) consistently across ERP
modules.

Status is NEVER communicated by color alone: every component also
renders the status label as text (and StatusDot is meant to be paired
with a text label by the caller).

Color resolution now goes through `core.variants.resolve_variant`, the
same engine `Button` uses -- so `StatusChip`/`StatusBadge`/`StatusDot` are
Bootstrap's `.badge .bg-{variant}` idea: a known ERP status string
(`"approved"`, `"paid"`, ...) is looked up in `_STATUS_TONE` to find its
variant, but you can also pass `variant=` directly to skin an
arbitrary/custom label without adding it to the lookup table.
"""
from __future__ import annotations

from typing import Optional, Sequence

import flet as ft

from prisqo_ui.theme import Theme
from prisqo_ui.components.core.variants import VariantName, resolve_variant

# Canonical status -> semantic variant mapping. Unknown statuses fall back
# to "neutral" so nothing ever renders unstyled.
_STATUS_TONE: dict[str, VariantName] = {
    "draft": "neutral",
    "pending": "warning",
    "approved": "success",
    "rejected": "danger",
    "posted": "info",
    "cancelled": "danger",
    "active": "success",
    "inactive": "neutral",
    "paid": "success",
    "unpaid": "danger",
    "partially paid": "warning",
    "in stock": "success",
    "low stock": "warning",
    "out of stock": "danger",
}


def _resolve_tone(status: str) -> VariantName:
    return _STATUS_TONE.get(status.strip().lower(), "neutral")


def StatusChip(theme: Theme, label: str, status: Optional[str] = None, variant: Optional[VariantName] = None) -> ft.Container:
    """A filled, rounded chip — the primary status indicator.

    Resolves its color from `status` (looked up against the known ERP
    status vocabulary) unless `variant` is passed explicitly, e.g.
    `StatusChip(theme, label="Beta", variant="info")` for a label that
    isn't one of the canonical statuses.
    """
    tone = variant or _resolve_tone(status or label)
    colors = resolve_variant(theme, tone)
    return ft.Container(
        content=ft.Text(label, style=theme.typography.caption(colors.text), max_lines=1, overflow=ft.TextOverflow.ELLIPSIS),
        bgcolor=colors.soft_bg,
        padding=ft.Padding.symmetric(horizontal=10, vertical=4),
        border_radius=theme.radius.ROUND,
    )


def StatusBadge(theme: Theme, label: str, status: Optional[str] = None, variant: Optional[VariantName] = None) -> ft.Container:
    """An outlined badge — slightly lower-emphasis than StatusChip."""
    tone = variant or _resolve_tone(status or label)
    colors = resolve_variant(theme, tone)
    return ft.Container(
        content=ft.Text(label, style=theme.typography.caption(colors.text), max_lines=1, overflow=ft.TextOverflow.ELLIPSIS),
        border=ft.Border.all(1, colors.border),
        padding=ft.Padding.symmetric(horizontal=10, vertical=3),
        border_radius=theme.radius.ROUND,
    )


def StatusDot(theme: Theme, status: str, label: Optional[str] = None, variant: Optional[VariantName] = None) -> ft.Row:
    """A small colored dot with an adjacent text label (never color-only)."""
    tone = variant or _resolve_tone(status)
    colors = resolve_variant(theme, tone)
    return ft.Row(
        controls=[
            ft.Container(width=8, height=8, bgcolor=colors.solid, border_radius=theme.radius.ROUND),
            ft.Text(label or status, style=theme.typography.body_small(theme.text_secondary)),
        ],
        spacing=6,
        tight=True,
    )


# Bootstrap-familiar alias: `.badge .bg-{variant}` reads naturally as
# `Badge(theme, label, variant="success")`. `StatusBadge` stays the
# canonical export for existing call sites.
Badge = StatusBadge


def StatusChipGroup(
    theme: Theme,
    chips: Sequence[ft.Control],
    gap: Optional[float] = None,
) -> ft.Row:
    """Lays out multiple `StatusChip`/`StatusBadge`/`StatusDot` controls the
    way CSS `flex-wrap: wrap` lays out a row of tags: they sit side by side
    for as long as they fit the available width, and a chip that no longer
    fits drops to its own line instead of clipping or forcing the row (and
    whatever it's inside -- a table cell, a card header) wider than its
    container.

    This is the group-level counterpart to `StatusChip` itself: a single
    chip never needs to wrap, but any place that renders several of them
    together (tags on a record, multiple statuses in one table cell)
    should reach for this instead of a plain `ft.Row`.

    Usage:
        StatusChipGroup(theme, [StatusChip(theme, "Approved"), StatusChip(theme, "Posted")])
    """
    spacing = gap if gap is not None else theme.spacing.SM
    return ft.Row(
        controls=list(chips),
        wrap=True,
        spacing=spacing,
        run_spacing=spacing,
    )

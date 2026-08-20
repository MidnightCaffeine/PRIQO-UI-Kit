"""`FlexRow` — a container that behaves like CSS `display: flex; flex-wrap: wrap`.

Flet's `ft.Row` already implements real flex-wrap under the hood (`wrap=True`
lays items out left-to-right and only drops an item to the next line once
it no longer fits, exactly like the CSS property) — it's just easy to
forget the handful of props (`wrap`, `spacing`, `run_spacing`, alignment
enums) needed to get that behavior consistently. `FlexRow` bundles those
with this kit's theme-driven spacing so every place that needs "these
fields sit side-by-side, but the *n*-th one drops to its own line once
the screen gets too narrow to fit them all" reaches for one component
instead of five loose props.

This is deliberately NOT the same tool as `FormRow` (forms/fields.py):
- `FormRow` is a `ft.ResponsiveRow` — a 12-column grid keyed to Flet's
  fixed breakpoints (`xs`/`md`/...). Every field stacks to full width
  together the instant the viewport crosses the `md` breakpoint,
  regardless of whether they'd actually still fit. Reach for `FormRow`
  when you want that Bootstrap-style "all-or-nothing" stack.
- `FlexRow` wraps based on the controls' own intrinsic/assigned widths
  filling the available space — the same continuous, content-driven
  wrapping as CSS flexbox. A row of four 220px fields in a 500px-wide
  container wraps after the second one; in a 700px container it wraps
  after the third; it isn't tied to a breakpoint at all. Reach for
  `FlexRow` for toolbars, filter bars, tag/chip groups, or field groups
  where you want fields to keep pairing up for as long as they fit,
  wrapping one at a time rather than all stacking together at once.

Usage:
    FlexRow(
        theme,
        [
            AppTextField(theme, label="First Name", width=220),
            AppTextField(theme, label="Last Name", width=220),
            AppTextField(theme, label="Middle Name", width=220),
        ],
    )
    # On a wide window all three sit on one line. Narrow the window and
    # "Middle Name" (then "Last Name") drops to its own line, one at a
    # time, exactly like `flex-wrap: wrap` — never all three snapping to
    # a stack together the way a `ResponsiveRow`/`FormRow` would.

    # Controls with no explicit width (e.g. plain buttons or chips) wrap
    # by their natural/content width, same as flex items with no
    # flex-basis set:
    FlexRow(theme, [Chip(theme, "Beverage"), Chip(theme, "Grocery"), Chip(theme, "Dairy")])

    # `min_item_width` is a convenience equivalent to CSS `flex-basis`
    # applied uniformly: any control that doesn't already set its own
    # `.width` gets wrapped to this minimum, so a mixed list of fields
    # wraps predictably instead of at whatever width each one happens
    # to default to.
    FlexRow(theme, [AppTextField(theme, label="City"), AppTextField(theme, label="ZIP")],
            min_item_width=200)
"""
from __future__ import annotations

from typing import Optional, Sequence

import flet as ft

from prisqo_ui.theme import Theme

_JUSTIFY = {
    "start": ft.MainAxisAlignment.START,
    "center": ft.MainAxisAlignment.CENTER,
    "end": ft.MainAxisAlignment.END,
    "space_between": ft.MainAxisAlignment.SPACE_BETWEEN,
    "space_around": ft.MainAxisAlignment.SPACE_AROUND,
    "space_evenly": ft.MainAxisAlignment.SPACE_EVENLY,
}

_ALIGN = {
    "start": ft.CrossAxisAlignment.START,
    "center": ft.CrossAxisAlignment.CENTER,
    "end": ft.CrossAxisAlignment.END,
    "stretch": ft.CrossAxisAlignment.STRETCH,
}


def FlexRow(
    theme: Theme,
    controls: Sequence[ft.Control],
    min_item_width: Optional[float] = None,
    gap: Optional[float] = None,
    justify: str = "start",
    align: str = "start",
    expand: bool = False,
) -> ft.Row:
    """
    Args:
        controls:       the flex items, left to right.
        min_item_width: CSS `flex-basis`-style minimum width applied to any
                         control that doesn't already set its own `.width`.
                         Leave `None` to let every control wrap at its own
                         natural or pre-set width.
        gap:            CSS `gap` shorthand — spacing between items on the
                         same line AND between wrapped lines. Defaults to
                         `theme.spacing.MD` (use the two-value form via a
                         plain `ft.Row(wrap=True, ...)` directly if you
                         need independent row/column gaps).
        justify:        main-axis alignment — "start" | "center" | "end" |
                         "space_between" | "space_around" | "space_evenly".
        align:          cross-axis alignment — "start" | "center" | "end" |
                         "stretch".
        expand:         let the row fill its parent's main-axis size
                         (CSS `width: 100%` on the flex container).
    """
    spacing = gap if gap is not None else theme.spacing.MD

    items: list[ft.Control] = []
    for c in controls:
        if min_item_width is not None and getattr(c, "width", None) is None:
            items.append(ft.Container(content=c, width=min_item_width))
        else:
            items.append(c)

    return ft.Row(
        controls=items,
        wrap=True,
        spacing=spacing,
        run_spacing=spacing,
        alignment=_JUSTIFY.get(justify, ft.MainAxisAlignment.START),
        vertical_alignment=_ALIGN.get(align, ft.CrossAxisAlignment.START),
        expand=expand,
    )

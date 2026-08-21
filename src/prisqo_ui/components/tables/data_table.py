"""`AppDataTable` — the core ERP list-view table.

Wraps `ft.DataTable` (the standard Flet 0.85.3 table control) with
theme-aware styling, row selection, custom cell rendering (for status
chips, amounts, row actions, ...), and loading / empty states.
"""
from __future__ import annotations

import dataclasses
from typing import Any, Callable, Mapping, MutableMapping, Optional, Sequence

import flet as ft

from prisqo_ui.theme import Theme
from prisqo_ui.components.feedback.feedback import SkeletonTable, EmptyState
from prisqo_ui.components.buttons.buttons import AppIconButton


def to_row(obj: Any) -> Mapping:
    """Normalize one record into the plain `Mapping` `AppDataTable` needs.

    `AppDataTable` (like every ERP list-view backing store) is written
    against `Mapping` rows -- `row[key]` / `row.get(key)` -- because
    that's the shape query results, JSON API responses, and dict-based
    mocks all already come in. Callers whose data instead lives in
    `@dataclass` records (a very common ERP pattern: a typed
    `Item`/`Order`/`Invoice` row model) shouldn't have to hand-roll a
    dict-conversion at every call site:

        rows = [to_row(item) for item in item_records]
        AppDataTable(theme, COLUMNS, rows, row_id_field="sku")

    ...though `AppDataTable` itself now calls this on every row already,
    so passing dataclass instances straight through works too.

    Already-a-`Mapping` input (plain `dict`s, the common case) passes
    through unchanged. `@dataclass` instances are converted via
    `dataclasses.asdict` (shallow -- nested dataclasses are left as-is,
    matching what `_cell_content`'s `row.get(col["key"])` lookups need:
    one level of field access per column). Any other object falls back
    to `vars(obj)` (its `__dict__`), which covers plain attribute-bag
    objects (e.g. ORM rows) the same way.
    """
    if isinstance(obj, Mapping):
        return obj
    if dataclasses.is_dataclass(obj) and not isinstance(obj, type):
        return dataclasses.asdict(obj)
    try:
        return vars(obj)
    except TypeError as exc:
        raise TypeError(
            f"to_row() cannot convert {type(obj).__name__!r}: expected a "
            "Mapping, a dataclass instance, or an object with a __dict__."
        ) from exc


def AppDataTable(
    theme: Theme,
    columns: Sequence[Mapping],
    rows: Sequence[Any],
    row_id_field: str = "id",
    selectable: bool = False,
    selected_ids: Optional[set] = None,
    on_selection_change: Optional[Callable[[set], None]] = None,
    row_actions: Optional[Sequence[Mapping]] = None,
    loading: bool = False,
    empty_title: str = "No records",
    empty_description: str = "There are no records matching your current filters.",
    page: Optional[ft.Page] = None,
    min_column_width: float = 56,
) -> ft.Control:
    """
    columns: sequence of {"key": str, "label": str, "numeric": bool (optional),
             "render": Callable[[row], ft.Control] (optional)}
    rows: sequence of `Mapping` records (plain dicts, the common case), OR
          `@dataclass` / attribute-bag records -- anything `to_row()` can
          normalize. Every row is run through `to_row()` up front, so the
          rest of this function (and any `render` callable in `columns`)
          only ever sees plain `Mapping` rows and can keep using
          `row["key"]` / `row.get("key")` regardless of what callers
          passed in.
    row_actions: sequence of {"icon": IconData, "tooltip": str,
             "on_click": Callable[[row], None]}
    min_column_width: absolute lower bound under a column's own header-
          based floor (see `page` below) -- mostly a safety net for very
          short headers/abbreviations. Override per-column with a
          `"min_width"` key on that column's dict in `columns` for
          precise control. Below its floor a column stops compressing
          and the table falls back to horizontal scrolling instead of
          shrinking further.
    page: optional; used only to seed an initial width before layout
          happens, so the table isn't zero-width for a frame. The actual
          fill/compress/scroll sizing (see below) comes from the
          container's own rendered size instead of a `page.width`
          guess, so it stays correct even next to a sidebar, inside a
          padded card, etc.

    Column sizing, in order of preference, as the container gets
    narrower: (1) every column gets its "comfortable" width -- enough
    for its header and its widest cell value; (2) once that no longer
    fits, every column is proportionally squeezed toward its own floor
    -- by default just enough to keep its own header legible, not one
    flat width for every column regardless of what's actually in it --
    just enough to fit the available space, no scrollbar; (3) once even
    every column at its floor still doesn't fit, the table stops
    shrinking and the surrounding row becomes horizontally scrollable
    instead of clipping or squeezing text into illegibility.
    """
    if loading:
        return SkeletonTable(theme, rows=6, columns=len(columns))

    rows = [to_row(r) for r in rows]

    if not rows:
        return EmptyState(theme, empty_title, empty_description, icon=ft.Icons.INBOX)

    selection: MutableMapping[str, bool] = {rid: True for rid in (selected_ids or set())}

    def _toggle_all(e: ft.ControlEvent) -> None:
        checked = e.control.value if hasattr(e.control, "value") else False
        for r in rows:
            rid = r[row_id_field]
            if checked:
                selection[rid] = True
            else:
                selection.pop(rid, None)
        table.rows = _build_rows()
        table.update()
        if on_selection_change:
            on_selection_change(set(selection.keys()))

    def _toggle_row(rid) -> Callable:
        def _handler(e: ft.ControlEvent) -> None:
            if e.control.selected:
                selection[rid] = True
            else:
                selection.pop(rid, None)
            if on_selection_change:
                on_selection_change(set(selection.keys()))

        return _handler

    def _cell_content(col: Mapping, row: Mapping) -> ft.Control:
        renderer = col.get("render")
        if renderer:
            return renderer(row)
        value = row.get(col["key"], "")
        return ft.Text(str(value), style=theme.typography.table_body(theme.text_primary))

    def _text_width(text: str, font_size: float = 13.0) -> float:
        """Rough px-per-character estimate for a string at `font_size`.

        Flet has no synchronous text-measurement API, so this is a
        deliberately simple approximation (~0.58x font-size per glyph,
        which is in the right ballpark for typical UI sans-serif fonts)
        -- good enough to size a column to its *actual* content instead
        of applying one flat width to every column regardless of what's
        in it.
        """
        return len(text) * font_size * 0.58

    def _column_floor_width(col: Mapping) -> float:
        """The narrowest this column is allowed to get while compressing.

        Defaults to just enough to keep *this column's own header*
        legible, not one flat width applied to every column regardless
        of what's actually in it. A uniform floor (e.g. always 130px)
        floors short columns -- a 3-digit "Qty", a 2-letter status code
        -- exactly as high as long ones, which drags the whole table's
        floor up and makes it fall back to horizontal scroll far sooner
        than the content genuinely requires. `min_column_width` is kept
        as an absolute lower bound underneath this (mostly a safety net
        for very short/abbreviated headers); override per-column with a
        `"min_width"` key for precise control.
        """
        custom = col.get("min_width")
        if custom is not None:
            return custom
        header_w = _text_width(str(col.get("label", "")))
        return max(min_column_width, header_w + 8.0)

    def _column_comfortable_width(col: Mapping) -> float:
        """This column's width if it gets everything its content wants."""
        col_min = _column_floor_width(col)
        header_w = _text_width(str(col.get("label", "")))
        if col.get("render"):
            # Custom-rendered cells (status chips, etc.) aren't plain
            # text, so their width can't be estimated this way -- fall
            # back to just the header estimate; `col_min` still
            # guarantees a sane floor for these columns.
            cell_w = 0.0
        else:
            cell_w = max(
                (_text_width(str(row.get(col["key"], ""))) for row in rows),
                default=0.0,
            )
        # No extra per-column padding added here: the table's own
        # `column_spacing`/`horizontal_margin` (below) and Flutter's
        # default cell padding already account for that. Adding a flat
        # padding constant on top of *every* column double-counted that
        # spacing and was inflating the natural width enough to trigger
        # horizontal scroll even when the content actually fit.
        return max(col_min, header_w, cell_w)

    def _build_rows() -> list:
        data_rows = []
        for row in rows:
            rid = row[row_id_field]
            cells = [ft.DataCell(_cell_content(col, row)) for col in columns]
            if row_actions:
                cells.append(
                    ft.DataCell(
                        ft.Row(
                            controls=[
                                AppIconButton(
                                    theme,
                                    icon=action["icon"],
                                    tooltip=action["tooltip"],
                                    danger=action.get("danger", False),
                                    on_click=lambda e, a=action, r=row: a["on_click"](r),
                                )
                                for action in row_actions
                            ],
                            spacing=0,
                            tight=True,
                        )
                    )
                )
            data_rows.append(
                ft.DataRow(
                    cells=cells,
                    selected=rid in selection,
                    on_select_change=_toggle_row(rid) if selectable else None,
                )
            )
        return data_rows

    # One resizable `Container` per column header -- `.width` on these is
    # what actually gets adjusted as the table is squeezed (see
    # `_apply_width` below), between each column's own "comfortable"
    # (content-driven) width and its floor (`min_width`/`min_column_width`).
    col_width_boxes: list[ft.Container] = []
    comfortable_widths: list[float] = []
    min_widths: list[float] = []
    header_cols: list[ft.DataColumn] = []
    for col in columns:
        comfortable_w = _column_comfortable_width(col)
        col_min = _column_floor_width(col)
        box = ft.Container(
            content=ft.Text(col["label"], style=theme.typography.table_header(theme.text_muted)),
            width=comfortable_w,
            alignment=ft.Alignment.CENTER_RIGHT if col.get("numeric") else ft.Alignment.CENTER_LEFT,
        )
        col_width_boxes.append(box)
        comfortable_widths.append(comfortable_w)
        min_widths.append(col_min)
        header_cols.append(ft.DataColumn(label=box, numeric=col.get("numeric", False)))
    if row_actions:
        header_cols.append(ft.DataColumn(label=ft.Text("")))

    table = ft.DataTable(
        columns=header_cols,
        rows=_build_rows(),
        show_checkbox_column=selectable,
        on_select_all=_toggle_all if selectable else None,
        heading_row_color=theme.surface_variant,
        heading_row_height=44,
        data_row_min_height=48,
        data_row_max_height=56,
        divider_thickness=1,
        border=ft.Border.all(1, theme.border),
        border_radius=theme.radius.LG,
        column_spacing=theme.spacing.LG,
        horizontal_margin=theme.spacing.MD,
        # `width` is driven by `_sync_width` below instead of a plain
        # `expand=True`: an *expanded* table is forced to exactly the
        # container's width no matter what, which is what silently
        # clipped columns that needed more room than that. Setting an
        # explicit `width` that's the larger of "available space" and
        # "what the columns' actual content needs" gets both properties
        # at once -- fills the row when content fits, only grows past
        # the viewport (and becomes scrollable, via the wrapping `Row`
        # below) when it genuinely doesn't.
    )

    row_wrap = ft.Row(
        controls=[table],
        # Horizontal scroll only engages once `table.width` (set below)
        # is actually wider than this Row's own width -- i.e. once the
        # columns genuinely don't fit -- even after column widths/
        # spacing are already tuned. `ADAPTIVE` (mouse-drag/trackpad/
        # scrollbar) generally reads better for wide data tables than
        # `AUTO`, which only shows a scrollbar while actively scrolling.
        scroll=ft.ScrollMode.ADAPTIVE,
        expand=True,
    )

    container = ft.Container(
        content=row_wrap,
        bgcolor=theme.surface,
        border_radius=theme.radius.LG,
        clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
        expand=True,
    )

    def _natural_totals() -> tuple[float, float]:
        # Chrome the table adds outside the adjustable columns
        # themselves: the checkbox column, the row-actions column, the
        # spacing between columns, and the table's own left/right
        # margins. Same for both totals below since none of it shrinks.
        n_all_cols = len(columns)
        chrome = 0.0
        if row_actions:
            # Fixed by the icon-button row this column actually renders
            # (see `_build_rows`), not tied to the text-column floor
            # logic above -- those are a different kind of content.
            chrome += 40 * len(row_actions) + 16
            n_all_cols += 1
        if selectable:
            chrome += 48
            n_all_cols += 1
        chrome += theme.spacing.LG * max(n_all_cols - 1, 0)
        chrome += theme.spacing.MD * 2
        return sum(comfortable_widths) + chrome, sum(min_widths) + chrome

    def _apply_width(available: float) -> None:
        comfortable_total, min_total = _natural_totals()

        if comfortable_total <= min_total or available >= comfortable_total:
            # Either there's nothing to compress, or there's room enough
            # to give every column exactly what its content wants.
            ratio = 1.0
        elif available <= min_total:
            # No room to adjust left, even with every column squeezed
            # down to its floor -- this is the genuine overflow case.
            ratio = 0.0
        else:
            # Still fits, but only once each column gives up some of its
            # comfortable width. Shrinking every column by the same
            # proportion of its own min..comfortable range (rather than
            # the same flat pixel amount) keeps a short column and a
            # long column each losing a fair share of what they asked
            # for, instead of one column doing all the compressing.
            ratio = (available - min_total) / (comfortable_total - min_total)

        for box, mn, cw in zip(col_width_boxes, min_widths, comfortable_widths):
            box.width = mn + ratio * (cw - mn)

        content_total = sum(box.width for box in col_width_boxes) + (comfortable_total - sum(comfortable_widths))
        # `content_total` reconstructs the full table width (columns +
        # chrome) from the widths just assigned above. By construction
        # it lands on `available` whenever compression alone can make it
        # fit (ratio between 0 and 1); it only exceeds `available` once
        # every column is already at its floor and there's genuinely no
        # more room to adjust -- exactly the point `table.width` should
        # grow past the container and let `row_wrap`'s scroll take over.
        table.width = max(available, content_total)
        try:
            if table.page:
                table.update()
        except RuntimeError:
            # Not attached to the page yet -- nothing to refresh, the
            # width is already set for when it does get added.
            pass

    def _on_container_size_change(e: ft.LayoutSizeChangeEvent) -> None:
        # `e.width` is the container's *actual* rendered width -- the
        # real constraint imposed by wherever this table happens to sit
        # (a sidebar, a padded card, a narrower column, ...). Driving
        # the fill/compress/scroll decision off this instead of a
        # `page.width` guess is what makes it correct in those layouts.
        _apply_width(e.width)

    container.on_size_change = _on_container_size_change

    # Seed a width immediately so the table isn't zero-width for the one
    # frame before the first `on_size_change` fires. Purely a fallback
    # estimate -- `on_size_change` corrects it to the real value right
    # after.
    _apply_width((page.width if page and page.width else 1024) - theme.spacing.LG * 2)

    return container

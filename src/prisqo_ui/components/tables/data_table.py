"""`AppDataTable` — the core ERP list-view table.

Wraps `ft.DataTable` (the standard Flet 0.85.3 table control) with
theme-aware styling, row selection, custom cell rendering (for status
chips, amounts, row actions, ...), and loading / empty states.
"""
from __future__ import annotations

from typing import Callable, Mapping, MutableMapping, Optional, Sequence

import flet as ft

from prisqo_ui.theme import Theme
from prisqo_ui.components.feedback.feedback import SkeletonTable, EmptyState
from prisqo_ui.components.buttons.buttons import AppIconButton


def AppDataTable(
    theme: Theme,
    columns: Sequence[Mapping],
    rows: Sequence[Mapping],
    row_id_field: str = "id",
    selectable: bool = False,
    selected_ids: Optional[set] = None,
    on_selection_change: Optional[Callable[[set], None]] = None,
    row_actions: Optional[Sequence[Mapping]] = None,
    loading: bool = False,
    empty_title: str = "No records",
    empty_description: str = "There are no records matching your current filters.",
    page: Optional[ft.Page] = None,
    min_column_width: float = 130,
) -> ft.Control:
    """
    columns: sequence of {"key": str, "label": str, "numeric": bool (optional),
             "render": Callable[[row], ft.Control] (optional)}
    row_actions: sequence of {"icon": IconData, "tooltip": str,
             "on_click": Callable[[row], None]}
    page: pass the page in so the table can size itself to *fill* the
          available width (the normal case) while still knowing when its
          columns genuinely need more room than that and switching to a
          horizontally-scrollable, content-width table instead of
          clipping. Without `page`, the table just always fills the
          container width (no scroll) -- the pre-existing behaviour.
    """
    if loading:
        return SkeletonTable(theme, rows=6, columns=len(columns))

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

    header_cols = [
        ft.DataColumn(
            label=ft.Text(col["label"], style=theme.typography.table_header(theme.text_muted)),
            numeric=col.get("numeric", False),
        )
        for col in columns
    ]
    if row_actions:
        header_cols.append(ft.DataColumn(label=ft.Text("")))

    n_cols = len(header_cols)

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
        # "what the columns actually need" gets both properties at once
        # -- fills the row when content fits, only grows past the
        # viewport (and becomes scrollable, via the wrapping `Row`
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

    def _sync_width(_e: Optional[ft.ControlEvent] = None) -> None:
        # Rough estimate of the space actually available to the table:
        # the page width minus the outer container's own horizontal
        # chrome. It won't perfectly account for e.g. a sidebar the
        # table happens to sit next to, but combined with the natural
        # minimum below it reliably gives "fill when it fits, scroll
        # when it doesn't" instead of ever silently clipping.
        available = (page.width if page and page.width else 1024) - (theme.spacing.LG * 2)
        natural_min = n_cols * min_column_width
        table.width = max(available, natural_min)
        try:
            if table.page:
                table.update()
        except RuntimeError:
            # Not attached to the page yet (e.g. this is the initial
            # build, before `page.show_dialog`/layout insertion) --
            # nothing to refresh yet, `table.width` is already set for
            # when it does get added.
            pass

    if page is not None:
        _sync_width()
        _prev_resize = page.on_resize

        def _on_resize(e: ft.ControlEvent) -> None:
            if _prev_resize:
                _prev_resize(e)
            _sync_width(e)

        page.on_resize = _on_resize
    else:
        # No `page` handed in -- fall back to always filling the
        # container (matches this component's original behaviour).
        table.expand = True

    return container

"""Generic `LookupField` — the base for all ERP lookup components.

Displays the current selection and opens a searchable dialog listing
candidate records (mock data only — no database, no API calls).
"""
from __future__ import annotations

from typing import Callable, Mapping, Optional, Sequence

import flet as ft

from prisqo_ui.theme import Theme
from prisqo_ui.components.buttons.buttons import AppIconButton, GhostButton


def LookupField(
    theme: Theme,
    page: ft.Page,
    items: Sequence[Mapping],
    display_field: str,
    label: str = "Select",
    subtitle_field: Optional[str] = None,
    value: Optional[Mapping] = None,
    dialog_title: Optional[str] = None,
    search_hint: str = "Search...",
    required: bool = False,
    disabled: bool = False,
    width: Optional[float] = None,
    on_select: Optional[Callable[[Optional[Mapping]], None]] = None,
) -> ft.Container:
    state = {"value": value}
    display_label = f"{label} *" if required else label

    display_text = ft.Text(
        state["value"][display_field] if state["value"] else "",
        style=theme.typography.body(theme.text_primary if state["value"] else theme.text_muted),
    )

    def _placeholder_text() -> str:
        return state["value"][display_field] if state["value"] else f"Select {label.lower()}..."

    display_text.value = _placeholder_text()

    clear_btn = AppIconButton(
        theme,
        icon=ft.Icons.CLOSE,
        tooltip="Clear",
        on_click=lambda e: _clear(e),
    )
    clear_btn.visible = state["value"] is not None

    def _clear(e: ft.ControlEvent) -> None:
        state["value"] = None
        display_text.value = _placeholder_text()
        display_text.style = theme.typography.body(theme.text_muted)
        clear_btn.visible = False
        field_box.update()
        if on_select:
            on_select(None)

    def _open_dialog(e: ft.ControlEvent) -> None:
        if disabled:
            return

        results_column = ft.Column(spacing=2, scroll=ft.ScrollMode.AUTO, height=320)

        def _row_for(item: Mapping) -> ft.Control:
            subtitle = ft.Text(str(item.get(subtitle_field, "")), style=theme.typography.caption(theme.text_muted)) if subtitle_field else None
            content_col = [ft.Text(str(item[display_field]), style=theme.typography.body(theme.text_primary))]
            if subtitle:
                content_col.append(subtitle)
            return ft.Container(
                content=ft.Column(controls=content_col, spacing=2, tight=True),
                padding=ft.Padding.symmetric(horizontal=12, vertical=10),
                border_radius=theme.radius.SM,
                ink=True,
                on_click=lambda ev, it=item: _select(it),
            )

        def _refresh(query: str = "", mounted: bool = True) -> None:
            q = query.strip().lower()
            filtered = [it for it in items if q in str(it[display_field]).lower()] if q else list(items)
            if filtered:
                results_column.controls = [_row_for(it) for it in filtered]
            else:
                results_column.controls = [
                    ft.Container(
                        content=ft.Text(
                            "No results found.",
                            style=theme.typography.body_small(theme.text_muted),
                        ),
                        padding=theme.spacing.LG,
                        alignment=ft.Alignment(0, 0),
                    )
                ]
            # `results_column` is only attached to the page once `page.show_dialog(dialog)`
            # runs below, so the very first call (building the initial result list before
            # the dialog is shown) must NOT call .update() — Flet raises "Control must be
            # added to the page first" if you do.
            if mounted:
                results_column.update()

        def _select(item: Mapping) -> None:
            state["value"] = item
            display_text.value = item[display_field]
            display_text.style = theme.typography.body(theme.text_primary)
            clear_btn.visible = True
            field_box.update()
            page.pop_dialog()
            if on_select:
                on_select(item)

        search = ft.TextField(
            hint_text=search_hint,
            autofocus=True,
            prefix_icon=ft.Icons.SEARCH,
            border=ft.InputBorder.OUTLINE,
            border_radius=theme.radius.MD,
            border_color=theme.border,
            focused_border_color=theme.primary,
            bgcolor=theme.surface,
            color=theme.text_primary,
            hint_style=theme.typography.body(theme.text_muted),
            content_padding=ft.Padding.symmetric(horizontal=12, vertical=10),
            on_change=lambda ev: _refresh(ev.control.value),
        )

        _refresh("", mounted=False)

        dialog = ft.AlertDialog(
            modal=True,
            bgcolor=theme.surface,
            title=ft.Text(dialog_title or f"Select {label}", style=theme.typography.section_title(theme.text_primary)),
            content=ft.Container(
                content=ft.Column(controls=[search, results_column], spacing=theme.spacing.SM, tight=True),
                width=420,
            ),
            actions=[
                GhostButton(theme, "Cancel", on_click=lambda ev: page.pop_dialog()),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        page.show_dialog(dialog)

    field_box = ft.Container(
        content=ft.Row(
            controls=[
                ft.Column(
                    controls=[
                        ft.Text(display_label, style=theme.typography.label(theme.text_secondary)),
                        display_text,
                    ],
                    spacing=2,
                    tight=True,
                    expand=True,
                ),
                clear_btn,
                ft.Icon(ft.Icons.SEARCH, size=18, color=theme.text_muted),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        ),
        bgcolor=theme.surface_variant if disabled else theme.surface,
        border=ft.Border.all(1, theme.border),
        border_radius=theme.radius.MD,
        padding=ft.Padding.symmetric(horizontal=12, vertical=8),
        width=width,
        on_click=None if disabled else _open_dialog,
        ink=not disabled,
    )
    return field_box

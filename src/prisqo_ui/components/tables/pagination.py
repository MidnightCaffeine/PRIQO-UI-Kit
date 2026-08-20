"""`Pagination` — reusable page navigation for `AppDataTable`."""
from __future__ import annotations

from typing import Callable, Optional

import flet as ft

from prisqo_ui.theme import Theme
from prisqo_ui.components.buttons.buttons import AppIconButton
from prisqo_ui.components.forms.fields import AppDropdown


def Pagination(
    theme: Theme,
    current_page: int,
    total_pages: int,
    page_size: int = 25,
    total_records: Optional[int] = None,
    page_size_options: tuple = (10, 25, 50, 100),
    on_page_change: Optional[Callable[[int], None]] = None,
    on_page_size_change: Optional[Callable[[int], None]] = None,
) -> ft.Row:
    total_pages = max(1, total_pages)
    current_page = max(1, min(current_page, total_pages))

    def _go(page_num: int) -> Callable:
        def _handler(e: ft.ControlEvent) -> None:
            if on_page_change and 1 <= page_num <= total_pages:
                on_page_change(page_num)

        return _handler

    left = ft.Row(
        controls=[
            ft.Text(
                f"Page {current_page} of {total_pages}" + (f" \u2022 {total_records} records" if total_records is not None else ""),
                style=theme.typography.body_small(theme.text_muted),
            ),
        ]
    )

    nav = ft.Row(
        controls=[
            AppIconButton(theme, ft.Icons.FIRST_PAGE, "First page", on_click=_go(1), disabled=current_page == 1),
            AppIconButton(theme, ft.Icons.CHEVRON_LEFT, "Previous page", on_click=_go(current_page - 1), disabled=current_page == 1),
            AppIconButton(theme, ft.Icons.CHEVRON_RIGHT, "Next page", on_click=_go(current_page + 1), disabled=current_page == total_pages),
            AppIconButton(theme, ft.Icons.LAST_PAGE, "Last page", on_click=_go(total_pages), disabled=current_page == total_pages),
        ],
        spacing=0,
    )

    page_size_dd = AppDropdown(
        theme,
        options=[str(s) for s in page_size_options],
        value=str(page_size),
        width=90,
        on_change=lambda e: on_page_size_change and on_page_size_change(int(e.control.value)),
    )

    return ft.Row(
        controls=[left, ft.Row(controls=[page_size_dd, nav], spacing=theme.spacing.MD)],
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
    )

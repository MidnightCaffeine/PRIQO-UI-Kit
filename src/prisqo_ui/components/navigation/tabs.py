"""`AppTabs` — built on the modern `ft.Tabs` / `ft.TabBar` / `ft.TabBarView`
trio (Flet 0.85.3's replacement for passing `tabs=[Tab(...)]` directly
into a single legacy `Tabs` control).
"""
from __future__ import annotations

from typing import Callable, Mapping, Optional, Sequence

import flet as ft

from prisqo_ui.theme import Theme


def AppTabs(
    theme: Theme,
    tabs: Sequence[Mapping],
    selected_index: int = 0,
    on_change: Optional[Callable] = None,
    height: Optional[float] = 420,
) -> ft.Tabs:
    """
    tabs: sequence of {"label": str, "content": ft.Control}
    """
    tab_bar = ft.TabBar(
        tabs=[ft.Tab(label=t["label"]) for t in tabs],
        label_color=theme.primary,
        unselected_label_color=theme.text_muted,
        indicator_color=theme.primary,
        divider_color=theme.divider,
        label_text_style=theme.typography.button(),
        unselected_label_text_style=theme.typography.button(),
    )
    tab_view = ft.TabBarView(controls=[t["content"] for t in tabs])
    return ft.Tabs(
        length=len(tabs),
        selected_index=selected_index,
        on_change=on_change,
        content=ft.Column(
            controls=[tab_bar, ft.Container(content=tab_view, height=height, expand=height is None)],
            spacing=0,
        ),
    )

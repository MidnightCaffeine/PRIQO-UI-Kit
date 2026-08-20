"""`AppShell` — combines Sidebar + Navbar + page content into the full
application frame, and owns the responsive behaviour between them.

Breakpoints follow `theme.breakpoint` (kept live by `ThemeManager` on
every page resize -- see `theme/breakpoints.py`):

- `lg` / `xl` and up: sidebar fully expanded, always visible, no hamburger.
- `md`:                sidebar collapsed to an icon rail, always visible,
                        no hamburger (icons + tooltips are enough at this
                        width, matching Bootstrap's `.navbar-expand-md`).
- `xs` / `sm`:          sidebar is hidden entirely and a hamburger button
                        appears in the navbar. Tapping it opens the full
                        sidebar as a temporary overlay drawer on top of the
                        content, with a scrim behind it -- tapping the
                        scrim (or the drawer's own close button) closes it.

Because `Sidebar` and `Navbar` need different props depending on that
state (collapsed rail vs. full drawer; hamburger vs. no hamburger),
`AppShell` takes *builder* callables rather than pre-built controls, so it
can decide `collapsed`/`on_menu_click` itself and hand them to the
builders:

    AppShell(
        theme,
        build_sidebar=lambda collapsed, on_close=None: Sidebar(theme, groups, collapsed=collapsed, on_close=on_close, ...),
        build_navbar=lambda on_menu_click: Navbar(theme, title="Dashboard", on_menu_click=on_menu_click, ...),
        content=page_content,
        drawer_open=state["sidebar_open"],
        on_toggle_drawer=toggle_drawer,
    )

The caller owns `drawer_open` as ordinary state (e.g. a dict entry
alongside whatever other page state it already tracks) and re-renders
when `on_toggle_drawer` fires, the same way the rest of this kit's
call-and-response demos already re-render on click.
"""
from __future__ import annotations

from typing import Callable, Optional

import flet as ft

from prisqo_ui.theme import Theme, breakpoint_at_most

SidebarBuilder = Callable[..., ft.Control]  # (collapsed: bool, on_close: Optional[Callable]) -> ft.Control
NavbarBuilder = Callable[[Optional[Callable]], ft.Control]  # (on_menu_click) -> ft.Control


def AppShell(
    theme: Theme,
    build_sidebar: SidebarBuilder,
    build_navbar: NavbarBuilder,
    content: ft.Control,
    *,
    drawer_open: bool = False,
    on_toggle_drawer: Optional[Callable[[bool], None]] = None,
) -> ft.Control:
    is_small = breakpoint_at_most(theme.breakpoint, "sm")
    is_medium = theme.breakpoint == "md"

    def _toggle(open_: bool) -> Callable:
        return lambda e: on_toggle_drawer(open_) if on_toggle_drawer else None

    if is_small:
        navbar = build_navbar(_toggle(True) if on_toggle_drawer else None)
        main_column = ft.Column(controls=[navbar, content], spacing=0, expand=True)

        if not drawer_open:
            return main_column

        drawer_sidebar = build_sidebar(False, _toggle(False) if on_toggle_drawer else None)
        scrim = ft.Container(
            bgcolor=ft.Colors.with_opacity(0.4, "#000000"),
            on_click=_toggle(False) if on_toggle_drawer else None,
            left=0,
            top=0,
            right=0,
            bottom=0,
            animate_opacity=150,
        )
        drawer = ft.Container(
            content=drawer_sidebar,
            left=0,
            top=0,
            bottom=0,
            animate=ft.Animation(150, ft.AnimationCurve.EASE_OUT),
            shadow=theme.shadows.card,
        )
        return ft.Stack(controls=[main_column, scrim, drawer], expand=True)

    # md and up: sidebar is always visible, collapsed to an icon rail at
    # `md`, fully expanded at `lg`+. No hamburger/drawer needed.
    sidebar = build_sidebar(is_medium, None)
    navbar = build_navbar(None)
    main_column = ft.Column(controls=[navbar, content], spacing=0, expand=True)
    return ft.Row(controls=[sidebar, main_column], spacing=0, expand=True)

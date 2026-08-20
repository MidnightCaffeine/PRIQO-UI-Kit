"""PRISQO UI KIT — component showcase application.

Run with `python main.py`. Lets you visually inspect every component in
both Light and Dark themes before copying them into PRISQO ERP.
"""
from __future__ import annotations

import flet as ft

from prisqo_ui.theme import ThemeManager, AppThemeMode, Theme
from prisqo_ui.components.layout import Sidebar, Navbar, PageContainer, AppShell

from showcase.pages import (
    overview,
    buttons_demo,
    cards_demo,
    forms_demo,
    lookups_demo,
    tables_demo,
    dialogs_demo,
    feedback_demo,
    status_demo,
    financial_demo,
    navigation_demo,
    pos_demo,
    pos_screen_demo,
    erp_demo,
    typography_demo,
)

PAGES = [
    ("overview", "Overview", ft.Icons.DASHBOARD_OUTLINED, overview),
    ("buttons", "Buttons", ft.Icons.SMART_BUTTON, buttons_demo),
    ("typography", "Typography", ft.Icons.TEXT_FIELDS, typography_demo),
    ("cards", "Cards", ft.Icons.DASHBOARD_CUSTOMIZE_OUTLINED, cards_demo),
    ("forms", "Forms", ft.Icons.EDIT_NOTE, forms_demo),
    ("lookups", "Lookups", ft.Icons.SEARCH, lookups_demo),
    ("tables", "Tables", ft.Icons.TABLE_CHART_OUTLINED, tables_demo),
    ("dialogs", "Dialogs", ft.Icons.CHAT_BUBBLE_OUTLINE, dialogs_demo),
    ("feedback", "Feedback", ft.Icons.NOTIFICATIONS_NONE, feedback_demo),
    ("status", "Status", ft.Icons.LABEL_OUTLINE, status_demo),
    ("financial", "Financial", ft.Icons.PAYMENTS_OUTLINED, financial_demo),
    ("navigation", "Navigation", ft.Icons.MENU_OPEN, navigation_demo),
    ("pos", "POS", ft.Icons.POINT_OF_SALE, pos_demo),
    ("pos_screen", "POS Screen (Full)", ft.Icons.STOREFRONT, pos_screen_demo),
    ("erp", "ERP Components", ft.Icons.BUSINESS_CENTER_OUTLINED, erp_demo),
]

PAGE_LOOKUP = {key: (title, icon, module) for key, title, icon, module in PAGES}


def main(page: ft.Page) -> None:
    page.title = "PRISQO UI KIT"
    page.padding = 0
    page.spacing = 0
    page.fonts = {}

    theme_manager = ThemeManager(page, initial_mode=AppThemeMode.LIGHT)
    state = {"active": "overview", "sidebar_open": False}

    content_area = ft.Container(expand=True)
    shell_holder = ft.Container(expand=True)

    def _theme_button(mode: AppThemeMode, label: str, icon: str) -> ft.Control:
        theme = theme_manager.theme
        active = theme_manager.mode == mode
        return ft.Container(
            content=ft.Row(
                controls=[ft.Icon(icon, size=15, color="#FFFFFF" if active else theme.text_secondary), ft.Text(label, style=theme.typography.caption("#FFFFFF" if active else theme.text_secondary))],
                spacing=4,
            ),
            bgcolor=theme.primary if active else theme.surface_variant,
            padding=ft.Padding.symmetric(horizontal=10, vertical=6),
            border_radius=theme.radius.MD,
            ink=True,
            on_click=lambda e, m=mode: theme_manager.set_mode(m),
        )

    def _toggle_drawer(open_: bool) -> None:
        state["sidebar_open"] = open_
        _render()

    def _render() -> None:
        theme = theme_manager.theme
        active_key = state["active"]
        title, icon, module = PAGE_LOOKUP[active_key]

        groups = [
            {
                "title": "PRISQO ERP",
                "items": [
                    {"key": key, "label": lbl, "icon": ic} for key, lbl, ic, _ in PAGES
                ],
            }
        ]

        def build_sidebar(collapsed: bool, on_close) -> ft.Control:
            return Sidebar(
                theme,
                groups,
                active_key=active_key,
                collapsed=collapsed,
                on_close=on_close,
                header=ft.Row(
                    controls=[
                        ft.Container(
                            content=ft.Icon(ft.Icons.HEXAGON, color=theme.primary, size=22),
                            bgcolor="#FFFFFF",
                            padding=6,
                            border_radius=theme.radius.MD,
                        ),
                        ft.Text("PRISQO UI KIT", style=theme.typography.card_title("#FFFFFF")) if not collapsed else ft.Container(),
                    ],
                    spacing=theme.spacing.SM,
                ),
                on_navigate=_navigate,
            )

        theme_switcher = ft.Row(
            controls=[
                _theme_button(AppThemeMode.LIGHT, "Light", ft.Icons.LIGHT_MODE),
                _theme_button(AppThemeMode.DARK, "Dark", ft.Icons.DARK_MODE),
                _theme_button(AppThemeMode.SYSTEM, "System", ft.Icons.SETTINGS_SUGGEST),
            ],
            spacing=6,
            wrap=True,
            run_spacing=6,
        )

        def build_navbar(on_menu_click) -> ft.Control:
            return Navbar(theme, title=title, actions=[theme_switcher], on_menu_click=on_menu_click)

        page_content = module.build(theme, page)
        container = PageContainer(theme, page_content, max_width=1180)

        shell_holder.content = AppShell(
            theme,
            build_sidebar=build_sidebar,
            build_navbar=build_navbar,
            content=container,
            drawer_open=state["sidebar_open"],
            on_toggle_drawer=_toggle_drawer,
        )
        page.bgcolor = theme.background
        page.update()

    def _navigate(key: str) -> None:
        state["active"] = key
        state["sidebar_open"] = False
        _render()

    theme_manager.subscribe(lambda theme: _render())

    page.add(shell_holder)
    _render()


def run() -> None:
    ft.app(target=main)

"""Semantic theme tokens + ThemeManager.

Components must only ever reference `Theme` fields (semantic tokens) —
never raw hex colors. This is what makes automatic light/dark support
possible without touching component source code.
"""
from __future__ import annotations

from dataclasses import dataclass, field, replace
from enum import Enum
from typing import Callable, List, Optional

import flet as ft

from .radius import RADIUS, Radius
from .spacing import SPACING, Spacing
from .typography import TYPOGRAPHY, Typography
from .shadows import Shadows
from .breakpoints import BREAKPOINTS, resolve_breakpoint


class AppThemeMode(str, Enum):
    LIGHT = "light"
    DARK = "dark"
    SYSTEM = "system"


@dataclass(frozen=True)
class Theme:
    """Semantic design tokens consumed by every reusable component."""

    mode: str  # "light" | "dark" — the *resolved* mode, never "system"

    # Surfaces
    background: str
    surface: str
    surface_variant: str

    # Sidebar (has its own palette — it stays dark-ish in both themes)
    sidebar_bg: str
    sidebar_text: str
    sidebar_text_muted: str
    sidebar_active_bg: str

    # Text
    text_primary: str
    text_secondary: str
    text_muted: str
    text_on_primary: str

    # Structure
    border: str
    divider: str

    # Brand / primary
    primary: str
    primary_hover: str
    primary_pressed: str
    primary_disabled: str
    primary_light: str

    # Semantic status colors
    success: str
    success_bg: str
    warning: str
    warning_bg: str
    danger: str
    danger_bg: str
    info: str
    info_bg: str

    neutral_bg: str
    neutral_text: str

    focus: str

    # Shared design-system building blocks
    spacing: Spacing = field(default_factory=lambda: SPACING)
    radius: Radius = field(default_factory=lambda: RADIUS)
    typography: Typography = field(default_factory=lambda: TYPOGRAPHY)
    shadows: Shadows = field(default_factory=Shadows)

    # Responsive: the breakpoint this Theme instance was resolved for
    # ("xs".."xxl", see `theme/breakpoints.py`). `typography` above is
    # already scaled for it -- this field exists so components that need
    # to change *layout* (not just text size) responsively -- e.g. a
    # sidebar collapsing to icons-only, a form going single-column -- can
    # branch on `theme.breakpoint` without importing the resolver
    # themselves. `ThemeManager` keeps it in sync with the page width.
    breakpoint: str = "lg"

    @property
    def is_dark(self) -> bool:
        return self.mode == "dark"


ThemeListener = Callable[[Theme], None]


class ThemeManager:
    """Owns the active `Theme`, the selected `AppThemeMode`, and notifies
    subscribed components when the resolved theme changes (mode switch,
    the OS-level brightness changing while in SYSTEM mode, or the page
    being resized across a responsive breakpoint -- see
    `theme/breakpoints.py`).
    """

    def __init__(self, page: ft.Page, initial_mode: AppThemeMode = AppThemeMode.LIGHT) -> None:
        from .light_theme import LIGHT_THEME
        from .dark_theme import DARK_THEME

        self._page = page
        self._light = LIGHT_THEME
        self._dark = DARK_THEME
        self._mode = initial_mode
        self._listeners: List[ThemeListener] = []
        self._breakpoint = resolve_breakpoint(page.width).name

        page.on_platform_brightness_change = self._on_platform_brightness_change
        # Chain any resize handler the host app already set, so adopting
        # ThemeManager's responsive typography doesn't silently break an
        # app's own `page.on_resize` usage.
        self._prior_on_resize: Optional[Callable] = page.on_resize
        page.on_resize = self._on_resize
        self._apply_to_page()

    # -- public API ---------------------------------------------------
    @property
    def mode(self) -> AppThemeMode:
        return self._mode

    @property
    def breakpoint(self) -> str:
        """Current responsive breakpoint name ("xs".."xxl"), kept in sync
        with the page width. Same value as `self.theme.breakpoint`.
        """
        return self._breakpoint

    @property
    def theme(self) -> Theme:
        base = self._base_theme()
        bp = resolve_breakpoint(self._page.width)
        if bp.typography_scale == base.typography.scale and bp.name == base.breakpoint:
            return base
        return replace(
            base,
            typography=replace(base.typography, scale=bp.typography_scale),
            breakpoint=bp.name,
        )

    def set_mode(self, mode: AppThemeMode) -> None:
        if mode == self._mode:
            return
        self._mode = mode
        self._apply_to_page()
        self._notify()

    def subscribe(self, listener: ThemeListener) -> Callable[[], None]:
        """Register a listener; returns an unsubscribe function."""
        self._listeners.append(listener)

        def unsubscribe() -> None:
            if listener in self._listeners:
                self._listeners.remove(listener)

        return unsubscribe

    # -- internals ------------------------------------------------------
    def _base_theme(self) -> Theme:
        if self._mode == AppThemeMode.DARK:
            return self._dark
        if self._mode == AppThemeMode.LIGHT:
            return self._light
        # SYSTEM -> resolve from platform brightness
        return self._dark if self._page.platform_brightness == ft.Brightness.DARK else self._light

    def _on_platform_brightness_change(self, e: ft.ControlEvent) -> None:
        if self._mode == AppThemeMode.SYSTEM:
            self._notify()

    def _on_resize(self, e: ft.ControlEvent) -> None:
        new_bp = resolve_breakpoint(self._page.width).name
        if new_bp != self._breakpoint:
            self._breakpoint = new_bp
            self._notify()
        if self._prior_on_resize is not None:
            self._prior_on_resize(e)

    def _apply_to_page(self) -> None:
        mapping = {
            AppThemeMode.LIGHT: ft.ThemeMode.LIGHT,
            AppThemeMode.DARK: ft.ThemeMode.DARK,
            AppThemeMode.SYSTEM: ft.ThemeMode.SYSTEM,
        }
        self._page.theme_mode = mapping[self._mode]
        self._page.bgcolor = self.theme.background
        self._page.update()

    def _notify(self) -> None:
        self._page.bgcolor = self.theme.background
        current = self.theme
        for listener in list(self._listeners):
            listener(current)
        self._page.update()

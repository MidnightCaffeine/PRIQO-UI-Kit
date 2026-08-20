"""Centralized typography scale — now responsive.

Each helper returns an `ft.TextStyle` for a semantic text role. Color is
passed in by the caller (usually a theme token) so the same scale works
for both light and dark themes without duplication.

`scale` makes the whole scale responsive, the same way Bootstrap's base
font size and `.display-*`/`.fs-*` utilities are tuned per breakpoint
rather than fixed at one pixel size regardless of viewport. `ThemeManager`
resolves the active breakpoint from the page width (see
`theme/breakpoints.py`) and hands back a `Theme` whose `typography` is a
copy of this scale with `scale` set accordingly — components never
compute this themselves, they just keep calling
`theme.typography.page_title(...)` etc. as before.

Sizes below are the ones this kit already shipped with (the `lg`
breakpoint / `scale=1.0` baseline); every other breakpoint is a
proportional adjustment of these, not a separately maintained scale.
"""
from dataclasses import dataclass

import flet as ft

FONT_FAMILY = "Segoe UI, Inter, Roboto, sans-serif"

# A floor so aggressive scale-down (e.g. a very narrow POS screen) never
# shrinks text past legibility -- mirrors how Bootstrap's fluid type
# (`clamp()`) is bounded on both ends rather than shrinking indefinitely.
_MIN_SIZE = 10


@dataclass(frozen=True)
class Typography:
    """Font-size / weight scale, independent of color.

    `scale` (default `1.0`) multiplies every size below. Don't set it
    directly on a shared instance -- `ThemeManager` produces a
    breakpoint-scaled copy per resolved `Theme` via
    `dataclasses.replace(typography, scale=...)`.
    """

    font_family: str = FONT_FAMILY
    scale: float = 1.0

    def _size(self, base: int) -> int:
        return max(_MIN_SIZE, round(base * self.scale))

    def page_title(self, color: str | None = None) -> ft.TextStyle:
        return ft.TextStyle(size=self._size(24), weight=ft.FontWeight.W_700, color=color, font_family=self.font_family)

    def section_title(self, color: str | None = None) -> ft.TextStyle:
        return ft.TextStyle(size=self._size(18), weight=ft.FontWeight.W_600, color=color, font_family=self.font_family)

    def card_title(self, color: str | None = None) -> ft.TextStyle:
        return ft.TextStyle(size=self._size(15), weight=ft.FontWeight.W_600, color=color, font_family=self.font_family)

    def body(self, color: str | None = None) -> ft.TextStyle:
        return ft.TextStyle(size=self._size(14), weight=ft.FontWeight.W_400, color=color, font_family=self.font_family)

    def body_small(self, color: str | None = None) -> ft.TextStyle:
        return ft.TextStyle(size=self._size(13), weight=ft.FontWeight.W_400, color=color, font_family=self.font_family)

    def caption(self, color: str | None = None) -> ft.TextStyle:
        return ft.TextStyle(size=self._size(12), weight=ft.FontWeight.W_400, color=color, font_family=self.font_family)

    def label(self, color: str | None = None) -> ft.TextStyle:
        return ft.TextStyle(size=self._size(12), weight=ft.FontWeight.W_600, color=color, font_family=self.font_family, letter_spacing=0.2)

    def button(self, color: str | None = None) -> ft.TextStyle:
        return ft.TextStyle(size=self._size(14), weight=ft.FontWeight.W_600, color=color, font_family=self.font_family)

    def table_header(self, color: str | None = None) -> ft.TextStyle:
        return ft.TextStyle(size=self._size(12), weight=ft.FontWeight.W_600, color=color, font_family=self.font_family, letter_spacing=0.3)

    def table_body(self, color: str | None = None) -> ft.TextStyle:
        return ft.TextStyle(size=self._size(13), weight=ft.FontWeight.W_400, color=color, font_family=self.font_family)

    def kpi(self, color: str | None = None) -> ft.TextStyle:
        return ft.TextStyle(size=self._size(26), weight=ft.FontWeight.W_700, color=color, font_family=self.font_family)

    def currency(self, color: str | None = None) -> ft.TextStyle:
        return ft.TextStyle(size=self._size(14), weight=ft.FontWeight.W_600, color=color, font_family=self.font_family)


TYPOGRAPHY = Typography()

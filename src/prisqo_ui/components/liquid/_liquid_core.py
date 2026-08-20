"""Shared "liquid" press/bounce interaction primitive.

Flet renders through Flutter, not a browser, so it has no equivalent to
the CSS/SVG `feGaussianBlur` + `feColorMatrix` "goo" filter trick used by
web-based liquid UI demos (metaballs merging into each other). This
module approximates the same *feel* — a soft squish on press and an
elastic overshoot on release — using Flet's native `animate_scale` +
`ELASTIC_OUT` easing, which is the closest native equivalent available.
"""
from __future__ import annotations

from typing import Callable, Optional

import flet as ft

from prisqo_ui.theme import Theme

PRESS_SCALE = 0.92
RELEASE_ANIMATION = ft.Animation(340, ft.AnimationCurve.ELASTIC_OUT)
PRESS_ANIMATION = ft.Animation(110, ft.AnimationCurve.EASE_OUT)
HOVER_ANIMATION = ft.Animation(180, ft.AnimationCurve.EASE_OUT)


def LiquidPressable(
    theme: Theme,
    content: ft.Control,
    bgcolor: str,
    on_click: Optional[Callable] = None,
    hover_bgcolor: Optional[str] = None,
    radius: Optional[int] = None,
    disabled: bool = False,
    width: Optional[float] = None,
    height: Optional[float] = None,
    tooltip: Optional[str] = None,
    border: Optional[ft.Border] = None,
    padding: Optional[ft.Padding] = None,
) -> ft.GestureDetector:
    """The base "liquid" interactive surface every liquid button/control
    is built on: squishes down on press, bounces back with an elastic
    overshoot on release, and lightens on hover.
    """
    box = ft.Container(
        content=content,
        bgcolor=theme.surface_variant if disabled else bgcolor,
        border=border,
        border_radius=radius if radius is not None else theme.radius.LG,
        width=width,
        height=height,
        padding=padding,
        alignment=ft.Alignment(0, 0),
        scale=1.0,
        animate_scale=RELEASE_ANIMATION,
        animate=HOVER_ANIMATION,
        opacity=0.55 if disabled else 1.0,
        tooltip=tooltip,
        clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
    )

    def _set_scale(value: float, animation: ft.Animation) -> None:
        box.animate_scale = animation
        box.scale = value
        box.update()

    def _tap_down(e: ft.ControlEvent) -> None:
        if disabled:
            return
        _set_scale(PRESS_SCALE, PRESS_ANIMATION)

    def _tap_up(e: ft.ControlEvent) -> None:
        if disabled:
            return
        _set_scale(1.0, RELEASE_ANIMATION)
        if on_click:
            on_click(e)

    def _tap_cancel(e: ft.ControlEvent) -> None:
        if disabled:
            return
        _set_scale(1.0, RELEASE_ANIMATION)

    def _hover(e: ft.ControlEvent) -> None:
        if disabled or not hover_bgcolor:
            return
        box.bgcolor = hover_bgcolor if e.data == "true" else bgcolor
        box.update()

    box.on_hover = _hover

    return ft.GestureDetector(
        content=box,
        mouse_cursor=ft.MouseCursor.FORBIDDEN if disabled else ft.MouseCursor.CLICK,
        on_tap_down=None if disabled else _tap_down,
        on_tap_up=None if disabled else _tap_up,
        on_tap_cancel=None if disabled else _tap_cancel,
    )

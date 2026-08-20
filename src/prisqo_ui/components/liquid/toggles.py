"""Liquid-style toggle controls.

Approximates the CodePen "liquid" checkbox/radio/switch feel (a dot that
elastically "drops" into place) using Flet's native `animate_position` /
`animate_scale` with `ELASTIC_OUT` easing -- the closest native
equivalent to the original SVG gooey-filter + GSAP implementation, which
has no direct counterpart in Flutter's rendering model.
"""
from __future__ import annotations

from typing import Callable, Mapping, Optional, Sequence

import flet as ft

from prisqo_ui.theme import Theme

BOUNCE = ft.Animation(360, ft.AnimationCurve.ELASTIC_OUT)
QUICK = ft.Animation(150, ft.AnimationCurve.EASE_OUT)


def LiquidSwitch(
    theme: Theme,
    value: bool = False,
    label: Optional[str] = None,
    disabled: bool = False,
    on_change: Optional[Callable[[bool], None]] = None,
    width: int = 46,
    height: int = 26,
) -> ft.Control:
    """A track + thumb switch where the thumb "drops" into place with an
    elastic bounce, and briefly stretches sideways mid-travel to suggest
    a liquid drop of momentum (approximating the gooey merge effect).
    """
    thumb_size = height - 6
    pad = 3
    state = {"on": value}

    def _thumb_left(on: bool) -> float:
        return (width - thumb_size - pad) if on else pad

    track = ft.Container(
        width=width,
        height=height,
        border_radius=height / 2,
        bgcolor=(theme.text_muted if disabled else theme.primary) if state["on"] else theme.border,
        animate=QUICK,
    )
    thumb = ft.Container(
        width=thumb_size,
        height=thumb_size,
        left=_thumb_left(state["on"]),
        top=pad,
        border_radius=thumb_size / 2,
        bgcolor="#FFFFFF",
        animate_position=BOUNCE,
        animate=ft.Animation(160, ft.AnimationCurve.EASE_OUT),
        shadow=theme.shadows.card,
    )
    stack = ft.Stack(controls=[track, thumb], width=width, height=height)

    def _toggle(e: ft.ControlEvent) -> None:
        if disabled:
            return
        state["on"] = not state["on"]
        track.bgcolor = theme.primary if state["on"] else theme.border
        # A quick sideways stretch mid-flight suggests liquid momentum,
        # then the elastic position animation settles it into place.
        thumb.width = thumb_size + 6
        thumb.left = _thumb_left(state["on"]) - (3 if state["on"] else -3)
        thumb.update()
        thumb.width = thumb_size
        thumb.left = _thumb_left(state["on"])
        thumb.update()
        track.update()
        if on_change:
            on_change(state["on"])

    control = ft.GestureDetector(
        content=stack,
        mouse_cursor=ft.MouseCursor.FORBIDDEN if disabled else ft.MouseCursor.CLICK,
        on_tap_up=None if disabled else _toggle,
    )

    if not label:
        return control

    return ft.Row(
        controls=[control, ft.Text(label, style=theme.typography.body(theme.text_muted if disabled else theme.text_primary))],
        spacing=theme.spacing.SM,
    )


def LiquidCheckbox(
    theme: Theme,
    value: bool = False,
    label: Optional[str] = None,
    disabled: bool = False,
    on_change: Optional[Callable[[bool], None]] = None,
    size: int = 22,
) -> ft.Control:
    """A checkbox whose fill + checkmark scale in with an elastic
    overshoot when checked, rather than simply appearing.
    """
    state = {"on": value}

    check_icon = ft.Icon(
        ft.Icons.CHECK_ROUNDED,
        size=size * 0.7,
        color="#FFFFFF",
        scale=1.0 if state["on"] else 0.0,
        animate_scale=BOUNCE,
        opacity=1.0 if state["on"] else 0.0,
        animate_opacity=QUICK,
    )
    box = ft.Container(
        width=size,
        height=size,
        border_radius=theme.radius.SM,
        bgcolor=theme.primary if state["on"] else theme.surface,
        border=ft.Border.all(2, theme.border if not state["on"] else theme.primary),
        alignment=ft.Alignment(0, 0),
        content=check_icon,
        animate=QUICK,
        scale=1.0,
        animate_scale=BOUNCE,
    )

    def _toggle(e: ft.ControlEvent) -> None:
        if disabled:
            return
        state["on"] = not state["on"]
        box.bgcolor = theme.primary if state["on"] else theme.surface
        box.border = ft.Border.all(2, theme.primary if state["on"] else theme.border)
        box.scale = 1.12
        check_icon.scale = 1.0 if state["on"] else 0.0
        check_icon.opacity = 1.0 if state["on"] else 0.0
        box.update()
        box.scale = 1.0
        box.update()
        if on_change:
            on_change(state["on"])

    control = ft.GestureDetector(
        content=box,
        mouse_cursor=ft.MouseCursor.FORBIDDEN if disabled else ft.MouseCursor.CLICK,
        on_tap_up=None if disabled else _toggle,
    )

    if not label:
        return control

    return ft.GestureDetector(
        content=ft.Row(
            controls=[
                box,
                ft.Text(label, style=theme.typography.body(theme.text_muted if disabled else theme.text_primary)),
            ],
            spacing=theme.spacing.SM,
        ),
        mouse_cursor=ft.MouseCursor.FORBIDDEN if disabled else ft.MouseCursor.CLICK,
        on_tap_up=None if disabled else _toggle,
    )


def LiquidRadioGroup(
    theme: Theme,
    options: Sequence[Mapping],
    value: Optional[str] = None,
    disabled: bool = False,
    on_change: Optional[Callable[[str], None]] = None,
    size: int = 20,
    vertical: bool = True,
) -> ft.Control:
    """
    options: sequence of {"key": str, "label": str}

    Each option's inner dot scales in with an elastic bounce when
    selected -- the closest native approximation to the original
    liquid-drop radio animation.
    """
    state = {"value": value}
    dots: dict[str, ft.Container] = {}
    outers: dict[str, ft.Container] = {}

    def _build_option(opt: Mapping) -> ft.Control:
        key = opt["key"]
        selected = key == state["value"]
        dot = ft.Container(
            width=size * 0.5,
            height=size * 0.5,
            border_radius=size,
            bgcolor=theme.primary,
            scale=1.0 if selected else 0.0,
            animate_scale=BOUNCE,
        )
        outer = ft.Container(
            width=size,
            height=size,
            border_radius=size,
            border=ft.Border.all(2, theme.primary if selected else theme.border),
            alignment=ft.Alignment(0, 0),
            content=dot,
            animate=QUICK,
        )
        dots[key] = dot
        outers[key] = outer

        row = ft.Row(
            controls=[outer, ft.Text(opt["label"], style=theme.typography.body(theme.text_muted if disabled else theme.text_primary))],
            spacing=theme.spacing.SM,
        )
        return ft.GestureDetector(
            content=row,
            mouse_cursor=ft.MouseCursor.FORBIDDEN if disabled else ft.MouseCursor.CLICK,
            on_tap_up=None if disabled else (lambda e, k=key: _select(k)),
        )

    def _select(key: str) -> None:
        if disabled or key == state["value"]:
            return
        previous = state["value"]
        state["value"] = key
        if previous in dots:
            dots[previous].scale = 0.0
            outers[previous].border = ft.Border.all(2, theme.border)
            dots[previous].update()
            outers[previous].update()
        dots[key].scale = 1.0
        outers[key].border = ft.Border.all(2, theme.primary)
        dots[key].update()
        outers[key].update()
        if on_change:
            on_change(key)

    items = [_build_option(o) for o in options]
    return (
        ft.Column(controls=items, spacing=theme.spacing.MD, tight=True)
        if vertical
        else ft.Row(controls=items, spacing=theme.spacing.LG, wrap=True, run_spacing=theme.spacing.SM)
    )

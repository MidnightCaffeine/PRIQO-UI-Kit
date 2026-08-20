"""Feedback components — toasts, loading, skeletons, empty/error states.

The design principle here (section 31/32/33 of the spec) is: never show
a blank screen while data loads, and never leak raw exceptions to the UI.

`Toast`/`Snackbar` render via `notification_center.notify` — a custom
top-right-by-default overlay notification (not `ft.SnackBar`, which
Flutter always anchors to the bottom of the screen and can't be
repositioned). See `notification_center.py` for the full customization
surface (title, icon, position, actions, sticky/duration, or a complete
custom `content` control — SweetAlert-`Swal.fire()`-style).
"""
from __future__ import annotations

from typing import Callable, Optional, Sequence

import flet as ft

from prisqo_ui.theme import Theme
from prisqo_ui.components.core.variants import VariantName
from .notification_center import notify, Position


def _tone_colors(theme: Theme, tone: str) -> tuple[str, str]:
    return {
        "success": (theme.success, theme.success_bg),
        "warning": (theme.warning, theme.warning_bg),
        "danger": (theme.danger, theme.danger_bg),
        "info": (theme.info, theme.info_bg),
    }.get(tone, (theme.text_primary, theme.surface_variant))


def Toast(
    theme: Theme,
    page: ft.Page,
    message: str,
    tone: VariantName = "info",
    *,
    title: Optional[str] = None,
    icon: Optional[str] = None,
    position: Position = "top-right",
    duration_ms: int = 3000,
    closable: bool = True,
    actions: Optional[Sequence[ft.Control]] = None,
    content: Optional[ft.Control] = None,
) -> Callable[[], None]:
    """A brief, self-dismissing notification. Shows immediately, top-right
    by default. Returns a `dismiss()` callable if you need to close it early.
    """
    return notify(
        theme,
        page,
        message,
        tone,
        title=title,
        icon=icon,
        position=position,
        duration_ms=duration_ms,
        closable=closable,
        actions=actions,
        content=content,
    )


def Snackbar(
    theme: Theme,
    page: ft.Page,
    message: str,
    action_label: Optional[str] = None,
    on_action: Optional[Callable] = None,
    tone: VariantName = "info",
    *,
    position: Position = "top-right",
    duration_ms: int = 5000,
) -> Callable[[], None]:
    """A notification bar with an optional action (Undo, Retry, ...)."""
    color, _ = _tone_colors(theme, tone)
    actions = None
    if action_label:
        def _run_action(e: ft.ControlEvent) -> None:
            dismiss()
            if on_action:
                on_action(e)

        actions = [ft.TextButton(text=action_label, on_click=_run_action, style=ft.ButtonStyle(color=color))]

    dismiss = notify(
        theme,
        page,
        message,
        tone,
        position=position,
        duration_ms=duration_ms,
        actions=actions,
    )
    return dismiss


def LoadingSpinner(theme: Theme, label: Optional[str] = None, size: int = 24) -> ft.Column:
    controls = [ft.ProgressRing(width=size, height=size, stroke_width=2.5, color=theme.primary)]
    if label:
        controls.append(ft.Text(label, style=theme.typography.body_small(theme.text_muted)))
    return ft.Column(controls=controls, horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=theme.spacing.SM, tight=True)


def _skeleton_block(theme: Theme, width: Optional[float], height: float, radius: Optional[int] = None) -> ft.Container:
    return ft.Container(
        width=width,
        height=height,
        bgcolor=theme.surface_variant,
        border_radius=radius if radius is not None else theme.radius.SM,
        animate_opacity=ft.Animation(700, ft.AnimationCurve.EASE_IN_OUT),
    )


def SkeletonText(theme: Theme, lines: int = 3, width: Optional[float] = None) -> ft.Column:
    widths = [width or 260, (width or 260) * 0.8, (width or 260) * 0.6]
    return ft.Column(
        controls=[_skeleton_block(theme, widths[i % 3], 12) for i in range(lines)],
        spacing=theme.spacing.SM,
        tight=True,
    )


def SkeletonCircle(theme: Theme, size: int = 40) -> ft.Container:
    return _skeleton_block(theme, size, size, radius=theme.radius.ROUND)


def SkeletonCard(theme: Theme) -> ft.Container:
    return ft.Container(
        content=ft.Column(
            controls=[
                ft.Row(controls=[SkeletonCircle(theme, 36), _skeleton_block(theme, 120, 14)], spacing=theme.spacing.SM),
                _skeleton_block(theme, None, 14),
                _skeleton_block(theme, 180, 14),
            ],
            spacing=theme.spacing.MD,
            tight=True,
        ),
        bgcolor=theme.surface,
        border=ft.Border.all(1, theme.border),
        border_radius=theme.radius.LG,
        padding=theme.spacing.LG,
    )


def SkeletonTable(theme: Theme, rows: int = 5, columns: int = 4) -> ft.Column:
    header = ft.Row(controls=[_skeleton_block(theme, 90, 12) for _ in range(columns)], spacing=theme.spacing.LG)
    body_rows = [
        ft.Row(controls=[_skeleton_block(theme, 90, 12) for _ in range(columns)], spacing=theme.spacing.LG)
        for _ in range(rows)
    ]
    return ft.Column(controls=[header, ft.Divider(height=1, color=theme.divider), *body_rows], spacing=theme.spacing.MD, tight=True)


def SkeletonDashboard(theme: Theme) -> ft.Column:
    kpis = ft.Row(controls=[SkeletonCard(theme) for _ in range(3)], spacing=theme.spacing.MD)
    return ft.Column(controls=[kpis, SkeletonTable(theme)], spacing=theme.spacing.LG, tight=True)


def EmptyState(
    theme: Theme,
    title: str,
    description: Optional[str] = None,
    icon: str = None,
    action: Optional[ft.Control] = None,
) -> ft.Container:
    controls = [
        ft.Icon(icon or ft.Icons.INBOX, size=40, color=theme.text_muted),
        ft.Text(title, style=theme.typography.section_title(theme.text_primary)),
    ]
    if description:
        controls.append(ft.Text(description, style=theme.typography.body_small(theme.text_muted), text_align=ft.TextAlign.CENTER))
    if action:
        controls.append(ft.Container(content=action, padding=ft.Padding.only(top=theme.spacing.SM)))
    return ft.Container(
        content=ft.Column(
            controls=controls,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=theme.spacing.SM,
            tight=True,
        ),
        padding=theme.spacing.XXL,
        alignment=ft.Alignment(0, 0),
    )


def ErrorState(
    theme: Theme,
    title: str = "Something went wrong",
    description: Optional[str] = None,
    action: Optional[ft.Control] = None,
) -> ft.Container:
    """Never expose raw technical exceptions here — keep `description` user-friendly."""
    controls = [
        ft.Icon(ft.Icons.ERROR_OUTLINE, size=40, color=theme.danger),
        ft.Text(title, style=theme.typography.section_title(theme.text_primary)),
    ]
    if description:
        controls.append(ft.Text(description, style=theme.typography.body_small(theme.text_muted), text_align=ft.TextAlign.CENTER))
    if action:
        controls.append(ft.Container(content=action, padding=ft.Padding.only(top=theme.spacing.SM)))
    return ft.Container(
        content=ft.Column(
            controls=controls,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=theme.spacing.SM,
            tight=True,
        ),
        padding=theme.spacing.XXL,
        alignment=ft.Alignment(0, 0),
    )

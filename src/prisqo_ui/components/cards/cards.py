"""Card components — the primary surface for grouping ERP content."""
from __future__ import annotations

from typing import Callable, Optional, Sequence

import flet as ft

from prisqo_ui.theme import Theme
from prisqo_ui.components.core.variants import VariantName, resolve_variant


def AppCard(
    theme: Theme,
    content: ft.Control,
    title: Optional[str] = None,
    subtitle: Optional[str] = None,
    icon: Optional[str] = None,
    actions: Optional[Sequence[ft.Control]] = None,
    footer: Optional[ft.Control] = None,
    on_click: Optional[Callable] = None,
    padding: Optional[int] = None,
    variant: Optional[VariantName] = None,
    width: Optional[float] = None,
) -> ft.Container:
    """The base card surface. Every other card in this library composes it.

    `variant`, if passed, adds a `.card.border-{variant}`-style 3px accent
    on the card's left edge (via `resolve_variant`) -- the same variant
    engine `Button`/`StatusChip`/`Alert` use. Leave it `None` for the
    default neutral card border.

    `width` is optional and left `None` by default (the card sizes to its
    content/parent, same as before) -- pass it when placing the card in a
    fixed-width grid slot. Overflow handling below (`max_lines` + ellipsis
    on title/subtitle, `wrap=True` on the icon+title row) degrades safely
    either way: it only changes anything once something upstream actually
    bounds the card's width, so it never breaks the unbounded/auto-sized
    layouts already used throughout the showcase.
    """
    header_row: Optional[ft.Control] = None
    if title or icon or actions:
        header_children = []
        if icon:
            header_children.append(
                ft.Container(
                    content=ft.Icon(icon, color=theme.primary, size=18),
                    bgcolor=theme.primary_light,
                    padding=8,
                    border_radius=theme.radius.MD,
                )
            )
        if title or subtitle:
            title_col = ft.Column(spacing=2, tight=True)
            if title:
                title_col.controls.append(
                    ft.Text(
                        title,
                        style=theme.typography.card_title(theme.text_primary),
                        max_lines=1,
                        overflow=ft.TextOverflow.ELLIPSIS,
                    )
                )
            if subtitle:
                title_col.controls.append(
                    ft.Text(
                        subtitle,
                        style=theme.typography.body_small(theme.text_muted),
                        max_lines=1,
                        overflow=ft.TextOverflow.ELLIPSIS,
                    )
                )
            header_children.append(title_col)
        header_row = ft.Row(
            controls=[
                # `wrap=True` here means a long title/subtitle that can't sit
                # comfortably next to the icon drops to its own line instead
                # of being clipped or pushing the card wider than its
                # container -- the same flex-wrap idiom `FlexRow` uses.
                ft.Row(controls=header_children, spacing=theme.spacing.SM, expand=True, wrap=True, run_spacing=4),
                ft.Row(controls=list(actions or []), spacing=theme.spacing.SM, wrap=True, run_spacing=4),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        )

    body_children = []
    if header_row is not None:
        body_children.append(header_row)
    body_children.append(content)
    if footer is not None:
        body_children.append(ft.Divider(height=1, color=theme.divider))
        body_children.append(footer)

    accent_border = None
    if variant is not None:
        accent = resolve_variant(theme, variant)
        accent_border = ft.Border(
            left=ft.BorderSide(3, accent.solid),
            top=ft.BorderSide(1, theme.border),
            right=ft.BorderSide(1, theme.border),
            bottom=ft.BorderSide(1, theme.border),
        )

    return ft.Container(
        content=ft.Column(controls=body_children, spacing=theme.spacing.MD, tight=True, horizontal_alignment=ft.CrossAxisAlignment.STRETCH),
        bgcolor=theme.surface,
        border=accent_border or ft.Border.all(1, theme.border),
        border_radius=theme.radius.LG,
        padding=padding if padding is not None else theme.spacing.LG,
        shadow=theme.shadows.card,
        on_click=on_click,
        ink=on_click is not None,
        animate=ft.Animation(120, ft.AnimationCurve.EASE_OUT),
        width=width,
        clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
    )


def SectionCard(
    theme: Theme,
    title: str,
    content: ft.Control,
    subtitle: Optional[str] = None,
    actions: Optional[Sequence[ft.Control]] = None,
) -> ft.Container:
    """A card used to group a labelled section of a form or a page."""
    return AppCard(theme=theme, content=content, title=title, subtitle=subtitle, actions=actions)


def _trend_color(theme: Theme, trend: Optional[str]) -> str:
    if not trend:
        return theme.text_muted
    return theme.success if trend.strip().startswith("+") else theme.danger if trend.strip().startswith("-") else theme.text_muted


def KPICard(
    theme: Theme,
    title: str,
    value: str,
    trend: Optional[str] = None,
    trend_label: Optional[str] = None,
    icon: Optional[str] = None,
    width: Optional[float] = None,
) -> ft.Container:
    """A headline number card, e.g. Today's Sales, Open Orders, Low Stock Items."""
    trend_row: Optional[ft.Control] = None
    if trend:
        trend_icon = ft.Icons.ARROW_UPWARD if trend.strip().startswith("+") else (
            ft.Icons.ARROW_DOWNWARD if trend.strip().startswith("-") else ft.Icons.REMOVE
        )
        color = _trend_color(theme, trend)
        trend_row = ft.Row(
            controls=[
                ft.Icon(trend_icon, size=14, color=color),
                ft.Text(trend, style=theme.typography.caption(color)),
                ft.Text(
                    trend_label or "",
                    style=theme.typography.caption(theme.text_muted),
                    max_lines=1,
                    overflow=ft.TextOverflow.ELLIPSIS,
                )
                if trend_label
                else ft.Container(),
            ],
            spacing=4,
            wrap=True,
            run_spacing=2,
        )

    header = ft.Row(
        controls=[
            ft.Text(title, style=theme.typography.label(theme.text_muted), max_lines=1, overflow=ft.TextOverflow.ELLIPSIS, expand=True),
            ft.Icon(icon, size=18, color=theme.text_muted) if icon else ft.Container(),
        ],
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
    )

    content = ft.Column(
        controls=[
            header,
            ft.Text(value, style=theme.typography.kpi(theme.text_primary), max_lines=1, overflow=ft.TextOverflow.ELLIPSIS),
            trend_row if trend_row else ft.Container(),
        ],
        spacing=theme.spacing.SM,
        tight=True,
    )

    return ft.Container(
        content=content,
        bgcolor=theme.surface,
        border=ft.Border.all(1, theme.border),
        border_radius=theme.radius.LG,
        padding=theme.spacing.LG,
        shadow=theme.shadows.card,
        width=width,
        clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
    )


def StatCard(
    theme: Theme,
    label: str,
    value: str,
    icon: Optional[str] = None,
    color: Optional[str] = None,
    width: Optional[float] = None,
) -> ft.Container:
    """A compact stat tile — used for dashboards with many small numbers."""
    accent = color or theme.primary
    return ft.Container(
        content=ft.Row(
            controls=[
                ft.Container(
                    content=ft.Icon(icon, color=accent, size=20) if icon else ft.Container(),
                    bgcolor=ft.Colors.with_opacity(0.12, accent),
                    padding=10,
                    border_radius=theme.radius.MD,
                    visible=icon is not None,
                ),
                ft.Column(
                    controls=[
                        ft.Text(value, style=theme.typography.section_title(theme.text_primary), max_lines=1, overflow=ft.TextOverflow.ELLIPSIS),
                        ft.Text(label, style=theme.typography.body_small(theme.text_muted), max_lines=1, overflow=ft.TextOverflow.ELLIPSIS),
                    ],
                    spacing=2,
                    tight=True,
                    expand=True,
                ),
            ],
            spacing=theme.spacing.MD,
        ),
        bgcolor=theme.surface,
        border=ft.Border.all(1, theme.border),
        border_radius=theme.radius.LG,
        padding=theme.spacing.MD,
        width=width,
        clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
    )


def MetricCard(
    theme: Theme,
    title: str,
    value: str,
    delta: Optional[str] = None,
    delta_positive: bool = True,
    footer_note: Optional[str] = None,
    width: Optional[float] = None,
) -> ft.Container:
    """A metric card with a value and an optional delta badge."""
    delta_badge = None
    if delta:
        color = theme.success if delta_positive else theme.danger
        bg = theme.success_bg if delta_positive else theme.danger_bg
        delta_badge = ft.Container(
            content=ft.Text(delta, style=theme.typography.caption(color), max_lines=1, overflow=ft.TextOverflow.ELLIPSIS),
            bgcolor=bg,
            padding=ft.Padding.symmetric(horizontal=8, vertical=2),
            border_radius=theme.radius.ROUND,
        )
    return ft.Container(
        content=ft.Column(
            controls=[
                ft.Text(title, style=theme.typography.body_small(theme.text_muted), max_lines=1, overflow=ft.TextOverflow.ELLIPSIS),
                ft.Row(
                    controls=[
                        ft.Text(value, style=theme.typography.section_title(theme.text_primary), max_lines=1, overflow=ft.TextOverflow.ELLIPSIS, expand=True),
                        delta_badge if delta_badge else ft.Container(),
                    ],
                    spacing=theme.spacing.SM,
                ),
                ft.Text(footer_note, style=theme.typography.caption(theme.text_muted), max_lines=1, overflow=ft.TextOverflow.ELLIPSIS) if footer_note else ft.Container(),
            ],
            spacing=6,
            tight=True,
        ),
        bgcolor=theme.surface,
        border=ft.Border.all(1, theme.border),
        border_radius=theme.radius.LG,
        padding=theme.spacing.MD,
        width=width,
        clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
    )

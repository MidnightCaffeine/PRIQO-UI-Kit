"""The shared engine behind `Toast`, `Snackbar`, and `ToastService`.

Flet's built-in `ft.SnackBar` is a Flutter `Scaffold` feature: it is
always anchored to the *bottom* of the screen, and neither Flutter nor
Flet expose a way to move it. To place notifications in the upper-right
corner (SweetAlert/Toastify-style, and the position most desktop/ERP UIs
default to) they can't be built from `ft.SnackBar` at all -- they have to
be plain controls placed in `page.overlay` and positioned by hand.

`notify()` below is that: it renders a small card into a per-position
overlay host (created once per `page`, reused after that) that stacks
top-right (or wherever `position` says), auto-dismisses on a timer,
and is fully content-customizable the way SweetAlert's `Swal.fire()` is
-- a `title`, an `icon`/`variant`, `actions` (buttons), or a complete
`content` control override for anything bespoke.

`Toast`, `Snackbar`, and `ToastService` in this package are all thin
call-signature-compatible wrappers around this one engine, so existing
call sites (`Toast(theme, page, "Saved.")`, `toast.success(...)`) don't
need to change to get the new positioning -- only code that wants the
new customization options (`title=`, `icon=`, `position=`, `actions=`)
needs to pass them.
"""
from __future__ import annotations

import asyncio
from typing import Callable, Optional, Sequence

import flet as ft

from prisqo_ui.theme import Theme
from prisqo_ui.components.core.variants import VariantName, resolve_variant

Position = str  # "top-right" | "top-left" | "top-center" | "bottom-right" | "bottom-left" | "bottom-center"

_DEFAULT_POSITION: Position = "top-right"
_MARGIN = 16

_TONE_ICON = {
    "success": ft.Icons.CHECK_CIRCLE_OUTLINE,
    "danger": ft.Icons.ERROR_OUTLINE,
    "warning": ft.Icons.WARNING_AMBER_OUTLINED,
    "info": ft.Icons.INFO_OUTLINE,
    "neutral": ft.Icons.INFO_OUTLINE,
}

_HOSTS_ATTR = "_prisqo_notification_hosts"


def _position_kwargs(position: Position) -> dict:
    kwargs: dict = {}
    if "top" in position:
        kwargs["top"] = _MARGIN
    if "bottom" in position:
        kwargs["bottom"] = _MARGIN
    if "center" in position:
        kwargs["left"] = 0
        kwargs["right"] = 0
    else:
        if "right" in position:
            kwargs["right"] = _MARGIN
        if "left" in position:
            kwargs["left"] = _MARGIN
    return kwargs


def _alignment_for(position: Position) -> str:
    if "center" in position:
        return ft.CrossAxisAlignment.CENTER
    if "right" in position:
        return ft.CrossAxisAlignment.END
    return ft.CrossAxisAlignment.START


def _get_host(page: ft.Page, position: Position) -> ft.Column:
    """Returns the (created-once) overlay column that notifications at
    `position` get inserted into, creating it on first use."""
    hosts = getattr(page, _HOSTS_ATTR, None)
    if hosts is None:
        hosts = {}
        setattr(page, _HOSTS_ATTR, hosts)
    if position not in hosts:
        column = ft.Column(spacing=10, tight=True, horizontal_alignment=_alignment_for(position))
        container = ft.Container(content=column, width=380, **_position_kwargs(position))
        page.overlay.append(container)
        hosts[position] = column
    return hosts[position]


def dismiss_all(page: ft.Page, position: Optional[Position] = None) -> None:
    """Clears active notifications -- all of them, or just one `position`."""
    hosts = getattr(page, _HOSTS_ATTR, None)
    if not hosts:
        return
    targets = [hosts[position]] if position else list(hosts.values())
    for column in targets:
        column.controls.clear()
    if page:
        page.update()


def _dismiss(page: ft.Page, column: ft.Column, card: ft.Control) -> None:
    if card in column.controls:
        column.controls.remove(card)
        try:
            page.update()
        except Exception:
            pass


async def _auto_dismiss(page: ft.Page, column: ft.Column, card: ft.Control, duration_ms: int) -> None:
    await asyncio.sleep(duration_ms / 1000)
    _dismiss(page, column, card)


def notify(
    theme: Theme,
    page: ft.Page,
    message: str = "",
    tone: VariantName = "info",
    *,
    title: Optional[str] = None,
    icon: Optional[str] = None,
    position: Position = _DEFAULT_POSITION,
    duration_ms: Optional[int] = 3000,
    closable: bool = True,
    actions: Optional[Sequence[ft.Control]] = None,
    content: Optional[ft.Control] = None,
    on_close: Optional[Callable] = None,
) -> Callable[[], None]:
    """Renders one notification card and returns a `dismiss()` callable
    (call it to close the card early, e.g. after an Undo action runs).

    `duration_ms=None` makes the notification sticky -- it stays until the
    user dismisses it (via the close button) or `dismiss()`/`dismiss_all()`
    is called; useful when `actions` require a decision.
    """
    try:
        column = _get_host(page, position)
        colors = resolve_variant(theme, tone)

        if content is not None:
            body: ft.Control = content
        else:
            text_controls = []
            if title:
                text_controls.append(ft.Text(title, style=theme.typography.label(theme.text_primary)))
            text_controls.append(
                ft.Text(
                    message,
                    style=theme.typography.body_small(theme.text_secondary if title else theme.text_primary),
                    max_lines=4,
                    overflow=ft.TextOverflow.ELLIPSIS,
                )
            )
            body = ft.Column(controls=text_controls, spacing=2, tight=True)

        card_holder = {"card": None}

        def _close(e: Optional[ft.ControlEvent] = None) -> None:
            _dismiss(page, column, card_holder["card"])
            if on_close:
                on_close(e)

        row_children = [
            ft.Icon(icon or _TONE_ICON.get(tone, ft.Icons.INFO_OUTLINE), color=colors.solid, size=20),
            ft.Container(content=body, expand=True),
        ]
        if closable:
            # `ft.IconButton` carries its own ~8px built-in hit-padding, so
            # centering it against the message text (rather than the old
            # `START` alignment, which pinned it to the top and made it
            # look offset whenever the message was a single line) needs
            # that padding zeroed out too, or the text still reads as
            # sitting above/below the button instead of level with it.
            row_children.append(
                ft.IconButton(
                    icon=ft.Icons.CLOSE,
                    icon_size=16,
                    icon_color=theme.text_muted,
                    on_click=_close,
                    tooltip="Dismiss",
                    style=ft.ButtonStyle(padding=0),
                    width=24,
                    height=24,
                )
            )

        column_children = [ft.Row(controls=row_children, spacing=theme.spacing.SM, vertical_alignment=ft.CrossAxisAlignment.CENTER)]
        if actions:
            column_children.append(ft.Row(controls=list(actions), spacing=theme.spacing.SM, wrap=True, run_spacing=4))

        card = ft.Container(
            content=ft.Column(controls=column_children, spacing=theme.spacing.SM, tight=True),
            bgcolor=theme.surface,
            border=ft.Border.all(1, theme.border),
            border_radius=theme.radius.MD,
            padding=theme.spacing.MD,
            shadow=theme.shadows.card,
            width=360,
            animate_opacity=200,
        )
        card_holder["card"] = card

        # Newest-on-top for the common top-anchored positions (matches
        # SweetAlert/Toastify convention); newest-at-bottom otherwise.
        if position.startswith("top"):
            column.controls.insert(0, card)
        else:
            column.controls.append(card)
        page.update()

        if duration_ms:
            try:
                page.run_task(_auto_dismiss, page, column, card, duration_ms)
            except Exception:
                # If this Flet build doesn't support `page.run_task`, degrade
                # gracefully to a sticky notification (manual close still
                # works) rather than crashing the app.
                pass

        return _close
    except Exception:
        # A notification failing to render should never crash the app.
        return lambda: None

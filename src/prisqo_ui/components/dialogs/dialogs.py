"""Dialog components.

All dialogs share the same header/content/footer structure and are
opened via `page.show_dialog(...)` (the Flet 0.85.3 API) and dismissed
via `page.pop_dialog()`.

Responsive sizing (see `_dialog_shell`): every dialog here sizes itself
to its content and never exceeds the viewport. Width is clamped to the
page width so a dialog never overflows horizontally on a narrow/mobile
screen, and height is capped to a share of the viewport with the content
area becoming internally scrollable once it would otherwise push the
dialog (or its action buttons) off-screen.

Field layout inside a dialog: reach for `FlexRow` (not `FormRow`) when
laying out multiple fields side by side. `FormRow` wraps at breakpoints
based on the *page's* width (via `ft.ResponsiveRow`), which is usually
much wider than the dialog itself, so a `FormRow` inside a 420-480px
dialog will still try to fit 2-3 fields per line and overflow. `FlexRow`
wraps based on the actual width it's given, which inside a dialog is the
dialog's own (already-clamped) content width -- exactly the "make the
field narrower or move it to the next line" behavior a modal needs.
"""
from __future__ import annotations

import inspect
from typing import Callable, Optional, Sequence

import flet as ft

from prisqo_ui.theme import Theme
from prisqo_ui.components.buttons.buttons import PrimaryButton, SecondaryButton, DangerButton
from prisqo_ui.components.core.variants import VariantName, resolve_variant

# Detected once at import time: newer Flet exposes `ft.AlertDialog(scrollable=True)`,
# which mirrors Flutter's `AlertDialog(scrollable: true)` -- the dialog shrinks to
# fit its content and, once content would exceed the screen, scrolls internally
# without the dialog itself ever overflowing the viewport. Older Flet lacks this
# param, so `_dialog_shell` falls back to a height-capped scrollable container.
#
# IMPORTANT: every dialog constructor in this file (`AppDialog`, `ConfirmDialog`,
# `FormDialog`, `AsyncFormDialog`, `Swal`, ...) routes through this one function
# with no per-dialog special-casing, so whichever branch is picked applies
# identically to all of them -- `FormDialog` and `AsyncFormDialog` cannot drift
# out of sync with each other as long as neither bypasses `_dialog_shell`.
_ALERTDIALOG_SUPPORTS_SCROLLABLE = "scrollable" in inspect.signature(ft.AlertDialog.__init__).parameters

_ICON_BY_VARIANT: dict = {
    "info": ft.Icons.HELP_OUTLINE,
    "success": ft.Icons.CHECK_CIRCLE_OUTLINE,
    "warning": ft.Icons.WARNING_AMBER,
    "danger": ft.Icons.DELETE_OUTLINE,
    "neutral": ft.Icons.INFO_OUTLINE,
}


def _dialog_shell(
    theme: Theme,
    page: ft.Page,
    title: str,
    content: ft.Control,
    actions: Sequence[ft.Control],
    icon: Optional[ft.Control] = None,
    width: float = 420,
) -> ft.AlertDialog:
    page_width = page.width or 1024
    page_height = page.height or 800
    # On a narrow/mobile viewport the dialog gives up trying to be `width`
    # px wide and instead fills nearly the full screen (minus a small side
    # margin) so it never overflows horizontally.
    side_margin = 32 if page_width < 600 else 64
    dialog_width = min(width, max(280, page_width - side_margin))

    header = ft.Row(
        controls=[
            ft.Row(
                controls=[icon, ft.Text(title, style=theme.typography.section_title(theme.text_primary), expand=True)]
                if icon
                else [ft.Text(title, style=theme.typography.section_title(theme.text_primary), expand=True)],
                spacing=theme.spacing.SM,
                expand=True,
            ),
        ],
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
    )

    if _ALERTDIALOG_SUPPORTS_SCROLLABLE:
        dialog_content = ft.Container(content=content, width=dialog_width, padding=ft.Padding.only(top=theme.spacing.SM))
        scrollable_kwargs = {"scrollable": True}
    else:
        # Fallback: cap the content area to a share of the viewport and make
        # it scroll internally once content exceeds that cap. The cap is
        # generous (roughly three quarters of the viewport, minus rough
        # chrome for the header/actions) so short content -- a one-line
        # confirm message, a couple of fields -- isn't stretched to fill it;
        # it just leaves the rest of that budget unused rather than
        # overflowing the screen once content genuinely runs long.
        max_content_height = max(160, page_height * 0.75 - 140)
        scroll_col = ft.Column(
            controls=[content],
            scroll=ft.ScrollMode.AUTO,
            tight=True,
            horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
        )
        dialog_content = ft.Container(
            content=scroll_col,
            width=dialog_width,
            height=max_content_height,
            padding=ft.Padding.only(top=theme.spacing.SM),
        )
        scrollable_kwargs = {}

    return ft.AlertDialog(
        modal=True,
        bgcolor=theme.surface,
        shape=ft.RoundedRectangleBorder(radius=theme.radius.LG),
        title=header,
        content=dialog_content,
        actions=list(actions),
        actions_alignment=ft.MainAxisAlignment.END,
        actions_padding=ft.Padding.all(theme.spacing.LG),
        **scrollable_kwargs,
    )


def AppDialog(
    theme: Theme,
    page: ft.Page,
    title: str,
    content: ft.Control,
    primary_label: str = "OK",
    secondary_label: Optional[str] = "Cancel",
    on_primary: Optional[Callable] = None,
    width: float = 420,
) -> None:
    """The generic dialog every other dialog in this file composes."""

    def _primary(e: ft.ControlEvent) -> None:
        page.pop_dialog()
        if on_primary:
            on_primary(e)

    actions = []
    if secondary_label:
        actions.append(SecondaryButton(theme, secondary_label, on_click=lambda e: page.pop_dialog()))
    actions.append(PrimaryButton(theme, primary_label, on_click=_primary))

    dialog = _dialog_shell(theme, page, title, content, actions, width=width)
    page.show_dialog(dialog)


def ConfirmDialog(
    theme: Theme,
    page: ft.Page,
    title: str,
    message: str,
    confirm_label: str = "Confirm",
    cancel_label: str = "Cancel",
    on_confirm: Optional[Callable] = None,
    icon: Optional[str] = None,
    variant: VariantName = "info",
) -> None:
    """A neutral yes/no confirmation (e.g. "Post this transaction?").

    `icon`/`variant` are optional overrides (SweetAlert-style) if the
    default question-mark/info styling doesn't fit -- e.g.
    `ConfirmDialog(..., icon=ft.Icons.SEND, variant="success")`.
    """

    def _confirm(e: ft.ControlEvent) -> None:
        page.pop_dialog()
        if on_confirm:
            on_confirm(e)

    accent = resolve_variant(theme, variant)
    content = ft.Text(message, style=theme.typography.body(theme.text_secondary))
    actions = [
        SecondaryButton(theme, cancel_label, on_click=lambda e: page.pop_dialog()),
        PrimaryButton(theme, confirm_label, on_click=_confirm),
    ]
    dialog = _dialog_shell(
        theme,
        page,
        title,
        content,
        actions,
        icon=ft.Icon(icon or _ICON_BY_VARIANT.get(variant, ft.Icons.HELP_OUTLINE), color=accent.solid, size=22),
    )
    page.show_dialog(dialog)


def DeleteDialog(
    theme: Theme,
    page: ft.Page,
    item_name: str,
    on_confirm: Optional[Callable] = None,
    title: str = "Delete record?",
    icon: Optional[str] = None,
) -> None:
    """A destructive confirmation, styled with danger emphasis."""

    def _confirm(e: ft.ControlEvent) -> None:
        page.pop_dialog()
        if on_confirm:
            on_confirm(e)

    content = ft.Text(
        f'This will permanently delete "{item_name}". This action cannot be undone.',
        style=theme.typography.body(theme.text_secondary),
    )
    actions = [
        SecondaryButton(theme, "Cancel", on_click=lambda e: page.pop_dialog()),
        DangerButton(theme, "Delete", on_click=_confirm),
    ]
    dialog = _dialog_shell(
        theme,
        page,
        title,
        content,
        actions,
        icon=ft.Icon(icon or ft.Icons.DELETE_OUTLINE, color=theme.danger, size=22),
    )
    page.show_dialog(dialog)


def WarningDialog(
    theme: Theme,
    page: ft.Page,
    title: str,
    message: str,
    acknowledge_label: str = "Understood",
    on_acknowledge: Optional[Callable] = None,
    icon: Optional[str] = None,
) -> None:
    """A single-action dialog used to surface an important warning."""

    def _ack(e: ft.ControlEvent) -> None:
        page.pop_dialog()
        if on_acknowledge:
            on_acknowledge(e)

    content = ft.Text(message, style=theme.typography.body(theme.text_secondary))
    actions = [PrimaryButton(theme, acknowledge_label, on_click=_ack)]
    dialog = _dialog_shell(
        theme,
        page,
        title,
        content,
        actions,
        icon=ft.Icon(icon or ft.Icons.WARNING_AMBER, color=theme.warning, size=22),
    )
    page.show_dialog(dialog)


def Swal(
    theme: Theme,
    page: ft.Page,
    title: str,
    text: Optional[str] = None,
    icon: Optional[str] = None,
    variant: VariantName = "info",
    content: Optional[ft.Control] = None,
    confirm_label: str = "OK",
    cancel_label: Optional[str] = None,
    on_confirm: Optional[Callable] = None,
    on_cancel: Optional[Callable] = None,
    width: float = 420,
) -> None:
    """A SweetAlert-`Swal.fire()`-style general-purpose alert: pass a
    `variant` ("info" | "success" | "warning" | "danger" | "neutral") for
    an on-brand icon/accent colour picked automatically, or override the
    `icon` directly. Pass `content` instead of `text` for full control
    over the body (e.g. a form, a list, an image) -- exactly like
    SweetAlert's `html`/custom-content option.

    `cancel_label` is omitted by default (single "OK" button, like a plain
    `Swal.fire("Saved!")`); pass it to get a confirm/cancel pair.

    Examples:
        Swal(theme, page, "Saved!", "Your changes have been saved.", variant="success")
        Swal(theme, page, "Delete item?", variant="danger",
             confirm_label="Delete", cancel_label="Cancel", on_confirm=do_delete)
    """
    accent = resolve_variant(theme, variant)
    body = content if content is not None else ft.Text(text or "", style=theme.typography.body(theme.text_secondary))

    def _confirm(e: ft.ControlEvent) -> None:
        page.pop_dialog()
        if on_confirm:
            on_confirm(e)

    def _cancel(e: ft.ControlEvent) -> None:
        page.pop_dialog()
        if on_cancel:
            on_cancel(e)

    actions = []
    if cancel_label:
        actions.append(SecondaryButton(theme, cancel_label, on_click=_cancel))
    actions.append(PrimaryButton(theme, confirm_label, on_click=_confirm))

    dialog = _dialog_shell(
        theme,
        page,
        title,
        body,
        actions,
        icon=ft.Icon(icon or _ICON_BY_VARIANT.get(variant, ft.Icons.INFO_OUTLINE), color=accent.solid, size=22),
        width=width,
    )
    page.show_dialog(dialog)


def AsyncFormDialog(
    theme: Theme,
    page: ft.Page,
    title: str,
    form_content: ft.Control,
    on_submit: Optional[Callable[[], bool]] = None,
    on_cancel: Optional[Callable] = None,
    submit_label: str = "Save",
    cancel_label: str = "Cancel",
    width: float = 480,
) -> None:
    """A form dialog for submits that hit the network/DB (`on_submit`
    runs on a background thread) and forms too long to fit on screen
    (e.g. a `DynamicRowList`-heavy modal) without pushing the actions
    off the bottom of the viewport.

    Height/scroll behaviour is handled by `_dialog_shell` itself now (see
    the module docstring) -- this no longer needs its own fixed-height
    scroll container. Use `FlexRow`, not `FormRow`, if `form_content`
    lays fields out side by side (see module docstring).

    Unlike `FormDialog`, which always closes on submit, this dialog only
    closes when `on_submit()` explicitly returns `True` — returning
    `False`/`None` (e.g. after a validation failure surfaced via
    `ToastService.error`) leaves it open with the submit button restored
    so the user can correct and retry. While `on_submit` is running, the
    submit button shows a spinner and both buttons are disabled so a
    slow request can't be double-submitted.
    """

    busy = {"value": False}

    def _submit(e: ft.ControlEvent) -> None:
        if busy["value"]:
            return
        if not on_submit:
            page.pop_dialog()
            return
        _set_busy(True)
        page.run_thread(_run_submit)

    def _cancel(e: ft.ControlEvent) -> None:
        if busy["value"]:
            return
        page.pop_dialog()
        if on_cancel:
            on_cancel(e)

    def _set_busy(is_busy: bool) -> None:
        # `loading`/`disabled` are baked into these liquid buttons at
        # construction time rather than being reactive props, so toggling
        # busy state means swapping the action controls, not mutating them.
        busy["value"] = is_busy
        dialog.actions = [
            SecondaryButton(theme, cancel_label, on_click=_cancel, disabled=is_busy),
            PrimaryButton(theme, submit_label, on_click=_submit, disabled=is_busy, loading=is_busy),
        ]
        if dialog.page:
            dialog.update()

    def _run_submit() -> None:
        try:
            result = on_submit() if on_submit else True
        except Exception:
            result = None
        _set_busy(False)
        if result is True:
            page.pop_dialog()

    initial_actions = [
        SecondaryButton(theme, cancel_label, on_click=_cancel),
        PrimaryButton(theme, submit_label, on_click=_submit),
    ]
    dialog = _dialog_shell(theme, page, title, form_content, initial_actions, width=width)
    page.show_dialog(dialog)


def FormDialog(
    theme: Theme,
    page: ft.Page,
    title: str,
    form_content: ft.Control,
    submit_label: str = "Save",
    cancel_label: str = "Cancel",
    on_submit: Optional[Callable] = None,
    width: float = 480,
) -> None:
    """A dialog that hosts a form (e.g. Quick Add Item).

    Use `FlexRow`, not `FormRow`, if `form_content` lays fields out side
    by side (see module docstring) -- and see `AsyncFormDialog` if
    `on_submit` needs to hit the network/DB.
    """

    def _submit(e: ft.ControlEvent) -> None:
        page.pop_dialog()
        if on_submit:
            on_submit(e)

    actions = [
        SecondaryButton(theme, cancel_label, on_click=lambda e: page.pop_dialog()),
        PrimaryButton(theme, submit_label, on_click=_submit),
    ]
    dialog = _dialog_shell(theme, page, title, form_content, actions, width=width)
    page.show_dialog(dialog)

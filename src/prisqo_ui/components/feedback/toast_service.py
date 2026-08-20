"""`ToastService` — a page-bound toast helper with ERP-flavored shortcuts.

Ported from PRISCO ERP's `shared/ui/components/notifications/toast_service.py`.
The standalone `Toast(theme, page, message, tone)` function in
`feedback.py` is the one-shot primitive (fixed 3s duration, call it
fresh every time); `ToastService` wraps it as a small stateful object you
instantiate once per page and call repeatedly — matching how ERP screens
actually use it (one instance handed to a controller, then
`toast.success(...)` / `toast.error(...)` called from many places) and
adding severity-scaled durations (errors stay on screen longer) plus
canned messages for the handful of outcomes (saved/updated/deleted,
permission denied, validation failure, API error, duplicate entry, not
found) that repeat across nearly every ERP form and list screen.

Notifications render top-right by default via `notification_center.notify`
(see that module for why: `ft.SnackBar` can't be repositioned away from
the bottom of the screen). Pass `position=` to `ToastService(...)` to
change it for every call, e.g. `ToastService(theme, page, position="bottom-right")`.

Usage:
    toast = ToastService(theme, page)
    toast.success("Customer saved.")
    toast.error("Email address format is invalid.")
    toast.warning("Transaction contains non-refundable charges.")
    toast.info("Synchronizing in background...")

    toast.saved("Customer")             # "Customer saved successfully."
    toast.updated("Item")               # "Item updated successfully."
    toast.deleted("Purchase Order")     # "Purchase Order deleted."
    toast.permission_denied("void this transaction")
    toast.validation_failed("Email", "must be a valid address")
    toast.api_error("The server did not respond.")
    toast.duplicate_entry("SKU")
    toast.not_found("Customer")
"""
from __future__ import annotations

from typing import Callable, Optional, Sequence

import flet as ft

from prisqo_ui.theme import Theme
from prisqo_ui.components.core.variants import VariantName
from .notification_center import notify, Position

_DURATION_SUCCESS = 3000
_DURATION_INFO = 3000
_DURATION_WARNING = 4500
_DURATION_ERROR = 5500


class ToastService:
    """Centralized toast notification service — one instance per page."""

    def __init__(self, theme: Theme, page: ft.Page, position: Position = "top-right"):
        self.theme = theme
        self.page = page
        self.position = position

    # ── Public API ──────────────────────────────────────────────────
    def success(self, message: str, **kwargs) -> Callable[[], None]:
        """Confirm completed operations: saves, updates, deletes, payments."""
        return self._show(message, "success", _DURATION_SUCCESS, **kwargs)

    def error(self, message: str, **kwargs) -> Callable[[], None]:
        """Signal failures: validation errors, network/DB errors, permission denials."""
        return self._show(message, "danger", _DURATION_ERROR, **kwargs)

    def warning(self, message: str, **kwargs) -> Callable[[], None]:
        """Alert about non-blocking risks: unsaved changes, refund restrictions."""
        return self._show(message, "warning", _DURATION_WARNING, **kwargs)

    def info(self, message: str, **kwargs) -> Callable[[], None]:
        """Provide neutral status: background jobs, sync status, tips."""
        return self._show(message, "info", _DURATION_INFO, **kwargs)

    # ── Convenience shortcuts ───────────────────────────────────────
    def saved(self, entity: str = "Record") -> Callable[[], None]:
        return self.success(f"{entity} saved successfully.")

    def updated(self, entity: str = "Record") -> Callable[[], None]:
        return self.success(f"{entity} updated successfully.")

    def deleted(self, entity: str = "Record") -> Callable[[], None]:
        return self.success(f"{entity} deleted.")

    def permission_denied(self, action: str = "perform this action") -> Callable[[], None]:
        return self.error(f"You do not have permission to {action}.")

    def validation_failed(self, field_name: str, reason: str) -> Callable[[], None]:
        return self.error(f"{field_name}: {reason}")

    def api_error(self, detail: str = "") -> Callable[[], None]:
        msg = "A server error occurred."
        if detail:
            msg += f" {detail}"
        return self.error(msg)

    def duplicate_entry(self, field_name: str) -> Callable[[], None]:
        return self.error(f"{field_name} already exists. Please use a different value.")

    def not_found(self, entity: str) -> Callable[[], None]:
        return self.error(f"{entity} not found.")

    # ── Internal ────────────────────────────────────────────────────
    def _show(
        self,
        message: str,
        tone: VariantName,
        duration_ms: int,
        *,
        title: Optional[str] = None,
        icon: Optional[str] = None,
        actions: Optional[Sequence[ft.Control]] = None,
        content: Optional[ft.Control] = None,
        closable: bool = True,
        position: Optional[Position] = None,
    ) -> Callable[[], None]:
        return notify(
            self.theme,
            self.page,
            message,
            tone,
            title=title,
            icon=icon,
            position=position or self.position,
            duration_ms=duration_ms,
            closable=closable,
            actions=actions,
            content=content,
        )

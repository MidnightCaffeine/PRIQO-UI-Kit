"""Feedback showcase — toasts, loading, skeletons, empty/error states."""
from __future__ import annotations

import flet as ft

from prisqo_ui.theme import Theme
from prisqo_ui.components.cards import SectionCard
from prisqo_ui.components.buttons import PrimaryButton, SecondaryButton, OutlineButton
from prisqo_ui.components.feedback import (
    Toast,
    Snackbar,
    ToastService,
    LoadingSpinner,
    SkeletonText,
    SkeletonCircle,
    SkeletonCard,
    SkeletonTable,
    EmptyState,
    ErrorState,
    Alert,
)


def build(theme: Theme, page: ft.Page) -> ft.Control:
    def _toast(tone: str) -> ft.ControlEventHandler:
        def _handler(e: ft.ControlEvent) -> None:
            Toast(theme, page, f"This is a {tone} toast message.", tone=tone)

        return _handler

    def _snackbar(e: ft.ControlEvent) -> None:
        Snackbar(theme, page, "Item archived.", action_label="Undo", on_action=lambda ev: None)

    def _positioned_toast(position: str) -> ft.ControlEventHandler:
        def _handler(e: ft.ControlEvent) -> None:
            Toast(theme, page, f"Notification at {position}.", tone="info", position=position, title="Heads up")

        return _handler

    position_triggers = ft.Row(
        controls=[
            OutlineButton(theme, "Top Right (default)", on_click=_positioned_toast("top-right")),
            OutlineButton(theme, "Top Center", on_click=_positioned_toast("top-center")),
            OutlineButton(theme, "Bottom Left", on_click=_positioned_toast("bottom-left")),
        ],
        spacing=12,
        wrap=True,
        run_spacing=12,
    )

    toast_service = ToastService(theme, page)

    def _service_toast(kind: str) -> ft.ControlEventHandler:
        def _handler(e: ft.ControlEvent) -> None:
            if kind == "saved":
                toast_service.saved("Customer")
            elif kind == "deleted":
                toast_service.deleted("Purchase Order")
            elif kind == "permission_denied":
                toast_service.permission_denied("void this transaction")
            elif kind == "duplicate_entry":
                toast_service.duplicate_entry("SKU")

        return _handler

    service_triggers = ft.Row(
        controls=[
            PrimaryButton(theme, "toast.saved()", on_click=_service_toast("saved")),
            SecondaryButton(theme, "toast.deleted()", on_click=_service_toast("deleted")),
            OutlineButton(theme, "toast.permission_denied()", on_click=_service_toast("permission_denied")),
            OutlineButton(theme, "toast.duplicate_entry()", on_click=_service_toast("duplicate_entry")),
        ],
        spacing=12,
        wrap=True,
        run_spacing=12,
    )

    toast_triggers = ft.Row(
        controls=[
            PrimaryButton(theme, "Success Toast", on_click=_toast("success")),
            OutlineButton(theme, "Info Toast", on_click=_toast("info")),
            SecondaryButton(theme, "Warning Toast", on_click=_toast("warning")),
            SecondaryButton(theme, "Danger Toast", on_click=_toast("danger")),
            SecondaryButton(theme, "Snackbar with Action", on_click=_snackbar),
        ],
        spacing=12,
        wrap=True,
        run_spacing=12,
    )

    loading = ft.Row(
        controls=[LoadingSpinner(theme, "Loading records..."), LoadingSpinner(theme, size=18)],
        spacing=32,
    )

    skeletons = ft.Column(
        controls=[
            ft.Row(controls=[SkeletonCircle(theme), SkeletonText(theme, lines=2, width=180)], spacing=12),
            ft.Row(controls=[SkeletonCard(theme), SkeletonCard(theme)], spacing=16, wrap=True),
            SkeletonTable(theme, rows=3, columns=4),
        ],
        spacing=16,
        tight=True,
    )

    states = ft.Row(
        controls=[
            ft.Container(
                content=EmptyState(
                    theme,
                    "No inventory items",
                    "There are no items matching your current filters.",
                    icon=ft.Icons.INBOX_OUTLINED,
                    action=OutlineButton(theme, "Clear Filters"),
                ),
                bgcolor=theme.surface,
                border=ft.Border.all(1, theme.border),
                border_radius=theme.radius.LG,
                width=380,
            ),
            ft.Container(
                content=ErrorState(
                    theme,
                    "Unable to load inventory",
                    "We couldn't retrieve the inventory records. Please try again.",
                    action=PrimaryButton(theme, "Try Again", icon=ft.Icons.REFRESH),
                ),
                bgcolor=theme.surface,
                border=ft.Border.all(1, theme.border),
                border_radius=theme.radius.LG,
                width=380,
            ),
        ],
        spacing=16,
        wrap=True,
        run_spacing=16,
    )

    alerts = ft.Column(
        controls=[
            Alert(theme, "Your changes have been saved.", variant="success", title="Saved"),
            Alert(theme, "This record was posted and can no longer be edited.", variant="info"),
            Alert(theme, "Stock for this item is running low.", variant="warning", title="Low stock", dismissible=True),
            Alert(theme, "This action cannot be undone.", variant="danger", title="Delete customer?"),
        ],
        spacing=12,
        tight=True,
    )

    return ft.Column(
        controls=[
            SectionCard(
                theme,
                "Alert",
                alerts,
                subtitle="Inline, persistent status banners \u2014 unlike Toast/Snackbar, these stay until dismissed",
            ),
            SectionCard(theme, "Toast & Snackbar", toast_triggers, subtitle="Click to trigger \u2014 all render top-right by default (customizable)"),
            SectionCard(
                theme,
                "Toast Position",
                position_triggers,
                subtitle="SweetAlert-style: position, title, icon, and duration are all customizable per call",
            ),
            SectionCard(
                theme,
                "Toast Service",
                service_triggers,
                subtitle="Page-bound helper with ERP shortcuts — saved/updated/deleted, permission_denied, duplicate_entry, ...",
            ),
            SectionCard(theme, "Loading Spinner", loading),
            SectionCard(theme, "Skeletons", skeletons, subtitle="Text, circle, card, table"),
            SectionCard(theme, "Empty & Error States", states),
        ],
        spacing=16,
        tight=True,
    )

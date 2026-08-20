"""Dialogs showcase — buttons that trigger each dialog type."""
from __future__ import annotations

import flet as ft

from prisqo_ui.theme import Theme
from prisqo_ui.components.cards import SectionCard
from prisqo_ui.components.buttons import PrimaryButton, SecondaryButton, DangerButton, OutlineButton
from prisqo_ui.components.dialogs import AppDialog, ConfirmDialog, DeleteDialog, WarningDialog, FormDialog, AsyncFormDialog, Swal
from prisqo_ui.components.forms import AppTextField, CurrencyField, DynamicRowList, RowField
from prisqo_ui.components.feedback import ToastService
import time


def build(theme: Theme, page: ft.Page) -> ft.Control:
    def _open_app_dialog(e: ft.ControlEvent) -> None:
        AppDialog(theme, page, "Item Details", ft.Text("Coca-Cola 1L \u2014 SKU BEV-001", style=theme.typography.body(theme.text_secondary)))

    def _open_confirm(e: ft.ControlEvent) -> None:
        ConfirmDialog(theme, page, "Post Transaction?", "This will post the transaction to the general ledger.")

    def _open_delete(e: ft.ControlEvent) -> None:
        DeleteDialog(theme, page, "Coca-Cola 1L")

    def _open_warning(e: ft.ControlEvent) -> None:
        WarningDialog(theme, page, "Low Stock Warning", "This item is below the reorder threshold.")

    def _open_form(e: ft.ControlEvent) -> None:
        FormDialog(
            theme,
            page,
            "Quick Add Item",
            ft.Column(
                controls=[AppTextField(theme, label="Item Name", required=True), CurrencyField(theme, label="Price")],
                spacing=12,
                tight=True,
            ),
            submit_label="Add Item",
        )

    def _open_async_form(e: ft.ControlEvent) -> None:
        toast = ToastService(theme, page)
        rows = DynamicRowList(
            theme,
            [
                RowField("medicine_name", "Medicine", required=True, group=0),
                RowField("unit", "Unit", kind="dropdown", options=["tablets", "ml", "mg"], group=1),
                RowField("frequency", "Frequency", group=1),
            ],
            add_label="Prescribed medicine",
        )

        def _submit() -> bool:
            try:
                data = rows.get_rows()
            except ValueError as ex:
                toast.error(str(ex))
                return False
            time.sleep(1.2)  # simulate a network/DB save so the spinner state is visible
            toast.saved("Prescription")
            return True

        AsyncFormDialog(
            theme,
            page,
            "New Prescription",
            rows.build(),
            on_submit=_submit,
            submit_label="Save Prescription",
        )

    def _open_swal_success(e: ft.ControlEvent) -> None:
        Swal(theme, page, "Saved!", "Your changes have been saved.", variant="success")

    def _open_swal_delete(e: ft.ControlEvent) -> None:
        def _do_delete(ev: ft.ControlEvent) -> None:
            toast = ToastService(theme, page)
            toast.deleted("Item")

        Swal(
            theme,
            page,
            "Delete item?",
            "This can't be undone.",
            variant="danger",
            confirm_label="Delete",
            cancel_label="Cancel",
            on_confirm=_do_delete,
        )

    triggers = ft.Row(
        controls=[
            PrimaryButton(theme, "Open App Dialog", on_click=_open_app_dialog),
            OutlineButton(theme, "Open Confirm Dialog", on_click=_open_confirm),
            DangerButton(theme, "Open Delete Dialog", on_click=_open_delete),
            SecondaryButton(theme, "Open Warning Dialog", on_click=_open_warning),
            PrimaryButton(theme, "Open Form Dialog", icon=ft.Icons.ADD, on_click=_open_form),
            PrimaryButton(theme, "Open Async Form Dialog", icon=ft.Icons.MEDICAL_SERVICES, on_click=_open_async_form),
            OutlineButton(theme, "Swal: Success", icon=ft.Icons.AUTO_AWESOME, on_click=_open_swal_success),
            OutlineButton(theme, "Swal: Delete", icon=ft.Icons.AUTO_AWESOME, on_click=_open_swal_delete),
        ],
        spacing=16,
        wrap=True,
        run_spacing=12,
    )

    return ft.Column(
        controls=[
            SectionCard(
                theme,
                "Dialog Types",
                triggers,
                subtitle="AppDialog, ConfirmDialog, DeleteDialog, WarningDialog, FormDialog, AsyncFormDialog, Swal \u2014 click to preview",
            ),
        ],
        spacing=16,
        tight=True,
    )

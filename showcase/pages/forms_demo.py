"""Forms showcase."""
from __future__ import annotations

import datetime as _dt

import flet as ft

from prisqo_ui.theme import Theme
from prisqo_ui.components.cards import SectionCard
from prisqo_ui.components.buttons import PrimaryButton, SecondaryButton
from prisqo_ui.components.layout import FlexRow
from prisqo_ui.components.forms import (
    AppTextField,
    NumberField,
    CurrencyField,
    PercentageField,
    SearchField,
    AppDropdown,
    DateField,
    TimeField,
    DateRangeField,
    FormSection,
    FormRow,
    FormActions,
    DynamicRowList,
    RowField,
)


def build(theme: Theme, page: ft.Page) -> ft.Control:
    states = ft.Row(
        controls=[
            AppTextField(theme, label="Item Name", value="Coca-Cola 1L", width=220),
            AppTextField(theme, label="SKU", hint="Type to search...", width=220),
            AppTextField(theme, label="Notes", disabled=True, value="Read-only value", width=220),
            AppTextField(theme, label="Email", error="Invalid email address", value="not-an-email", width=220),
        ],
        spacing=16,
        wrap=True,
        run_spacing=16,
    )

    field_types = FormRow(
        theme,
        [
            NumberField(theme, label="Quantity", value="12"),
            CurrencyField(theme, label="Unit Price", value="75.00"),
            PercentageField(theme, label="VAT Rate", value="12"),
            AppDropdown(theme, label="Category", options=["Beverage", "Grocery", "Dairy"], value="Beverage"),
        ],
    )

    search_row = ft.Row(
        controls=[
            SearchField(theme, hint="Search items...", width=280),
            SearchField(theme, hint="Searching...", value="cok", loading=True, width=280),
        ],
        spacing=16,
        wrap=True,
        run_spacing=16,
    )

    date_row = ft.Row(
        controls=[
            DateField(theme, page, label="Transaction Date", value=_dt.date.today(), width=220),
            TimeField(theme, page, label="Transaction Time", value=_dt.datetime.now().time(), width=200),
            DateRangeField(theme, page, label="Report Range", width=200),
        ],
        spacing=16,
        wrap=True,
        run_spacing=16,
    )

    dynamic_rows = DynamicRowList(
        theme,
        [
            RowField("medicine_name", "Medicine", required=True, group=0),
            RowField("dose", "Dose #", group=0, flex=1),
            RowField("unit", "Unit", kind="dropdown", options=["tablets", "ml", "mg"], group=1),
            RowField("frequency", "Frequency", group=1),
            RowField("notes", "Notes", kind="multiline", group=2),
        ],
        add_label="Prescribed medicine",
    ).build()

    flex_row = ft.Container(
        content=FlexRow(
            theme,
            [
                AppTextField(theme, label="First Name", width=220),
                AppTextField(theme, label="Last Name", width=220),
                AppTextField(theme, label="Middle Name", width=220),
            ],
        ),
        width=480,  # narrowed to demonstrate wrapping without resizing the window
        border=ft.Border.all(1, theme.border),
        border_radius=theme.radius.SM,
        padding=theme.spacing.MD,
    )

    section = FormSection(
        theme,
        "Item Details",
        subtitle="Grouped fields with a divider and consistent spacing",
        fields=[
            FormRow(theme, [AppTextField(theme, label="Item Name", required=True), AppDropdown(theme, label="Category", options=["Beverage", "Grocery"], required=True)]),
            FormRow(theme, [NumberField(theme, label="Stock", value="0"), CurrencyField(theme, label="Price", value="0.00")]),
        ],
    )

    actions = FormActions(theme, PrimaryButton(theme, "Save Item", icon=ft.Icons.SAVE), SecondaryButton(theme, "Cancel"))

    return ft.Column(
        controls=[
            SectionCard(theme, "Text Field States", states, subtitle="Normal, hint, disabled, error"),
            SectionCard(theme, "Numeric / Currency / Percentage / Dropdown", field_types),
            SectionCard(theme, "Search Field", search_row, subtitle="Normal and loading states"),
            SectionCard(theme, "Date Fields", date_row, subtitle="Click to open the date/time picker"),
            SectionCard(
                theme,
                "Dynamic Row List",
                dynamic_rows,
                subtitle="Repeatable rows with add/remove — e.g. a Prescription modal's medicine list",
            ),
            SectionCard(
                theme,
                "Flex Row",
                flex_row,
                subtitle="CSS flex-wrap behavior: fields wrap one at a time as space runs out — "
                         "container below is fixed at 480px wide, so \"Middle Name\" has already dropped to its own line",
            ),
            SectionCard(theme, "Form Section + Form Row + Form Actions", ft.Column(controls=[section, actions], spacing=20, tight=True)),
        ],
        spacing=16,
        tight=True,
    )

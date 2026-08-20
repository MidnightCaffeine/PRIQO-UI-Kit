"""Lookups showcase — generic LookupField + all ERP-specific lookups."""
from __future__ import annotations

import flet as ft

from prisqo_ui.theme import Theme
from prisqo_ui.components.cards import SectionCard
from prisqo_ui.components.forms.lookup_field import LookupField
from prisqo_ui.components.erp import ItemLookup, CustomerLookup, VendorLookup, EmployeeLookup, LocationLookup
from prisqo_ui.mock_data import ITEMS


def build(theme: Theme, page: ft.Page) -> ft.Control:
    generic = LookupField(
        theme,
        page,
        items=[{"label": "Option A"}, {"label": "Option B"}, {"label": "Option C"}],
        display_field="label",
        label="Generic Lookup",
        width=280,
    )

    erp_lookups = ft.Row(
        controls=[
            ft.Container(content=ItemLookup(theme, page, width=260), width=260),
            ft.Container(content=CustomerLookup(theme, page, width=260), width=260),
            ft.Container(content=VendorLookup(theme, page, width=260), width=260),
            ft.Container(content=EmployeeLookup(theme, page, width=260), width=260),
            ft.Container(content=LocationLookup(theme, page, width=260), width=260),
        ],
        spacing=16,
        wrap=True,
        run_spacing=16,
    )

    preselected = ft.Row(
        controls=[
            ft.Container(content=ItemLookup(theme, page, value=ITEMS[0], width=260), width=260),
            ft.Container(content=ItemLookup(theme, page, disabled=True, width=260), width=260),
        ],
        spacing=16,
    )

    return ft.Column(
        controls=[
            SectionCard(theme, "Generic LookupField", generic, subtitle="Click the field to open the search dialog"),
            SectionCard(theme, "ERP-Specific Lookups", erp_lookups, subtitle="Item, Customer, Vendor, Employee, Location"),
            SectionCard(theme, "Preselected & Disabled", preselected),
        ],
        spacing=16,
        tight=True,
    )

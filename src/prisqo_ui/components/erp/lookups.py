"""ERP-specific lookups — thin, pre-configured wrappers around the
generic `LookupField`, each pointed at its own mock dataset.
"""
from __future__ import annotations

from typing import Callable, Mapping, Optional, Sequence

import flet as ft

from prisqo_ui.theme import Theme
from prisqo_ui.components.forms.lookup_field import LookupField
from prisqo_ui.mock_data import ITEMS, CUSTOMERS, VENDORS, EMPLOYEES, LOCATIONS


def ItemLookup(
    theme: Theme,
    page: ft.Page,
    value: Optional[Mapping] = None,
    items: Sequence[Mapping] = ITEMS,
    required: bool = False,
    disabled: bool = False,
    width: Optional[float] = None,
    on_select: Optional[Callable[[Optional[Mapping]], None]] = None,
) -> ft.Container:
    return LookupField(
        theme, page, items, display_field="name", subtitle_field="category",
        label="Item", dialog_title="Select Item", search_hint="Search items...",
        value=value, required=required, disabled=disabled, width=width, on_select=on_select,
    )


def CustomerLookup(
    theme: Theme,
    page: ft.Page,
    value: Optional[Mapping] = None,
    customers: Sequence[Mapping] = CUSTOMERS,
    required: bool = False,
    disabled: bool = False,
    width: Optional[float] = None,
    on_select: Optional[Callable[[Optional[Mapping]], None]] = None,
) -> ft.Container:
    return LookupField(
        theme, page, customers, display_field="name", subtitle_field="type",
        label="Customer", dialog_title="Select Customer", search_hint="Search customers...",
        value=value, required=required, disabled=disabled, width=width, on_select=on_select,
    )


def VendorLookup(
    theme: Theme,
    page: ft.Page,
    value: Optional[Mapping] = None,
    vendors: Sequence[Mapping] = VENDORS,
    required: bool = False,
    disabled: bool = False,
    width: Optional[float] = None,
    on_select: Optional[Callable[[Optional[Mapping]], None]] = None,
) -> ft.Container:
    return LookupField(
        theme, page, vendors, display_field="name", subtitle_field="category",
        label="Vendor", dialog_title="Select Vendor", search_hint="Search vendors...",
        value=value, required=required, disabled=disabled, width=width, on_select=on_select,
    )


def EmployeeLookup(
    theme: Theme,
    page: ft.Page,
    value: Optional[Mapping] = None,
    employees: Sequence[Mapping] = EMPLOYEES,
    required: bool = False,
    disabled: bool = False,
    width: Optional[float] = None,
    on_select: Optional[Callable[[Optional[Mapping]], None]] = None,
) -> ft.Container:
    return LookupField(
        theme, page, employees, display_field="name", subtitle_field="role",
        label="Employee", dialog_title="Select Employee", search_hint="Search employees...",
        value=value, required=required, disabled=disabled, width=width, on_select=on_select,
    )


def LocationLookup(
    theme: Theme,
    page: ft.Page,
    value: Optional[Mapping] = None,
    locations: Sequence[Mapping] = LOCATIONS,
    required: bool = False,
    disabled: bool = False,
    width: Optional[float] = None,
    on_select: Optional[Callable[[Optional[Mapping]], None]] = None,
) -> ft.Container:
    return LookupField(
        theme, page, locations, display_field="name", subtitle_field="city",
        label="Location", dialog_title="Select Location", search_hint="Search locations...",
        value=value, required=required, disabled=disabled, width=width, on_select=on_select,
    )

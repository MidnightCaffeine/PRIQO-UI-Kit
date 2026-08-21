"""Form field components.

Every field follows the same visual language: a labelled outline field
with consistent normal / hover / focus / disabled / error states, built
entirely from semantic theme tokens.
"""
from __future__ import annotations

import datetime as _dt
from typing import Callable, Optional, Sequence

import flet as ft

from prisqo_ui.theme import Theme
from prisqo_ui.components.buttons.buttons import AppIconButton


def _shared_field_kwargs(theme: Theme, error: Optional[str], disabled: bool) -> dict:
    """Kwargs supported by BOTH `ft.TextField` and `ft.Dropdown`."""
    border_color = theme.danger if error else theme.border
    focused_border = theme.danger if error else theme.primary
    return dict(
        border=ft.InputBorder.OUTLINE,
        border_radius=theme.radius.MD,
        border_color=border_color,
        border_width=1,
        focused_border_color=focused_border,
        focused_border_width=1.5,
        bgcolor=theme.surface_variant if disabled else theme.surface,
        color=theme.text_muted if disabled else theme.text_primary,
        label_style=theme.typography.label(theme.text_secondary),
        hint_style=theme.typography.body(theme.text_muted),
        text_style=theme.typography.body(theme.text_primary),
        error_style=theme.typography.caption(theme.danger),
        content_padding=ft.Padding.symmetric(horizontal=12, vertical=10),
    )


def _common_field_kwargs(theme: Theme, error: Optional[str], disabled: bool) -> dict:
    """Kwargs for `ft.TextField`-based fields only (adds cursor/selection)."""
    kwargs = _shared_field_kwargs(theme, error, disabled)
    kwargs.update(
        cursor_color=theme.primary,
        selection_color=ft.Colors.with_opacity(0.25, theme.primary),
    )
    return kwargs


def AppTextField(
    theme: Theme,
    label: Optional[str] = None,
    value: str = "",
    hint: Optional[str] = None,
    required: bool = False,
    disabled: bool = False,
    read_only: bool = False,
    error: Optional[str] = None,
    helper_text: Optional[str] = None,
    width: Optional[float] = None,
    multiline: bool = False,
    password: bool = False,
    prefix_icon: Optional[str] = None,
    on_change: Optional[Callable] = None,
    on_submit: Optional[Callable] = None,
) -> ft.TextField:
    display_label = f"{label} *" if (label and required) else label
    return ft.TextField(
        label=display_label,
        value=value,
        hint_text=hint,
        disabled=disabled,
        read_only=read_only,
        error=error,
        helper=helper_text,
        helper_style=theme.typography.caption(theme.text_muted),
        width=width,
        multiline=multiline,
        password=password,
        can_reveal_password=password,
        prefix_icon=prefix_icon,
        on_change=on_change,
        on_submit=on_submit,
        **_common_field_kwargs(theme, error, disabled),
    )


def NumberField(
    theme: Theme,
    label: Optional[str] = None,
    value: str = "",
    required: bool = False,
    disabled: bool = False,
    error: Optional[str] = None,
    width: Optional[float] = None,
    allow_decimal: bool = True,
    hint: Optional[str] = None,
    helper_text: Optional[str] = None,
    on_change: Optional[Callable] = None,
) -> ft.TextField:
    """Numeric `ft.TextField`.

    `hint`/`helper_text` mirror `AppTextField`'s own params exactly
    (`hint` -> `hint_text`, `helper_text` -> `helper` styled via
    `theme.typography.caption`) so numeric fields aren't a special case
    within the same form.
    """
    pattern = r"^\d*\.?\d*$" if allow_decimal else r"^\d*$"
    display_label = f"{label} *" if (label and required) else label
    return ft.TextField(
        label=display_label,
        value=value,
        hint_text=hint,
        helper=helper_text,
        helper_style=theme.typography.caption(theme.text_muted),
        disabled=disabled,
        error=error,
        width=width,
        text_align=ft.TextAlign.RIGHT,
        keyboard_type=ft.KeyboardType.NUMBER,
        input_filter=ft.InputFilter(regex_string=pattern, allow=True, replacement_string=""),
        on_change=on_change,
        **_common_field_kwargs(theme, error, disabled),
    )


def CurrencyField(
    theme: Theme,
    label: str = "Amount",
    value: str = "",
    required: bool = False,
    disabled: bool = False,
    error: Optional[str] = None,
    width: Optional[float] = None,
    currency_symbol: str = "\u20b1",
    on_change: Optional[Callable] = None,
) -> ft.TextField:
    display_label = f"{label} *" if required else label
    return ft.TextField(
        label=display_label,
        value=value,
        disabled=disabled,
        error=error,
        width=width,
        text_align=ft.TextAlign.RIGHT,
        prefix=ft.Text(f"{currency_symbol} ", style=theme.typography.body(theme.text_secondary)),
        keyboard_type=ft.KeyboardType.NUMBER,
        input_filter=ft.InputFilter(regex_string=r"^\d*\.?\d{0,2}$", allow=True, replacement_string=""),
        on_change=on_change,
        **_common_field_kwargs(theme, error, disabled),
    )


def PercentageField(
    theme: Theme,
    label: str = "Percentage",
    value: str = "",
    disabled: bool = False,
    error: Optional[str] = None,
    width: Optional[float] = None,
    on_change: Optional[Callable] = None,
) -> ft.TextField:
    return ft.TextField(
        label=label,
        value=value,
        disabled=disabled,
        error=error,
        width=width,
        text_align=ft.TextAlign.RIGHT,
        suffix=ft.Text("%", style=theme.typography.body(theme.text_secondary)),
        keyboard_type=ft.KeyboardType.NUMBER,
        input_filter=ft.InputFilter(regex_string=r"^\d{0,3}\.?\d{0,2}$", allow=True, replacement_string=""),
        on_change=on_change,
        **_common_field_kwargs(theme, error, disabled),
    )


def SearchField(
    theme: Theme,
    hint: str = "Search...",
    value: str = "",
    loading: bool = False,
    width: Optional[float] = None,
    on_change: Optional[Callable] = None,
    on_submit: Optional[Callable] = None,
    on_clear: Optional[Callable] = None,
) -> ft.TextField:
    """A search input with a leading search icon and a clear (x) button."""
    suffix: ft.Control
    if loading:
        suffix = ft.Container(
            content=ft.ProgressRing(width=16, height=16, stroke_width=2, color=theme.primary),
            padding=ft.Padding.only(right=8),
        )
    elif value:
        suffix = AppIconButton(theme, ft.Icons.CLOSE, "Clear search", on_click=on_clear)
    else:
        suffix = ft.Container(width=0)

    return ft.TextField(
        hint_text=hint,
        value=value,
        width=width,
        prefix_icon=ft.Icons.SEARCH,
        suffix=suffix,
        on_change=on_change,
        on_submit=on_submit,
        **_common_field_kwargs(theme, None, False),
    )


def AppDropdown(
    theme: Theme,
    label: Optional[str] = None,
    options: Sequence[str] = (),
    value: Optional[str] = None,
    required: bool = False,
    disabled: bool = False,
    error: Optional[str] = None,
    width: Optional[float] = None,
    on_change: Optional[Callable] = None,
) -> ft.Dropdown:
    display_label = f"{label} *" if (label and required) else label
    return ft.Dropdown(
        label=display_label,
        value=value,
        options=[ft.DropdownOption(key=o, text=o) for o in options],
        disabled=disabled,
        error_text=error,
        width=width,
        on_select=on_change,
        **_shared_field_kwargs(theme, error, disabled),
    )


def DateField(
    theme: Theme,
    page: ft.Page,
    label: str = "Date",
    value: Optional[_dt.date] = None,
    disabled: bool = False,
    error: Optional[str] = None,
    width: Optional[float] = None,
    on_change: Optional[Callable[[_dt.date], None]] = None,
) -> ft.TextField:
    """A read-only text field that opens a `DatePicker` dialog on click."""
    field = ft.TextField(
        label=label,
        value=value.strftime("%b %d, %Y") if value else "",
        read_only=True,
        disabled=disabled,
        error=error,
        width=width,
        suffix_icon=ft.Icons.CALENDAR_MONTH,
        **_common_field_kwargs(theme, error, disabled),
    )

    def _open_picker(e: ft.ControlEvent) -> None:
        if disabled:
            return

        def _on_picked(ev: ft.ControlEvent) -> None:
            picked = picker.value
            if picked:
                field.value = picked.strftime("%b %d, %Y")
                field.update()
                if on_change:
                    on_change(picked)

        picker = ft.DatePicker(
            value=value or _dt.date.today(),
            on_change=_on_picked,
        )
        page.show_dialog(picker)

    field.on_click = _open_picker
    return field


def TimeField(
    theme: Theme,
    page: ft.Page,
    label: str = "Time",
    value: Optional[_dt.time] = None,
    disabled: bool = False,
    error: Optional[str] = None,
    width: Optional[float] = None,
    on_change: Optional[Callable[[_dt.time], None]] = None,
) -> ft.TextField:
    """A read-only text field that opens a `TimePicker` dialog on click.

    Mirrors `DateField` exactly (same read-only + picker-on-click
    convention) since Flet has no native masked-input for times either.
    """
    field = ft.TextField(
        label=label,
        value=value.strftime("%I:%M %p") if value else "",
        read_only=True,
        disabled=disabled,
        error=error,
        width=width,
        suffix_icon=ft.Icons.ACCESS_TIME,
        **_common_field_kwargs(theme, error, disabled),
    )

    def _open_picker(e: ft.ControlEvent) -> None:
        if disabled:
            return

        def _on_picked(ev: ft.ControlEvent) -> None:
            picked = picker.value
            if picked:
                field.value = picked.strftime("%I:%M %p")
                field.update()
                if on_change:
                    on_change(picked)

        picker = ft.TimePicker(
            value=value or _dt.datetime.now().time(),
            on_change=_on_picked,
        )
        page.show_dialog(picker)

    field.on_click = _open_picker
    return field


def DateRangeField(
    theme: Theme,
    page: ft.Page,
    label: str = "Date Range",
    start: Optional[_dt.date] = None,
    end: Optional[_dt.date] = None,
    width: Optional[float] = None,
    on_change: Optional[Callable[[Optional[_dt.date], Optional[_dt.date]], None]] = None,
) -> ft.Row:
    """Two linked DateFields representing a start/end range."""
    state = {"start": start, "end": end}

    def _start_changed(d: _dt.date) -> None:
        state["start"] = d
        if on_change:
            on_change(state["start"], state["end"])

    def _end_changed(d: _dt.date) -> None:
        state["end"] = d
        if on_change:
            on_change(state["start"], state["end"])

    start_field = DateField(theme, page, label=f"{label} - From", value=start, width=width, on_change=_start_changed)
    end_field = DateField(theme, page, label=f"{label} - To", value=end, width=width, on_change=_end_changed)
    return ft.Row(controls=[start_field, end_field], spacing=theme.spacing.MD)


def FormSection(theme: Theme, title: str, fields: Sequence[ft.Control], subtitle: Optional[str] = None) -> ft.Column:
    """Groups a labelled cluster of fields inside a form (no card chrome)."""
    header = [ft.Text(title, style=theme.typography.section_title(theme.text_primary))]
    if subtitle:
        header.append(ft.Text(subtitle, style=theme.typography.body_small(theme.text_muted)))
    return ft.Column(
        controls=[
            ft.Column(controls=header, spacing=2, tight=True),
            ft.Divider(height=1, color=theme.divider),
            ft.Column(controls=list(fields), spacing=theme.spacing.MD, tight=True),
        ],
        spacing=theme.spacing.MD,
        tight=True,
    )


def FormRow(theme: Theme, fields: Sequence[ft.Control]) -> ft.ResponsiveRow:
    """Lays fields side-by-side on desktop, stacking on narrower widths."""
    cols = max(1, 12 // max(1, len(fields)))
    return ft.ResponsiveRow(
        controls=[ft.Container(content=f, col={"xs": 12, "md": cols}) for f in fields],
        spacing=theme.spacing.MD,
        run_spacing=theme.spacing.MD,
    )


def FormActions(
    theme: Theme,
    primary: ft.Control,
    secondary: Optional[ft.Control] = None,
    align_right: bool = True,
) -> ft.Row:
    """Standard action bar at the bottom of a form (Cancel + Save)."""
    controls = [c for c in (secondary, primary) if c is not None]
    return ft.Row(
        controls=controls,
        alignment=ft.MainAxisAlignment.END if align_right else ft.MainAxisAlignment.START,
        spacing=theme.spacing.SM,
    )

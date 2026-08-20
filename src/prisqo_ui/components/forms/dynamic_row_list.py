"""`DynamicRowList` — reusable "+ <Type>" repeat-row component for ERP forms.

Ported from PRISCO ERP's `shared/ui/components/forms/dynamic_row_list.py`,
where it backs the Doctor Console's Prescription, Vaccine, Surgery,
Allergy, and Condition modals so each one only supplies its own field
schema instead of hand-rolling add/remove-row plumbing. Rebuilt here on
top of this library's theme tokens and liquid buttons instead of the
original's `AppColors` / plain `ft.TextButton` / `ft.IconButton`.

Usage:
    schema = [
        RowField("medicine_name", "Medicine", required=True, group=0),
        RowField("unit", "Unit", kind="dropdown",
                 options=["tablets", "ml", "mg"], group=1),
        RowField("frequency", "Frequency", group=1),
    ]
    rows = DynamicRowList(theme, schema, add_label="Prescribed medicine")
    content = rows.build()          # embed this ft.Control in a form/dialog
    ...
    data = rows.get_rows()          # -> list[dict], raises ValueError
                                     #    on a missing required field

Note for PRISCO ERP call sites migrating from the original
`shared/ui/components/forms/dynamic_row_list.py`: pass `theme` as the
first constructor argument (this library's DI convention), and drop any
manual " *" suffix baked into `label` strings — `required=True` now
appends it automatically, matching `AppTextField`/`AppDropdown`
elsewhere in the kit. Everything else (`RowField` fields, `.build()`,
`.get_rows()`) is a drop-in match.
"""
from __future__ import annotations

import itertools
from dataclasses import dataclass, field
from typing import Optional

import flet as ft

from prisqo_ui.theme import Theme
from prisqo_ui.components.buttons.buttons import GhostButton, AppIconButton
from prisqo_ui.components.forms.fields import AppTextField, AppDropdown


@dataclass
class RowField:
    """One field within a repeated row.

    `group` controls which fields render on the same row together (e.g.
    "Vaccine" + "Dose #" can share group 0, while "Notes" sits alone in
    group 1 underneath).
    """
    key: str
    label: str
    kind: str = "text"                 # "text" | "multiline" | "dropdown" | "search"
    required: bool = False
    options: list[str] = field(default_factory=list)
    group: int = 0
    flex: int = 1


class _SearchRowField(ft.Column):
    """Backs `RowField(kind="search")`: a text field the user types into
    and submits (Enter), with a results list of clickable rows underneath.
    Clicking a result writes it straight into the text field — so the
    selected value stays visible right where the user was typing — and
    clears the results.

    `.value` proxies the text field so `DynamicRowList.get_rows()` can
    read `ctrl.value` off every row control the same way regardless of
    kind.
    """

    def __init__(self, theme: Theme, label: str, options: list[str], required: bool = False, expand: int = 1):
        self._theme = theme
        self._options = options
        display_label = f"{label} *" if required else label
        self._search_field = AppTextField(theme, label=display_label)
        self._search_field.expand = True
        self._search_field.on_submit = self._do_search
        self._results_col = ft.Column(spacing=2)
        super().__init__(
            controls=[self._search_field, self._results_col],
            spacing=4, tight=True, expand=expand,
        )

    def _do_search(self, e: ft.ControlEvent) -> None:
        theme = self._theme
        q = (self._search_field.value or "").strip().lower()
        self._results_col.controls.clear()
        if q:
            matches = [o for o in self._options if q in o.lower()][:10]
            if not matches:
                self._results_col.controls.append(
                    ft.Text("No matching items.", style=theme.typography.caption(theme.text_muted))
                )
            for m in matches:
                self._results_col.controls.append(
                    ft.Container(
                        padding=theme.spacing.SM,
                        bgcolor=theme.surface_variant,
                        border_radius=theme.radius.SM,
                        ink=True,
                        on_click=lambda ev, m=m: self._select(m),
                        content=ft.Text(m, style=theme.typography.body(theme.text_primary)),
                    )
                )
        self._safe_update()

    def _select(self, m: str) -> None:
        self._search_field.value = m
        self._results_col.controls.clear()
        self._safe_update()

    def _safe_update(self) -> None:
        if self._search_field.page:
            self.update()

    @property
    def value(self):
        return self._search_field.value

    @value.setter
    def value(self, v):
        self._search_field.value = v


class DynamicRowList:
    """Renders N repeatable rows built from `row_fields`, with a
    "+ <add_label>" ghost button beneath them to append a fresh row and a
    small remove ("x") icon button on every row once there is more than
    one. Always keeps at least one row on screen — removing the last
    remaining row is a no-op.
    """

    _ids = itertools.count()

    def __init__(
        self,
        theme: Theme,
        row_fields: list[RowField],
        add_label: str = "Row",
        initial_rows: int = 1,
    ):
        self._theme = theme
        self._schema = row_fields
        self._add_label = add_label
        self._rows: list[dict] = []           # [{"_id": int, "controls": {key: Control}}]
        self._rows_col = ft.Column(spacing=theme.spacing.MD)
        for _ in range(max(1, initial_rows)):
            self._add_row_state()

    # ------------------------------------------------------------------
    # Construction
    # ------------------------------------------------------------------
    def _make_control(self, spec: RowField) -> ft.Control:
        theme = self._theme
        if spec.kind == "dropdown":
            ctrl = AppDropdown(theme, label=spec.label, options=spec.options, required=spec.required)
        elif spec.kind == "search":
            return _SearchRowField(theme, label=spec.label, options=spec.options, required=spec.required, expand=spec.flex)
        elif spec.kind == "multiline":
            ctrl = AppTextField(theme, label=spec.label, multiline=True, required=spec.required)
            ctrl.min_lines = 2
        else:
            ctrl = AppTextField(theme, label=spec.label, required=spec.required)
        ctrl.expand = spec.flex
        return ctrl

    def _add_row_state(self) -> None:
        row_id = next(self._ids)
        controls = {spec.key: self._make_control(spec) for spec in self._schema}
        self._rows.append({"_id": row_id, "controls": controls})

    # ------------------------------------------------------------------
    # Rendering
    # ------------------------------------------------------------------
    def build(self) -> ft.Control:
        """Returns the full control (rows + add button) to embed in a form/dialog."""
        theme = self._theme
        self._render()
        self._add_btn = GhostButton(theme, f"+ {self._add_label}", on_click=self._on_add_click)
        self._wrapper = ft.Column(
            spacing=theme.spacing.MD,
            controls=[self._rows_col, ft.Row(alignment=ft.MainAxisAlignment.END, controls=[self._add_btn])],
        )
        return self._wrapper

    def _render(self) -> None:
        theme = self._theme
        groups = sorted({spec.group for spec in self._schema})
        multi = len(self._rows) > 1
        self._rows_col.controls = [
            ft.Container(
                padding=ft.Padding.only(bottom=theme.spacing.SM) if multi else ft.Padding.all(0),
                border=ft.Border(bottom=ft.BorderSide(1, theme.divider)) if multi else None,
                content=ft.Column(
                    spacing=theme.spacing.SM,
                    controls=(
                        [
                            ft.Row(
                                alignment=ft.MainAxisAlignment.END,
                                controls=[
                                    AppIconButton(
                                        theme,
                                        icon=ft.Icons.CLOSE,
                                        tooltip="Remove",
                                        on_click=(lambda e, rid=row["_id"]: self._remove_row(e, rid)),
                                    )
                                ],
                            )
                        ]
                        if multi else []
                    )
                    + [
                        ft.Row(
                            spacing=theme.spacing.MD,
                            controls=[row["controls"][s.key] for s in self._schema if s.group == g],
                        )
                        for g in groups
                    ],
                ),
            )
            for row in self._rows
        ]

    # ------------------------------------------------------------------
    # Handlers
    # ------------------------------------------------------------------
    def _on_add_click(self, e: ft.ControlEvent) -> None:
        self._add_row_state()
        self._render()
        if self._wrapper.page:
            self._wrapper.update()

    def _remove_row(self, e: ft.ControlEvent, row_id: int) -> None:
        if len(self._rows) <= 1:
            return
        self._rows = [r for r in self._rows if r["_id"] != row_id]
        self._render()
        if self._wrapper.page:
            self._wrapper.update()

    # ------------------------------------------------------------------
    # Data extraction
    # ------------------------------------------------------------------
    def get_rows(self) -> list[dict]:
        """One dict per non-blank row. A row is "blank" (and silently
        skipped) only if every field in it is empty. Raises ValueError
        (a message suitable to surface directly to the user, e.g. via
        `ToastService.error`) if a row has *some* data but is missing a
        required field, or if no row has any data at all.
        """
        out: list[dict] = []
        for row in self._rows:
            values = {}
            for spec in self._schema:
                ctrl = row["controls"][spec.key]
                v = ctrl.value
                values[spec.key] = v.strip() if isinstance(v, str) else v
            if not any(v not in (None, "") for v in values.values()):
                continue
            for spec in self._schema:
                if spec.required and not values.get(spec.key):
                    raise ValueError(f"{spec.label} is required.")
            out.append(values)
        if not out:
            first_required = next((s for s in self._schema if s.required), self._schema[0])
            raise ValueError(f"Add at least one entry ({first_required.label}).")
        return out

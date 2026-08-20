"""PRISQO ERP — Login → Dashboard demo, built entirely from the PRISQO UI KIT.

Run with:
    python demo_app.py

Flow:
    1. Login page (email/password, remember-me, sign-in button, states)
    2. On sign-in -> Dashboard (sidebar + navbar + KPI cards + chart + table)
    3. "New Sale" / "+" opens a FormDialog (the "modal") built from form fields
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "src"))

import flet as ft

from prisqo_ui.theme import ThemeManager, AppThemeMode
from prisqo_ui.components.layout import Sidebar, Navbar, PageContainer, PageHeader, UserMenu, NotificationMenu, AppShell
from prisqo_ui.components.buttons import PrimaryButton, OutlineButton, GhostButton, AppIconButton
from prisqo_ui.components.cards import AppCard, KPICard, StatCard
from prisqo_ui.components.forms import AppTextField, AppDropdown, FormRow, FormActions
from prisqo_ui.components.dialogs import FormDialog
from prisqo_ui.components.status import StatusChip
from prisqo_ui.components.charts import ChartCard
from prisqo_ui.components.liquid import LiquidCheckbox
from prisqo_ui.components.feedback import Toast
from prisqo_ui.mock_data import ITEMS, CUSTOMERS


# ---------------------------------------------------------------------------
# LOGIN PAGE
# ---------------------------------------------------------------------------

def build_login(page: ft.Page, theme, on_success) -> ft.Control:
    FIELD_WIDTH = 320

    username_field = AppTextField(
        theme,
        hint="User Name",
        prefix_icon=ft.Icons.PERSON_OUTLINE,
        width=FIELD_WIDTH,
    )
    password_field = AppTextField(
        theme,
        hint="Password",
        password=True,
        prefix_icon=ft.Icons.LOCK_OUTLINE,
        width=FIELD_WIDTH,
    )
    error_text = ft.Text("", style=theme.typography.caption(theme.danger), visible=False)
    remember = LiquidCheckbox(theme, label="Remember me", value=True)

    login_button_holder = ft.Container()

    def do_login(e: ft.ControlEvent | None = None) -> None:
        if not username_field.value or not password_field.value:
            error_text.value = "Please enter both username and password."
            error_text.visible = True
            page.update()
            return
        error_text.visible = False
        on_success(username_field.value)

    login_button_holder.content = PrimaryButton(theme, "Sign In", on_click=do_login, width=FIELD_WIDTH)
    password_field.on_submit = do_login

    # -- Left panel: brand / welcome, with decorative circles ------------
    def _circle(size: float, color: str, opacity: float, left=None, top=None, right=None, bottom=None) -> ft.Container:
        return ft.Container(
            width=size,
            height=size,
            border_radius=size / 2,
            bgcolor=ft.Colors.with_opacity(opacity, color),
            left=left,
            top=top,
            right=right,
            bottom=bottom,
        )

    left_panel = ft.Container(
        content=ft.Stack(
            controls=[
                _circle(320, "#FFFFFF", 0.10, left=-140, top=-120),
                _circle(200, "#FFFFFF", 0.14, left=-40, top=170),
                _circle(160, theme.primary_pressed, 0.55, right=-60, bottom=-60),
                ft.Container(
                    content=ft.Column(
                        controls=[
                            ft.Text("WELCOME", style=theme.typography.page_title("#FFFFFF")),
                            ft.Text("Your Headline Name", style=theme.typography.section_title(ft.Colors.with_opacity(0.85, "#FFFFFF"))),
                            ft.Container(height=theme.spacing.SM),
                            ft.Text(
                                "Sign in to access your PRISQO ERP workspace — sales, inventory, "
                                "and everything else your store runs on, in one place.",
                                style=theme.typography.body_small(ft.Colors.with_opacity(0.75, "#FFFFFF")),
                            ),
                        ],
                        spacing=6,
                        tight=True,
                    ),
                    padding=ft.Padding.only(left=40, right=40, top=90),
                ),
            ],
            expand=True,
        ),
        gradient=ft.LinearGradient(
            begin=ft.Alignment(-1, -1),
            end=ft.Alignment(1, 1),
            colors=[theme.primary_hover, theme.primary_pressed],
        ),
        width=320,
        border_radius=ft.BorderRadius(top_left=theme.radius.LG, bottom_left=theme.radius.LG, top_right=0, bottom_right=0),
        clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
    )

    # -- Right panel: the sign-in form ------------------------------------
    right_panel = ft.Container(
        content=ft.Column(
            controls=[
                ft.Text("Sign in", style=theme.typography.page_title(theme.text_primary)),
                ft.Text(
                    "Lorem ipsum dolor sit amet, consectetur adipiscing elit.",
                    style=theme.typography.caption(theme.text_muted),
                ),
                ft.Container(height=theme.spacing.SM),
                ft.Column(controls=[username_field, password_field, error_text], spacing=theme.spacing.MD, tight=True),
                ft.Row(
                    controls=[
                        remember,
                        ft.Container(
                            content=ft.Text("Forgot Password?", style=theme.typography.body_small(theme.primary)),
                            ink=True,
                            border_radius=theme.radius.SM,
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    width=FIELD_WIDTH,
                ),
                login_button_holder,
                ft.Row(
                    controls=[
                        ft.Container(expand=True, content=ft.Divider(height=1, color=theme.divider)),
                        ft.Text("Or", style=theme.typography.caption(theme.text_muted)),
                        ft.Container(expand=True, content=ft.Divider(height=1, color=theme.divider)),
                    ],
                    width=FIELD_WIDTH,
                ),
                OutlineButton(theme, "Sign in with other", width=FIELD_WIDTH),
                ft.Container(height=theme.spacing.SM),
                ft.Row(
                    controls=[
                        ft.Text("Don't have an account?", style=theme.typography.body_small(theme.text_muted)),
                        ft.Container(
                            content=ft.Text("Sign Up", style=theme.typography.body_small(theme.primary)),
                            ink=True,
                            border_radius=theme.radius.SM,
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=4,
                ),
            ],
            spacing=theme.spacing.MD,
            tight=True,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        bgcolor=theme.surface,
        width=380,
        padding=ft.Padding.symmetric(horizontal=36, vertical=44),
        border_radius=ft.BorderRadius(top_right=theme.radius.LG, bottom_right=theme.radius.LG, top_left=0, bottom_left=0),
    )

    split_card = ft.Container(
        content=ft.Row(
            controls=[left_panel, right_panel],
            spacing=0,
            tight=True,
            vertical_alignment=ft.CrossAxisAlignment.STRETCH,
        ),
        border_radius=theme.radius.LG,
        shadow=theme.shadows.card,
        clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
    )

    return ft.Container(
        content=split_card,
        gradient=ft.LinearGradient(
            begin=ft.Alignment(-1, -1),
            end=ft.Alignment(1, 1),
            colors=[theme.primary, theme.primary_pressed],
        ),
        alignment=ft.Alignment(0, 0),
        expand=True,
    )


# ---------------------------------------------------------------------------
# MODAL — "New Sale" quick-add form dialog
# ---------------------------------------------------------------------------

def open_new_sale_modal(theme, page: ft.Page) -> None:
    customer_dd = AppDropdown(theme, label="Customer", options=[c["name"] for c in CUSTOMERS], value=CUSTOMERS[0]["name"], required=True, width=210)
    item_dd = AppDropdown(theme, label="Item", options=[i["name"] for i in ITEMS], required=True, width=210)
    qty_field = AppTextField(theme, label="Quantity", value="1", width=210)
    notes_field = AppTextField(theme, label="Notes", hint="Optional", multiline=True, width=430)

    form = ft.Column(
        controls=[
            FormRow(theme, [customer_dd, item_dd]),
            FormRow(theme, [qty_field]),
            notes_field,
        ],
        spacing=theme.spacing.MD,
        tight=True,
    )

    def _submit(e: ft.ControlEvent) -> None:
        Toast(theme, page, f"Sale created for {customer_dd.value or 'customer'}.", tone="success")

    FormDialog(
        theme,
        page,
        title="New Sale",
        form_content=form,
        submit_label="Create Sale",
        on_submit=_submit,
        width=470,
    )


# ---------------------------------------------------------------------------
# DASHBOARD PAGE
# ---------------------------------------------------------------------------

def build_dashboard_content(theme, page: ft.Page) -> ft.Control:
    kpi_row = ft.ResponsiveRow(
        controls=[
            ft.Container(content=KPICard(theme, "Today's Sales", "₱48,320", trend="+12%", trend_label="vs yesterday", icon=ft.Icons.PAYMENTS_OUTLINED), col={"xs": 12, "md": 3}),
            ft.Container(content=KPICard(theme, "Open Orders", "27", trend="+3", trend_label="new today", icon=ft.Icons.RECEIPT_LONG_OUTLINED), col={"xs": 12, "md": 3}),
            ft.Container(content=KPICard(theme, "Low Stock Items", "12", trend="-2", trend_label="restocked", icon=ft.Icons.INVENTORY_2_OUTLINED), col={"xs": 12, "md": 3}),
            ft.Container(content=KPICard(theme, "Active Customers", "184", trend="+5%", trend_label="this month", icon=ft.Icons.PEOPLE_OUTLINE), col={"xs": 12, "md": 3}),
        ],
        spacing=theme.spacing.MD,
        run_spacing=theme.spacing.MD,
    )

    chart = ChartCard(
        theme,
        title="Sales this week",
        subtitle="Gross revenue per day",
        data=[
            {"label": "Mon", "value": 32000},
            {"label": "Tue", "value": 41000},
            {"label": "Wed", "value": 28000},
            {"label": "Thu", "value": 52000},
            {"label": "Fri", "value": 61000},
            {"label": "Sat", "value": 48000},
            {"label": "Sun", "value": 39000},
        ],
    )

    stat_tiles = ft.Column(
        controls=[
            StatCard(theme, "Pending Approvals", "6", icon=ft.Icons.PENDING_ACTIONS, color=theme.warning),
            StatCard(theme, "Overdue Invoices", "3", icon=ft.Icons.WARNING_AMBER, color=theme.danger),
            StatCard(theme, "Deliveries Today", "9", icon=ft.Icons.LOCAL_SHIPPING_OUTLINED, color=theme.info),
        ],
        spacing=theme.spacing.MD,
    )

    middle_row = ft.ResponsiveRow(
        controls=[
            ft.Container(content=chart, col={"xs": 12, "md": 8}),
            ft.Container(content=stat_tiles, col={"xs": 12, "md": 4}),
        ],
        spacing=theme.spacing.MD,
        run_spacing=theme.spacing.MD,
    )

    rows = []
    for i, item in enumerate(ITEMS):
        rows.append({
            "id": item["sku"],
            "sku": item["sku"],
            "name": item["name"],
            "category": item["category"],
            "stock": item["stock"],
            "status": item["status"],
        })

    from prisqo_ui.components.tables import AppDataTable

    table = AppDataTable(
        theme,
        columns=[
            {"key": "sku", "label": "SKU"},
            {"key": "name", "label": "Item"},
            {"key": "category", "label": "Category"},
            {"key": "stock", "label": "Stock", "numeric": True},
            {"key": "status", "label": "Status", "render": lambda r: StatusChip(theme, r["status"])},
        ],
        rows=rows,
        row_id_field="id",
    )

    inventory_card = AppCard(
        theme,
        title="Inventory Snapshot",
        subtitle="Items needing attention",
        icon=ft.Icons.INVENTORY_2_OUTLINED,
        content=table,
        actions=[GhostButton(theme, "View all", icon=ft.Icons.ARROW_FORWARD)],
    )

    return ft.Column(
        controls=[kpi_row, middle_row, inventory_card],
        spacing=theme.spacing.LG,
        tight=True,
        horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
    )


def build_dashboard(theme_manager, page: ft.Page, user_email: str, on_logout, sidebar_open: bool, on_toggle_drawer) -> ft.Control:
    theme = theme_manager.theme

    groups = [
        {
            "title": "PRISQO ERP",
            "items": [
                {"key": "dashboard", "label": "Dashboard", "icon": ft.Icons.DASHBOARD_OUTLINED},
                {"key": "sales", "label": "Sales", "icon": ft.Icons.POINT_OF_SALE, "badge": "3"},
                {"key": "inventory", "label": "Inventory", "icon": ft.Icons.INVENTORY_2_OUTLINED},
                {"key": "customers", "label": "Customers", "icon": ft.Icons.PEOPLE_OUTLINE},
                {"key": "reports", "label": "Reports", "icon": ft.Icons.BAR_CHART_OUTLINED},
            ],
        },
        {
            "title": "Settings",
            "items": [
                {"key": "settings", "label": "Preferences", "icon": ft.Icons.SETTINGS_OUTLINED},
            ],
        },
    ]

    def build_sidebar(collapsed: bool, on_close) -> ft.Control:
        return Sidebar(
            theme,
            groups,
            active_key="dashboard",
            collapsed=collapsed,
            on_close=on_close,
            header=ft.Row(
                controls=[
                    ft.Container(
                        content=ft.Icon(ft.Icons.HEXAGON, color=theme.primary, size=22),
                        bgcolor="#FFFFFF",
                        padding=6,
                        border_radius=theme.radius.MD,
                    ),
                    ft.Text("PRISQO ERP", style=theme.typography.card_title("#FFFFFF")) if not collapsed else ft.Container(),
                ],
                spacing=theme.spacing.SM,
            ),
            footer=ft.Container(
                content=ft.Row(
                    controls=[
                        ft.Icon(ft.Icons.LOGOUT, size=16, color=theme.sidebar_text),
                        ft.Text("Sign out", style=theme.typography.body_small(theme.sidebar_text)) if not collapsed else ft.Container(),
                    ],
                    spacing=theme.spacing.SM,
                ),
                padding=ft.Padding.symmetric(horizontal=12, vertical=9),
                ink=True,
                on_click=lambda e: on_logout(),
                border_radius=theme.radius.MD,
            ),
        )

    user_menu = UserMenu(theme, name=user_email.split("@")[0].title(), role="Administrator")

    def build_navbar(on_menu_click) -> ft.Control:
        return Navbar(
            theme,
            title="Dashboard",
            actions=[
                PrimaryButton(theme, "New Sale", icon=ft.Icons.ADD, on_click=lambda e: open_new_sale_modal(theme, page), height=38),
                NotificationMenu(theme, count=4),
            ],
            on_menu_click=on_menu_click,
            user_menu=user_menu,
        )

    header = PageHeader(
        theme,
        title=f"Welcome back, {user_email.split('@')[0].title()}",
        subtitle="Here's what's happening in your store today.",
    )

    body = ft.Column(
        controls=[header, build_dashboard_content(theme, page)],
        spacing=theme.spacing.LG,
        tight=True,
        expand=True,
        horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
    )
    container = PageContainer(theme, body)

    return AppShell(
        theme,
        build_sidebar=build_sidebar,
        build_navbar=build_navbar,
        content=container,
        drawer_open=sidebar_open,
        on_toggle_drawer=on_toggle_drawer,
    )


# ---------------------------------------------------------------------------
# APP ENTRY
# ---------------------------------------------------------------------------

def main(page: ft.Page) -> None:
    page.title = "PRISQO ERP"
    page.padding = 0
    page.spacing = 0

    theme_manager = ThemeManager(page, initial_mode=AppThemeMode.LIGHT)
    state = {"user": None, "sidebar_open": False}
    root = ft.Container(expand=True)

    def render() -> None:
        theme = theme_manager.theme
        page.bgcolor = theme.background
        if state["user"] is None:
            root.content = build_login(page, theme, on_success=login_success)
        else:
            root.content = build_dashboard(
                theme_manager,
                page,
                state["user"],
                on_logout=logout,
                sidebar_open=state["sidebar_open"],
                on_toggle_drawer=toggle_drawer,
            )
        page.update()

    def login_success(email: str) -> None:
        state["user"] = email
        render()

    def logout() -> None:
        state["user"] = None
        render()

    def toggle_drawer(open_: bool) -> None:
        state["sidebar_open"] = open_
        render()

    theme_manager.subscribe(lambda t: render())
    page.add(root)
    render()


if __name__ == "__main__":
    ft.app(target=main)

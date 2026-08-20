# PRISQO UI KIT

A **standalone, reusable Flet 0.85.3 UI component library** for the future
PRISQO ERP application.

This project does **not** depend on the existing PRISQO ERP codebase, a
database, FastAPI, or any external API. It is meant to be developed and
visually inspected on its own, then copied/integrated into PRISQO ERP later.

- Modern Flet 0.85.3 API only (no legacy `ElevatedButton`, no old padding
  helpers, no Flet 1.x APIs).
- **Liquid-style interactions**: every button, switch, checkbox, and radio
  squishes on press and bounces back with an elastic overshoot on release
  (see "Liquid interaction style" below).
- Full Light / Dark / System theme support via semantic design tokens.
- 70+ components across buttons, cards, forms, tables, dialogs, feedback,
  status, navigation, financial, ERP-specific, and POS-friendly categories.
- A complete showcase application to visually inspect every component.

---

## 1. Installation

```bash
pip install -r requirements.txt
```

Requires **Python 3.11+** and **Flet 0.85.3** exactly (see `requirements.txt`).

## 2. Running the showcase

```bash
python main.py
```

This launches the **PRISQO UI KIT** showcase — a design-system documentation
app with a sidebar for every component category and a Light / Dark / System
theme switcher in the top bar.

## 3. Project structure

```
prisqo_ui/
├── main.py                    # Entry point — launches the showcase
├── requirements.txt
├── pyproject.toml
├── src/prisqo_ui/
│   ├── theme/                 # Design tokens: colors, spacing, radius,
│   │                          # shadows, responsive typography,
│   │                          # breakpoints, light/dark theme, ThemeManager
│   ├── mock_data.py           # Mock ERP data (items, customers, vendors,
│   │                          # employees, locations) — no DB, no API
│   └── components/
│       ├── core/               # Bootstrap-style foundation: variants.py
│       │                      # (resolve_variant/resolve_size) + helpers.py
│       │                      # (spacing/color/flex utility functions)
│       ├── layout/            # AppShell, Sidebar, Navbar, PageContainer,
│       │                      # PageHeader, Breadcrumb
│       ├── buttons/           # Bootstrap-style: base Button(variant=,size=)
│       │                      # + Primary/Secondary/Outline/Ghost/Danger/
│       │                      # Success/Warning/Info/Icon/Loading presets
│       ├── cards/             # AppCard, SectionCard, KPICard, StatCard,
│       │                      # MetricCard
│       ├── forms/             # Text/Number/Currency/Percentage/Search
│       │                      # fields, Dropdown, DateField, LookupField,
│       │                      # FormSection/Row/Actions
│       ├── tables/            # AppDataTable, FilterBar, Pagination,
│       │                      # BulkActionBar, ColumnSelector
│       ├── dialogs/           # AppDialog, ConfirmDialog, DeleteDialog,
│       │                      # WarningDialog, FormDialog
│       ├── feedback/          # Toast, Snackbar, Alert, LoadingSpinner,
│       │                      # Skeletons, EmptyState, ErrorState
│       ├── status/            # StatusChip, StatusBadge, StatusDot, Badge
│       ├── navigation/        # AppTabs, Menu (+ re-exports SidebarItem)
│       ├── charts/            # ChartCard (lightweight bar chart)
│       ├── liquid/            # LiquidPressable (core), LiquidSwitch,
│       │                      # LiquidCheckbox, LiquidRadioGroup
│       ├── erp/                # ItemLookup, CustomerLookup, VendorLookup,
│       │                      # EmployeeLookup, LocationLookup,
│       │                      # AmountDisplay, TotalsSummary,
│       │                      # PaymentSummary, InventoryStatus,
│       │                      # ApprovalStatus
│       └── pos/                # LargeButton, NumericInput,
│                              # QuantityControl, CartItem, CartSummary,
│                              # TenderButton
└── showcase/
    ├── app.py                 # Showcase shell (sidebar nav + theme switcher)
    └── pages/                 # One demo module per component category
```

## 4. Liquid interaction style

Every `Button` variant, `LiquidSwitch`, `LiquidCheckbox`, and
`LiquidRadioGroup` is built on `components/liquid/_liquid_core.py`'s
`LiquidPressable`: controls squish down (`scale=0.92`) on press and spring
back with an `ELASTIC_OUT` overshoot on release, approximating a "liquid"
feel.

**Note on fidelity:** Flet renders through Flutter, not a browser, so it
has no equivalent to the CSS/SVG `feGaussianBlur` + `feColorMatrix` "goo"
filter that web-based liquid UI demos use to make a dot visually *merge*
into a track like a metaball. What's implemented here is the closest
native approximation — elastic scale/position animation — not a literal
gooey blend effect.

```python
from prisqo_ui.components.liquid import LiquidSwitch, LiquidCheckbox, LiquidRadioGroup

LiquidSwitch(theme, value=True, label="Notifications", on_change=lambda v: ...)
LiquidCheckbox(theme, value=False, label="Remember me", on_change=lambda v: ...)
LiquidRadioGroup(
    theme,
    options=[{"key": "cash", "label": "Cash"}, {"key": "card", "label": "Card"}],
    value="cash",
    on_change=lambda key: ...,
)
```

**Known limitation:** `AppDataTable`'s row-selection checkboxes come from
Flet's native `ft.DataTable` (`show_checkbox_column=True`), which renders
Flutter's built-in checkbox widget. That one checkbox family is not
currently swappable for `LiquidCheckbox` without replacing the native
data table entirely — every other checkbox/switch/radio/button in the
library (including `ColumnSelector`'s per-column checkboxes) uses the
liquid style.

## 5. Component + helper pattern (Bootstrap-style)

`src/prisqo_ui/components/core/` is the foundation every other component
family should build on — the same role Bootstrap's `$theme-colors` Sass
map and shared mixins play. Nothing here is component-specific; it's the
one place a variant/size/spacing decision gets made.

```python
from prisqo_ui.components.core import helpers as u
from prisqo_ui.components.core.variants import resolve_variant, resolve_size, VARIANTS, SIZES
```

**`resolve_variant(theme, "success")`** returns a `VariantColors` bundle
(`solid`, `solid_hover`, `on_solid`, `text`, `soft_bg`, `border`) resolved
against the active `Theme`. This is Bootstrap's `button-variant()` /
`badge-variant()` mixin — any component (buttons, badges, alerts, card
accents, or a component you add later) calls this instead of hand-rolling
its own `if variant == "danger": ...` color lookup. Valid variants:
`primary, secondary, success, danger, warning, info, neutral, light, dark`.

**`resolve_size(theme, "lg")`** returns a `SizeSpec` (height, padding,
font size, icon size, radius) — Bootstrap's `.btn-sm`/`.btn-lg` scale,
shared by every component that accepts `size=`.

**`Button()`** in `components/buttons` is the base component built on
these two functions — `PrimaryButton`, `SecondaryButton`, `DangerButton`,
`SuccessButton`, `WarningButton`, `InfoButton`, and `OutlineButton` are
all one-line `Button(variant="...")` presets, exactly like Bootstrap's
`.btn-primary` is `.btn` plus a modifier class rather than a separate
component:

```python
from prisqo_ui.components.buttons import Button

Button(theme, "Approve", variant="success", size="lg")
Button(theme, "Export", variant="primary", outline=True)
Button(theme, "Dismiss", variant="secondary", ghost=True, size="sm")
```

`StatusChip` / `StatusBadge` / `StatusDot` (`components/status`) and the
new `Alert` (`components/feedback`) follow the same rule — they resolve
an ERP status string to a variant automatically, but also accept an
explicit `variant=` for one-off labels. `AppCard` accepts an optional
`variant=` for a `.card.border-{variant}`-style accent edge.

**`helpers.py`** covers what Bootstrap's utility classes do —
composable one-liners instead of custom CSS:

```python
u.p(theme, 3)                 # padding, all sides — Bootstrap's .p-3
u.mt(theme, 4)                # margin-top — .mt-4
u.gap(theme, 2)                # Row/Column spacing — .gap-2
u.text_color(theme, "danger")  # .text-danger
u.bg_color(theme, "success")   # .bg-success-subtle (soft=True by default)
u.rounded(theme, "lg")         # .rounded-lg
u.shadow(theme, "raised")      # .shadow

u.row(theme, [a, b, c], gap=2, justify="between", align="center")  # .d-flex .gap-2 .justify-content-between
u.stack(theme, [a, b], gap=1)                                       # vertical version

u.Box(theme, content=my_control, p=3, mt=4, bg="info", rounded="lg", shadow="card")
```

The spacing scale is Bootstrap's familiar `0–5` (plus `6`), mapped onto
this kit's existing `Spacing` tokens (`1` → `XS`/4px … `6` → `XXL`/32px),
so it stays themeable from `theme/spacing.py` rather than hardcoding
pixels.

**Extending the pattern to other component families** (cards, forms,
tables, dialogs, nav, ...): pull colors from `resolve_variant` and
sizing from `resolve_size` instead of adding new local color/size logic,
add a thin named preset only when a call site benefits from it (the way
`DangerButton` exists but `Button(variant="danger")` also always works),
and reach for `helpers.py` for spacing/layout instead of one-off
`ft.Padding`/`ft.Margin` literals.

## 6. Responsive typography

Every `theme.typography.<role>()` call is now responsive: `ThemeManager`
tracks the page width, resolves it against a Bootstrap-style breakpoint
scale (`theme/breakpoints.py` — same `xs/sm/md/lg/xl/xxl` names and
min-widths as Bootstrap's `$grid-breakpoints`), and hands components a
`Theme` whose `typography` is scaled for that breakpoint. Components
never measure anything themselves — they just keep calling
`theme.typography.page_title(color)` like before, and get back a
correctly-sized `ft.TextStyle` for whatever the page width currently is.

```python
from prisqo_ui.theme import BREAKPOINTS, resolve_breakpoint

# xs (phones)  -> 0.88x   sm -> 0.92x   md (tablets) -> 0.96x
# lg (laptops) -> 1.00x   xl -> 1.04x   xxl (wide desktop) -> 1.08x
```

`lg` (≈992px, a typical laptop) is the 1.0× baseline this kit's existing
type scale was designed at — nothing changes at that width. Below it,
text scales down (bounded by a `10px` floor so it never becomes
illegible); above it, text scales up slightly for large back-office
monitors.

This happens automatically wherever `ThemeManager` is already wired up —
resizing the window fires the same `subscribe()` callback used for
light/dark switching, so the whole UI rebuilds with the new scale. No
component changes are required; see the **Typography** page in the
showcase app for a live breakpoint/scale readout.

For layout (not just text) that should also respond to screen size,
`components/core/helpers.py` adds:

```python
from prisqo_ui.components.core import helpers as u

u.is_mobile(theme)     # below sm  — .d-sm-none territory
u.is_tablet(theme)     # md/lg
u.is_desktop(theme)    # xl and up

columns = u.responsive(theme, xs=1, sm=1, md=2, lg=3)  # Bootstrap's responsive-prop cascade
```

`theme.breakpoint` (`"xs"`…`"xxl"`) is also available directly on any
`Theme` instance for custom branching.

## 7. Theme system

Every component takes a `theme: Theme` as its first argument. `Theme` is a
dataclass of **semantic tokens** — components never reference raw hex colors.

```python
from prisqo_ui.theme import LIGHT_THEME, DARK_THEME, ThemeManager, AppThemeMode

# In a Flet app:
theme_manager = ThemeManager(page, initial_mode=AppThemeMode.LIGHT)
theme_manager.set_mode(AppThemeMode.DARK)          # switch instantly, no restart
theme_manager.subscribe(lambda theme: rebuild_ui()) # react to theme changes
```

`AppThemeMode.SYSTEM` follows the OS-level brightness via
`page.platform_brightness` / `page.on_platform_brightness_change` and updates
automatically if the OS theme changes while the app is open.

### Semantic tokens available on `Theme`

```
background, surface, surface_variant
sidebar_bg, sidebar_text, sidebar_text_muted, sidebar_active_bg
text_primary, text_secondary, text_muted, text_on_primary
border, divider
primary, primary_hover, primary_pressed, primary_disabled, primary_light
success, success_bg, warning, warning_bg, danger, danger_bg, info, info_bg
neutral_bg, neutral_text, focus
spacing (XS..XXL), radius (SM..ROUND), typography (page_title..currency),
shadows (card, raised, dropdown)
```

## 8. Component usage examples

```python
from prisqo_ui.theme import LIGHT_THEME as theme
from prisqo_ui.components.buttons import PrimaryButton
from prisqo_ui.components.cards import KPICard
from prisqo_ui.components.status import StatusChip
from prisqo_ui.components.erp import AmountDisplay, ItemLookup

PrimaryButton(theme, text="Save", icon=ft.Icons.SAVE, on_click=handle_save)

KPICard(
    theme,
    title="Today's Sales",
    value="\u20b1125,450.00",
    trend="+12.5%",
    trend_label="vs yesterday",
)

StatusChip(theme, label="Active", status="active")

AmountDisplay(theme, amount=1250.50)

ItemLookup(theme, page, on_select=lambda item: print(item))
```

Most components that open a dialog (lookups, `AppDialog`/`ConfirmDialog`/etc.)
need the current Flet `page` object as their second argument, since dialogs
are shown via `page.show_dialog(...)` / dismissed via `page.pop_dialog()` —
the modern Flet 0.85.3 dialog API.

## 9. Customization

All raw color values live in **one place**:
`src/prisqo_ui/theme/colors.py` (`LightPalette` / `DarkPalette`).

To restyle the whole library, edit the palettes there and/or the semantic
mappings in `light_theme.py` / `dark_theme.py` — no component file needs to
change, since components only ever read `theme.<semantic_token>`.

Spacing (`theme/spacing.py`), radius (`theme/radius.py`), typography
(`theme/typography.py`), and shadows (`theme/shadows.py`) are similarly
centralized.

## 10. Integration into PRISQO ERP

1. Copy `src/prisqo_ui/` into the PRISQO ERP project (e.g. as a local
   package or installable dependency).
2. Wire up a `ThemeManager` once, near your app's root `main(page)` function.
3. Import components from `prisqo_ui.components.<category>` wherever you
   build ERP pages/screens.
4. Replace the mock data in `prisqo_ui/mock_data.py` and the lookup
   defaults in `components/erp/lookups.py` with real data sources — the
   components themselves do not know or care where the data comes from.
5. `TotalsSummary` / `PaymentSummary` / `AmountDisplay` are display-only;
   continue to compute VAT, discounts, and totals in your ERP's business
   logic layer and pass the results in.

## 11. What this library intentionally does NOT do

- No SQL, no database access, no API requests, no authentication.
- No inventory, VAT, discount, or posting/accounting calculations.
- No dependency on FastAPI, MySQL, or the existing PRISQO ERP codebase.

These are the responsibility of the PRISQO ERP application layer that will
eventually consume this component library.

## 12. Changelog — ported from PRISCO ERP

The following components were added after comparing this library against
PRISCO ERP's existing hand-rolled `client/shared/ui/components/` widgets,
to close gaps the app already depended on:

- **`TimeField`** (`components/forms`) — same read-only + picker-on-click
  convention as `DateField`, using `ft.TimePicker`. PRISCO ERP had a
  `time_field`/`attach_time_picker` helper with no equivalent here.
- **`DynamicRowList` / `RowField`** (`components/forms`) — the repeatable
  "+ Row" add/remove pattern PRISCO ERP's Doctor Console uses for its
  Prescription/Vaccine/Surgery/Allergy/Condition forms. Rebuilt on this
  library's `AppTextField`/`AppDropdown`/`GhostButton`/`AppIconButton`
  instead of the original's raw colors and stock Flet buttons.
- **`ToastService`** (`components/feedback`) — a page-bound wrapper around
  the existing one-shot `Toast()` function, adding severity-scaled
  durations and the canned shortcuts (`saved`, `updated`, `deleted`,
  `permission_denied`, `validation_failed`, `api_error`,
  `duplicate_entry`, `not_found`) PRISCO ERP calls from nearly every form
  and list screen.
- **`AsyncFormDialog`** (`components/dialogs`) — a `FormDialog` variant
  for submits that hit the network/DB: it only closes when `on_submit()`
  returns `True`, shows a busy/spinner state on the submit button while
  it runs (via `page.run_thread`, so a slow request can't be
  double-submitted), and caps + scrolls tall content so a
  `DynamicRowList`-heavy form doesn't push its actions off-screen.
  `FormDialog` itself is unchanged — existing call sites that rely on it
  closing unconditionally on submit keep working.

Every addition above follows the existing conventions: `theme: Theme` as
the first argument, semantic tokens only (no raw hex), and the liquid
button/interaction style already used throughout the rest of the kit.


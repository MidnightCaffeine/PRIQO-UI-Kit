"""Dark theme — intentionally designed, not an inverted light theme."""
from .colors import DARK_PALETTE as P
from .shadows import dark_shadows
from .theme import Theme

DARK_THEME = Theme(
    mode="dark",
    background=P.BACKGROUND,
    surface=P.SURFACE,
    surface_variant=P.SURFACE_VARIANT,
    sidebar_bg=P.SIDEBAR_BG,
    sidebar_text=P.SIDEBAR_TEXT,
    sidebar_text_muted=P.SIDEBAR_TEXT_MUTED,
    sidebar_active_bg=P.SIDEBAR_ACTIVE_BG,
    text_primary=P.TEXT_PRIMARY,
    text_secondary=P.TEXT_SECONDARY,
    text_muted=P.TEXT_MUTED,
    text_on_primary=P.TEXT_ON_PRIMARY,
    border=P.BORDER,
    divider=P.DIVIDER,
    primary=P.PRIMARY,
    primary_hover=P.PRIMARY_LIGHT,
    primary_pressed=P.PRIMARY_DARK,
    primary_disabled="#3B3F52",
    primary_light=P.PRIMARY_LIGHT,
    success=P.SUCCESS,
    success_bg=P.SUCCESS_BG,
    warning=P.WARNING,
    warning_bg=P.WARNING_BG,
    danger=P.DANGER,
    danger_bg=P.DANGER_BG,
    info=P.INFO,
    info_bg=P.INFO_BG,
    neutral_bg=P.NEUTRAL_BG,
    neutral_text=P.NEUTRAL_TEXT,
    focus=P.PRIMARY_LIGHT,
    shadows=dark_shadows(),
)

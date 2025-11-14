"""
Components package initialization
"""

from .theme import inject_theme_css, apply_plotly_theme, get_theme_colors
from .layout import (
    auth_guard,
    app_header,
    page_header,
    sidebar_brand,
    sidebar_user_info,
    metric_card,
    status_badge,
    nc_level_badge,
    info_box,
    section_divider,
    empty_state
)
from .auth import show_login_form, logout

__all__ = [
    'inject_theme_css',
    'apply_plotly_theme',
    'get_theme_colors',
    'auth_guard',
    'app_header',
    'page_header',
    'sidebar_brand',
    'sidebar_user_info',
    'metric_card',
    'status_badge',
    'nc_level_badge',
    'info_box',
    'section_divider',
    'empty_state',
    'show_login_form',
    'logout'
]

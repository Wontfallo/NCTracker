"""
Layout Components for NCTracker
Reusable layout elements and page structure
"""

import streamlit as st
from typing import List, Dict, Optional, Callable


def auth_guard() -> bool:
    """
    Check if user is authenticated, redirect to login if not
    Returns True if authenticated, False otherwise
    """
    if 'user' not in st.session_state or st.session_state.user is None:
        st.warning("Please log in to access this page")
        st.stop()
        return False
    return True


def app_header(title: str, subtitle: Optional[str] = None, icon: str = "📋"):
    """
    Render professional app header with gradient
    
    Args:
        title: Main heading text
        subtitle: Optional subtitle text
        icon: Emoji icon
    """
    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg, #6366F1 0%, #4F46E5 50%, #4338CA 100%);
        color: white;
        padding: 2.5rem 2rem;
        border-radius: 16px;
        margin-bottom: 2rem;
        text-align: center;
        box-shadow: 0 10px 40px rgba(99, 102, 241, 0.3);
        position: relative;
        overflow: hidden;
    ">
        <div style="position: relative; z-index: 1;">
            <div style="font-size: 3rem; margin-bottom: 0.5rem;">{icon}</div>
            <h1 style="
                font-size: 2.5rem;
                font-weight: 700;
                margin: 0;
                text-shadow: 0 2px 4px rgba(0,0,0,0.2);
            ">
                {title}
            </h1>
            {f'<p style="font-size: 1.125rem; opacity: 0.95; margin-top: 0.5rem;">{subtitle}</p>' if subtitle else ''}
        </div>
    </div>
    """, unsafe_allow_html=True)


def page_header(title: str, actions: Optional[List] = None):
    """
    Render a page header with optional action buttons
    
    Args:
        title: Page title
        actions: List of action button configs
    """
    cols = st.columns([3, 1])
    
    with cols[0]:
        st.markdown(f"""
        <h2 style="
            color: var(--color-text);
            font-weight: 700;
            margin: 0;
            padding-bottom: 1rem;
            border-bottom: 2px solid var(--color-border);
        ">{title}</h2>
        """, unsafe_allow_html=True)
    
    with cols[1]:
        if actions:
            for action in actions:
                if callable(action):
                    action()


def sidebar_brand():
    """Render branded sidebar header"""
    st.sidebar.markdown("""
    <div style="
        text-align: center;
        padding: 1.5rem 0.5rem;
        border-bottom: 2px solid var(--color-border);
        margin-bottom: 1.5rem;
    ">
        <div style="font-size: 2.5rem; margin-bottom: 0.5rem;">🔍</div>
        <h2 style="
            color: var(--color-primary-400);
            font-weight: 700;
            margin: 0;
            font-size: 1.5rem;
        ">NCTracker</h2>
        <p style="
            color: var(--color-text-muted);
            font-size: 0.75rem;
            margin: 0.25rem 0 0 0;
            text-transform: uppercase;
            letter-spacing: 0.1em;
        ">Quality Management</p>
    </div>
    """, unsafe_allow_html=True)


def sidebar_user_info():
    """Display user info in sidebar"""
    if 'user' in st.session_state and st.session_state.user:
        user = st.session_state.user
        
        st.sidebar.markdown(f"""
        <div style="
            background: var(--color-bg-2);
            border: 1px solid var(--color-border);
            border-radius: 12px;
            padding: 1rem;
            margin-bottom: 1.5rem;
        ">
            <div style="
                display: flex;
                align-items: center;
                gap: 0.75rem;
                margin-bottom: 0.5rem;
            ">
                <div style="
                    background: var(--color-primary-600);
                    color: white;
                    width: 40px;
                    height: 40px;
                    border-radius: 50%;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    font-weight: 700;
                    font-size: 1.125rem;
                ">
                    {user['full_name'][0].upper() if user.get('full_name') else 'U'}
                </div>
                <div style="flex: 1;">
                    <div style="
                        color: var(--color-text);
                        font-weight: 600;
                        font-size: 0.875rem;
                    ">{user.get('full_name', 'User')}</div>
                    <div style="
                        color: var(--color-text-muted);
                        font-size: 0.75rem;
                        text-transform: capitalize;
                    ">{user.get('role', 'User').replace('_', ' ')}</div>
                </div>
            </div>
            <div style="
                font-size: 0.75rem;
                color: var(--color-text-muted);
                padding-top: 0.5rem;
                border-top: 1px solid var(--color-border);
            ">
                {user.get('department', 'N/A')}
            </div>
        </div>
        """, unsafe_allow_html=True)


def metric_card(label: str, value: str, delta: Optional[str] = None, 
                delta_color: str = "normal", icon: str = "📊"):
    """
    Render a custom metric card with enhanced styling
    
    Args:
        label: Metric label
        value: Metric value
        delta: Optional delta/change text
        delta_color: Color for delta (normal, positive, negative)
        icon: Emoji icon
    """
    delta_colors = {
        "normal": "var(--color-info)",
        "positive": "var(--color-success)",
        "negative": "var(--color-error)",
        "off": "var(--color-text-muted)"
    }
    
    delta_html = ""
    if delta:
        color = delta_colors.get(delta_color, delta_colors["normal"])
        delta_html = f"""
        <div style="
            color: {color};
            font-size: 0.875rem;
            font-weight: 500;
            margin-top: 0.5rem;
        ">
            {delta}
        </div>
        """
    
    card_html = f"""
    <div class="metric-card">
        <div style="font-size: 2rem; margin-bottom: 0.5rem; opacity: 0.8;">{icon}</div>
        <div style="
            font-size: 0.75rem;
            font-weight: 600;
            color: var(--color-text-muted);
            text-transform: uppercase;
            letter-spacing: 0.05em;
            margin-bottom: 0.5rem;
        ">{label}</div>
        <div style="
            font-size: 2rem;
            font-weight: 700;
            color: var(--color-text);
            line-height: 1;
        ">{value}</div>
        {delta_html}
    </div>
    """

    if hasattr(st, "html"):
        st.html(card_html)
    else:
        st.markdown(card_html, unsafe_allow_html=True)


def status_badge(status: str) -> str:
    """
    Generate HTML for a status badge
    
    Args:
        status: Status value (NEW, IN_PROGRESS, PENDING_APPROVAL, CLOSED)
    
    Returns:
        HTML string for badge
    """
    status_config = {
        'NEW': {'label': 'New', 'class': 'status-new', 'icon': '🆕'},
        'IN_PROGRESS': {'label': 'In Progress', 'class': 'status-in-progress', 'icon': '⚙️'},
        'PENDING_APPROVAL': {'label': 'Pending Approval', 'class': 'status-pending-approval', 'icon': '⏳'},
        'CLOSED': {'label': 'Closed', 'class': 'status-closed', 'icon': '✅'},
    }
    
    config = status_config.get(status, {'label': status, 'class': 'status-new', 'icon': '📋'})
    
    return f"""
    <span class="{config['class']}">
        {config['icon']} {config['label']}
    </span>
    """


def nc_level_badge(level: int) -> str:
    """
    Generate HTML for NC level badge
    
    Args:
        level: NC level (1-4)
    
    Returns:
        HTML string for badge
    """
    level_config = {
        1: {'label': 'Critical', 'class': 'nc-level-1', 'icon': '🔴'},
        2: {'label': 'Adverse', 'class': 'nc-level-2', 'icon': '🟠'},
        3: {'label': 'Moderate', 'class': 'nc-level-3', 'icon': '🟡'},
        4: {'label': 'Low', 'class': 'nc-level-4', 'icon': '🟢'},
    }
    
    config = level_config.get(level, {'label': f'Level {level}', 'class': 'nc-level-3', 'icon': '⚪'})
    
    return f"""
    <span class="{config['class']}">
        {config['icon']} Level {level} - {config['label']}
    </span>
    """


def info_box(title: str, content: str, type: str = "info"):
    """
    Render an info box
    
    Args:
        title: Box title
        content: Box content
        type: Box type (info, success, warning, error)
    """
    icons = {
        'info': 'ℹ️',
        'success': '✅',
        'warning': '⚠️',
        'error': '❌'
    }
    
    st.markdown(f"""
    <div class="badge-{type}" style="
        padding: 1rem;
        border-radius: 12px;
        margin: 1rem 0;
    ">
        <div style="
            font-weight: 600;
            margin-bottom: 0.5rem;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        ">
            <span>{icons.get(type, 'ℹ️')}</span>
            <span>{title}</span>
        </div>
        <div style="font-size: 0.875rem; line-height: 1.6;">
            {content}
        </div>
    </div>
    """, unsafe_allow_html=True)


def section_divider(text: Optional[str] = None):
    """
    Render a section divider
    
    Args:
        text: Optional divider text
    """
    if text:
        st.markdown(f"""
        <div style="
            display: flex;
            align-items: center;
            margin: 2rem 0;
            gap: 1rem;
        ">
            <div style="flex: 1; height: 2px; background: var(--color-border);"></div>
            <div style="
                color: var(--color-text-muted);
                font-weight: 600;
                font-size: 0.875rem;
                text-transform: uppercase;
                letter-spacing: 0.1em;
            ">{text}</div>
            <div style="flex: 1; height: 2px; background: var(--color-border);"></div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style="height: 2px; background: var(--color-border); margin: 2rem 0;"></div>
        """, unsafe_allow_html=True)


def empty_state(icon: str, title: str, message: str, action_label: Optional[str] = None):
    """
    Render an empty state message
    
    Args:
        icon: Emoji icon
        title: Empty state title
        message: Empty state message
        action_label: Optional CTA button label
    """
    st.markdown(f"""
    <div style="
        text-align: center;
        padding: 4rem 2rem;
        background: var(--color-bg-2);
        border: 2px dashed var(--color-border);
        border-radius: 16px;
        margin: 2rem 0;
    ">
        <div style="font-size: 4rem; margin-bottom: 1rem; opacity: 0.5;">{icon}</div>
        <h3 style="
            color: var(--color-text);
            font-weight: 600;
            margin-bottom: 0.5rem;
        ">{title}</h3>
        <p style="
            color: var(--color-text-muted);
            font-size: 1rem;
            margin-bottom: 1.5rem;
        ">{message}</p>
    </div>
    """, unsafe_allow_html=True)
    
    if action_label:
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            return st.button(action_label, type="primary", width="stretch")

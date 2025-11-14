"""
Theme Management Component for NCTracker
Handles dark/light mode theming with persistence
"""

import streamlit as st
import streamlit.components.v1 as components
from pathlib import Path


def inject_theme_css():
    """Inject the custom modern theme CSS into the app"""
    css_file = Path(__file__).parent.parent / "assets" / "theme_modern.css"
    
    if css_file.exists():
        with open(css_file, "r", encoding="utf-8") as f:
            css_content = f.read()
        
        st.markdown(f"""
        <style>
        {css_content}
        </style>
        """, unsafe_allow_html=True)
    else:
        st.warning("Theme CSS file not found")


def inject_theme_js():
    """Inject theme toggle JavaScript"""
    js_file = Path(__file__).parent.parent / "assets" / "theme.js"
    
    if js_file.exists():
        with open(js_file, "r", encoding="utf-8") as f:
            js_content = f.read()
        
        components.html(f"""
        <script>
        {js_content}
        </script>
        """, height=0)


def theme_toggle():
    """
    Render a theme toggle button
    Returns the current theme
    """
    # Initialize session state
    if 'theme' not in st.session_state:
        st.session_state.theme = 'dark'
    
    col1, col2 = st.columns([6, 1])
    
    with col2:
        if st.session_state.theme == 'dark':
            if st.button("☀️ Light", key="theme_toggle", help="Switch to light mode"):
                st.session_state.theme = 'light'
                # Send message to JS
                components.html("""
                <script>
                window.parent.postMessage({
                    type: 'nctracker:setTheme',
                    theme: 'light'
                }, '*');
                </script>
                """, height=0)
                st.rerun()
        else:
            if st.button("🌙 Dark", key="theme_toggle", help="Switch to dark mode"):
                st.session_state.theme = 'dark'
                # Send message to JS
                components.html("""
                <script>
                window.parent.postMessage({
                    type: 'nctracker:setTheme',
                    theme: 'dark'
                }, '*');
                </script>
                """, height=0)
                st.rerun()
    
    return st.session_state.theme


def apply_plotly_theme():
    """
    Configure Plotly to use dark theme matching the app
    """
    import plotly.express as px
    import plotly.graph_objects as go
    import plotly.io as pio
    
    # Create custom dark template aligned with modern theme palette
    pio.templates["nctracker_dark"] = go.layout.Template(
        layout=go.Layout(
            paper_bgcolor='#0f172a',
            plot_bgcolor='#111c34',
            font=dict(
                family='system-ui, -apple-system, sans-serif',
                size=14,
                color='#f8fafc'
            ),
            title=dict(
                font=dict(size=20, color='#f8fafc', weight='bold'),
                x=0.5,
                xanchor='center'
            ),
            xaxis=dict(
                gridcolor='#24324d',
                linecolor='#24324d',
                zerolinecolor='#24324d',
                tickfont=dict(color='#cbd5f5'),
                title=dict(font=dict(color='#f8fafc')),
            ),
            yaxis=dict(
                gridcolor='#24324d',
                linecolor='#24324d',
                zerolinecolor='#24324d',
                tickfont=dict(color='#cbd5f5'),
                title=dict(font=dict(color='#f8fafc')),
            ),
            legend=dict(
                bgcolor='#111c34',
                bordercolor='#24324d',
                font=dict(color='#f8fafc')
            ),
            hovermode='closest',
            hoverlabel=dict(
                bgcolor='#1e293b',
                bordercolor='#38bdf8',
                font=dict(color='#f8fafc', size=13)
            )
        )
    )
    
    # Set as default
    pio.templates.default = "nctracker_dark"
    
    # Set custom colorway - bright colors
    px.defaults.color_discrete_sequence = [
        '#38bdf8',
        '#6366f1',
        '#f97316',
        '#22c55e',
        '#ef4444',
        '#818cf8',
        '#facc15',
        '#14b8a6',
    ]


def get_theme_colors():
    """
    Return a dictionary of theme colors for use in code
    """
    return {
        'primary': '#38bdf8',
        'secondary': '#6366f1',
        'success': '#22c55e',
        'warning': '#f97316',
        'error': '#ef4444',
        'info': '#818cf8',
        'bg_0': '#0f172a',
        'bg_1': '#111c34',
        'bg_2': '#1e293b',
        'panel': '#24324d',
        'border': '#2f3c58',
        'text': '#f8fafc',
        'text_muted': '#cbd5f5',
    }

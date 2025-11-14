"""
NCTracker - Professional Quality NCR Management System
Version 2.0 - Modern Dark Mode UI/UX

Main Entry Point - Handles authentication and routing
"""

import streamlit as st
import sys
from pathlib import Path

# Add components to path
sys.path.append(str(Path(__file__).parent))

from components import inject_theme_css, apply_plotly_theme, show_login_form
from database import db

# Page configuration
st.set_page_config(
    page_title="NCTracker - Quality Management System",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': None,
        'Report a bug': None,
        'About': "NCTracker v2.0 - Professional Quality NCR Management"
    }
)

# Apply professional dark theme
inject_theme_css()
apply_plotly_theme()

# Initialize session state
def init_session_state():
    """Initialize all session state variables"""
    if 'user' not in st.session_state:
        st.session_state.user = None
    if 'current_ncr' not in st.session_state:
        st.session_state.current_ncr = None
    if 'ncr_form_data' not in st.session_state:
        st.session_state.ncr_form_data = {}
    if 'current_section' not in st.session_state:
        st.session_state.current_section = 1
    if 'theme' not in st.session_state:
        st.session_state.theme = 'dark'

init_session_state()

# Main application logic
def main():
    """Main application entry point"""
    
    # Check authentication
    if st.session_state.user is None:
        # Show login page
        show_login_form()
    else:
        # User is authenticated - redirect to dashboard
        st.switch_page("pages/01_📊_Dashboard.py")

if __name__ == "__main__":
    main()

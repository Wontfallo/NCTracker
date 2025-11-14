"""
Logout Page - Clear session and return to login
"""

import streamlit as st
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from components import inject_theme_css, logout

st.set_page_config(
    page_title="Logout - NCTracker",
    page_icon="🚪",
    layout="centered"
)

inject_theme_css()

# Logout handler
logout()

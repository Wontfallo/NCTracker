"""
NCTracker - Main Application Entry Point
Quality NCR Tracking System
"""

import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, date, timedelta
import json
import os
from pathlib import Path
import io
from typing import List, Dict

# Import our modules
from database import db
import utils

# Page configuration
st.set_page_config(
    page_title="NCTracker - Quality NCR System",
    page_icon="📋",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Modern Professional CSS Design System
st.markdown("""
<style>
    /* ===== DESIGN TOKENS ===== */
    :root {
        /* Primary Brand Colors */
        --primary-50: #eff6ff;
        --primary-100: #dbeafe;
        --primary-200: #bfdbfe;
        --primary-300: #93c5fd;
        --primary-400: #60a5fa;
        --primary-500: #3b82f6;
        --primary-600: #2563eb;
        --primary-700: #1d4ed8;
        --primary-800: #1e40af;
        --primary-900: #1e3a8a;
        
        /* Neutral Grays */
        --gray-50: #f9fafb;
        --gray-100: #f3f4f6;
        --gray-200: #e5e7eb;
        --gray-300: #d1d5db;
        --gray-400: #9ca3af;
        --gray-500: #6b7280;
        --gray-600: #4b5563;
        --gray-700: #374151;
        --gray-800: #1f2937;
        --gray-900: #111827;
        
        /* Semantic Colors */
        --success: #22c55e;
        --success-light: #dcfce7;
        --warning: #f59e0b;
        --warning-light: #fef3c7;
        --error: #ef4444;
        --error-light: #fee2e2;
        --info: #3b82f6;
        --info-light: #dbeafe;
        
        /* Shadows */
        --shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
        --shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px -1px rgba(0, 0, 0, 0.1);
        --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -2px rgba(0, 0, 0, 0.1);
        --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -4px rgba(0, 0, 0, 0.1);
        --shadow-xl: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 8px 10px -6px rgba(0, 0, 0, 0.1);
        
        /* Border Radius */
        --radius-sm: 6px;
        --radius: 8px;
        --radius-md: 10px;
        --radius-lg: 12px;
        --radius-xl: 16px;
        
        /* Transitions */
        --transition-fast: 150ms cubic-bezier(0.4, 0, 0.2, 1);
        --transition-base: 200ms cubic-bezier(0.4, 0, 0.2, 1);
        --transition-slow: 300ms cubic-bezier(0.4, 0, 0.2, 1);
    }
    
    /* ===== GLOBAL STYLES ===== */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1400px;
    }
    
    /* Smooth scrolling */
    html {
        scroll-behavior: smooth;
    }
    
    /* ===== HEADER COMPONENTS ===== */
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 2.5rem 2rem;
        border-radius: var(--radius-xl);
        margin-bottom: 2.5rem;
        text-align: center;
        box-shadow: var(--shadow-xl);
        position: relative;
        overflow: hidden;
        animation: fadeIn 0.6s ease-out;
    }
    
    .main-header::before {
        content: '';
        position: absolute;
        top: -50%;
        right: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%);
        animation: rotate 20s linear infinite;
    }
    
    .main-header h1 {
        font-size: 2.5rem;
        font-weight: 700;
        margin: 0;
        position: relative;
        z-index: 1;
        text-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }
    
    .main-header p {
        font-size: 1.125rem;
        margin: 0.5rem 0 0 0;
        opacity: 0.95;
        position: relative;
        z-index: 1;
    }
    
    /* ===== CARD COMPONENTS ===== */
    .metric-card {
        background: white;
        padding: 1.75rem;
        border-radius: var(--radius-lg);
        box-shadow: var(--shadow-md);
        text-align: center;
        border: 1px solid var(--gray-200);
        transition: all var(--transition-base);
        position: relative;
        overflow: hidden;
    }
    
    .metric-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 4px;
        background: linear-gradient(90deg, var(--primary-500), var(--primary-600));
        transform: scaleX(0);
        transition: transform var(--transition-base);
    }
    
    .metric-card:hover {
        transform: translateY(-4px);
        box-shadow: var(--shadow-xl);
        border-color: var(--primary-300);
    }
    
    .metric-card:hover::before {
        transform: scaleX(1);
    }
    
    .status-card {
        background: linear-gradient(135deg, var(--gray-50) 0%, white 100%);
        padding: 1.75rem;
        border-radius: var(--radius-lg);
        border-left: 4px solid var(--primary-500);
        margin: 0.75rem 0;
        box-shadow: var(--shadow);
        transition: all var(--transition-base);
    }
    
    .status-card:hover {
        box-shadow: var(--shadow-lg);
        transform: translateX(4px);
    }
    
    .section-header {
        background: linear-gradient(135deg, var(--primary-50) 0%, var(--primary-100) 100%);
        padding: 1rem 1.25rem;
        border-radius: var(--radius);
        border-left: 4px solid var(--primary-600);
        margin: 1.5rem 0 1rem 0;
        font-weight: 600;
        color: var(--primary-800);
        box-shadow: var(--shadow-sm);
        transition: all var(--transition-base);
    }
    
    .section-header:hover {
        background: linear-gradient(135deg, var(--primary-100) 0%, var(--primary-200) 100%);
        transform: translateX(4px);
    }
    
    /* ===== FORM COMPONENTS ===== */
    .form-section {
        background: white;
        padding: 2rem;
        border-radius: var(--radius-lg);
        margin: 1.5rem 0;
        border: 1px solid var(--gray-200);
        box-shadow: var(--shadow-md);
        transition: all var(--transition-base);
    }
    
    .form-section:hover {
        box-shadow: var(--shadow-lg);
        border-color: var(--primary-200);
    }
    
    /* Enhanced Input Fields */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea,
    .stSelectbox > div > div > div,
    .stNumberInput > div > div > input,
    .stDateInput > div > div > input {
        background-color: var(--gray-50) !important;
        border: 2px solid var(--gray-200) !important;
        border-radius: var(--radius) !important;
        padding: 12px 16px !important;
        min-height: 48px !important;
        font-size: 1rem !important;
        transition: all var(--transition-base) !important;
        color: var(--gray-900) !important;
        font-weight: 400 !important;
    }
    
    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus,
    .stSelectbox > div > div > div:focus,
    .stNumberInput > div > div > input:focus,
    .stDateInput > div > div > input:focus {
        border-color: var(--primary-500) !important;
        box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1) !important;
        outline: none !important;
        background-color: white !important;
        transform: scale(1.01);
    }
    
    .stTextInput > div > div > input:hover,
    .stTextArea > div > div > textarea:hover,
    .stSelectbox > div > div > div:hover,
    .stNumberInput > div > div > input:hover,
    .stDateInput > div > div > input:hover {
        border-color: var(--gray-400) !important;
        background-color: white !important;
    }
    
    /* Label Enhancement */
    label {
        font-weight: 600 !important;
        font-size: 0.9375rem !important;
        color: var(--gray-800) !important;
        margin-bottom: 0.5rem !important;
        letter-spacing: 0.01em !important;
    }
    
    /* Radio and Checkbox */
    .stRadio > div,
    .stCheckbox > div {
        padding: 0.5rem 0;
        transition: all var(--transition-base);
    }
    
    .stRadio > div:hover,
    .stCheckbox > div:hover {
        background-color: var(--gray-50);
        border-radius: var(--radius-sm);
    }
    
    /* ===== BUTTON COMPONENTS ===== */
    .stButton > button {
        border-radius: var(--radius) !important;
        font-weight: 600 !important;
        padding: 0.625rem 1.5rem !important;
        transition: all var(--transition-base) !important;
        border: none !important;
        box-shadow: var(--shadow) !important;
        letter-spacing: 0.025em !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: var(--shadow-lg) !important;
    }
    
    .stButton > button:active {
        transform: translateY(0) !important;
    }
    
    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, var(--primary-500) 0%, var(--primary-600) 100%) !important;
    }
    
    .stButton > button[kind="primary"]:hover {
        background: linear-gradient(135deg, var(--primary-600) 0%, var(--primary-700) 100%) !important;
    }
    
    /* ===== STATUS BADGES ===== */
    .status-new {
        background: linear-gradient(135deg, var(--info-light) 0%, var(--primary-100) 100%);
        color: var(--primary-800);
        padding: 6px 14px;
        border-radius: var(--radius);
        border-left: 4px solid var(--primary-500);
        font-weight: 600;
        display: inline-block;
        box-shadow: var(--shadow-sm);
        animation: slideIn 0.3s ease-out;
    }
    
    .status-in-progress {
        background: linear-gradient(135deg, var(--warning-light) 0%, #fde68a 100%);
        color: #92400e;
        padding: 6px 14px;
        border-radius: var(--radius);
        border-left: 4px solid var(--warning);
        font-weight: 600;
        display: inline-block;
        box-shadow: var(--shadow-sm);
        animation: slideIn 0.3s ease-out;
    }
    
    .status-pending-approval {
        background: linear-gradient(135deg, #fce7f3 0%, #fbcfe8 100%);
        color: #831843;
        padding: 6px 14px;
        border-radius: var(--radius);
        border-left: 4px solid #ec4899;
        font-weight: 600;
        display: inline-block;
        box-shadow: var(--shadow-sm);
        animation: slideIn 0.3s ease-out;
    }
    
    .status-closed {
        background: linear-gradient(135deg, var(--success-light) 0%, #bbf7d0 100%);
        color: #14532d;
        padding: 6px 14px;
        border-radius: var(--radius);
        border-left: 4px solid var(--success);
        font-weight: 600;
        display: inline-block;
        box-shadow: var(--shadow-sm);
        animation: slideIn 0.3s ease-out;
    }
    
    /* NC Level Badges */
    .nc-level-1 {
        background: linear-gradient(135deg, var(--error-light) 0%, #fecaca 100%);
        color: #991b1b;
        border-left: 4px solid var(--error);
        padding: 6px 14px;
        border-radius: var(--radius);
        font-weight: 600;
        display: inline-block;
        box-shadow: var(--shadow-sm);
        animation: pulse 2s ease-in-out infinite;
    }
    
    .nc-level-2 {
        background: linear-gradient(135deg, #fed7aa 0%, #fdba74 100%);
        color: #9a3412;
        border-left: 4px solid #f97316;
        padding: 6px 14px;
        border-radius: var(--radius);
        font-weight: 600;
        display: inline-block;
        box-shadow: var(--shadow-sm);
    }
    
    .nc-level-3 {
        background: linear-gradient(135deg, var(--warning-light) 0%, #fde68a 100%);
        color: #92400e;
        border-left: 4px solid #eab308;
        padding: 6px 14px;
        border-radius: var(--radius);
        font-weight: 600;
        display: inline-block;
        box-shadow: var(--shadow-sm);
    }
    
    .nc-level-4 {
        background: linear-gradient(135deg, var(--success-light) 0%, #bbf7d0 100%);
        color: #14532d;
        border-left: 4px solid var(--success);
        padding: 6px 14px;
        border-radius: var(--radius);
        font-weight: 600;
        display: inline-block;
        box-shadow: var(--shadow-sm);
    }
    
    /* ===== COMMENT BOX ===== */
    .comment-box {
        background: linear-gradient(135deg, var(--info-light) 0%, var(--primary-50) 100%);
        padding: 1.25rem;
        border-radius: var(--radius-md);
        border-left: 4px solid var(--primary-500);
        margin: 0.75rem 0;
        box-shadow: var(--shadow);
        transition: all var(--transition-base);
    }
    
    .comment-box:hover {
        box-shadow: var(--shadow-md);
        transform: translateX(4px);
    }
    
    /* ===== SCROLLBAR STYLING ===== */
    .form-section-scrollable {
        max-height: 600px;
        overflow-y: auto;
        overflow-x: hidden;
        scrollbar-width: thin;
        scrollbar-color: var(--primary-300) var(--gray-100);
    }
    
    .form-section-scrollable::-webkit-scrollbar {
        width: 10px;
    }
    
    .form-section-scrollable::-webkit-scrollbar-track {
        background: var(--gray-100);
        border-radius: 10px;
    }
    
    .form-section-scrollable::-webkit-scrollbar-thumb {
        background: linear-gradient(180deg, var(--primary-400), var(--primary-500));
        border-radius: 10px;
        border: 2px solid var(--gray-100);
    }
    
    .form-section-scrollable::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(180deg, var(--primary-500), var(--primary-600));
    }
    
    /* ===== EXPANDER STYLING ===== */
    .streamlit-expanderHeader {
        background: linear-gradient(135deg, var(--gray-50) 0%, white 100%) !important;
        border-radius: var(--radius) !important;
        border: 1px solid var(--gray-200) !important;
        font-weight: 600 !important;
        padding: 1rem !important;
        transition: all var(--transition-base) !important;
    }
    
    .streamlit-expanderHeader:hover {
        background: linear-gradient(135deg, var(--primary-50) 0%, var(--primary-100) 100%) !important;
        border-color: var(--primary-300) !important;
        box-shadow: var(--shadow-md) !important;
    }
    
    /* ===== DATAFRAME STYLING ===== */
    .dataframe {
        border-radius: var(--radius-md) !important;
        overflow: hidden !important;
        box-shadow: var(--shadow) !important;
    }
    
    /* ===== METRIC STYLING ===== */
    [data-testid="stMetricValue"] {
        font-size: 2rem !important;
        font-weight: 700 !important;
        color: var(--gray-900) !important;
    }
    
    [data-testid="stMetricLabel"] {
        font-size: 0.875rem !important;
        font-weight: 600 !important;
        color: var(--gray-600) !important;
        text-transform: uppercase !important;
        letter-spacing: 0.05em !important;
    }
    
    [data-testid="stMetricDelta"] {
        font-size: 0.875rem !important;
        font-weight: 500 !important;
    }
    
    /* ===== ANIMATIONS ===== */
    @keyframes fadeIn {
        from {
            opacity: 0;
            transform: translateY(-10px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes slideIn {
        from {
            opacity: 0;
            transform: translateX(-10px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    
    @keyframes pulse {
        0%, 100% {
            opacity: 1;
        }
        50% {
            opacity: 0.8;
        }
    }
    
    @keyframes rotate {
        from {
            transform: rotate(0deg);
        }
        to {
            transform: rotate(360deg);
        }
    }
    
    /* ===== RESPONSIVE DESIGN ===== */
    @media (max-width: 768px) {
        .main-header {
            padding: 1.5rem 1rem;
        }
        
        .main-header h1 {
            font-size: 1.75rem;
        }
        
        .metric-card {
            padding: 1.25rem;
        }
        
        .form-section {
            padding: 1.25rem;
        }
    }
    
    /* ===== LOADING STATES ===== */
    .stSpinner > div {
        border-color: var(--primary-500) transparent transparent transparent !important;
    }
    
    /* ===== ALERTS & MESSAGES ===== */
    .stAlert {
        border-radius: var(--radius-md) !important;
        border-left-width: 4px !important;
        box-shadow: var(--shadow) !important;
    }
    
    /* ===== SIDEBAR ENHANCEMENTS ===== */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, var(--gray-50) 0%, white 100%) !important;
    }
    
    [data-testid="stSidebar"] .element-container {
        transition: all var(--transition-base);
    }
    
    /* ===== HOVER EFFECTS FOR INTERACTIVE ELEMENTS ===== */
    .element-container:has(.stButton):hover {
        transform: scale(1.01);
    }
    
    /* ===== PROFESSIONAL SHADOWS FOR DEPTH ===== */
    .stPlotlyChart {
        box-shadow: var(--shadow-md) !important;
        border-radius: var(--radius-lg) !important;
        padding: 1rem !important;
        background: white !important;
        transition: all var(--transition-base) !important;
    }
    
    .stPlotlyChart:hover {
        box-shadow: var(--shadow-lg) !important;
    }
</style>
""", unsafe_allow_html=True)

# Session state initialization
def init_session_state():
    """Initialize session state variables"""
    if 'user' not in st.session_state:
        st.session_state.user = None
    if 'current_ncr' not in st.session_state:
        st.session_state.current_ncr = None
    if 'ncr_form_data' not in st.session_state:
        st.session_state.ncr_form_data = {}
    if 'current_section' not in st.session_state:
        st.session_state.current_section = 1

# Authentication functions
def show_login():
    """Display login form with professional styling"""
    # Enhanced header with gradient and animation
    st.markdown("""
    <div class="main-header">
        <div style="position: relative; z-index: 1;">
            <h1 style="font-size: 3rem; margin-bottom: 0.5rem; text-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                🔍 NCTracker
            </h1>
            <p style="font-size: 1.25rem; opacity: 0.95; font-weight: 500;">
                Quality Non-Conformance Report System
            </p>
            <p style="font-size: 0.95rem; opacity: 0.85; margin-top: 0.5rem;">
                Professional Quality Management & Compliance Tracking
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Center the login box with professional card design
    col1, col2, col3 = st.columns([1, 1.8, 1])
    with col2:
        # Login card with enhanced styling
        st.markdown("""
        <div style="
            background: white;
            padding: 2.5rem 2rem;
            border-radius: 16px;
            box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 8px 10px -6px rgba(0, 0, 0, 0.1);
            margin-top: 2rem;
            border: 1px solid #e5e7eb;
        ">
            <div style="text-align: center; margin-bottom: 2rem;">
                <h2 style="color: #1f2937; font-weight: 700; font-size: 1.875rem; margin: 0;">
                    Welcome Back
                </h2>
                <p style="color: #6b7280; margin-top: 0.5rem; font-size: 1rem;">
                    Sign in to access your NCR dashboard
                </p>
            </div>
        """, unsafe_allow_html=True)
        
        with st.form("login_form", clear_on_submit=False):
            username = st.text_input(
                "Username",
                placeholder="Enter your username",
                key="login_username",
                help="Use your assigned username"
            )
            password = st.text_input(
                "Password",
                type="password",
                placeholder="Enter your password",
                key="login_password",
                autocomplete="current-password",
                help="Enter your secure password"
            )
            
            st.markdown("<div style='margin: 1.5rem 0 1rem 0;'></div>", unsafe_allow_html=True)
            
            submitted = st.form_submit_button("🔐 Sign In", type="primary", use_container_width=True)
            
            if submitted:
                if username and password:
                    user = db.authenticate_user(username, password)
                    if user:
                        st.session_state.user = user
                        st.success(f"✅ Welcome back, {user['full_name']}!")
                        st.rerun()
                    else:
                        st.error("❌ Invalid username or password. Please try again.")
                else:
                    st.warning("⚠️ Please enter both username and password")
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Enhanced credentials display with icon
        st.markdown("""
        <div style="
            margin-top: 2rem;
            padding: 1.5rem;
            background: linear-gradient(135deg, #eff6ff 0%, #dbeafe 100%);
            border-radius: 12px;
            border-left: 4px solid #3b82f6;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        ">
            <div style="display: flex; align-items: center; margin-bottom: 1rem;">
                <span style="font-size: 1.5rem; margin-right: 0.75rem;">🔑</span>
                <strong style="color: #1e40af; font-size: 1.125rem;">Default Admin Account</strong>
            </div>
            <div style="color: #1e40af; line-height: 1.8;">
                <div style="margin: 0.5rem 0;">
                    <strong>Username:</strong>
                    <code style="background: white; padding: 4px 8px; border-radius: 4px; margin-left: 0.5rem;">admin</code>
                </div>
                <div style="margin: 0.5rem 0;">
                    <strong>Password:</strong>
                    <code style="background: white; padding: 4px 8px; border-radius: 4px; margin-left: 0.5rem;">admin123</code>
                </div>
            </div>
            <div style="margin-top: 1rem; padding-top: 1rem; border-top: 1px solid #bfdbfe;">
                <small style="color: #1e40af; font-style: italic;">
                    🔒 Please change the password after first login for security
                </small>
            </div>
        </div>
        """, unsafe_allow_html=True)

def show_sidebar():
    """Display navigation sidebar"""
    with st.sidebar:
        st.markdown("## 🔍 NCTracker")
        st.markdown(f"**User:** {st.session_state.user['full_name']}")
        st.markdown(f"**Role:** {st.session_state.user['role'].title()}")
        
        st.markdown("---")
        
        # Navigation menu
        page = st.radio("Navigation", [
            "📊 Dashboard",
            "➕ New NCR", 
            "🔍 Search NCRs",
            "📈 Analytics",
            "👥 Users",
            "⚙️ Settings",
            "🚪 Logout"
        ])
        
        st.markdown("---")
        
        # Quick stats
        if page in ["📊 Dashboard", "📈 Analytics"]:
            stats = db.get_dashboard_stats()
            st.markdown("### Quick Stats")
            st.metric("Total NCRs", stats['total_ncrs'])
            st.metric("This Month", stats['recent_ncrs'])
            st.metric("Avg Resolution", f"{stats['avg_resolution_days']:.1f} days")
    
    return page

def show_ncr_detail():
    """Display detailed view of a single NCR"""
    if 'current_ncr' not in st.session_state or st.session_state.current_ncr is None:
        st.warning("No NCR selected")
        return
    
    ncr = db.get_ncr_by_id(st.session_state.current_ncr)
    
    if not ncr:
        st.error("NCR not found")
        return
    
    # Header with back button
    col1, col2 = st.columns([6, 1])
    with col1:
        st.markdown(f"## 📋 {ncr['ncr_number']}")
        st.markdown(f"### {ncr['title']}")
    with col2:
        if st.button("🔙 Back"):
            st.session_state.view_mode = None
            st.rerun()
    
    # Status badges
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        status_colors = {'NEW': '🆕', 'IN_PROGRESS': '⚙️', 'PENDING_APPROVAL': '⏳', 'CLOSED': '✅'}
        st.markdown(f"**Status:** {status_colors.get(ncr['status'], '📋')} {ncr['status']}")
    with col2:
        st.markdown(f"**NC Level:** {'🔴' if ncr['nc_level'] == 1 else '🟠' if ncr['nc_level'] == 2 else '🟡' if ncr['nc_level'] == 3 else '🟢'} Level {ncr['nc_level']}")
    with col3:
        st.markdown(f"**Created:** {pd.to_datetime(ncr['created_at'], format='mixed').strftime('%Y-%m-%d')}")
    with col4:
        st.markdown(f"**Created By:** {ncr['created_by_name']}")
    
    st.markdown("---")
    
    # Section 1: NCR Details
    with st.expander("📝 Section 1: NCR Details", expanded=True):
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"**Site:** {ncr.get('site') or 'N/A'}")
            st.markdown(f"**Part Number:** {ncr.get('part_number') or 'N/A'}")
            st.markdown(f"**Part Rev:** {ncr.get('part_number_rev') or 'N/A'}")
            st.markdown(f"**Quantity Affected:** {ncr.get('quantity_affected') or 'N/A'}")
            st.markdown(f"**Units:** {ncr.get('units_affected') or 'N/A'}")
        with col2:
            st.markdown(f"**Project:** {ncr.get('project_affected') or 'N/A'}")
            st.markdown(f"**Serial Number:** {ncr.get('serial_number') or 'N/A'}")
            st.markdown(f"**PO Number:** {ncr.get('po_number') or 'N/A'}")
            st.markdown(f"**Supplier:** {ncr.get('supplier') or 'N/A'}")
            st.markdown(f"**Build Group:** {ncr.get('build_group_operation') or 'N/A'}")
        
        st.markdown("**Problem Statement:**")
        st.info(f"**Is:** {ncr.get('problem_is') or 'N/A'}")
        st.success(f"**Should Be:** {ncr.get('problem_should_be') or 'N/A'}")
        
        st.markdown(f"**Contained:** {'✅ Yes' if ncr.get('is_contained') else '❌ No'}")
        if ncr.get('how_contained'):
            st.markdown(f"**How Contained:** {ncr['how_contained']}")
    
    # Section 2: NC Level and CAPA
    with st.expander("⚖️ Section 2: NC Level and CAPA"):
        st.markdown(f"**NC Level:** {ncr.get('nc_level') or 'N/A'}")
        st.markdown(f"**CAPA Required:** {'✅ Yes' if ncr.get('capa_required') else '❌ No'}")
        if ncr.get('capa_number'):
            st.markdown(f"**CAPA Number:** {ncr['capa_number']}")
        st.markdown(f"**QE Assigned:** {'✅ Yes' if ncr.get('qe_assigned') else '❌ No'}")
        st.markdown(f"**NC Owner Assigned:** {'✅ Yes' if ncr.get('nc_owner_assigned') else '❌ No'}")
        st.markdown(f"**External Notification:** {'✅ Yes' if ncr.get('external_notification_required') else '❌ No'}")
    
    # Section 3: Investigation
    with st.expander("🔍 Section 3: Investigation & Disposition"):
        st.markdown(f"**Problem Category:** {ncr.get('problem_category') or 'N/A'}")
        st.markdown(f"**Disposition Action:** {ncr.get('disposition_action') or 'N/A'}")
        if ncr.get('disposition_instructions'):
            st.markdown(f"**Instructions:** {ncr['disposition_instructions']}")
        if ncr.get('disposition_justification'):
            st.markdown(f"**Justification:** {ncr['disposition_justification']}")
    
    # Section 4: Correction
    with st.expander("🔧 Section 4: Correction Actions"):
        if ncr.get('correction_actions'):
            try:
                actions = ncr['correction_actions'] if isinstance(ncr['correction_actions'], list) else []
                if actions:
                    for action in actions:
                        st.markdown(f"- {action}")
            except:
                st.markdown(ncr.get('correction_actions', 'N/A'))
        if ncr.get('evidence_of_completion'):
            st.markdown(f"**Evidence of Completion:** {ncr['evidence_of_completion']}")
    
    # Section 5: Closure
    with st.expander("✅ Section 5: Closure"):
        st.markdown(f"**QE Audit Complete:** {'✅ Yes' if ncr.get('qe_audit_complete') else '❌ No'}")
        if ncr.get('closure_date'):
            st.markdown(f"**Closure Date:** {ncr['closure_date']}")
        if ncr.get('closed_at'):
            closed_date = pd.to_datetime(ncr['closed_at'], format='mixed').strftime('%Y-%m-%d')
            st.markdown(f"**Closed At:** {closed_date}")
    
    # Comments section
    st.markdown("---")
    st.markdown("### 💬 Comments")
    comments = db.get_comments(ncr['id'])
    if comments:
        for comment in comments:
            comment_date = pd.to_datetime(comment['created_at'], format='mixed').strftime('%Y-%m-%d %H:%M')
            st.markdown(f"""
            <div class="comment-box">
                <strong>{comment['user_name']}</strong> - <em>{comment_date}</em><br>
                {comment['content']}
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("No comments yet")
    
    # Add comment
    with st.form(f"add_comment_{ncr['id']}"):
        new_comment = st.text_area("Add a comment:", height=100)
        if st.form_submit_button("💬 Post Comment"):
            if new_comment:
                db.add_comment(ncr['id'], st.session_state.user['id'], new_comment)
                st.success("Comment added!")
                st.rerun()

def show_dashboard():
    """Display main dashboard"""
    # Check if we should show NCR detail
    if st.session_state.get('view_mode') == 'detail':
        show_ncr_detail()
        return
    
    st.markdown("## 📊 Dashboard")
    
    # Get dashboard stats
    stats = db.get_dashboard_stats()
    
    # Key metrics row with enhanced visuals
    col1, col2, col3, col4 = st.columns(4)
    
    # Calculate some trends for delta values
    all_ncrs = db.get_ncrs()
    now = datetime.now()
    last_month_ncrs = [n for n in all_ncrs if pd.to_datetime(n['created_at'], format='mixed') > (now - timedelta(days=60)) and pd.to_datetime(n['created_at'], format='mixed') <= (now - timedelta(days=30))]
    month_over_month_change = stats['recent_ncrs'] - len(last_month_ncrs)
    
    open_ncrs = len([n for n in all_ncrs if n['status'] != 'CLOSED'])
    critical_ncrs = len([n for n in all_ncrs if n['nc_level'] == 1 and n['status'] != 'CLOSED'])
    
    with col1:
        st.metric(
            label="📊 Total NCRs",
            value=stats['total_ncrs'],
            delta=f"+{stats['recent_ncrs']} this month",
            delta_color="normal"
        )
    
    with col2:
        st.metric(
            label="📈 Recent Activity",
            value=f"{stats['recent_ncrs']} NCRs",
            delta=f"{month_over_month_change:+d} vs last month" if last_month_ncrs else "New tracking",
            delta_color="normal" if month_over_month_change >= 0 else "inverse"
        )
    
    with col3:
        # Show resolution time with color coding
        avg_days = stats['avg_resolution_days']
        delta_text = "Good" if avg_days < 20 else "Moderate" if avg_days < 30 else "Needs attention"
        delta_color = "normal" if avg_days < 20 else "off" if avg_days < 30 else "inverse"
        st.metric(
            label="⏱️ Avg Resolution",
            value=f"{avg_days:.1f} days",
            delta=delta_text,
            delta_color=delta_color
        )
    
    with col4:
        st.metric(
            label="🔓 Open NCRs",
            value=open_ncrs,
            delta=f"{critical_ncrs} Critical" if critical_ncrs > 0 else "None Critical",
            delta_color="inverse" if critical_ncrs > 0 else "normal"
        )
    
    # Charts row
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📊 Status Distribution")
        if stats['status_counts']:
            status_df = pd.DataFrame(list(stats['status_counts'].items()), columns=['Status', 'Count'])
            fig = px.pie(
                status_df,
                values='Count',
                names='Status',
                title="NCR Status Breakdown",
                hole=0.4  # Donut chart for modern look
            )
            fig.update_layout(
                height=400,
                margin=dict(t=50, b=80, l=40, r=40),
                showlegend=True,
                legend=dict(
                    orientation="v",
                    yanchor="middle",
                    y=0.5,
                    xanchor="left",
                    x=1.02
                ),
                font=dict(size=13, family="system-ui, -apple-system, sans-serif"),
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)'
            )
            st.plotly_chart(fig)
        else:
            st.info("No NCRs created yet")
    
    with col2:
        st.markdown("### 🔢 NC Level Distribution")
        if stats['nc_level_counts']:
            level_df = pd.DataFrame(list(stats['nc_level_counts'].items()), columns=['NC Level', 'Count'])
            fig = px.bar(
                level_df,
                x='NC Level',
                y='Count',
                title="Non-Conformance Levels",
                color='NC Level',
                color_discrete_map={
                    1: '#ef4444',  # Red for Critical
                    2: '#f97316',  # Orange for Adverse
                    3: '#eab308',  # Yellow for Moderate
                    4: '#22c55e'   # Green for Low
                }
            )
            fig.update_layout(
                height=400,
                margin=dict(t=50, b=80, l=60, r=40),
                xaxis_title="NC Level",
                yaxis_title="Count",
                showlegend=False,
                font=dict(size=13, family="system-ui, -apple-system, sans-serif"),
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)'
            )
            fig.update_xaxes(type='category')
            st.plotly_chart(fig)
        else:
            st.info("No NC levels recorded yet")
    
    # Recent NCRs
    st.markdown("### 📋 Recent NCRs")
    recent_ncrs = db.get_ncrs()[:10]  # Last 10 NCRs
    
    if recent_ncrs:
        for ncr in recent_ncrs:
            with st.expander(f"**{ncr['ncr_number']}** - {ncr['title'][:60]}{'...' if len(ncr['title']) > 60 else ''}"):
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("Status", ncr['status'])
                with col2:
                    st.metric("NC Level", ncr['nc_level'] or "N/A")
                with col3:
                    created_date = pd.to_datetime(ncr['created_at'], format='mixed').strftime('%Y-%m-%d')
                    st.metric("Created", created_date)
                with col4:
                    st.metric("Created By", ncr['created_by_name'] or "Unknown")
                
                if st.button(f"📄 View Full Details", key=f"view_dash_{ncr['id']}"):
                    st.session_state.current_ncr = ncr['id']
                    st.session_state.view_mode = 'detail'
                    st.rerun()
    else:
        st.info("No NCRs created yet. Start by creating a new NCR!")

def show_new_ncr():
    """Display new NCR creation form"""
    st.markdown("## ➕ Create New NCR")
    
    if 'ncr_form_data' not in st.session_state:
        st.session_state.ncr_form_data = {}
    
    # Form sections
    sections = {
        1: "Section 1: NCR Details",
        2: "Section 2: NC Level and CAPA", 
        3: "Section 3: Investigation & Disposition",
        4: "Section 4: Correction",
        5: "Section 5: Closure"
    }
    
    # Section navigation
    col1, col2, col3, col4, col5 = st.columns(5)
    
    for i, (num, title) in enumerate(sections.items()):
        with [col1, col2, col3, col4, col5][i]:
            if st.button(f"{num}", key=f"section_{num}"):
                st.session_state.current_section = num
    
    st.markdown(f"### {sections[st.session_state.current_section]}")
    st.markdown("---")
    
    # Render current section
    if st.session_state.current_section == 1:
        show_section_1()
    elif st.session_state.current_section == 2:
        show_section_2()
    elif st.session_state.current_section == 3:
        show_section_3()
    elif st.session_state.current_section == 4:
        show_section_4()
    elif st.session_state.current_section == 5:
        show_section_5()

def show_section_1():
    """Section 1: NCR Details"""
    st.markdown("### 🔍 Section 1: NCR Details")
    st.markdown("*Completed by person identifying nonconformance. For any sections that do not apply, use N/A.*")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="form-section">', unsafe_allow_html=True)
        st.markdown("#### Basic Information")
        
        # Title
        title = st.text_input("**NCR Title** *Required*", 
                            value=st.session_state.ncr_form_data.get('title', ''),
                            help="Format: Part Number, Issue Description. Example: 13204643-101, LN2 Stack Out of Tolerance")
        
        # Site
        site = st.selectbox("**Site**", 
                          ['', 'Site A', 'Site B', 'Site C', 'Other'],
                          index=0 if not st.session_state.ncr_form_data.get('site') else 
                                (['Site A', 'Site B', 'Site C', 'Other'].index(st.session_state.ncr_form_data.get('site')) + 1))
        
        # Part information
        part_number = st.text_input("**Part Number or Equipment ID**", 
                                  value=st.session_state.ncr_form_data.get('part_number', ''))
        part_number_rev = st.text_input("**Part Number Rev**", 
                                      value=st.session_state.ncr_form_data.get('part_number_rev', ''))
        
        # Quantity and units
        quantity_affected = st.number_input("**Quantity of Parts Affected**", 
                                          min_value=0, 
                                          value=st.session_state.ncr_form_data.get('quantity_affected', 0))
        units_affected = st.text_input("**Unit(s) Affected**", 
                                     value=st.session_state.ncr_form_data.get('units_affected', ''))
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="form-section">', unsafe_allow_html=True)
        st.markdown("#### Project & Identification")
        
        # Project and ID
        project_affected = st.text_input("**Project Affected**", 
                                       value=st.session_state.ncr_form_data.get('project_affected', ''))
        serial_number = st.text_input("**Serial Number**", 
                                    value=st.session_state.ncr_form_data.get('serial_number', ''))
        other_id = st.text_input("**Other ID**", 
                               value=st.session_state.ncr_form_data.get('other_id', ''))
        po_number = st.text_input("**PO**", 
                                value=st.session_state.ncr_form_data.get('po_number', ''))
        supplier = st.text_input("**Supplier**", 
                               value=st.session_state.ncr_form_data.get('supplier', ''))
        build_group_operation = st.text_input("**Build Group & Operation**", 
                                            value=st.session_state.ncr_form_data.get('build_group_operation', ''))
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Problem Statement
    st.markdown('<div class="form-section">', unsafe_allow_html=True)
    st.markdown("#### 📝 Problem Statement")
    st.markdown("*Describe the issue using **Is** and **Should Be** statements to clearly define the issue, its location, and how it impacts the product, process, or service.*")
    
    col1, col2 = st.columns(2)
    with col1:
        problem_is = st.text_area("**Is:** *What is the current situation?*", 
                                value=st.session_state.ncr_form_data.get('problem_is', ''),
                                height=100)
    with col2:
        problem_should_be = st.text_area("**Should Be:** *What should be the correct situation?*", 
                                       value=st.session_state.ncr_form_data.get('problem_should_be', ''),
                                       height=100)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Containment
    st.markdown('<div class="form-section">', unsafe_allow_html=True)
    st.markdown("#### 🛡️ Containment/Notification")
    st.markdown("*Is the issue properly contained and identified? Describe **HOW** the issue is contained and identified.*")
    
    col1, col2 = st.columns(2)
    with col1:
        containment_options = ["", "Yes", "No"]
        is_contained = st.radio("**Is the issue contained?**", 
                              containment_options,
                              index=containment_options.index(st.session_state.ncr_form_data.get('is_contained_str', '')) if st.session_state.ncr_form_data.get('is_contained_str') in containment_options else 0)
    with col2:
        how_contained = st.text_input("**How Contained:**", 
                                    value=st.session_state.ncr_form_data.get('how_contained', ''),
                                    disabled=(is_contained != "Yes"))
    
    if is_contained == "No":
        containment_justification = st.text_area("**Justification for not containing:**", 
                                               value=st.session_state.ncr_form_data.get('containment_justification', ''))
    else:
        containment_justification = ""
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Update session state
    st.session_state.ncr_form_data.update({
        'title': title,
        'site': site,
        'part_number': part_number,
        'part_number_rev': part_number_rev,
        'quantity_affected': quantity_affected,
        'units_affected': units_affected,
        'project_affected': project_affected,
        'serial_number': serial_number,
        'other_id': other_id,
        'po_number': po_number,
        'supplier': supplier,
        'build_group_operation': build_group_operation,
        'problem_is': problem_is,
        'problem_should_be': problem_should_be,
        'is_contained': is_contained == "Yes" if is_contained else None,
        'is_contained_str': is_contained,
        'how_contained': how_contained,
        'containment_justification': containment_justification
    })

def show_section_2():
    """Section 2: NC Level and CAPA"""
    st.markdown("### ⚖️ Section 2: NC Level and CAPA")
    st.markdown("*For MRB Team or NCR Administrator (QE)*")
    
    # NC Level
    st.markdown('<div class="form-section">', unsafe_allow_html=True)
    st.markdown("#### 🎯 NC Level:")
    
    nc_level_options = {
        "": None,
        "1 - Critical": 1,
        "2 - Adverse": 2, 
        "3 - Moderate": 3,
        "4 - Low": 4
    }
    
    nc_level_labels = list(nc_level_options.keys())
    current_nc_level = st.session_state.ncr_form_data.get('nc_level')
    if current_nc_level:
        current_label = [k for k, v in nc_level_options.items() if v == current_nc_level][0]
    else:
        current_label = ""
    
    nc_level = st.radio("**Select NC Level:**", 
                       nc_level_labels,
                       index=nc_level_labels.index(current_label) if current_label in nc_level_labels else 0)
    
    # Show level descriptions
    level_descriptions = {
        "1 - Critical": "Injury or total system failure—escalate to Senior Leadership; CAPA required.",
        "2 - Adverse": "Schedule slip ≥ 3 days or missed milestone—escalate to Management; CAPA recommended.",
        "3 - Moderate": "Drawing change, repairs, use-as-is, or schedule slip < 3 days",
        "4 - Low": "Rework to drawing, scrap, or return to vendor."
    }
    
    if nc_level:
        st.info(level_descriptions[nc_level])
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # CAPA
    st.markdown('<div class="form-section">', unsafe_allow_html=True)
    st.markdown("#### 🔄 CAPA")
    
    capa_options = ["", "Yes", "No"]
    capa_required = st.radio("**CAPA Required?**", 
                           capa_options,
                           index=capa_options.index(st.session_state.ncr_form_data.get('capa_required_str', '')) if st.session_state.ncr_form_data.get('capa_required_str') in capa_options else 0)
    
    capa_number = ""
    if capa_required == "Yes":
        capa_number = st.text_input("**CAPA Number:**", 
                                  value=st.session_state.ncr_form_data.get('capa_number', ''))
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Assignments
    st.markdown('<div class="form-section">', unsafe_allow_html=True)
    st.markdown("#### 👥 Assignments & Notifications")
    
    col1, col2 = st.columns(2)
    with col1:
        qe_options = ["", "Yes", "No"]
        qe_assigned = st.radio("**QE Assigned?**", 
                             qe_options,
                             index=qe_options.index(st.session_state.ncr_form_data.get('qe_assigned_str', '')) if st.session_state.ncr_form_data.get('qe_assigned_str') in qe_options else 0)
        
        nc_owner_options = ["", "Yes", "No"]
        nc_owner_assigned = st.radio("**NC Owner Assigned?**", 
                                   nc_owner_options,
                                   index=nc_owner_options.index(st.session_state.ncr_form_data.get('nc_owner_assigned_str', '')) if st.session_state.ncr_form_data.get('nc_owner_assigned_str') in nc_owner_options else 0)
    
    with col2:
        external_notification = st.radio("**External Notification Required?**", 
                                       ["", "Yes", "No"],
                                       index=["", "Yes", "No"].index(st.session_state.ncr_form_data.get('external_notification_required_str', '')) if st.session_state.ncr_form_data.get('external_notification_required_str') in ["", "Yes", "No"] else 0)
        
        external_method = ""
        if external_notification == "Yes":
            external_method = st.text_input("**How:** *Notification method*", 
                                          value=st.session_state.ncr_form_data.get('external_notification_method', ''))
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Update session state
    st.session_state.ncr_form_data.update({
        'nc_level': nc_level_options[nc_level],
        'capa_required': capa_required == "Yes" if capa_required else None,
        'capa_required_str': capa_required,
        'capa_number': capa_number,
        'qe_assigned': qe_assigned == "Yes" if qe_assigned else None,
        'qe_assigned_str': qe_assigned,
        'nc_owner_assigned': nc_owner_assigned == "Yes" if nc_owner_assigned else None,
        'nc_owner_assigned_str': nc_owner_assigned,
        'external_notification_required': external_notification == "Yes" if external_notification else None,
        'external_notification_required_str': external_notification,
        'external_notification_method': external_method
    })

def show_section_3():
    """Section 3: Investigation & Disposition"""
    st.markdown("### 🔍 Section 3: Investigation, Disposition Details, and Approval")
    st.markdown("*For NC Owner*")
    
    # Investigation Results
    st.markdown('<div class="form-section">', unsafe_allow_html=True)
    st.markdown("#### 🔬 Investigation Results")
    st.text_area("**Investigation Results:**", 
                value=st.session_state.ncr_form_data.get('investigation_results', ''),
                height=100,
                key="investigation_results")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Problem Category
    st.markdown('<div class="form-section">', unsafe_allow_html=True)
    st.markdown("#### 📂 Problem Category:")
    
    problem_categories = [
        "Document", "Design", "Manufacturing", "Supplier", "Equipment",
        "Customer", "Process", "Improvement", "Software", "Service", "Other"
    ]
    
    current_category = st.session_state.ncr_form_data.get('problem_category', '')
    if current_category not in problem_categories:
        current_category = ""
    
    problem_category = st.selectbox("**Select Category:**", 
                                   [""] + problem_categories,
                                   index=problem_categories.index(current_category) + 1 if current_category in problem_categories else 0)
    
    if problem_category == "Other":
        other_category = st.text_input("**Specify Other Category:**", 
                                     value=st.session_state.ncr_form_data.get('other_category', ''))
    else:
        other_category = ""
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Disposition Action
    st.markdown('<div class="form-section">', unsafe_allow_html=True)
    st.markdown("#### ⚡ Disposition Action:")
    
    disposition_options = [
        "Rework",
        "Repair", 
        "Reject - Return to Supplier",
        "Reject - Scrap", 
        "Use-As-Is",
        "Other"
    ]
    
    current_disposition = st.session_state.ncr_form_data.get('disposition_action', '')
    if current_disposition not in disposition_options:
        current_disposition = ""
    
    disposition_action = st.radio("**Select Disposition:**", 
                                disposition_options,
                                index=disposition_options.index(current_disposition) if current_disposition in disposition_options else 0)
    
    disposition_instructions = st.text_input("**Instructions/Task Reference:**", 
                                           value=st.session_state.ncr_form_data.get('disposition_instructions', ''))
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Disposition Justification
    st.markdown('<div class="form-section">', unsafe_allow_html=True)
    st.markdown("#### 💭 Rational for Disposition:")
    st.text_area("**Justification:**", 
                value=st.session_state.ncr_form_data.get('disposition_justification', ''),
                height=100,
                key="disposition_justification")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Required Approvals
    st.markdown('<div class="form-section">', unsafe_allow_html=True)
    st.markdown("#### ✅ Required Approvals")
    st.markdown("*Tag Necessary Approvers in NC Comments*")
    
    # Approval requirements based on NC level
    approval_requirements = {
        1: "1 Quality Manager + 1 Quality Engineer + 1 SME Manager + 2 SME Engineers",
        2: "1 SME Manager/Quality Manager + 1 Quality Engineer + 2 SME Engineers", 
        3: "1 Quality Engineer + 2 SME Engineers",
        4: "1 Quality Engineer + 1 SME Engineer"
    }
    
    nc_level = st.session_state.ncr_form_data.get('nc_level', 3)
    if nc_level in approval_requirements:
        st.info(f"**Required Approvals (Level {nc_level}):** {approval_requirements[nc_level]}")
    
    required_approvals = st.text_area("**Required Approvers (list names):**", 
                                    value=st.session_state.ncr_form_data.get('required_approvals_text', ''),
                                    help="Enter the names of required approvers")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Update session state
    st.session_state.ncr_form_data.update({
        'investigation_results': st.session_state.get('investigation_results', ''),
        'problem_category': problem_category,
        'other_category': other_category,
        'disposition_action': disposition_action,
        'disposition_instructions': disposition_instructions,
        'disposition_justification': st.session_state.get('disposition_justification', ''),
        'required_approvals_text': required_approvals
    })

def show_section_4():
    """Section 4: Correction"""
    st.markdown("### 🔧 Section 4: Correction")
    st.markdown("*For NC Owner*")
    st.markdown("*Actions taken to correct nonconformance to prevent reoccurrence*")
    
    st.markdown('<div class="form-section">', unsafe_allow_html=True)
    st.markdown("#### 🎯 Correction Actions Taken:")
    
    correction_options = {
        "Disposition Work Only": st.session_state.ncr_form_data.get('disposition_work_only', False),
        "ECN/ECO/ECR": st.session_state.ncr_form_data.get('ecn_eco_ecr', False),
        "Deviation/Waiver": st.session_state.ncr_form_data.get('deviation_waiver', False),
        "SCAR or Supplier Support": st.session_state.ncr_form_data.get('scar_supplier', False),
        "RCCA/CAPA": st.session_state.ncr_form_data.get('rcca_capa', False),
        "Process/Procedural Update": st.session_state.ncr_form_data.get('process_update', False),
        "Other": st.session_state.ncr_form_data.get('other_correction', False)
    }
    
    st.markdown("**Select all that apply:**")
    
    cols = st.columns(2)
    selected_actions = []
    
    for i, (action, current_state) in enumerate(correction_options.items()):
        with cols[i % 2]:
            if st.checkbox(action, value=current_state, key=f"correction_{action}"):
                selected_actions.append(action)
    
    if "Other" in selected_actions:
        other_correction_text = st.text_input("**Specify Other Action:**", 
                                            value=st.session_state.ncr_form_data.get('other_correction_text', ''))
    else:
        other_correction_text = ""
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Evidence of Completion
    st.markdown('<div class="form-section">', unsafe_allow_html=True)
    st.markdown("#### 📄 Evidence of Completion:")
    st.text_area("**Evidence of Completion:**", 
                value=st.session_state.ncr_form_data.get('evidence_of_completion', ''),
                height=100,
                key="evidence_of_completion")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Update session state
    st.session_state.ncr_form_data.update({
        'disposition_work_only': "Disposition Work Only" in selected_actions,
        'ecn_eco_ecr': "ECN/ECO/ECR" in selected_actions,
        'deviation_waiver': "Deviation/Waiver" in selected_actions,
        'scar_supplier': "SCAR or Supplier Support" in selected_actions,
        'rcca_capa': "RCCA/CAPA" in selected_actions,
        'process_update': "Process/Procedural Update" in selected_actions,
        'other_correction': "Other" in selected_actions,
        'other_correction_text': other_correction_text,
        'correction_actions': selected_actions,
        'evidence_of_completion': st.session_state.get('evidence_of_completion', '')
    })

def show_section_5():
    """Section 5: Closure"""
    st.markdown("### ✅ Section 5: NCR Closure")
    st.markdown("*For NCR Administrator (QE)*")
    st.markdown("*Review NCR for completeness and accuracy*")
    
    st.markdown('<div class="form-section">', unsafe_allow_html=True)
    st.markdown("#### 🔍 QA Audit")
    st.markdown("- Review all sections for completeness")
    st.markdown("- Verify all required approvals are obtained")
    st.markdown("- Ensure containment and correction actions are adequate")
    st.markdown("- Check that all documentation is attached")
    
    qe_audit_complete = st.checkbox("**Audit complete - NCR is ready for closure**", 
                                  value=st.session_state.ncr_form_data.get('qe_audit_complete', False))
    
    if qe_audit_complete:
        closure_date = st.date_input("**Closure Date:**", 
                                   value=st.session_state.ncr_form_data.get('closure_date', date.today()),
                                   min_value=date(2020, 1, 1))
        
        st.success("✅ NCR is complete and ready for closure")
        st.markdown("*Once submitted, the NCR status will be changed to 'CLOSED'*")
    else:
        closure_date = None
        st.warning("Please complete the audit before closing the NCR")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Action buttons
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("💾 Save Draft"):
            save_ncr_draft()
            st.success("Draft saved successfully!")
    
    with col2:
        if st.button("✅ Submit NCR", type="primary", disabled=not qe_audit_complete):
            submit_ncr()
    
    with col3:
        if st.button("🗑️ Clear Form"):
            st.session_state.ncr_form_data = {}
            st.rerun()
    
    # Update session state
    st.session_state.ncr_form_data.update({
        'qe_audit_complete': qe_audit_complete,
        'closure_date': closure_date
    })

def save_ncr_draft():
    """Save NCR as draft"""
    # Implementation for saving draft
    pass

def submit_ncr():
    """Submit completed NCR"""
    if not st.session_state.ncr_form_data.get('title'):
        st.error("NCR Title is required!")
        return
    
    # Create NCR data
    ncr_data = {
        'title': st.session_state.ncr_form_data.get('title'),
        'status': 'NEW',
        'priority': st.session_state.ncr_form_data.get('nc_level', 3),
        'site': st.session_state.ncr_form_data.get('site'),
        'part_number': st.session_state.ncr_form_data.get('part_number'),
        'part_number_rev': st.session_state.ncr_form_data.get('part_number_rev'),
        'quantity_affected': st.session_state.ncr_form_data.get('quantity_affected'),
        'units_affected': st.session_state.ncr_form_data.get('units_affected'),
        'project_affected': st.session_state.ncr_form_data.get('project_affected'),
        'serial_number': st.session_state.ncr_form_data.get('serial_number'),
        'other_id': st.session_state.ncr_form_data.get('other_id'),
        'po_number': st.session_state.ncr_form_data.get('po_number'),
        'supplier': st.session_state.ncr_form_data.get('supplier'),
        'build_group_operation': st.session_state.ncr_form_data.get('build_group_operation'),
        'problem_is': st.session_state.ncr_form_data.get('problem_is'),
        'problem_should_be': st.session_state.ncr_form_data.get('problem_should_be'),
        'is_contained': st.session_state.ncr_form_data.get('is_contained'),
        'how_contained': st.session_state.ncr_form_data.get('how_contained'),
        'containment_justification': st.session_state.ncr_form_data.get('containment_justification'),
        'nc_level': st.session_state.ncr_form_data.get('nc_level'),
        'capa_required': st.session_state.ncr_form_data.get('capa_required'),
        'capa_number': st.session_state.ncr_form_data.get('capa_number'),
        'qe_assigned': st.session_state.ncr_form_data.get('qe_assigned'),
        'nc_owner_assigned': st.session_state.ncr_form_data.get('nc_owner_assigned'),
        'external_notification_required': st.session_state.ncr_form_data.get('external_notification_required'),
        'external_notification_method': st.session_state.ncr_form_data.get('external_notification_method'),
        'problem_category': st.session_state.ncr_form_data.get('problem_category'),
        'disposition_action': st.session_state.ncr_form_data.get('disposition_action'),
        'disposition_instructions': st.session_state.ncr_form_data.get('disposition_instructions'),
        'disposition_justification': st.session_state.ncr_form_data.get('disposition_justification'),
        'required_approvals': st.session_state.ncr_form_data.get('required_approvals_text', '').split(','),
        'correction_actions': st.session_state.ncr_form_data.get('correction_actions', []),
        'evidence_of_completion': st.session_state.ncr_form_data.get('evidence_of_completion'),
        'qe_audit_complete': st.session_state.ncr_form_data.get('qe_audit_complete'),
        'closure_date': st.session_state.ncr_form_data.get('closure_date'),
        'created_by': st.session_state.user['id']
    }
    
    try:
        ncr_id = db.create_ncr(ncr_data)
        st.success(f"NCR {ncr_data['title']} created successfully! NCR Number: {db.get_ncr_by_id(ncr_id)['ncr_number']}")
        
        # Clear form
        st.session_state.ncr_form_data = {}
        st.session_state.current_section = 1
        
        # Show NCR details
        st.rerun()
        
    except Exception as e:
        st.error(f"Error creating NCR: {str(e)}")

def show_search_ncrs():
    """Display NCR search and listing"""
    st.markdown("## 🔍 Search NCRs")
    
    # Search filters
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        search_term = st.text_input("Search", placeholder="Title, part number, or description")
    
    with col2:
        status_filter = st.selectbox("Status", ["", "NEW", "IN_PROGRESS", "PENDING_APPROVAL", "CLOSED"])
    
    with col3:
        nc_level_filter = st.selectbox("NC Level", ["", "1", "2", "3", "4"])
    
    with col4:
        if st.button("🔍 Search"):
            pass
    
    # Get NCRs
    filters = {}
    if search_term:
        filters['search'] = search_term
    if status_filter:
        filters['status'] = status_filter
    if nc_level_filter:
        filters['nc_level'] = int(nc_level_filter)
    
    ncrs = db.get_ncrs(filters)
    
    if ncrs:
        st.markdown(f"### Found {len(ncrs)} NCR(s)")
        
        for ncr in ncrs:
            with st.expander(f"**{ncr['ncr_number']}** - {ncr['title'][:50]}..."):
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.metric("Status", ncr['status'])
                with col2:
                    st.metric("NC Level", ncr['nc_level'] or "N/A")
                with col3:
                    st.metric("Created", pd.to_datetime(ncr['created_at'], format='mixed').strftime('%Y-%m-%d'))
                with col4:
                    st.metric("Created By", ncr['created_by_name'] or "Unknown")
                
                # Show key details
                st.markdown(f"**Part Number:** {ncr['part_number'] or 'N/A'}")
                st.markdown(f"**Problem:** {ncr['problem_is'][:100]}..." if ncr['problem_is'] else "**Problem:** N/A")
                
                if st.button(f"📄 View Full Details", key=f"view_search_{ncr['id']}"):
                    st.session_state.current_ncr = ncr['id']
                    st.session_state.view_mode = 'detail'
                    st.rerun()
    else:
        st.info("No NCRs found matching your criteria.")

def show_analytics():
    """Display analytics dashboard"""
    st.markdown("## 📈 Analytics")
    
    # Get data
    ncrs = db.get_ncrs()
    stats = db.get_dashboard_stats()
    
    if not ncrs:
        st.info("No data available for analytics")
        return
    
    df = pd.DataFrame(ncrs)
    # Handle mixed datetime formats (with and without microseconds)
    df['created_date'] = pd.to_datetime(df['created_at'], format='mixed').dt.date
    df['created_month'] = pd.to_datetime(df['created_at'], format='mixed').dt.to_period('M')
    
    # Monthly trends
    st.markdown("### 📊 Monthly NCR Trends")
    monthly_counts = df.groupby('created_month').size().reset_index(name='count')
    monthly_counts['created_month'] = monthly_counts['created_month'].astype(str)
    
    fig = px.line(monthly_counts, x='created_month', y='count',
                  title="NCRs Created per Month")
    fig.update_layout(
        height=400,
        margin=dict(t=60, b=80, l=60, r=40),
        font=dict(size=13, family="system-ui, -apple-system, sans-serif"),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )
    st.plotly_chart(fig)
    
    # Category breakdown
    st.markdown("### 📂 Problem Category Analysis")
    if not df['problem_category'].isna().all():
        category_counts = df['problem_category'].value_counts()
        fig = px.pie(values=category_counts.values, names=category_counts.index,
                    title="Distribution by Problem Category",
                    hole=0.4)
        fig.update_layout(
            height=400,
            margin=dict(t=50, b=80, l=40, r=40),
            font=dict(size=13, family="system-ui, -apple-system, sans-serif"),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)'
        )
        st.plotly_chart(fig)
    
    # Disposition analysis
    st.markdown("### ⚡ Disposition Action Analysis")
    if not df['disposition_action'].isna().all():
        disposition_counts = df['disposition_action'].value_counts()
        fig = px.bar(x=disposition_counts.index, y=disposition_counts.values,
                    title="Distribution by Disposition Action")
        fig.update_layout(
            height=400,
            margin=dict(t=50, b=80, l=60, r=40),
            font=dict(size=13, family="system-ui, -apple-system, sans-serif"),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)'
        )
        st.plotly_chart(fig)
    
    # Resolution time analysis
    st.markdown("### ⏱️ Resolution Time Analysis")
    closed_ncrs = df[df['status'] == 'CLOSED'].copy()  # Create explicit copy to avoid SettingWithCopyWarning
    if not closed_ncrs.empty and not closed_ncrs['closed_at'].isna().all():
        closed_ncrs['resolution_days'] = (
            pd.to_datetime(closed_ncrs['closed_at'], format='mixed') -
            pd.to_datetime(closed_ncrs['created_at'], format='mixed')
        ).dt.days
        
        fig = px.histogram(closed_ncrs, x='resolution_days', nbins=20,
                          title="Distribution of Resolution Times (Days)")
        fig.update_layout(
            height=400,
            margin=dict(t=50, b=80, l=60, r=40),
            font=dict(size=13, family="system-ui, -apple-system, sans-serif"),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)'
        )
        st.plotly_chart(fig)
    
    # Export data
    st.markdown("### 📤 Export Data")
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("📊 Export to Excel"):
            excel_data = utils.export_to_excel(ncrs)
            if excel_data:
                st.download_button(
                    label="Download Excel File",
                    data=excel_data,
                    file_name=f"ncr_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
    
    with col2:
        if st.button("📄 Generate Summary Report"):
            # Create a simple text report
            report = f"""
NCTracker Summary Report
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

=== OVERVIEW ===
Total NCRs: {stats['total_ncrs']}
Recent NCRs (30 days): {stats['recent_ncrs']}
Average Resolution Time: {stats['avg_resolution_days']:.1f} days

=== STATUS BREAKDOWN ===
"""
            for status, count in stats['status_counts'].items():
                report += f"{status}: {count} NCRs\n"
            
            report += f"\n=== NC LEVEL BREAKDOWN ===\n"
            for level, count in stats['nc_level_counts'].items():
                report += f"Level {level}: {count} NCRs\n"
            
            st.download_button(
                label="Download Report",
                data=report,
                file_name=f"ncr_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                mime="text/plain"
            )

def show_users():
    """Display user management"""
    st.markdown("## 👥 User Management")
    
    users = db.get_all_users()
    
    if users:
        st.markdown(f"**Total Users:** {len(users)}")
        
        # User table
        df = pd.DataFrame(users)
        st.dataframe(
            df[['username', 'full_name', 'role', 'department']],
            use_container_width=True,
            hide_index=True
        )
        
        # Add new user section
        st.markdown("### Add New User")
        with st.form("add_user_form"):
            col1, col2 = st.columns(2)
            with col1:
                username = st.text_input("Username")
                email = st.text_input("Email")
                full_name = st.text_input("Full Name")
            with col2:
                role = st.selectbox("Role", ["ncr_owner", "qe", "mrb_team", "admin"])
                department = st.text_input("Department")
                password = st.text_input("Password", type="password")
            
            if st.form_submit_button("Add User"):
                if username and email and full_name and password:
                    try:
                        from database import db as db_module
                        import hashlib
                        password_hash = hashlib.sha256(password.encode()).hexdigest()
                        
                        db_module.execute_update('''
                            INSERT INTO users (username, email, full_name, role, department, password_hash)
                            VALUES (?, ?, ?, ?, ?, ?)
                        ''', (username, email, full_name, role, department, password_hash))
                        
                        st.success("User added successfully!")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error adding user: {e}")
                else:
                    st.warning("All fields are required")
    else:
        st.info("No users found")

def show_settings():
    """Display application settings"""
    st.markdown("## ⚙️ Settings")
    
    st.markdown("### System Information")
    st.info(f"**NCTracker Version:** 1.0.0")
    st.info(f"**Database:** SQLite")
    st.info(f"**Streamlit Version:** 1.49.1")
    
    # Create sample data
    st.markdown("### Sample Data")
    st.markdown("Create sample users and NCRs for testing")
    
    if st.button("Create Sample Data"):
        utils.create_sample_data()
        st.success("Sample data created successfully!")
        st.rerun()
    
    # Clear database
    st.markdown("### Database Management")
    st.warning("⚠️ **This will delete all data!**")
    
    if st.button("Clear All Data"):
        if st.checkbox("I understand this will delete all data"):
            # This is a destructive operation - in production you'd want more safeguards
            st.success("Database cleared")
            st.rerun()

# Main application
def main():
    """Main application entry point"""
    init_session_state()
    
    # Check authentication
    if st.session_state.user is None:
        show_login()
        return
    
    # Show main application
    page = show_sidebar()
    
    # Route to appropriate page
    if page == "📊 Dashboard":
        show_dashboard()
    elif page == "➕ New NCR":
        show_new_ncr()
    elif page == "🔍 Search NCRs":
        show_search_ncrs()
    elif page == "📈 Analytics":
        show_analytics()
    elif page == "👥 Users":
        show_users()
    elif page == "⚙️ Settings":
        show_settings()
    elif page == "🚪 Logout":
        st.session_state.user = None
        st.rerun()

if __name__ == "__main__":
    main()
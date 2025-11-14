"""
NCTracker Dashboard - Main Overview Page
Professional dark mode design with KPIs and analytics
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta

# Import custom components
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from components import (
    auth_guard, inject_theme_css, apply_plotly_theme,
    page_header, sidebar_brand, sidebar_user_info,
    metric_card, status_badge, nc_level_badge, empty_state
)
from database import db

# Page configuration
st.set_page_config(
    page_title="Dashboard - NCTracker",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply theme
inject_theme_css()
apply_plotly_theme()

# Auth guard
auth_guard()

# Sidebar
sidebar_brand()
sidebar_user_info()

# Main content
st.markdown("## 📊 Dashboard")
st.markdown("Overview of NCR activity and key metrics")

# Get dashboard data
stats = db.get_dashboard_stats()
all_ncrs = db.get_ncrs()

# Calculate additional metrics
now = datetime.now()
last_month_ncrs = [
    n for n in all_ncrs 
    if pd.to_datetime(n['created_at'], format='mixed') > (now - timedelta(days=60)) 
    and pd.to_datetime(n['created_at'], format='mixed') <= (now - timedelta(days=30))
]
month_over_month_change = stats['recent_ncrs'] - len(last_month_ncrs)
open_ncrs = len([n for n in all_ncrs if n['status'] != 'CLOSED'])
critical_ncrs = len([n for n in all_ncrs if n['nc_level'] == 1 and n['status'] != 'CLOSED'])

# KPI Cards Row
st.markdown("### 📈 Key Performance Indicators")
col1, col2, col3, col4 = st.columns(4)

with col1:
    metric_card(
        label="Total NCRs",
        value=str(stats['total_ncrs']),
        delta=f"+{stats['recent_ncrs']} this month",
        delta_color="normal",
        icon="📊"
    )

with col2:
    delta_text = f"{month_over_month_change:+d} vs last month" if last_month_ncrs else "New tracking"
    delta_color = "positive" if month_over_month_change >= 0 else "negative"
    metric_card(
        label="Recent Activity",
        value=f"{stats['recent_ncrs']}",
        delta=delta_text,
        delta_color=delta_color,
        icon="📈"
    )

with col3:
    avg_days = stats['avg_resolution_days']
    delta_text = "Excellent" if avg_days < 15 else "Good" if avg_days < 25 else "Needs Attention"
    delta_color = "positive" if avg_days < 15 else "normal" if avg_days < 25 else "negative"
    metric_card(
        label="Avg Resolution",
        value=f"{avg_days:.1f} days",
        delta=delta_text,
        delta_color=delta_color,
        icon="⏱️"
    )

with col4:
    delta_text = f"{critical_ncrs} Critical" if critical_ncrs > 0 else "None Critical"
    delta_color = "negative" if critical_ncrs > 0 else "positive"
    metric_card(
        label="Open NCRs",
        value=str(open_ncrs),
        delta=delta_text,
        delta_color=delta_color,
        icon="🔓"
    )

st.markdown("<div style='margin: 2rem 0;'></div>", unsafe_allow_html=True)

# Charts Row
col1, col2 = st.columns(2)

with col1:
    st.markdown("### 📊 Status Distribution")
    if stats['status_counts']:
        status_df = pd.DataFrame(
            list(stats['status_counts'].items()),
            columns=['Status', 'Count']
        )
        
        # Format status names
        status_labels = {
            'NEW': 'New',
            'IN_PROGRESS': 'In Progress',
            'PENDING_APPROVAL': 'Pending Approval',
            'CLOSED': 'Closed'
        }
        status_df['Status Label'] = status_df['Status'].map(status_labels)
        
        fig = go.Figure(data=[go.Pie(
            labels=status_df['Status Label'],
            values=status_df['Count'],
            hole=0.5,
            marker=dict(
                colors=['#06B6D4', '#F59E0B', '#EC4899', '#22C55E'],
                line=dict(color='#0E1526', width=2)
            ),
            textinfo='label+percent',
            textfont=dict(size=14, family='Inter, sans-serif'),
            hovertemplate='<b>%{label}</b><br>Count: %{value}<br>Percent: %{percent}<extra></extra>'
        )])
        fig.update_layout(
            height=400,
            margin=dict(t=30, b=30, l=30, r=30),
            showlegend=True,
            legend=dict(
                orientation="v",
                yanchor="middle",
                y=0.5,
                xanchor="left",
                x=1.02,
                font=dict(size=13)
            ),
            annotations=[dict(
                text=f'<b>{stats["total_ncrs"]}</b><br>Total',
                x=0.5, y=0.5,
                font=dict(size=20, color='#E5E7EB'),
                showarrow=False
            )]
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        empty_state(
            icon="📊",
            title="No Data Available",
            message="No NCRs have been created yet."
        )

with col2:
    st.markdown("### 🔢 NC Level Distribution")
    if stats['nc_level_counts']:
        level_df = pd.DataFrame(
            list(stats['nc_level_counts'].items()),
            columns=['NC Level', 'Count']
        )
        level_df = level_df.sort_values('NC Level')
        
        level_colors = {
            1: '#EF4444',  # Red - Critical
            2: '#F97316',  # Orange - Adverse
            3: '#F59E0B',  # Yellow - Moderate
            4: '#22C55E'   # Green - Low
        }
        
        colors = [level_colors.get(level, '#6366F1') for level in level_df['NC Level']]
        max_level_count = level_df['Count'].max() if not level_df.empty else 0
        
        fig = go.Figure(data=[go.Bar(
            x=level_df['NC Level'].astype(str),
            y=level_df['Count'],
            marker=dict(
                color=colors,
                line=dict(color='#0E1526', width=1.5)
            ),
            text=level_df['Count'],
            textposition='outside',
            textfont=dict(size=14, color='#E5E7EB'),
            hovertemplate='<b>Level %{x}</b><br>Count: %{y}<extra></extra>'
        )])
        
        fig.update_layout(
            height=400,
            margin=dict(t=30, b=60, l=60, r=60),
            xaxis=dict(
                title="NC Level",
                type='category',
                tickfont=dict(size=13)
            ),
            yaxis=dict(
                title="Count",
                tickfont=dict(size=13),
                range=[0, max_level_count * 1.25 if max_level_count else 5]
            ),
            showlegend=False
        )
        fig.update_traces(cliponaxis=False)
        st.plotly_chart(fig, use_container_width=True)
    else:
        empty_state(
            icon="🔢",
            title="No Level Data",
            message="No NC levels have been assigned yet."
        )

st.markdown("<div style='margin: 2rem 0;'></div>", unsafe_allow_html=True)

# Recent NCRs Table
st.markdown("### 📋 Recent NCRs")

recent_ncrs = all_ncrs[:15]  # Last 15 NCRs

if recent_ncrs:
    # Create DataFrame for display
    df_display = []
    for ncr in recent_ncrs:
        df_display.append({
            'NCR #': ncr['ncr_number'],
            'Title': ncr['title'][:50] + '...' if len(ncr['title']) > 50 else ncr['title'],
            'Status': ncr['status'],
            'NC Level': ncr['nc_level'] if ncr['nc_level'] else 'N/A',
            'Created': pd.to_datetime(ncr['created_at'], format='mixed').strftime('%Y-%m-%d'),
            'Created By': ncr['created_by_name'] or 'Unknown',
            'ID': ncr['id']
        })
    
    df = pd.DataFrame(df_display)
    
    # Display as interactive table
    st.dataframe(
        df[['NCR #', 'Title', 'Status', 'NC Level', 'Created', 'Created By']],
        width="stretch",
        height=400,
        hide_index=True
    )
    
    # Quick actions
    st.markdown("<div style='margin: 1rem 0;'></div>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        st.markdown(f"**Showing {len(recent_ncrs)} most recent NCRs**")
    with col2:
        if st.button("🔍 View All NCRs", width="stretch"):
            st.switch_page("pages/02_🔍_NCR_List.py")
    with col3:
        if st.button("➕ Create New NCR", type="primary", width="stretch"):
            st.switch_page("pages/04_➕_New_NCR.py")
    
else:
    if empty_state(
        icon="📋",
        title="No NCRs Yet",
        message="Start tracking quality issues by creating your first NCR.",
        action_label="➕ Create First NCR"
    ):
        st.switch_page("pages/04_➕_New_NCR.py")

st.markdown("<div style='margin: 3rem 0;'></div>", unsafe_allow_html=True)

# Footer
st.markdown("""
<div style="
    text-align: center;
    padding: 2rem 0;
    border-top: 1px solid var(--color-border);
    color: var(--color-text-muted);
    font-size: 0.875rem;
">
    NCTracker v2.0 - Professional Quality Management System<br>
    <small>Powered by Streamlit & Modern Web Technologies</small>
</div>
""", unsafe_allow_html=True)

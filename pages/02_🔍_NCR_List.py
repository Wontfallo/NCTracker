"""
NCR List Page - Search and browse all NCRs
"""

import streamlit as st
import pandas as pd
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

try:
    from streamlit_extras.tags import tagger_component  # type: ignore
except ImportError:  # pragma: no cover - optional dependency handled at runtime
    tagger_component = None

from components import (
    auth_guard, inject_theme_css, apply_plotly_theme,
    page_header, sidebar_brand, sidebar_user_info,
    status_badge, nc_level_badge, empty_state
)
from database import db

# Page config
st.set_page_config(
    page_title="NCR List - NCTracker",
    page_icon="🔍",
    layout="wide"
)

inject_theme_css()
apply_plotly_theme()
auth_guard()

sidebar_brand()
sidebar_user_info()

# Page content
st.markdown("## 🔍 NCR List")
st.markdown("Search, filter, and browse all Non-Conformance Reports")

st.markdown("<div style='margin: 1.5rem 0;'></div>", unsafe_allow_html=True)

# Filters
col1, col2, col3, col4 = st.columns(4)

with col1:
    search_term = st.text_input(
        "🔎 Search",
        placeholder="NCR number, title, part number...",
        help="Search across NCR number, title, and part number"
    )

with col2:
    status_filter = st.selectbox(
        "Status",
        ["All", "NEW", "IN_PROGRESS", "PENDING_APPROVAL", "CLOSED"]
    )

with col3:
    nc_level_filter = st.selectbox(
        "NC Level",
        ["All", "1 - Critical", "2 - Adverse", "3 - Moderate", "4 - Low"]
    )

with col4:
    sort_by = st.selectbox(
        "Sort By",
        ["Newest First", "Oldest First", "NCR Number", "NC Level"]
    )

# Retrieve NCR data once
all_ncrs = db.get_ncrs()

# Tag filter row
all_tags = sorted(
    {
        tag.strip()
        for record in all_ncrs
        for tag in (record.get('tags') or [])
        if isinstance(tag, str) and tag.strip()
    },
    key=lambda value: value.lower()
)

selected_tags = []
if all_tags:
    selected_tags = st.multiselect(
        "Filter by Tags",
        options=all_tags,
        help="Select one or more tags to narrow results"
    )

st.markdown("<div style='margin: 1.5rem 0;'></div>", unsafe_allow_html=True)

# Apply filters
filtered_ncrs = all_ncrs

if search_term:
    search_lower = search_term.lower()
    filtered_ncrs = [
        ncr for ncr in filtered_ncrs
        if search_lower in ncr['ncr_number'].lower()
        or search_lower in (ncr['title'] or '').lower()
        or search_lower in (ncr['part_number'] or '').lower()
    ]

if status_filter != "All":
    filtered_ncrs = [ncr for ncr in filtered_ncrs if ncr['status'] == status_filter]

if nc_level_filter != "All":
    level = int(nc_level_filter[0])
    filtered_ncrs = [ncr for ncr in filtered_ncrs if ncr['nc_level'] == level]

if selected_tags:
    selected_tag_set = set(selected_tags)
    filtered_ncrs = [
        ncr for ncr in filtered_ncrs
        if selected_tag_set.issubset(set(ncr.get('tags') or []))
    ]

# Sort
if sort_by == "Newest First":
    filtered_ncrs = sorted(filtered_ncrs, key=lambda x: x['created_at'], reverse=True)
elif sort_by == "Oldest First":
    filtered_ncrs = sorted(filtered_ncrs, key=lambda x: x['created_at'])
elif sort_by == "NCR Number":
    filtered_ncrs = sorted(filtered_ncrs, key=lambda x: x['ncr_number'])
elif sort_by == "NC Level":
    filtered_ncrs = sorted(filtered_ncrs, key=lambda x: (x['nc_level'] or 99, x['created_at']), reverse=True)

# Display results
st.markdown(f"### Found {len(filtered_ncrs)} NCR(s)")

if filtered_ncrs:
    # Create table
    for ncr in filtered_ncrs:
        with st.expander(f"**{ncr['ncr_number']}** - {ncr['title'][:70]}{'...' if len(ncr['title']) > 70 else ''}"):
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.markdown("**Status**")
                st.markdown(status_badge(ncr['status']), unsafe_allow_html=True)
            
            with col2:
                st.markdown("**NC Level**")
                if ncr['nc_level']:
                    st.markdown(nc_level_badge(ncr['nc_level']), unsafe_allow_html=True)
                else:
                    st.markdown("Not assigned")
            
            with col3:
                st.markdown("**Created**")
                st.markdown(pd.to_datetime(ncr['created_at'], format='mixed').strftime('%Y-%m-%d'))
            
            with col4:
                st.markdown("**Created By**")
                st.markdown(ncr['created_by_name'] or 'Unknown')
            
            st.markdown("<div style='margin: 0.75rem 0;'></div>", unsafe_allow_html=True)
            
            if ncr['part_number']:
                st.markdown(f"**Part:** {ncr['part_number']} {ncr['part_number_rev'] or ''}")
            
            if ncr['problem_is']:
                st.markdown(f"**Issue:** {ncr['problem_is'][:150]}{'...' if len(ncr['problem_is']) > 150 else ''}")

            if ncr.get('tags'):
                if tagger_component:
                    tagger_component("Tags", ncr['tags'])
                else:
                    tags_formatted = ", ".join(f"`{tag}`" for tag in ncr['tags'])
                    st.markdown(f"**Tags:** {tags_formatted}")
            
            st.markdown("<div style='margin: 0.75rem 0;'></div>", unsafe_allow_html=True)
            
            col_a, col_b, col_c = st.columns([2, 1, 1])
            with col_b:
                if st.button("📄 View Details", key=f"view_{ncr['id']}", width="stretch"):
                    st.session_state.current_ncr = ncr['id']
                    st.switch_page("pages/03_📄_NCR_Detail.py")
else:
    empty_state(
        icon="🔍",
        title="No NCRs Found",
        message="Try adjusting your search filters or create a new NCR."
    )

st.markdown("<div style='margin: 2rem 0;'></div>", unsafe_allow_html=True)

# Action buttons
col1, col2, col3 = st.columns([2, 1, 1])
with col2:
    if st.button("🔄 Refresh", width="stretch"):
        st.rerun()
with col3:
    if st.button("➕ New NCR", type="primary", width="stretch"):
        st.switch_page("pages/04_➕_New_NCR.py")

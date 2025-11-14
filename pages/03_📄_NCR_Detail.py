"""
NCR Detail Page - View and edit individual NCR
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
    sidebar_brand, sidebar_user_info,
    status_badge, nc_level_badge, info_box
)
from database import db

st.set_page_config(
    page_title="NCR Detail - NCTracker",
    page_icon="📄",
    layout="wide"
)

inject_theme_css()
apply_plotly_theme()
auth_guard()

sidebar_brand()
sidebar_user_info()

# Check if NCR is selected
if 'current_ncr' not in st.session_state or st.session_state.current_ncr is None:
    st.warning("⚠️ No NCR selected")
    if st.button("← Back to NCR List"):
        st.switch_page("pages/02_🔍_NCR_List.py")
    st.stop()

# Get NCR data
ncr = db.get_ncr_by_id(st.session_state.current_ncr)

if not ncr:
    st.error("❌ NCR not found")
    st.stop()

# Header
col1, col2 = st.columns([5, 1])
with col1:
    st.markdown(f"## 📋 {ncr['ncr_number']}")
    st.markdown(f"### {ncr['title']}")
with col2:
    if st.button("← Back"):
        st.session_state.current_ncr = None
        st.switch_page("pages/02_🔍_NCR_List.py")

# Status row
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
    st.markdown(f"**Created:** {pd.to_datetime(ncr['created_at'], format='mixed').strftime('%Y-%m-%d')}")
with col4:
    st.markdown(f"**By:** {ncr['created_by_name']}")

if ncr.get('tags'):
    st.markdown("---")
    st.markdown("**🏷️ Tags**")
    if tagger_component:
        tagger_component("NCR Tags", ncr['tags'])
    else:
        tags_formatted = ", ".join(f"`{tag}`" for tag in ncr['tags'])
        st.markdown(tags_formatted)

st.markdown("---")

# Tabs for sections
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "📝 Details",
    "⚖️ Level & CAPA",
    "🔍 Investigation",
    "🔧 Correction",
    "✅ Closure",
    "💬 Comments"
])

with tab1:
    st.markdown("### Section 1: NCR Details")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"**Site:** {ncr.get('site') or 'N/A'}")
        st.markdown(f"**Part Number:** {ncr.get('part_number') or 'N/A'}")
        st.markdown(f"**Part Rev:** {ncr.get('part_number_rev') or 'N/A'}")
        st.markdown(f"**Quantity:** {ncr.get('quantity_affected') or 'N/A'}")
        st.markdown(f"**Units:** {ncr.get('units_affected') or 'N/A'}")
    
    with col2:
        st.markdown(f"**Project:** {ncr.get('project_affected') or 'N/A'}")
        st.markdown(f"**Serial #:** {ncr.get('serial_number') or 'N/A'}")
        st.markdown(f"**PO #:** {ncr.get('po_number') or 'N/A'}")
        st.markdown(f"**Supplier:** {ncr.get('supplier') or 'N/A'}")
        st.markdown(f"**Build Group:** {ncr.get('build_group_operation') or 'N/A'}")
    
    st.markdown("---")
    st.markdown("#### Problem Statement")
    
    if ncr.get('problem_is'):
        info_box("Is (Current Situation)", ncr['problem_is'], "error")
    
    if ncr.get('problem_should_be'):
        info_box("Should Be (Expected)", ncr['problem_should_be'], "success")
    
    st.markdown("---")
    st.markdown("#### Containment")
    contained = "✅ Yes" if ncr.get('is_contained') else "❌ No"
    st.markdown(f"**Contained:** {contained}")
    if ncr.get('how_contained'):
        st.markdown(f"**How:** {ncr['how_contained']}")

with tab2:
    st.markdown("### Section 2: NC Level & CAPA")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**NC Level:**")
        if ncr['nc_level']:
            st.markdown(nc_level_badge(ncr['nc_level']), unsafe_allow_html=True)
        else:
            st.markdown("Not assigned")
        
        st.markdown(f"**CAPA Required:** {'✅ Yes' if ncr.get('capa_required') else '❌ No'}")
        if ncr.get('capa_number'):
            st.markdown(f"**CAPA #:** {ncr['capa_number']}")
    
    with col2:
        st.markdown(f"**QE Assigned:** {'✅ Yes' if ncr.get('qe_assigned') else '❌ No'}")
        st.markdown(f"**NC Owner Assigned:** {'✅ Yes' if ncr.get('nc_owner_assigned') else '❌ No'}")
        st.markdown(f"**External Notification:** {'✅ Yes' if ncr.get('external_notification_required') else '❌ No'}")

with tab3:
    st.markdown("### Section 3: Investigation & Disposition")
    
    st.markdown(f"**Problem Category:** {ncr.get('problem_category') or 'N/A'}")
    st.markdown(f"**Disposition Action:** {ncr.get('disposition_action') or 'N/A'}")
    
    if ncr.get('disposition_instructions'):
        info_box("Instructions", ncr['disposition_instructions'], "info")
    
    if ncr.get('disposition_justification'):
        info_box("Justification", ncr['disposition_justification'], "warning")

with tab4:
    st.markdown("### Section 4: Correction Actions")
    
    if ncr.get('correction_actions'):
        st.markdown("**Actions Taken:**")
        try:
            actions = ncr['correction_actions'] if isinstance(ncr['correction_actions'], list) else []
            for action in actions:
                st.markdown(f"- {action}")
        except:
            st.markdown(ncr.get('correction_actions', 'N/A'))
    
    if ncr.get('evidence_of_completion'):
        info_box("Evidence of Completion", ncr['evidence_of_completion'], "success")

with tab5:
    st.markdown("### Section 5: Closure")
    
    st.markdown(f"**QE Audit Complete:** {'✅ Yes' if ncr.get('qe_audit_complete') else '❌ No'}")
    
    if ncr.get('closure_date'):
        st.markdown(f"**Closure Date:** {ncr['closure_date']}")
    
    if ncr.get('closed_at'):
        st.markdown(f"**Closed At:** {pd.to_datetime(ncr['closed_at'], format='mixed').strftime('%Y-%m-%d %H:%M')}")

with tab6:
    st.markdown("### 💬 Comments")
    
    comments = db.get_comments(ncr['id'])
    
    if comments:
        for comment in comments:
            comment_date = pd.to_datetime(comment['created_at'], format='mixed').strftime('%Y-%m-%d %H:%M')
            st.markdown(f"""
            <div class="comment-box">
                <strong>{comment['user_name']}</strong> - <em>{comment_date}</em><br>
                <div style="margin-top: 0.5rem;">{comment['content']}</div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("No comments yet")
    
    # Add comment
    st.markdown("---")
    with st.form("add_comment"):
        new_comment = st.text_area("Add a comment:", height=100, placeholder="Enter your comment here...")
        if st.form_submit_button("💬 Post Comment", type="primary"):
            if new_comment:
                db.add_comment(ncr['id'], st.session_state.user['id'], new_comment)
                st.success("Comment added!")
                st.rerun()

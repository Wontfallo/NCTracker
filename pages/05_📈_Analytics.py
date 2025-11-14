"""
Analytics Page - Deep dive visualizations for NCTracker multipage app
"""

import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from components import (  # noqa: E402
    auth_guard,
    inject_theme_css,
    apply_plotly_theme,
    sidebar_brand,
    sidebar_user_info,
    metric_card,
    empty_state,
)
from database import db  # noqa: E402
import utils  # noqa: E402

st.set_page_config(
    page_title="Analytics - NCTracker",
    page_icon="📈",
    layout="wide",
)

inject_theme_css()
apply_plotly_theme()
auth_guard()

sidebar_brand()
sidebar_user_info()

st.markdown("## 📈 Analytics Dashboard")
st.markdown(
    "Understand trends, categories, and resolution performance across all Non-Conformance Reports."
)

stats = db.get_dashboard_stats()
ncrs = db.get_ncrs()

if not ncrs:
    empty_state(
        icon="📉",
        title="No Analytics Yet",
        message="Create NCRs to unlock analytics and trend insights.",
    )
    st.stop()

df = pd.DataFrame(ncrs)
df["created_at"] = pd.to_datetime(df["created_at"], format="mixed", errors="coerce")
df["created_date"] = df["created_at"].dt.date
df["created_month"] = df["created_at"].dt.to_period("M")
if "closed_at" in df.columns:
    df["closed_at"] = pd.to_datetime(df["closed_at"], format="mixed", errors="coerce")

closed_mask = df["status"] == "CLOSED"
closed_ncrs = int(closed_mask.sum())
open_ncrs = int((df["status"] != "CLOSED").sum())

col1, col2, col3 = st.columns(3)
with col1:
    metric_card(
        label="Total NCRs",
        value=str(stats["total_ncrs"]),
        delta=f"+{stats['recent_ncrs']} last 30 days",
        delta_color="normal",
        icon="📊",
    )
with col2:
    metric_card(
        label="Closed NCRs",
        value=str(closed_ncrs),
        delta=f"{stats['total_ncrs'] - closed_ncrs} open",
        delta_color="positive" if open_ncrs == 0 else "negative",
        icon="✅",
    )
with col3:
    metric_card(
        label="Avg Resolution",
        value=f"{stats['avg_resolution_days']:.1f} days",
        delta="Lower is better",
        delta_color="positive" if stats["avg_resolution_days"] < 20 else "normal",
        icon="⏱️",
    )

st.markdown("<div style='margin: 2rem 0;'></div>", unsafe_allow_html=True)

st.markdown("### 📊 Monthly NCR Trend")
monthly_counts = (
    df.dropna(subset=["created_month"]).groupby("created_month").size().reset_index(name="count")
)
monthly_counts["created_month"] = monthly_counts["created_month"].astype(str)
if not monthly_counts.empty:
    fig_monthly = px.line(
        monthly_counts,
        x="created_month",
        y="count",
        markers=True,
        title="NCRs Created per Month",
    )
    fig_monthly.update_layout(height=400, margin=dict(t=60, b=60, l=60, r=40))
    st.plotly_chart(fig_monthly, use_container_width=True)
else:
    st.info("Not enough data to display monthly trends.")

st.markdown("<div style='margin: 1.5rem 0;'></div>", unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    st.markdown("### 📂 Problem Categories")
    if not df["problem_category"].dropna().empty:
        category_counts = (
            df["problem_category"].fillna("Unspecified").value_counts().reset_index()
        )
        category_counts.columns = ["Category", "Count"]
        fig_category = px.pie(
            category_counts,
            names="Category",
            values="Count",
            hole=0.45,
            title="Distribution by Problem Category",
        )
        fig_category.update_layout(height=380, margin=dict(t=50, b=40, l=20, r=20))
        st.plotly_chart(fig_category, use_container_width=True)
    else:
        st.info("Problem categories will appear once NCRs include that data.")

with col2:
    st.markdown("### ⚡ Disposition Actions")
    if not df["disposition_action"].dropna().empty:
        disposition_counts = (
            df["disposition_action"].fillna("Unspecified").value_counts().reset_index()
        )
        disposition_counts.columns = ["Disposition", "Count"]
        fig_disposition = px.bar(
            disposition_counts,
            x="Disposition",
            y="Count",
            title="Disposition Action Distribution",
            text="Count",
        )
        fig_disposition.update_layout(
            height=380,
            margin=dict(t=60, b=80, l=40, r=20),
            xaxis_tickangle=-25,
        )
        fig_disposition.update_traces(textposition="outside")
        st.plotly_chart(fig_disposition, use_container_width=True)
    else:
        st.info("Disposition analytics will populate as NCRs progress.")

st.markdown("<div style='margin: 1.5rem 0;'></div>", unsafe_allow_html=True)

st.markdown("### ⏱️ Resolution Time Analysis")
if closed_ncrs and df["closed_at"].notna().any():
    resolution_days = (
        df.loc[closed_mask & df["closed_at"].notna(), "closed_at"]
        - df.loc[closed_mask & df["closed_at"].notna(), "created_at"]
    ).dt.days
    if not resolution_days.empty:
        fig_resolution = px.histogram(
            resolution_days,
            nbins=min(20, resolution_days.nunique()),
            title="Distribution of Resolution Times",
            labels={"value": "Days to Close"},
        )
        fig_resolution.update_layout(height=400, margin=dict(t=60, b=60, l=60, r=40))
        st.plotly_chart(fig_resolution, use_container_width=True)
    else:
        st.info("Resolution time requires both creation and closure timestamps.")
else:
    st.info("Closed NCRs with timestamps are needed to analyse resolution time.")

st.markdown("<div style='margin: 2rem 0;'></div>", unsafe_allow_html=True)

st.markdown("### 📤 Export & Reporting")
col1, col2 = st.columns(2)

with col1:
    if st.button("📊 Prepare Excel Export"):
        excel_data = utils.export_to_excel(ncrs)
        if excel_data:
            st.download_button(
                label="Download Excel",
                data=excel_data,
                file_name=f"ncr_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            )
        else:
            st.warning("Excel export is unavailable for this dataset.")

with col2:
    report_lines = [
        "NCTracker Summary Report",
        f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        "",
        "=== OVERVIEW ===",
        f"Total NCRs: {stats['total_ncrs']}",
        f"Recent NCRs (30 days): {stats['recent_ncrs']}",
        f"Average Resolution Time: {stats['avg_resolution_days']:.1f} days",
        "",
        "=== STATUS BREAKDOWN ===",
    ]
    for status, count in stats["status_counts"].items():
        report_lines.append(f"{status}: {count} NCRs")
    report_lines.append("")
    report_lines.append("=== NC LEVEL BREAKDOWN ===")
    for level, count in stats["nc_level_counts"].items():
        report_lines.append(f"Level {level}: {count} NCRs")

    report_content = "\n".join(report_lines)

    st.download_button(
        label="📄 Download Text Summary",
        data=report_content,
        file_name=f"ncr_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
        mime="text/plain",
    )

"""
Create New NCR Page - Guided multi-step form for NCTracker multipage app
"""

import streamlit as st
from datetime import date
from typing import List
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

try:
    from streamlit_extras.tags import tagger_component  # type: ignore
except ImportError:  # pragma: no cover - optional dependency handled at runtime
    tagger_component = None

from components import (  # noqa: E402
    auth_guard,
    inject_theme_css,
    apply_plotly_theme,
    sidebar_brand,
    sidebar_user_info,
)
from database import db  # noqa: E402

st.set_page_config(
    page_title="New NCR - NCTracker",
    page_icon="➕",
    layout="wide",
)

inject_theme_css()
apply_plotly_theme()
auth_guard()

sidebar_brand()
sidebar_user_info()

SECTION_LABELS = {
    1: "Section 1: NCR Details",
    2: "Section 2: NC Level & CAPA",
    3: "Section 3: Investigation & Disposition",
    4: "Section 4: Correction Actions",
    5: "Section 5: NCR Closure",
}

FORM_WIDGET_KEYS = {
    "text": [
        "investigation_results",
        "disposition_justification",
        "evidence_of_completion",
    ],
    "checkbox": [
        "Disposition Work Only",
        "ECN/ECO/ECR",
        "Deviation/Waiver",
        "SCAR or Supplier Support",
        "RCCA/CAPA",
        "Process/Procedural Update",
        "Other",
    ],
}
TAG_SUGGESTION_LIMIT = 12


def init_form_state():
    """Ensure required session state values exist."""
    if "ncr_form_data" not in st.session_state:
        st.session_state.ncr_form_data = {}
    if "current_section" not in st.session_state:
        st.session_state.current_section = 1
    st.session_state.ncr_form_data.setdefault("tags", [])


def clear_form_state():
    """Reset the multi-step form including widget-backed state."""
    st.session_state.ncr_form_data = {}
    st.session_state.current_section = 1

    for key in FORM_WIDGET_KEYS["text"]:
        st.session_state.pop(key, None)

    for action in FORM_WIDGET_KEYS["checkbox"]:
        st.session_state.pop(f"correction_{action}", None)

    st.session_state.pop("ncr_tags_input", None)


def set_section(section_index: int):
    """Update the visible section index."""
    st.session_state.current_section = section_index


def get_tag_suggestions() -> List[str]:
    """Collect a unique, sorted list of tags already used across NCRs."""
    try:
        records = db.get_ncrs()
    except Exception:  # pragma: no cover - defensive against DB access issues
        return []

    tag_set = {
        tag.strip()
        for record in records
        for tag in (record.get("tags") or [])
        if isinstance(tag, str) and tag.strip()
    }

    sorted_tags = sorted(tag_set, key=lambda value: value.lower())
    return sorted_tags[:TAG_SUGGESTION_LIMIT]


def render_navigation():
    """Render section navigation pills."""
    current_selection = st.session_state.current_section
    cols = st.columns(len(SECTION_LABELS))
    for idx, (section_id, heading) in enumerate(SECTION_LABELS.items()):
        is_active = current_selection == section_id
        label = f"{section_id}. {heading.split(':')[0]}"
        if cols[idx].button(
            label,
            type="primary" if is_active else "secondary",
            key=f"nav_{section_id}"
        ):
            current_selection = section_id

    if current_selection != st.session_state.current_section:
        st.session_state.current_section = current_selection
        st.rerun()


def render_section_1():
    """Section 1: NCR Details."""
    st.markdown("### 🔍 Section 1: NCR Details")
    st.markdown(
        "*Completed by the person identifying the nonconformance. Use N/A when fields do not apply.*"
    )

    form_data = st.session_state.ncr_form_data

    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<div class="form-section">', unsafe_allow_html=True)
        st.markdown("#### Basic Information")

        title = st.text_input(
            "**NCR Title** *Required*",
            value=form_data.get("title", ""),
            help=(
                "Format: Part Number, Issue Description. Example: 13204643-101, "
                "LN2 Stack Out of Tolerance"
            ),
        )

        site_options = ["", "Site A", "Site B", "Site C", "Other"]
        site = st.selectbox(
            "**Site**",
            site_options,
            index=site_options.index(form_data.get("site", ""))
            if form_data.get("site") in site_options
            else 0,
        )

        part_number = st.text_input(
            "**Part Number or Equipment ID**",
            value=form_data.get("part_number", ""),
        )
        part_number_rev = st.text_input(
            "**Part Number Rev**",
            value=form_data.get("part_number_rev", ""),
        )
        quantity_affected = st.number_input(
            "**Quantity of Parts Affected**",
            min_value=0,
            value=form_data.get("quantity_affected", 0),
        )
        units_affected = st.text_input(
            "**Unit(s) Affected**",
            value=form_data.get("units_affected", ""),
        )
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="form-section">', unsafe_allow_html=True)
        st.markdown("#### Project & Identification")

        project_affected = st.text_input(
            "**Project Affected**",
            value=form_data.get("project_affected", ""),
        )
        serial_number = st.text_input(
            "**Serial Number**",
            value=form_data.get("serial_number", ""),
        )
        other_id = st.text_input(
            "**Other ID**",
            value=form_data.get("other_id", ""),
        )
        po_number = st.text_input(
            "**PO**",
            value=form_data.get("po_number", ""),
        )
        supplier = st.text_input(
            "**Supplier**",
            value=form_data.get("supplier", ""),
        )
        build_group_operation = st.text_input(
            "**Build Group & Operation**",
            value=form_data.get("build_group_operation", ""),
        )
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="form-section">', unsafe_allow_html=True)
    st.markdown("#### 📝 Problem Statement")
    st.markdown(
        "*Describe the situation using **Is** and **Should Be** statements to highlight the gap.*"
    )

    col1, col2 = st.columns(2)
    with col1:
        problem_is = st.text_area(
            "**Is:** *What is the current situation?*",
            value=form_data.get("problem_is", ""),
            height=100,
        )
    with col2:
        problem_should_be = st.text_area(
            "**Should Be:** *What should be the correct situation?*",
            value=form_data.get("problem_should_be", ""),
            height=100,
        )
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="form-section">', unsafe_allow_html=True)
    st.markdown("#### 🛡️ Containment/Notification")
    st.markdown(
        "*Is the issue properly contained and identified? Provide details when applicable.*"
    )

    col1, col2 = st.columns(2)
    containment_options = ["", "Yes", "No"]
    current_containment = form_data.get("is_contained_str", "")
    with col1:
        is_contained = st.radio(
            "**Is the issue contained?**",
            containment_options,
            index=containment_options.index(current_containment)
            if current_containment in containment_options
            else 0,
        )
    with col2:
        how_contained = st.text_input(
            "**How Contained:**",
            value=form_data.get("how_contained", ""),
            disabled=is_contained != "Yes",
        )

    if is_contained == "No":
        containment_justification = st.text_area(
            "**Justification for not containing:**",
            value=form_data.get("containment_justification", ""),
        )
    else:
        containment_justification = ""
    st.markdown("</div>", unsafe_allow_html=True)

    st.session_state.ncr_form_data.update(
        {
            "title": title,
            "site": site,
            "part_number": part_number,
            "part_number_rev": part_number_rev,
            "quantity_affected": quantity_affected,
            "units_affected": units_affected,
            "project_affected": project_affected,
            "serial_number": serial_number,
            "other_id": other_id,
            "po_number": po_number,
            "supplier": supplier,
            "build_group_operation": build_group_operation,
            "problem_is": problem_is,
            "problem_should_be": problem_should_be,
            "is_contained": True if is_contained == "Yes" else False if is_contained == "No" else None,
            "is_contained_str": is_contained,
            "how_contained": how_contained,
            "containment_justification": containment_justification,
        }
    )

    st.markdown('<div class="form-section">', unsafe_allow_html=True)
    st.markdown("#### 🏷️ Tags & Keywords")
    st.markdown(
        "*Add quick labels so teams can search by supplier, process, product line, or campaign.*"
    )

    suggestions = get_tag_suggestions()
    existing_tags = form_data.get("tags", [])

    if suggestions:
        st.caption(
            "Common tags: " + ", ".join(f"`{tag}`" for tag in suggestions)
        )

    tags_input = st.text_input(
        "Enter tags (comma separated)",
        value=", ".join(existing_tags),
        placeholder="e.g. supplier, audit, level-1",
        key="ncr_tags_input",
    )

    tags = [tag.strip() for tag in tags_input.split(",") if tag.strip()]

    if tagger_component and tags:
        tagger_component("Current selection", tags)
    elif not tags:
        st.caption("No tags captured yet. Add some above to improve discovery.")

    st.session_state.ncr_form_data["tags"] = tags
    st.markdown("</div>", unsafe_allow_html=True)


def render_section_2():
    """Section 2: NC Level and CAPA."""
    st.markdown("### ⚖️ Section 2: NC Level and CAPA")
    st.markdown("*Managed by NCR administrator or QE.*")

    form_data = st.session_state.ncr_form_data

    st.markdown('<div class="form-section">', unsafe_allow_html=True)
    st.markdown("#### 🎯 NC Level")

    nc_level_options = {
        "": None,
        "1 - Critical": 1,
        "2 - Adverse": 2,
        "3 - Moderate": 3,
        "4 - Low": 4,
    }
    current_level = form_data.get("nc_level")
    current_label = next(
        (label for label, value in nc_level_options.items() if value == current_level),
        "",
    )
    nc_level = st.radio(
        "**Select NC Level:**",
        list(nc_level_options.keys()),
        index=list(nc_level_options.keys()).index(current_label)
        if current_label in nc_level_options
        else 0,
    )

    level_help = {
        "1 - Critical": "Injury or total system failure — escalate to senior leadership; CAPA required.",
        "2 - Adverse": "Schedule slip ≥ 3 days or missed milestone — escalate to management; CAPA recommended.",
        "3 - Moderate": "Drawing change, repairs, use-as-is, or schedule slip < 3 days.",
        "4 - Low": "Rework to drawing, scrap, or return to vendor.",
    }
    if nc_level in level_help:
        st.info(level_help[nc_level])
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="form-section">', unsafe_allow_html=True)
    st.markdown("#### 🔄 Corrective & Preventive Actions (CAPA)")

    capa_choices = ["", "Yes", "No"]
    capa_required_choice = st.radio(
        "**CAPA Required?**",
        capa_choices,
        index=capa_choices.index(form_data.get("capa_required_str", ""))
        if form_data.get("capa_required_str") in capa_choices
        else 0,
    )
    capa_number = ""
    if capa_required_choice == "Yes":
        capa_number = st.text_input(
            "**CAPA Number:**",
            value=form_data.get("capa_number", ""),
        )
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="form-section">', unsafe_allow_html=True)
    st.markdown("#### 👥 Assignments & Notifications")

    col1, col2 = st.columns(2)

    qe_choices = ["", "Yes", "No"]
    with col1:
        qe_choice = st.radio(
            "**QE Assigned?**",
            qe_choices,
            index=qe_choices.index(form_data.get("qe_assigned_str", ""))
            if form_data.get("qe_assigned_str") in qe_choices
            else 0,
        )
        owner_choice = st.radio(
            "**NC Owner Assigned?**",
            qe_choices,
            index=qe_choices.index(form_data.get("nc_owner_assigned_str", ""))
            if form_data.get("nc_owner_assigned_str") in qe_choices
            else 0,
        )

    with col2:
        notification_choices = ["", "Yes", "No"]
        notification_choice = st.radio(
            "**External Notification Required?**",
            notification_choices,
            index=notification_choices.index(form_data.get("external_notification_required_str", ""))
            if form_data.get("external_notification_required_str") in notification_choices
            else 0,
        )
        notification_method = ""
        if notification_choice == "Yes":
            notification_method = st.text_input(
                "**How:** *Notification method*",
                value=form_data.get("external_notification_method", ""),
            )
    st.markdown("</div>", unsafe_allow_html=True)

    st.session_state.ncr_form_data.update(
        {
            "nc_level": nc_level_options[nc_level],
            "capa_required": True if capa_required_choice == "Yes" else False if capa_required_choice == "No" else None,
            "capa_required_str": capa_required_choice,
            "capa_number": capa_number,
            "qe_assigned": True if qe_choice == "Yes" else False if qe_choice == "No" else None,
            "qe_assigned_str": qe_choice,
            "nc_owner_assigned": True if owner_choice == "Yes" else False if owner_choice == "No" else None,
            "nc_owner_assigned_str": owner_choice,
            "external_notification_required": True if notification_choice == "Yes" else False if notification_choice == "No" else None,
            "external_notification_required_str": notification_choice,
            "external_notification_method": notification_method,
        }
    )


def render_section_3():
    """Section 3: Investigation & Disposition."""
    st.markdown("### 🔍 Section 3: Investigation & Disposition")
    st.markdown("*Completed by the NC Owner.*")

    form_data = st.session_state.ncr_form_data

    st.markdown('<div class="form-section">', unsafe_allow_html=True)
    st.markdown("#### 🔬 Investigation Results")
    st.text_area(
        "**Investigation Results:**",
        value=form_data.get("investigation_results", ""),
        height=100,
        key="investigation_results",
    )
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="form-section">', unsafe_allow_html=True)
    st.markdown("#### 📂 Problem Category")
    categories = [
        "Document",
        "Design",
        "Manufacturing",
        "Supplier",
        "Equipment",
        "Customer",
        "Process",
        "Improvement",
        "Software",
        "Service",
        "Other",
    ]
    current_category = form_data.get("problem_category", "")
    if current_category not in categories:
        current_category = ""
    problem_category = st.selectbox(
        "**Select Category:**",
        [""] + categories,
        index=categories.index(current_category) + 1 if current_category else 0,
    )
    if problem_category == "Other":
        other_category = st.text_input(
            "**Specify Other Category:**",
            value=form_data.get("other_category", ""),
        )
    else:
        other_category = ""
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="form-section">', unsafe_allow_html=True)
    st.markdown("#### ⚡ Disposition Action")
    disposition_options = [
        "Rework",
        "Repair",
        "Reject - Return to Supplier",
        "Reject - Scrap",
        "Use-As-Is",
        "Other",
    ]
    current_disposition = (
        form_data.get("disposition_action")
        if form_data.get("disposition_action") in disposition_options
        else disposition_options[0]
    )
    disposition_action = st.radio(
        "**Select Disposition:**",
        disposition_options,
        index=disposition_options.index(current_disposition),
    )
    disposition_instructions = st.text_input(
        "**Instructions/Task Reference:**",
        value=form_data.get("disposition_instructions", ""),
    )
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="form-section">', unsafe_allow_html=True)
    st.markdown("#### 💭 Rationale for Disposition")
    st.text_area(
        "**Justification:**",
        value=form_data.get("disposition_justification", ""),
        height=100,
        key="disposition_justification",
    )
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="form-section">', unsafe_allow_html=True)
    st.markdown("#### ✅ Required Approvals")
    approval_requirements = {
        1: "1 Quality Manager + 1 Quality Engineer + 1 SME Manager + 2 SME Engineers",
        2: "1 SME Manager/Quality Manager + 1 Quality Engineer + 2 SME Engineers",
        3: "1 Quality Engineer + 2 SME Engineers",
        4: "1 Quality Engineer + 1 SME Engineer",
    }
    nc_level = form_data.get("nc_level", 3)
    if nc_level in approval_requirements:
        st.info(f"**Required Approvals (Level {nc_level}):** {approval_requirements[nc_level]}")
    required_approvals = st.text_area(
        "**Required Approvers (list names separated by commas):**",
        value=form_data.get("required_approvals_text", ""),
        help="Enter the names of required approvers",
    )
    st.markdown("</div>", unsafe_allow_html=True)

    st.session_state.ncr_form_data.update(
        {
            "problem_category": problem_category,
            "other_category": other_category,
            "disposition_action": disposition_action,
            "disposition_instructions": disposition_instructions,
            "required_approvals_text": required_approvals,
            "investigation_results": st.session_state.get("investigation_results", ""),
            "disposition_justification": st.session_state.get("disposition_justification", ""),
        }
    )


def render_section_4():
    """Section 4: Correction actions."""
    st.markdown("### 🔧 Section 4: Correction")
    st.markdown("*Document actions taken to correct the nonconformance and prevent recurrence.*")

    form_data = st.session_state.ncr_form_data

    st.markdown('<div class="form-section">', unsafe_allow_html=True)
    st.markdown("#### 🎯 Correction Actions Taken")

    correction_flags = {
        "Disposition Work Only": form_data.get("disposition_work_only", False),
        "ECN/ECO/ECR": form_data.get("ecn_eco_ecr", False),
        "Deviation/Waiver": form_data.get("deviation_waiver", False),
        "SCAR or Supplier Support": form_data.get("scar_supplier", False),
        "RCCA/CAPA": form_data.get("rcca_capa", False),
        "Process/Procedural Update": form_data.get("process_update", False),
        "Other": form_data.get("other_correction", False),
    }

    st.markdown("**Select all that apply:**")
    cols = st.columns(2)
    selected_actions = []
    for idx, (action, default_state) in enumerate(correction_flags.items()):
        key = f"correction_{action}"
        if cols[idx % 2].checkbox(action, value=default_state, key=key):
            selected_actions.append(action)

    if "Other" in selected_actions:
        other_correction_text = st.text_input(
            "**Specify Other Action:**",
            value=form_data.get("other_correction_text", ""),
        )
    else:
        other_correction_text = ""
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="form-section">', unsafe_allow_html=True)
    st.markdown("#### 📄 Evidence of Completion")
    st.text_area(
        "**Evidence of Completion:**",
        value=form_data.get("evidence_of_completion", ""),
        height=100,
        key="evidence_of_completion",
    )
    st.markdown("</div>", unsafe_allow_html=True)

    st.session_state.ncr_form_data.update(
        {
            "disposition_work_only": "Disposition Work Only" in selected_actions,
            "ecn_eco_ecr": "ECN/ECO/ECR" in selected_actions,
            "deviation_waiver": "Deviation/Waiver" in selected_actions,
            "scar_supplier": "SCAR or Supplier Support" in selected_actions,
            "rcca_capa": "RCCA/CAPA" in selected_actions,
            "process_update": "Process/Procedural Update" in selected_actions,
            "other_correction": "Other" in selected_actions,
            "other_correction_text": other_correction_text,
            "correction_actions": selected_actions,
            "evidence_of_completion": st.session_state.get("evidence_of_completion", ""),
        }
    )


def render_section_5():
    """Section 5: NCR closure."""
    st.markdown("### ✅ Section 5: NCR Closure")
    st.markdown("*Final review completed by Quality Engineering before closure.*")

    form_data = st.session_state.ncr_form_data

    st.markdown('<div class="form-section">', unsafe_allow_html=True)
    st.markdown("#### 🔍 QA Audit Checklist")
    st.markdown("- Review all sections for completeness")
    st.markdown("- Verify required approvals are documented")
    st.markdown("- Confirm containment and correction actions are adequate")
    st.markdown("- Ensure supporting documentation is attached")

    qe_audit_complete = st.checkbox(
        "**Audit complete - NCR is ready for closure**",
        value=form_data.get("qe_audit_complete", False),
    )

    if qe_audit_complete:
        closure_date = st.date_input(
            "**Closure Date:**",
            value=form_data.get("closure_date", date.today()),
            min_value=date(2020, 1, 1),
        )
        st.success("✅ NCR marked as ready for closure")
    else:
        closure_date = None
        st.warning("Complete the QA audit before closing the NCR.")
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("💾 Save Draft"):
            st.success("Draft saved in the current session.")
    with col2:
        if st.button("✅ Submit NCR", type="primary", disabled=not qe_audit_complete):
            submit_ncr()
    with col3:
        if st.button("🗑️ Clear Form"):
            clear_form_state()
            st.rerun()

    st.session_state.ncr_form_data.update(
        {
            "qe_audit_complete": qe_audit_complete,
            "closure_date": closure_date,
        }
    )


def submit_ncr():
    """Persist the NCR and redirect to its detail view."""
    form_data = st.session_state.ncr_form_data

    if not form_data.get("title"):
        st.error("NCR Title is required before submission.")
        return

    required_approvals_raw = form_data.get("required_approvals_text", "")
    required_approvals = [
        name.strip()
        for name in required_approvals_raw.split(",")
        if name and name.strip()
    ]

    ncr_payload = {
        "title": form_data.get("title"),
        "status": "NEW",
        "priority": form_data.get("nc_level", 3),
        "site": form_data.get("site"),
        "part_number": form_data.get("part_number"),
        "part_number_rev": form_data.get("part_number_rev"),
        "quantity_affected": form_data.get("quantity_affected"),
        "units_affected": form_data.get("units_affected"),
        "project_affected": form_data.get("project_affected"),
        "serial_number": form_data.get("serial_number"),
        "other_id": form_data.get("other_id"),
        "po_number": form_data.get("po_number"),
        "supplier": form_data.get("supplier"),
        "build_group_operation": form_data.get("build_group_operation"),
        "problem_is": form_data.get("problem_is"),
        "problem_should_be": form_data.get("problem_should_be"),
        "is_contained": form_data.get("is_contained"),
        "how_contained": form_data.get("how_contained"),
        "containment_justification": form_data.get("containment_justification"),
        "nc_level": form_data.get("nc_level"),
        "capa_required": form_data.get("capa_required"),
        "capa_number": form_data.get("capa_number"),
        "qe_assigned": form_data.get("qe_assigned"),
        "nc_owner_assigned": form_data.get("nc_owner_assigned"),
        "external_notification_required": form_data.get("external_notification_required"),
        "external_notification_method": form_data.get("external_notification_method"),
        "problem_category": form_data.get("problem_category"),
        "disposition_action": form_data.get("disposition_action"),
        "disposition_instructions": form_data.get("disposition_instructions"),
        "disposition_justification": form_data.get("disposition_justification"),
        "required_approvals": required_approvals,
        "correction_actions": form_data.get("correction_actions", []),
        "evidence_of_completion": form_data.get("evidence_of_completion"),
        "tags": form_data.get("tags", []),
        "created_by": st.session_state.user["id"],
    }

    try:
        ncr_id = db.create_ncr(ncr_payload)
        record = db.get_ncr_by_id(ncr_id)
        st.session_state.ncr_form_data = {}
        st.session_state.current_section = 1
        st.session_state.current_ncr = ncr_id
        st.session_state.pop("investigation_results", None)
        st.session_state.pop("disposition_justification", None)
        st.session_state.pop("evidence_of_completion", None)
        st.session_state.pop("ncr_tags_input", None)
        for action in FORM_WIDGET_KEYS["checkbox"]:
            st.session_state.pop(f"correction_{action}", None)
        st.success(f"NCR created successfully: {record['ncr_number']}")
        st.switch_page("pages/03_📄_NCR_Detail.py")
    except Exception as exc:  # pragma: no cover - Streamlit feedback path
        st.error(f"Error creating NCR: {exc}")


init_form_state()

st.markdown("## ➕ Create New NCR")
st.markdown(
    "Use the guided workflow below to capture all required information for a new Non-Conformance Report."
)

render_navigation()
st.markdown("---")

current_section = st.session_state.current_section
if current_section == 1:
    render_section_1()
elif current_section == 2:
    render_section_2()
elif current_section == 3:
    render_section_3()
elif current_section == 4:
    render_section_4()
else:
    render_section_5()

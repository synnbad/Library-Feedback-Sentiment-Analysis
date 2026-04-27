"""Workflow-oriented reports section for Streamlit."""

from __future__ import annotations

import streamlit as st

from modules import assessment_workflow
from ui import assessment_workflow_ui, context_ui, report_ui


def show_reports_page() -> None:
    """Display report, project, dashboard handoff, and methods workflows."""
    assessment_workflow.ensure_assessment_schema()
    st.title("Reports")
    st.caption("Build leadership-ready briefs from curated evidence, projects, and analyses.")
    context_ui.show_context_strip()

    tabs = st.tabs(["Leadership Reports", "Projects", "Evidence Drawer", "Dashboard Handoff", "Methods & Training"])
    with tabs[0]:
        report_ui.show_report_generation_page()
    with tabs[1]:
        assessment_workflow_ui._show_projects_tab()
    with tabs[2]:
        _show_evidence_drawer_placeholder()
    with tabs[3]:
        assessment_workflow_ui._show_dashboard_tab()
    with tabs[4]:
        assessment_workflow_ui._show_training_tab()


def _show_evidence_drawer_placeholder() -> None:
    st.markdown("### Evidence Drawer")
    st.info(
        "Report-specific evidence drawers are planned. Promoted insights, charts, metrics, "
        "and recommendations will collect here before being placed into report sections."
    )
    st.markdown(
        "- Source dataset and method\n"
        "- Evidence label and limitations\n"
        "- Owner and timestamp\n"
        "- Included or not included in the current report"
    )


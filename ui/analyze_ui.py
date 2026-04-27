"""Workflow-oriented analysis section for Streamlit."""

from __future__ import annotations

import streamlit as st

from modules import assessment_workflow
from ui import (
    assessment_workflow_ui,
    context_ui,
    qualitative_ui,
    quantitative_ui,
    visualization_ui,
)


def show_analyze_page() -> None:
    """Display analysis workflows by assessment question type."""
    st.title("Analyze")
    st.caption("Explore text feedback, metrics, trends, comparisons, charts, and modeling readiness.")
    context_ui.show_context_strip()

    tabs = st.tabs(["Text Feedback", "Metrics & Trends", "Comparisons", "Charts", "Modeling Readiness"])
    with tabs[0]:
        qualitative_ui.show_qualitative_analysis_page()
    with tabs[1]:
        quantitative_ui.show_quantitative_analysis_page()
    with tabs[2]:
        st.markdown("### Comparisons")
        assessment_workflow.ensure_assessment_schema()
        assessment_workflow_ui._show_benchmarking_tab()
    with tabs[3]:
        visualization_ui.show_visualizations_page()
    with tabs[4]:
        assessment_workflow.ensure_assessment_schema()
        assessment_workflow_ui._show_modeling_tab()


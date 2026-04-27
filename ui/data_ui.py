"""Workflow-oriented data section for Streamlit."""

from __future__ import annotations

import pandas as pd
import streamlit as st

from modules import csv_handler
from ui import context_ui, data_upload_ui


def show_data_page() -> None:
    """Display dataset import, management, privacy, metadata, and indexing status."""
    st.title("Data")
    st.caption("Import, review, describe, index, archive, and govern assessment datasets.")
    context_ui.show_context_strip()

    tabs = st.tabs(["Import", "Datasets", "PII Review", "Metadata", "Indexing"])
    with tabs[0]:
        data_upload_ui._show_upload_tab()
    with tabs[1]:
        data_upload_ui._show_manage_tab()
    with tabs[2]:
        _show_pii_review_tab()
    with tabs[3]:
        _show_metadata_tab()
    with tabs[4]:
        _show_indexing_tab()


def _show_pii_review_tab() -> None:
    st.markdown("### PII Review")
    st.info(
        "Upload-time PII blocking and redacted import are planned for this workflow. "
        "Until then, generated outputs continue to use existing PII redaction safeguards."
    )
    st.markdown("#### Target Review States")
    st.markdown(
        "- Blocking: high-risk identifiers require redacted import or admin override.\n"
        "- Needs review: possible identifiers should be confirmed before import.\n"
        "- Informational: low-risk findings are recorded in provenance."
    )


def _show_metadata_tab() -> None:
    st.markdown("### Metadata Readiness")
    datasets = csv_handler.get_datasets()
    if not datasets:
        st.info("No active datasets yet. Import a dataset to begin metadata review.")
        return

    rows = []
    for dataset in datasets:
        missing = [
            field
            for field in ("title", "description", "source", "usage_notes", "ethical_considerations")
            if not dataset.get(field)
        ]
        rows.append(
            {
                "id": dataset["id"],
                "name": dataset["name"],
                "type": dataset["dataset_type"],
                "missing_fields": ", ".join(missing) if missing else "complete",
            }
        )
    st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)


def _show_indexing_tab() -> None:
    st.markdown("### Indexing Status")
    datasets = csv_handler.get_datasets()
    if not datasets:
        st.info("No active datasets yet. Import a dataset to create an indexing job.")
        return

    rows = [
        {
            "id": dataset["id"],
            "name": dataset["name"],
            "status": dataset.get("indexing_status") or "pending",
            "indexed_at": dataset.get("indexed_at") or "",
            "error": dataset.get("indexing_error") or "",
        }
        for dataset in datasets
    ]
    st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)
    st.caption("Automatic post-import indexing and retry controls belong in this queue.")


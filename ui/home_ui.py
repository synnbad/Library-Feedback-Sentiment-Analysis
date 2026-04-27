"""
Home UI Module

Displays the dashboard and system status for the Library Assessment Decision Support System.
"""

from importlib.util import find_spec
from pathlib import Path
from urllib.error import URLError
from urllib.request import urlopen

import streamlit as st

from config.settings import Settings
from modules import csv_handler, query_intelligence, query_queue
from modules.database import execute_query
from ui import context_ui


def show_home_page():
    """Display operational dashboard with system overview and next actions."""
    st.title("Library Assessment Assistant")
    st.caption("Operational dashboard for local-first library assessment work.")
    context_ui.show_context_strip()
    
    # System status
    st.markdown("---")
    st.markdown("### System Status")

    system_status = display_system_status()
    quick_stats = display_quick_stats()

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("App", system_status["streamlit"])

    with col2:
        st.metric("Database", system_status["database"])

    with col3:
        st.metric("Ollama", system_status["ollama"])

    with col4:
        st.metric("ChromaDB", system_status["chromadb"])

    st.markdown("---")
    st.markdown("### Quick Stats")

    stats_col1, stats_col2, stats_col3 = st.columns(3)

    with stats_col1:
        st.metric("Datasets", quick_stats["datasets"])

    with stats_col2:
        st.metric("Survey Responses", quick_stats["survey_responses"])

    with stats_col3:
        st.metric("Users", quick_stats["users"])

    st.markdown("---")
    _display_attention_queue(system_status)
    _display_guided_next_steps()


def _display_attention_queue(system_status):
    """Show concise operational items that need attention."""
    st.markdown("### Needs Attention")
    datasets = csv_handler.get_datasets()
    items = []

    if not datasets:
        items.append(("Data", "No active datasets yet", "Open Data > Import and add an assessment file."))

    metadata_gap_count = 0
    unindexed_count = 0
    for dataset in datasets:
        if any(not dataset.get(field) for field in ("title", "description", "source")):
            metadata_gap_count += 1
        if not _is_indexed(dataset):
            unindexed_count += 1

    if metadata_gap_count:
        items.append(("Metadata", f"{metadata_gap_count} dataset(s) need core metadata", "Open Data > Metadata."))
    if unindexed_count:
        items.append(("Indexing", f"{unindexed_count} dataset(s) are not indexed", "Open Data > Indexing."))
    if system_status["ollama"] != "Connected":
        items.append(("Inference", f"Ollama is {system_status['ollama'].lower()}", "LLM drafting and RAG answers are paused."))

    if not items:
        st.success("No immediate operational issues detected.")
        return

    for category, issue, action in items:
        st.warning(f"**{category}:** {issue}. {action}")


def _is_indexed(dataset):
    """Return True for all internal states that mean ready for Ask."""
    return (dataset.get("indexing_status") or "").lower() in {"completed", "indexed", "ready"}


def display_system_status():
    """Check local component status for the dashboard."""
    status = {"streamlit": "Ready"}

    try:
        execute_query("SELECT 1 AS ok")
        status["database"] = "Connected"
    except Exception:
        status["database"] = "Unavailable"

    chroma_installed = find_spec("chromadb") is not None
    chroma_path = Path(Settings.CHROMA_DB_PATH)
    if chroma_installed and chroma_path.exists():
        status["chromadb"] = "Ready"
    elif chroma_installed:
        status["chromadb"] = "Installed"
    else:
        status["chromadb"] = "Missing"

    ollama_endpoint = f"{Settings.OLLAMA_URL.rstrip('/')}/api/tags"
    try:
        with urlopen(ollama_endpoint, timeout=1.5) as response:
            status["ollama"] = "Connected" if 200 <= response.status < 300 else "Degraded"
    except URLError:
        status["ollama"] = "Offline"
    except Exception:
        status["ollama"] = "Unavailable"

    return status


def display_quick_stats():
    """Display quick statistics from the local database."""
    stats = {
        "datasets": 0,
        "survey_responses": 0,
        "users": 0,
    }

    try:
        dataset_rows = execute_query("SELECT COUNT(*) AS count FROM datasets")
        response_rows = execute_query("SELECT COUNT(*) AS count FROM survey_responses")
        user_rows = execute_query("SELECT COUNT(*) AS count FROM users")

        stats["datasets"] = dataset_rows[0]["count"]
        stats["survey_responses"] = response_rows[0]["count"]
        stats["users"] = user_rows[0]["count"]
    except Exception:
        pass

    return stats


def _display_guided_next_steps():
    """Show dataset-aware next steps on the dashboard."""
    st.markdown("### Recommended Next Step")
    datasets = csv_handler.get_datasets()
    profiles = []
    for dataset in datasets[:5]:
        try:
            preview_df = csv_handler.get_preview(dataset["id"], n_rows=1000)
            if not preview_df.empty:
                profiles.append(query_intelligence.build_profile_from_dataset_record(dataset, preview_df))
        except Exception:
            continue

    st.info(query_intelligence.recommended_next_action(profiles))
    if not profiles:
        return

    summary = query_intelligence.combine_profiles(profiles)
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Profiled Rows", f"{summary['total_rows']:,}")
    with col2:
        st.metric("Dataset Types", ", ".join(summary["types"]))
    with col3:
        ready = []
        if summary["has_text"]:
            ready.append("Text")
        if summary["has_numeric"]:
            ready.append("Numeric")
        if summary["has_dates"]:
            ready.append("Trends")
        st.metric("Ready For", ", ".join(ready) if ready else "Review")

    with st.expander("Suggested Questions", expanded=False):
        questions = []
        for profile in profiles[:3]:
            questions.extend(query_intelligence.suggest_questions(profile, limit=2))
        for idx, question in enumerate(_dedupe(questions)[:5]):
            if st.button(question, key=f"home_question_{idx}", use_container_width=True):
                query_queue.queue_question(st.session_state, question)
                st.success("Queued. Open Ask to review, edit, and run it.")


def _dedupe(items):
    seen = set()
    result = []
    for item in items:
        if item and item not in seen:
            result.append(item)
            seen.add(item)
    return result

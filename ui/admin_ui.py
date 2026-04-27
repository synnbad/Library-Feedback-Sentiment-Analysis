"""Admin control plane for Streamlit."""

from __future__ import annotations

import pandas as pd
import streamlit as st

from config.settings import Settings
from modules import auth
from ui import context_ui, logs_ui


def show_admin_page() -> None:
    """Display admin-only controls and operational status."""
    username = st.session_state.get("username")
    if not auth.is_admin(username):
        st.error("Admin access is required for this section.")
        return

    st.title("Admin")
    st.caption("Manage users, backups, model settings, PII rules, audit logs, and system health.")
    context_ui.show_context_strip()

    tabs = st.tabs([
        "Users & Roles",
        "Backups & Restore",
        "Model Settings",
        "PII Rules",
        "Audit Logs",
        "System Health",
    ])
    with tabs[0]:
        _show_users_tab()
    with tabs[1]:
        _show_backups_tab()
    with tabs[2]:
        _show_model_settings_tab()
    with tabs[3]:
        _show_pii_rules_tab()
    with tabs[4]:
        logs_ui.show_logs_page()
    with tabs[5]:
        _show_system_health_tab()


def _show_users_tab() -> None:
    st.markdown("### Users & Roles")
    users = auth.list_users()
    if users:
        st.dataframe(pd.DataFrame(users), use_container_width=True, hide_index=True)
    else:
        st.info("No users found.")

    st.markdown("#### Planned User Management Actions")
    st.markdown(
        "- Create named users.\n"
        "- Assign admin, analyst, or viewer roles.\n"
        "- Reset passwords and disable accounts.\n"
        "- Review recent access by user."
    )


def _show_backups_tab() -> None:
    st.markdown("### Backups & Restore")
    st.info(
        "Explicit full-fidelity backup and overwrite restore workflows are planned. "
        "Restore will create an automatic pre-restore backup first."
    )


def _show_model_settings_tab() -> None:
    st.markdown("### Model Settings")
    st.text_input("Ollama Endpoint", value=Settings.OLLAMA_URL, disabled=True)
    st.text_input("LLM Model", value=Settings.OLLAMA_MODEL, disabled=True)
    st.text_input("Embedding Model", value=Settings.EMBEDDING_MODEL, disabled=True)
    st.caption("Admin-managed endpoint allowlisting and model changes are planned.")


def _show_pii_rules_tab() -> None:
    st.markdown("### PII Rules")
    rules = [{"type": key, "pattern": value} for key, value in Settings.PII_PATTERNS.items()]
    st.dataframe(pd.DataFrame(rules), use_container_width=True, hide_index=True)
    st.caption("Institution-specific labels, severity, and test text are planned.")


def _show_system_health_tab() -> None:
    st.markdown("### System Health")
    from ui.home_ui import display_quick_stats, display_system_status

    status = display_system_status()
    stats = display_quick_stats()
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Database", status["database"])
    col2.metric("ChromaDB", status["chromadb"])
    col3.metric("Ollama", status["ollama"])
    col4.metric("Datasets", stats["datasets"])


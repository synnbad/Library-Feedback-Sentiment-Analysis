"""Shared Streamlit context indicators."""

from __future__ import annotations

from datetime import datetime
from pathlib import Path

import streamlit as st

from config.settings import Settings
from modules import auth


def show_context_strip(scope: str | None = None) -> None:
    """Render a compact current-context strip at the top of workflow pages."""
    username = st.session_state.get("username") or "unknown"
    role = auth.get_user_role(username)
    backup_age = _backup_age_label()

    columns = st.columns([1, 1, 2, 1])
    columns[0].caption(f"User: {username}")
    columns[1].caption(f"Role: {role}")
    columns[2].caption(f"Scope: {scope or st.session_state.get('active_scope', 'All active datasets')}")
    columns[3].caption(f"Last backup: {backup_age}")


def _backup_age_label() -> str:
    """Return a lightweight backup freshness label without requiring backup support yet."""
    exports_dir = Path(Settings.EXPORTS_DIR)
    if not exports_dir.exists():
        return "not configured"

    backups = sorted(exports_dir.glob("*backup*"), key=lambda path: path.stat().st_mtime, reverse=True)
    if not backups:
        return "none"

    age_seconds = max(0, (datetime.now().timestamp() - backups[0].stat().st_mtime))
    age_days = int(age_seconds // 86400)
    if age_days == 0:
        return "today"
    if age_days == 1:
        return "1 day ago"
    return f"{age_days} days ago"


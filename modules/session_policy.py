"""Idle-session policy helpers for Streamlit authentication state.

The functions in this module are framework-light so timeout behavior can be
unit-tested without importing Streamlit or the database-backed auth module.
"""

from __future__ import annotations

import time
from collections.abc import MutableMapping
from typing import Any, Callable

LAST_ACTIVITY_KEY = "last_activity_at"


def _now(clock: Callable[[], float] | None = None) -> float:
    """Return the current epoch timestamp using an injectable clock."""
    return (clock or time.time)()


def mark_session_activity(
    session_state: MutableMapping[str, Any],
    *,
    clock: Callable[[], float] | None = None,
) -> float:
    """Record activity for the current authenticated session."""
    timestamp = _now(clock)
    session_state[LAST_ACTIVITY_KEY] = timestamp
    return timestamp


def session_has_expired(
    session_state: MutableMapping[str, Any],
    timeout_minutes: int,
    *,
    clock: Callable[[], float] | None = None,
) -> bool:
    """Return whether the session exceeded the configured idle timeout.

    A missing activity timestamp initializes the session instead of expiring it.
    Non-positive timeout values disable idle expiration explicitly.
    """
    if timeout_minutes <= 0:
        return False

    current_time = _now(clock)
    last_activity = session_state.get(LAST_ACTIVITY_KEY)
    if last_activity is None:
        session_state[LAST_ACTIVITY_KEY] = current_time
        return False

    try:
        elapsed_seconds = current_time - float(last_activity)
    except (TypeError, ValueError):
        session_state[LAST_ACTIVITY_KEY] = current_time
        return False

    return elapsed_seconds >= timeout_minutes * 60


def clear_session_activity(session_state: MutableMapping[str, Any]) -> None:
    """Remove idle-session metadata during logout or expiration."""
    session_state.pop(LAST_ACTIVITY_KEY, None)

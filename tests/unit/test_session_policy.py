from modules.session_policy import (
    LAST_ACTIVITY_KEY,
    clear_session_activity,
    mark_session_activity,
    session_has_expired,
)


def test_missing_activity_initializes_without_expiring():
    state = {}

    assert session_has_expired(state, 30, clock=lambda: 1000.0) is False
    assert state[LAST_ACTIVITY_KEY] == 1000.0


def test_session_expires_at_timeout_boundary():
    state = {LAST_ACTIVITY_KEY: 1000.0}

    assert session_has_expired(state, 1, clock=lambda: 1060.0) is True


def test_session_remains_active_before_timeout():
    state = {LAST_ACTIVITY_KEY: 1000.0}

    assert session_has_expired(state, 1, clock=lambda: 1059.9) is False


def test_disabled_timeout_never_expires():
    state = {LAST_ACTIVITY_KEY: 1000.0}

    assert session_has_expired(state, 0, clock=lambda: 999999.0) is False


def test_invalid_timestamp_is_repaired():
    state = {LAST_ACTIVITY_KEY: "not-a-timestamp"}

    assert session_has_expired(state, 10, clock=lambda: 2000.0) is False
    assert state[LAST_ACTIVITY_KEY] == 2000.0


def test_mark_and_clear_activity():
    state = {}

    assert mark_session_activity(state, clock=lambda: 1234.5) == 1234.5
    assert state[LAST_ACTIVITY_KEY] == 1234.5

    clear_session_activity(state)
    assert LAST_ACTIVITY_KEY not in state

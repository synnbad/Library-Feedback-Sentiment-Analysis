"""Idempotency helpers for user-triggered operations.

These helpers give Streamlit reruns and repeated clicks a durable place to
check whether an operation has already completed.
"""

from __future__ import annotations

import hashlib
import json
from typing import Any, Dict, Optional

from modules.database import ensure_idempotency_schema, execute_query, execute_update


def normalize_text(value: Any) -> str:
    """Normalize text for stable idempotency keys."""
    return " ".join(str(value or "").strip().lower().split())


def make_key(operation: str, *parts: Any) -> str:
    """Build a stable operation-scoped key."""
    payload = json.dumps(
        {
            "operation": normalize_text(operation),
            "parts": [_json_safe(part) for part in parts],
        },
        sort_keys=True,
        separators=(",", ":"),
        default=str,
    )
    digest = hashlib.sha256(payload.encode("utf-8")).hexdigest()
    return f"{operation}:{digest}"


def get_record(operation: str, idempotency_key: str) -> Optional[Dict[str, Any]]:
    """Return a stored idempotency record if it exists."""
    ensure_idempotency_schema()
    rows = execute_query(
        """
        SELECT operation, idempotency_key, status, result_json, error, created_at, updated_at
        FROM idempotency_keys
        WHERE operation = ? AND idempotency_key = ?
        """,
        (operation, idempotency_key),
    )
    return rows[0] if rows else None


def get_completed_result(operation: str, idempotency_key: str) -> Optional[Dict[str, Any]]:
    """Return the completed JSON result for an operation, if present."""
    record = get_record(operation, idempotency_key)
    if not record or record.get("status") != "completed" or not record.get("result_json"):
        return None
    result = json.loads(record["result_json"])
    if isinstance(result, dict):
        result["idempotency_reused"] = True
    return result


def start_operation(operation: str, idempotency_key: str) -> bool:
    """Record an in-progress operation.

    Returns True when this caller created the operation, False when a record
    already existed.
    """
    ensure_idempotency_schema()
    inserted_id = execute_update(
        """
        INSERT OR IGNORE INTO idempotency_keys (operation, idempotency_key, status)
        VALUES (?, ?, 'in_progress')
        """,
        (operation, idempotency_key),
    )
    return inserted_id != 0


def complete_operation(operation: str, idempotency_key: str, result: Dict[str, Any]) -> None:
    """Persist the successful result for future duplicate calls."""
    ensure_idempotency_schema()
    execute_update(
        """
        UPDATE idempotency_keys
        SET status = 'completed', result_json = ?, error = NULL, updated_at = CURRENT_TIMESTAMP
        WHERE operation = ? AND idempotency_key = ?
        """,
        (json.dumps(_json_safe(result), sort_keys=True, default=str), operation, idempotency_key),
    )


def fail_operation(operation: str, idempotency_key: str, error: str) -> None:
    """Persist a failed operation state."""
    ensure_idempotency_schema()
    execute_update(
        """
        UPDATE idempotency_keys
        SET status = 'failed', error = ?, updated_at = CURRENT_TIMESTAMP
        WHERE operation = ? AND idempotency_key = ?
        """,
        (str(error)[:1000], operation, idempotency_key),
    )


def _json_safe(value: Any) -> Any:
    """Convert common non-JSON values into stable JSON-safe structures."""
    if isinstance(value, dict):
        return {str(key): _json_safe(val) for key, val in sorted(value.items(), key=lambda item: str(item[0]))}
    if isinstance(value, set):
        return sorted(_json_safe(item) for item in value)
    if isinstance(value, (list, tuple)):
        return [_json_safe(item) for item in value]
    if isinstance(value, str):
        return normalize_text(value)
    if isinstance(value, (int, float, bool)) or value is None:
        return value
    return str(value)

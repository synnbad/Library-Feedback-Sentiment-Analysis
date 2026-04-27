import json

from modules import csv_handler


def test_get_datasets_returns_indexing_state(monkeypatch):
    captured = {}

    def fake_execute_query(query):
        captured["query"] = query
        return [
            {
                "id": 1,
                "name": "sample_usage_statistics",
                "dataset_type": "usage",
                "upload_date": "2026-04-27T10:00:00",
                "row_count": 10,
                "title": "Usage",
                "description": "Usage data",
                "source": "Local",
                "keywords": json.dumps(["usage"]),
                "usage_notes": "",
                "ethical_considerations": "",
                "analysis_capabilities": json.dumps(["trend"]),
                "indexing_status": "completed",
                "indexing_error": None,
                "indexed_at": "2026-04-27T10:05:00",
            }
        ]

    monkeypatch.setattr(csv_handler, "execute_query", fake_execute_query)

    datasets = csv_handler.get_datasets()

    assert "indexing_status" in captured["query"]
    assert "indexed_at" in captured["query"]
    assert datasets[0]["indexing_status"] == "completed"
    assert datasets[0]["indexed_at"] == "2026-04-27T10:05:00"
    assert datasets[0]["keywords"] == ["usage"]

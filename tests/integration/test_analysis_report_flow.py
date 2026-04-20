"""
Integration test for upload -> qualitative analysis -> report export.

This version reflects the current contract:
- strict CSV validation at the module API
- qualitative analysis requires at least Settings.MIN_RESPONSES_FOR_ANALYSIS rows
- report creation accepts include_viz/include_qualitative flags
"""

from io import StringIO
import os
import tempfile
from unittest.mock import patch

import pandas as pd
import pytest

from config.settings import Settings
from modules.csv_handler import validate_csv, parse_csv, store_dataset, delete_dataset
from modules.database import init_database
from modules.qualitative_analysis import analyze_dataset_sentiment, extract_themes
from modules.report_generator import generate_statistical_summary, create_report, export_report


@pytest.fixture
def isolated_db():
    """Point the application at a temporary SQLite database for this test."""
    fd, db_path = tempfile.mkstemp(suffix=".db")
    os.close(fd)

    original_db_path = Settings.DATABASE_PATH
    Settings.DATABASE_PATH = db_path
    init_database(db_path)

    try:
        yield db_path
    finally:
        Settings.DATABASE_PATH = original_db_path
        try:
            os.unlink(db_path)
        except OSError:
            pass


def test_analysis_report_flow(isolated_db):
    """Validate upload -> qualitative analysis -> report generation -> markdown export."""
    rows = [
        ("2024-01-01", "What works well?", "Great service and helpful staff."),
        ("2024-01-02", "What works well?", "Excellent library resources available."),
        ("2024-01-03", "What should improve?", "Could be better with more resources."),
        ("2024-01-04", "What works well?", "Helpful librarians and quiet spaces."),
        ("2024-01-05", "What should improve?", "Need more study rooms."),
        ("2024-01-06", "What works well?", "The library is welcoming and clean."),
        ("2024-01-07", "What should improve?", "Weekend hours are too short."),
        ("2024-01-08", "What works well?", "Staff are knowledgeable and kind."),
        ("2024-01-09", "What should improve?", "Computers could be faster."),
        ("2024-01-10", "What works well?", "Research support is excellent."),
    ]
    csv_lines = ["response_date,question,response_text"]
    csv_lines.extend([f'{date},"{question}","{response}"' for date, question, response in rows])
    csv_file = StringIO("\n".join(csv_lines))

    is_valid, message = validate_csv(csv_file, "survey")
    assert is_valid, f"CSV validation failed: {message}"

    csv_file.seek(0)
    df = parse_csv(csv_file)
    assert isinstance(df, pd.DataFrame)
    assert len(df) == 10

    dataset_id = store_dataset(
        df,
        "test_analysis_survey",
        "survey",
        "test_analysis_report_hash",
        {
            "title": "Test Analysis Survey",
            "description": "Integration test data",
            "source": "pytest",
        },
    )

    try:
        sentiment_results = analyze_dataset_sentiment(dataset_id)
        assert sentiment_results is not None
        assert "distribution" in sentiment_results
        assert sentiment_results["processed_responses"] == 10

        theme_results = extract_themes(dataset_id, n_themes=2)
        assert theme_results is not None
        assert len(theme_results["themes"]) > 0

        stats = generate_statistical_summary(dataset_id)
        assert stats is not None
        assert stats["row_count"] == 10
        assert stats["dataset_type"] == "survey"

        with patch("modules.report_generator.generate_narrative") as mock_narrative:
            mock_narrative.return_value = (
                "Test narrative: the survey reflects broadly positive feedback with clear improvement themes."
            )

            report = create_report(
                dataset_ids=[dataset_id],
                include_viz=False,
                include_qualitative=True,
            )

        report["title"] = "Test Integration Report"

        assert report is not None
        assert report["title"] == "Test Integration Report"
        assert "metadata" in report
        assert "qualitative_analysis" in report

        report_bytes, actual_format = export_report(report, format="markdown")
        assert report_bytes is not None
        assert len(report_bytes) > 0
        assert actual_format == "markdown"

        report_text = report_bytes.decode("utf-8")
        assert "Test Integration Report" in report_text
        assert "sentiment" in report_text.lower() or "analysis" in report_text.lower()
    finally:
        delete_dataset(dataset_id)

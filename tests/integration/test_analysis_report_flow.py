"""
Integration test for analysis and report generation flow.
Tests: CSV upload → qualitative analysis → report generation → export
Mocks Ollama to avoid delays.
"""
import pytest
import pandas as pd
from io import StringIO
from unittest.mock import patch
from modules.csv_handler import validate_csv, parse_csv, store_dataset
from modules.qualitative_analysis import analyze_dataset_sentiment, extract_themes
from modules.report_generator import generate_statistical_summary, create_report, export_report


def test_analysis_report_flow():
    """Test complete flow from upload to report export."""
    
    # Step 1: Create and validate CSV data
    csv_content = """response_text,date
Great service and helpful staff!,2024-01-15
Could be better with more resources,2024-01-16
Excellent library resources available,2024-01-17"""
    
    csv_file = StringIO(csv_content)
    is_valid, message = validate_csv(csv_file, "survey")
    assert is_valid, f"CSV validation failed: {message}"
    
    # Step 2: Parse and store dataset
    csv_file.seek(0)
    df = parse_csv(csv_file)
    assert df is not None
    assert len(df) == 3
    
    dataset_id = store_dataset(
        name="test_analysis_survey",
        dataset_type="survey",
        dataframe=df,
        metadata={
            "title": "Test Analysis Survey",
            "description": "Integration test data"
        }
    )
    assert dataset_id is not None
    
    # Step 3: Run qualitative analysis
    sentiment_results = analyze_dataset_sentiment(dataset_id)
    assert sentiment_results is not None
    assert "sentiment_distribution" in sentiment_results
    
    themes = extract_themes(dataset_id, num_themes=2)
    assert themes is not None
    
    # Step 4: Generate statistical summary
    stats = generate_statistical_summary(dataset_id)
    assert stats is not None
    assert "total_responses" in stats
    
    # Step 5: Create report (mock Ollama to avoid delays)
    with patch('modules.report_generator.generate_narrative') as mock_narrative:
        mock_narrative.return_value = "Test narrative: The survey shows positive sentiment."
        
        report = create_report(
            dataset_ids=[dataset_id],
            title="Test Integration Report",
            include_visualizations=False
        )
    
    assert report is not None
    assert "title" in report
    assert "datasets" in report
    
    # Step 6: Export report to markdown
    report_bytes, filename = export_report(report, format="markdown")
    assert report_bytes is not None
    assert len(report_bytes) > 0
    assert filename.endswith(".md")
    
    # Verify report content
    report_text = report_bytes.decode('utf-8')
    assert "Test Integration Report" in report_text
    assert "sentiment" in report_text.lower() or "analysis" in report_text.lower()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

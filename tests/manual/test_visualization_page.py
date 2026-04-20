"""
Manual and lightweight automated checks for the Visualization page.

Run the automated portion with pytest. To verify the Streamlit UI manually:
1. Start the app with `streamlit run streamlit_app.py`.
2. Log in.
3. Upload or select a dataset with at least one categorical and one numeric column.
4. Navigate to Visualizations.
5. Generate bar, line, and pie charts.
6. Export charts as HTML and PNG.
7. Confirm errors are clear for invalid column combinations.
"""

import sys
from pathlib import Path

import pandas as pd


project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from modules import visualization  # noqa: E402


def test_visualization_functions():
    """Smoke-test visualization module functions directly."""
    bar_data = pd.DataFrame({
        "Category": ["A", "B", "C", "D"],
        "Value": [10, 25, 15, 30],
    })
    line_data = pd.DataFrame({
        "Date": ["2024-01", "2024-02", "2024-03", "2024-04"],
        "Count": [100, 150, 120, 180],
    })
    pie_data = pd.DataFrame({
        "Type": ["Fiction", "Non-Fiction", "Reference", "Periodicals"],
        "Checkouts": [450, 320, 180, 250],
    })

    bar_fig = visualization.create_bar_chart(
        bar_data,
        x="Category",
        y="Value",
        title="Test Bar Chart",
        x_label="Categories",
        y_label="Values",
    )
    assert len(bar_fig.data) > 0

    line_fig = visualization.create_line_chart(
        line_data,
        x="Date",
        y="Count",
        title="Test Line Chart",
        x_label="Time Period",
        y_label="Count",
    )
    assert len(line_fig.data) > 0

    pie_fig = visualization.create_pie_chart(
        pie_data,
        values="Checkouts",
        names="Type",
        title="Test Pie Chart",
    )
    assert len(pie_fig.data) > 0

    html_bytes = visualization.export_chart(bar_fig, "test_chart", format="html")
    assert len(html_bytes) > 0
    assert "<html>" in html_bytes.decode("utf-8").lower()

    png_bytes = visualization.export_chart(bar_fig, "test_chart", format="png")
    assert len(png_bytes) > 0
    assert png_bytes[:4] == b"\x89PNG" or b"<html>" in png_bytes.lower()


if __name__ == "__main__":
    test_visualization_functions()
    print("Automated visualization checks passed.")
    print("Follow the module docstring instructions for manual Streamlit UI verification.")

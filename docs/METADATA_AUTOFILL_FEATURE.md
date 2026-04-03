# Metadata Auto-Fill Feature

## Overview

The metadata auto-fill feature automatically detects and populates FAIR/CARE metadata fields based on the uploaded dataset's characteristics, saving time and ensuring consistent metadata quality.

## How It Works

When you upload a CSV file, click the "Auto-Fill Metadata" button to automatically populate:

- **Title**: Generated from filename (cleaned and formatted)
- **Description**: Includes dataset statistics, content type, and date range
- **Source**: Detected from filename patterns (Qualtrics, ILS, Google Forms, etc.)
- **Keywords**: Auto-generated from column names and dataset type

## Auto-Detection Logic

### Title Generation
- Removes `.csv` extension
- Replaces underscores and hyphens with spaces
- Applies title case formatting
- Example: `library_feedback_spring_2024.csv` → "Library Feedback Spring 2024"

### Description Generation
Includes:
- Dataset type and record count
- Number of fields
- Content indicators (feedback, ratings, visits, etc.)
- Date range (if date columns detected)

Example: "Survey dataset with 150 records and 8 fields. Contains textual feedback responses. Includes rating/score data. Date range: 2024-01-15 to 2024-03-20."

### Source Detection
Automatically identifies source from filename:
- `qualtrics` → "Qualtrics Survey"
- `google` → "Google Forms"
- `ils`, `alma`, `sierra` → "Integrated Library System (ILS)"
- Default → "CSV Upload"

### Keyword Generation
Auto-generates keywords from:
- Dataset type (survey, usage, circulation)
- Column name analysis:
  - `feedback`, `comment`, `response` → "feedback"
  - `rating`, `score`, `satisfaction` → "ratings"
  - `student`, `undergraduate`, `graduate` → "students"
  - `faculty`, `staff` → "faculty-staff"
  - `visit`, `session` → "visits"
  - `checkout`, `borrow` → "circulation"
  - `book`, `material`, `item` → "materials"
- Current year (if detected in data)

## Usage

1. Upload a CSV file
2. Select dataset type
3. Click "Auto-Fill Metadata" button
4. Review and edit auto-generated fields as needed
5. Add usage notes and ethical considerations manually
6. Click "Upload Dataset"

## Benefits

- **Time Savings**: Reduces manual data entry
- **Consistency**: Ensures standardized metadata format
- **Accuracy**: Extracts actual characteristics from data
- **FAIR Compliance**: Supports Findability with rich metadata
- **Flexibility**: All fields remain editable after auto-fill

## Examples

### Survey Data
```
Filename: library_feedback_spring_2024.csv
Auto-filled:
- Title: Library Feedback Spring 2024
- Description: Survey dataset with 150 records and 8 fields. Contains textual feedback responses. Includes rating/score data. Date range: 2024-01-15 to 2024-03-20.
- Source: CSV Upload
- Keywords: survey, feedback, ratings, 2024
```

### ILS Circulation Data
```
Filename: alma_circulation_feb2024.csv
Auto-filled:
- Title: Alma Circulation Feb2024
- Description: Circulation dataset with 1,250 records and 6 fields. Contains circulation and borrowing data. Date range: 2024-02-01 to 2024-02-29.
- Source: Integrated Library System (ILS)
- Keywords: circulation, materials
```

### Qualtrics Survey
```
Filename: qualtrics_student_survey.csv
Auto-filled:
- Title: Qualtrics Student Survey
- Description: Survey dataset with 320 records and 12 fields. Date range: 2024-04-01 to 2024-04-15.
- Source: Qualtrics Survey
- Keywords: survey, feedback, ratings, students
```

## Technical Implementation

The auto-fill feature is implemented in `modules/csv_handler.py` as the `auto_detect_metadata()` function, which:

1. Parses the uploaded DataFrame
2. Analyzes column names and data types
3. Detects date ranges
4. Generates descriptive metadata
5. Returns a dictionary of metadata fields

The Streamlit UI stores auto-filled values in session state, allowing users to review and modify before final upload.

## Future Enhancements

Potential improvements:
- Machine learning-based content classification
- Automatic PII detection warnings
- Suggested ethical considerations based on data type
- Integration with institutional metadata standards
- Bulk metadata editing for multiple datasets

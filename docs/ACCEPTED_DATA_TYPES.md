# What Data Can the System Accept?

## Quick Answer

The system accepts **any CSV file** with tabular data. There are very few restrictions.

## ✓ What IS Accepted

### File Format
- **CSV files only** (.csv extension)
- Any CSV encoding (UTF-8, Latin-1, CP1252, UTF-16, etc.)
- Files up to 200MB in size
- Any number of columns
- Any column names
- Any column order

### Data Types

#### 1. Survey & Feedback Data
**Any data with text responses, comments, or feedback**

Examples:
- Patron satisfaction surveys
- LibQUAL+ data
- Comment cards
- Feedback forms
- Qualtrics exports
- Google Forms exports
- SurveyMonkey data
- Course evaluations
- Program feedback
- Service quality surveys
- Exit interviews
- Focus group transcripts (if in CSV)

**What works:**
- Open-ended text responses
- Rating scales (1-5, 1-10, etc.)
- Multiple choice responses
- Likert scales
- Yes/No questions
- Demographic data
- Timestamps
- Any combination of the above

#### 2. Usage & Statistics Data
**Any quantitative metrics or measurements**

Examples:
- Gate counts / door counts
- Website analytics
- Database usage statistics
- Computer/laptop usage logs
- WiFi connection data
- Room booking statistics
- Study room usage
- Equipment checkout data
- Digital resource usage
- Interlibrary loan statistics
- Reference transaction counts
- Instruction session attendance
- Program attendance
- Public Library Statistics (PLS)
- Academic library statistics (ACRL)
- COUNTER reports
- Google Analytics exports
- LibInsight data

**What works:**
- Time-series data
- Aggregated statistics
- Raw transaction logs
- Hourly/daily/monthly summaries
- Multiple metrics per row
- Categorical breakdowns

#### 3. Circulation Data
**Any data about materials borrowed or used**

Examples:
- ILS exports (Alma, Sierra, Koha, Evergreen, etc.)
- Checkout records
- Renewal records
- Hold/request data
- Return data
- Overdue items
- Lost/damaged items
- Material usage by type
- Collection usage statistics
- E-book checkouts
- Streaming media usage
- Reserve materials usage

**What works:**
- Individual transaction records
- Aggregated circulation statistics
- Material-level data
- Patron-level data (anonymized)
- Time-based circulation data
- Collection analysis data

### Column Types Accepted

#### Text Columns
- Short text (names, categories, IDs)
- Long text (comments, feedback, descriptions)
- Special characters (é, ñ, ü, etc.)
- Emojis (😊, 👍, etc.)
- URLs
- Email addresses (will be detected and can be redacted)
- Phone numbers (will be detected and can be redacted)

#### Numeric Columns
- Integers (1, 2, 3, 100, 1000)
- Decimals (3.14, 99.99, 0.5)
- Percentages (stored as numbers)
- Currency values (stored as numbers)
- Negative numbers
- Zero values
- Scientific notation

#### Date/Time Columns
- Standard dates (2024-01-15, 01/15/2024, 15-Jan-2024)
- Timestamps (2024-01-15 10:30:00)
- ISO 8601 format (2024-01-15T10:30:00Z)
- Month/Year only (2024-01, January 2024)
- Year only (2024)
- Relative dates (if parseable)

#### Categorical Columns
- User types (student, faculty, staff, public)
- Material types (book, DVD, journal, database)
- Locations (Main Library, Branch A, Online)
- Departments
- Programs
- Services
- Any classification or grouping

#### Mixed Columns
- Columns with multiple data types
- Columns with missing values (NaN, blank, null)
- Columns with inconsistent formatting

## ✗ What is NOT Accepted

### File Format Restrictions

#### 1. Non-CSV Formats
**Not accepted:**
- Excel files (.xlsx, .xls) - Must export to CSV first
- JSON files - Must convert to CSV first
- XML files - Must convert to CSV first
- PDF files - Must extract data to CSV first
- Word documents - Must convert to CSV first
- Text files (.txt) - Unless they're actually CSV format
- Database dumps - Must export to CSV first
- Binary formats

**Solution:** Export your data to CSV format from the source application

#### 2. Compressed Files
**Not accepted:**
- ZIP files (.zip)
- GZIP files (.gz)
- TAR files (.tar)
- RAR files (.rar)

**Solution:** Extract the CSV file before uploading

### Data Structure Restrictions

#### 1. Empty Files
**Not accepted:**
- Completely empty files
- Files with only headers (no data rows)
- Files with all blank/null values

**Why:** Nothing to analyze

**Solution:** Ensure file contains at least one row of actual data

#### 2. Completely Empty Columns
**Not accepted:**
- Columns where every single value is blank/null/NaN

**Why:** Empty columns provide no information

**Solution:** Remove completely empty columns before upload, or ensure they contain some data

#### 3. Malformed CSV
**Not accepted:**
- Files with inconsistent number of columns per row
- Files with unmatched quotes
- Files with invalid delimiters
- Corrupted files

**Why:** Cannot be parsed reliably

**Solution:** 
- Open in Excel/Google Sheets and re-save as CSV
- Use a CSV validator tool
- Check for formatting issues

### Size Restrictions

#### File Size Limit
**Maximum:** 200MB per file

**Why:** Performance and memory constraints

**Solution for larger files:**
- Split into multiple files by time period
- Upload as separate datasets
- Aggregate data before upload
- Remove unnecessary columns

**Typical file sizes:**
- 1,000 rows: ~100KB
- 10,000 rows: ~1MB
- 100,000 rows: ~10MB
- 1,000,000 rows: ~100MB

Most library datasets are well under the limit.

## Special Cases

### 1. Files with PII (Personally Identifiable Information)

**Accepted, but with caution:**
- Files containing names
- Files containing email addresses
- Files containing phone numbers
- Files containing student IDs

**What happens:**
- System detects PII automatically
- PII can be redacted before analysis
- You're warned about PII presence
- You control whether to redact or keep

**Best practice:** Anonymize data before upload when possible

### 2. Files with Special Characters

**Fully accepted:**
- International characters (café, naïve, résumé)
- Accented characters (é, ñ, ü, ö, å)
- Non-Latin scripts (if in UTF-8)
- Emojis and symbols

**System handles automatically:**
- Tries multiple encodings
- Preserves special characters
- Works with most character sets

### 3. Files with Inconsistent Data

**Accepted:**
- Some rows have values, others don't (sparse data)
- Different date formats in same column
- Mixed data types in same column
- Typos and variations

**What happens:**
- System handles missing values gracefully
- Attempts to parse dates flexibly
- Works with data as-is
- Analysis adapts to data quality

### 4. Very Wide Files (Many Columns)

**Accepted:**
- Files with 50+ columns
- Files with 100+ columns
- Files with 500+ columns

**Considerations:**
- All columns are stored
- Analysis focuses on relevant columns
- Visualizations may need column selection
- Performance may vary with extremely wide files

### 5. Very Long Files (Many Rows)

**Accepted:**
- Files with 10,000+ rows
- Files with 100,000+ rows
- Files with 1,000,000+ rows (if under 200MB)

**Considerations:**
- Processing time increases with size
- Sentiment analysis may take longer
- All features still work
- Consider sampling for very large datasets

## Data Quality Recommendations

### For Best Results

#### ✓ Do:
- Include column headers (first row)
- Use descriptive column names
- Include date information when available
- Remove completely empty columns
- Save as UTF-8 encoding when possible
- Keep file under 200MB
- Include relevant metadata

#### ✗ Avoid:
- Merged cells (Excel feature - doesn't work in CSV)
- Multiple header rows
- Summary rows mixed with data
- Formulas (export values only)
- Formatting (colors, fonts - lost in CSV)
- Charts/images (not supported in CSV)

### Data Preparation Tips

#### From Excel:
1. Remove any merged cells
2. Ensure first row is headers
3. Remove any summary rows
4. File → Save As → CSV UTF-8

#### From Google Sheets:
1. File → Download → CSV
2. Automatically uses UTF-8
3. One sheet at a time

#### From ILS/Database:
1. Use built-in CSV export
2. Include column headers
3. Export data (not formatted reports)

#### From Survey Platforms:
1. Export as CSV (not Excel)
2. Include all response data
3. Keep original column names

## What Happens After Upload?

### Automatic Processing

1. **Encoding Detection**: System tries multiple encodings
2. **Validation**: Checks file is valid CSV with data
3. **Storage**: Stores data in database
4. **PII Detection**: Scans for personally identifiable information
5. **Metadata Generation**: Can auto-fill metadata from file

### Available Analysis

Once uploaded, you can:
- **Query**: Ask questions in natural language
- **Analyze**: Run qualitative and quantitative analysis
- **Visualize**: Create charts and graphs
- **Report**: Generate comprehensive reports
- **Export**: Download results in various formats

### System Adapts To Your Data

- Detects column types automatically
- Finds date columns
- Identifies text vs. numeric columns
- Handles missing values
- Works with your actual column names

## Summary

### Simple Rules

✓ **YES**: Any CSV file with data  
✗ **NO**: Empty files, non-CSV formats, files over 200MB

### When in Doubt

If you can open it in Excel or Google Sheets and it looks like a table with rows and columns, it will probably work!

### Still Unsure?

Try uploading! The system will:
- Validate the file
- Show clear error messages if there's a problem
- Suggest solutions if validation fails
- Accept the file if it's valid

The validation is designed to be helpful, not restrictive.

## Examples of Real-World Data That Works

✓ Public Library Statistics (PLS) - All fields  
✓ Academic Library Statistics (ACRL) - All surveys  
✓ COUNTER reports - All versions  
✓ Qualtrics exports - All question types  
✓ LibQUAL+ data - Complete exports  
✓ ILS circulation exports - Any system  
✓ Google Analytics - CSV exports  
✓ LibInsight data - All report types  
✓ Gate count logs - Any format  
✓ Database usage statistics - Any vendor  
✓ Survey responses - Any platform  
✓ Feedback forms - Any structure  

If it's library data in CSV format, it works!

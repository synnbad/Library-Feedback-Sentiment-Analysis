# Data Requirements - Quick Reference

## ✓ What Works

### File Format
- **CSV files only** (.csv)
- Up to 200MB
- Any encoding (UTF-8, Latin-1, CP1252, etc.)

### Data Structure
- Any column names
- Any number of columns
- Any column order
- At least 1 row of data
- Column headers in first row

### Content Types
- **Survey data**: Feedback, responses, comments, ratings
- **Usage data**: Statistics, metrics, counts, analytics
- **Circulation data**: Checkouts, borrowing, material usage

### Column Types
- Text (short or long)
- Numbers (integers or decimals)
- Dates (any standard format)
- Categories (user types, locations, etc.)
- Mixed types
- Missing values (blanks are OK)

## ✗ What Doesn't Work

### File Format Issues
- Excel files (.xlsx, .xls) → Export to CSV first
- JSON, XML, PDF → Convert to CSV first
- Compressed files (.zip, .gz) → Extract first
- Files over 200MB → Split into smaller files

### Data Issues
- Completely empty files → Add data
- Only headers, no data → Add at least 1 row
- All columns completely empty → Remove empty columns
- Malformed CSV (inconsistent columns) → Fix formatting

## Common Data Sources That Work

✓ Qualtrics exports  
✓ Google Forms  
✓ ILS exports (Alma, Sierra, Koha, etc.)  
✓ Public Library Statistics (PLS)  
✓ ACRL statistics  
✓ COUNTER reports  
✓ LibQUAL+ data  
✓ Google Analytics (CSV export)  
✓ LibInsight data  
✓ Gate count logs  
✓ Database usage reports  
✓ Any custom CSV  

## Quick Checklist

Before uploading, verify:
- [ ] File is .csv format
- [ ] File size under 200MB
- [ ] First row has column headers
- [ ] At least one row of data
- [ ] Not all columns are empty

If all checked, your file will work!

## Need More Details?

See `ACCEPTED_DATA_TYPES.md` for comprehensive information.

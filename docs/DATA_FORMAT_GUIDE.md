# Data Format Guide

## Overview

The Library Assessment System is designed to be **flexible** and accept real-world library data in various formats. You don't need to restructure your data to match specific column names - the system adapts to your data structure.

## Supported Dataset Types

### 1. Survey Data

**What it is:** Any data containing patron feedback, responses, comments, or survey results.

**Accepted formats:**
- Qualtrics exports
- Google Forms exports
- LibQUAL+ data
- Custom survey data
- Feedback forms
- Comment cards

**Column flexibility:**
- ✓ Any column names are accepted
- ✓ Any number of columns
- ✓ No required column structure

**Common column patterns** (examples - not required):
- Date columns: `date`, `response_date`, `timestamp`, `StartDate`, `EndDate`
- Response columns: `feedback`, `comment`, `response`, `answer`, `Q1`, `Q2`, etc.
- Rating columns: `rating`, `score`, `satisfaction`, `rating_1`, `rating_2`
- Demographic columns: `user_type`, `status`, `department`, `role`

**Example 1: Qualtrics Export**
```csv
ResponseID,StartDate,EndDate,Q1_satisfaction,Q2_comments,Q3_rating
R_1,2024-01-15 10:30,2024-01-15 10:35,Very Satisfied,Great service!,5
R_2,2024-01-16 14:20,2024-01-16 14:25,Satisfied,Good resources,4
```

**Example 2: Simple Feedback Form**
```csv
date,name,feedback,rating
2024-01-15,Anonymous,Love the new study spaces,5
2024-01-16,Anonymous,Need more computers,3
```

**Example 3: LibQUAL+ Style**
```csv
ID,Date,Dimension,MinScore,PerceivedScore,DesiredScore,Comments
1,2024-01-15,Affect of Service,6,7,8,Staff very helpful
2,2024-01-16,Library as Place,5,6,9,Need more seating
```

### 2. Usage Data

**What it is:** Statistics about library usage, visits, sessions, or activity metrics.

**Accepted formats:**
- Gate count data
- Website analytics
- Database usage statistics
- Room booking data
- Computer usage logs
- Any time-series metrics

**Column flexibility:**
- ✓ Any column names are accepted
- ✓ Any metrics or measurements
- ✓ No required structure

**Common column patterns** (examples - not required):
- Date columns: `date`, `month`, `year`, `timestamp`, `period`
- Metric columns: `visits`, `sessions`, `users`, `checkouts`, `downloads`
- Category columns: `location`, `service`, `resource_type`, `user_type`

**Example 1: Gate Counts**
```csv
date,location,entries,exits,total_visits
2024-01-15,Main Library,450,445,450
2024-01-15,Science Library,230,228,230
```

**Example 2: Database Usage**
```csv
month,database_name,searches,sessions,downloads
2024-01,JSTOR,1250,890,340
2024-01,PubMed,2100,1450,680
```

**Example 3: Room Bookings**
```csv
date,room,bookings,hours_used,user_type
2024-01-15,Study Room A,8,24,undergraduate
2024-01-15,Study Room B,6,18,graduate
```

### 3. Circulation Data

**What it is:** Data about materials borrowed, checked out, or circulated.

**Accepted formats:**
- ILS exports (Alma, Sierra, Koha, etc.)
- Checkout records
- Holds/requests data
- Renewals data
- Material usage statistics

**Column flexibility:**
- ✓ Any column names are accepted
- ✓ Any ILS export format
- ✓ No required structure

**Common column patterns** (examples - not required):
- Date columns: `checkout_date`, `due_date`, `return_date`, `date`
- Material columns: `title`, `call_number`, `material_type`, `format`, `item_type`
- Patron columns: `patron_type`, `user_group`, `borrower_type`, `status`
- Transaction columns: `checkouts`, `renewals`, `holds`, `requests`

**Example 1: ILS Export**
```csv
checkout_date,title,call_number,material_type,patron_group,due_date
2024-01-15,Introduction to Python,QA76.73,Book,Undergraduate,2024-02-15
2024-01-15,Data Science Handbook,Q325,Book,Graduate,2024-02-15
```

**Example 2: Circulation Summary**
```csv
month,material_type,checkouts,renewals,patron_type
2024-01,Books,1250,340,Undergraduate
2024-01,DVDs,89,12,Faculty
```

**Example 3: Public Library Statistics (PLS)**
```csv
FSCSKEY,LIBNAME,TOTCIR,KIDCIRCL,ELMATCIR,PHYSCIR,TOTVISIT
AK0001,Anchorage Public Library,1250000,450000,89000,711000,890000
AK0002,Juneau Public Library,234000,89000,12000,133000,156000
```

## Key Points

### ✓ What IS Required

1. **Valid CSV format**: File must be a properly formatted CSV
2. **At least one row of data**: File cannot be empty
3. **Column headers**: First row should contain column names
4. **Some data**: Columns cannot be completely empty

### ✗ What is NOT Required

1. **Specific column names**: Use whatever names your system exports
2. **Specific column order**: Columns can be in any order
3. **Specific number of columns**: Have as many or as few as you need
4. **Data transformation**: No need to restructure your data

## Real-World Examples

### Example: Public Library Survey (PLS) Data

Your file `PLS_FY23_AE_pud23i.csv` is a perfect example of real-world data. It likely contains:
- Library identifiers (FSCSKEY, LIBNAME, etc.)
- Service metrics (circulation, visits, programs, etc.)
- Collection data (physical, electronic materials)
- Staffing information
- Financial data

**This data is fully supported!** Just select the appropriate dataset type:
- If it contains survey responses → Select "survey"
- If it contains usage statistics → Select "usage"  
- If it contains circulation data → Select "circulation"

The system will adapt to your column structure automatically.

## Tips for Best Results

### 1. Choose the Right Dataset Type

Match your data to the closest category:
- **Survey**: Anything with feedback, responses, or comments
- **Usage**: Metrics, statistics, counts, or measurements over time
- **Circulation**: Checkout records, borrowing data, or material usage

### 2. Include Date Information

If your data has dates, include them! The system can:
- Auto-detect date ranges for metadata
- Enable time-series analysis
- Support trend analysis

### 3. Use Descriptive Column Names

While not required, descriptive column names help:
- Auto-fill metadata works better
- Analysis results are more readable
- Visualizations have better labels

### 4. Keep Your Original Format

Don't restructure your data! The system is designed to work with:
- ILS exports as-is
- Survey platform exports as-is
- Analytics reports as-is
- Statistical summaries as-is

## What Happens After Upload?

1. **Validation**: System checks that file is valid CSV with data
2. **Storage**: Data is stored in the database
3. **Analysis**: You can run qualitative and quantitative analysis
4. **Querying**: Use natural language to query your data
5. **Visualization**: Create charts and graphs
6. **Reporting**: Generate comprehensive reports

The system adapts its analysis based on your actual column structure.

## Troubleshooting

### "Missing required columns" Error

**Old behavior** (before this update): System required specific column names
**New behavior** (current): System accepts any column structure

If you see this error:
1. Make sure you're using the latest version
2. The file should validate successfully now
3. If it still fails, check that:
   - File is not empty
   - File has column headers
   - Columns contain some data

### "Invalid CSV format" Error

This means the file structure itself is invalid:
- Check that it's actually a CSV file
- Ensure rows have consistent number of columns
- Verify there are no formatting issues

### Encoding Issues

If you see encoding errors:
- System automatically tries multiple encodings
- For best results, save as UTF-8
- See `ENCODING_FIX_SUMMARY.md` for details

## Need Help?

If you're unsure which dataset type to choose:
1. **Survey**: Does it have text responses or feedback? → Survey
2. **Usage**: Does it have counts, metrics, or statistics? → Usage
3. **Circulation**: Does it have checkout or borrowing data? → Circulation

When in doubt, choose the type that best describes the primary purpose of the data. The system will work with any of them!

## Summary

The Library Assessment System is designed to work with **your data as it is**. No restructuring, no column renaming, no data transformation required. Just upload your CSV and start analyzing!

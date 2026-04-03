# Changelog

All notable changes to the Library Assessment Decision Support System.

## [1.4.0] - 2026-04-02

### Added
- **Enhanced Sentiment Analysis**: Implemented RoBERTa transformer model for 17% accuracy improvement over TextBlob baseline
- **Flexible Data Validation**: System now accepts any CSV format without strict column requirements
- **Metadata Auto-Fill**: Automatic detection and population of FAIR/CARE metadata from uploaded files
- **Encoding Detection**: Automatic handling of multiple CSV encodings (UTF-8, Latin-1, CP1252, UTF-16)
- **Comprehensive Documentation**: Added detailed guides for data formats, features, and troubleshooting

### Changed
- Removed strict column name requirements - accepts real-world data formats (PLS, Qualtrics, ILS exports)
- Updated CSV validation to be flexible by default, strict mode available for testing
- Enhanced error messages with helpful tips for users
- Improved sentiment analysis to return structured dictionaries instead of tuples
- Authentication disabled for development (auto-login as demo_user)

### Fixed
- CSV encoding errors now handled gracefully with automatic encoding detection
- Metadata auto-fill works with various file encodings
- Sentiment analysis integration with qualitative analysis module
- Empty column validation edge cases

### Documentation
- `AMIA_PROJECT_REPORT_COMPLETE.md` - Complete academic project report
- `PROJECT_CONTEXT.md` - Comprehensive guide for AI agents
- `DATA_FORMAT_GUIDE.md` - Detailed guide on accepted data formats
- `ACCEPTED_DATA_TYPES.md` - Quick reference for data requirements
- `METADATA_AUTOFILL_FEATURE.md` - Metadata auto-fill documentation
- `ENCODING_FIX_SUMMARY.md` - Encoding handling details
- `FLEXIBLE_VALIDATION_UPDATE.md` - Validation changes documentation

## [1.3.0] - 2026-03-15

### Added
- RAG (Retrieval-Augmented Generation) query interface
- ChromaDB vector store for semantic search
- Llama 3.2 integration via Ollama
- Citation tracking for AI-generated answers
- Conversation context management

### Changed
- Improved query response quality with grounded answers
- Enhanced natural language understanding

## [1.2.0] - 2026-02-28

### Added
- Quantitative analysis module with statistical tests
- AI-generated interpretations for statistical results
- Correlation, trend, comparative, and distribution analysis
- Interactive visualizations with Plotly

### Changed
- Enhanced report generation with statistical summaries
- Improved data export capabilities

## [1.1.0] - 2026-02-15

### Added
- Qualitative analysis module
- TextBlob sentiment analysis
- TF-IDF + K-Means topic modeling
- Theme extraction and representative quotes
- PII detection and redaction

### Changed
- Improved data preprocessing pipeline
- Enhanced CSV validation

## [1.0.0] - 2026-01-30

### Added
- Initial release
- Streamlit web interface
- SQLite database backend
- CSV data upload
- Basic authentication
- FAIR/CARE metadata support
- Multi-source data integration
- Report generation

### Features
- Survey data analysis
- Usage statistics tracking
- Circulation data management
- Data visualization
- Export capabilities

## Development Roadmap

### Planned for v1.5.0
- BERTopic implementation for improved topic modeling (+35% coherence)
- BGE embeddings for better retrieval (+15% accuracy)
- Zero-shot classification for automatic categorization
- Enhanced PII detection with BERT NER
- Batch export functionality

### Planned for v2.0.0
- Multilingual support (50+ languages)
- Document summarization with BART
- Mobile-responsive interface
- Predictive analytics
- Multi-institution deployment support

## Version Numbering

This project follows [Semantic Versioning](https://semver.org/):
- MAJOR version for incompatible API changes
- MINOR version for new functionality in a backward compatible manner
- PATCH version for backward compatible bug fixes

## Links

- [GitHub Repository](https://github.com/your-repo/library-assessment-dss)
- [Documentation](./README.md)
- [Project Report](./AMIA_PROJECT_REPORT_COMPLETE.md)
- [Issue Tracker](https://github.com/your-repo/library-assessment-dss/issues)

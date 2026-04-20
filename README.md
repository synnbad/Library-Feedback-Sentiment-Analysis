# Library Assessment Decision Support System

Local-first Streamlit app for library assessment data. It lets library staff upload CSV data, analyze survey/usage/circulation patterns, ask natural-language questions with citations, and export reports.

All core AI processing is designed to run locally with SQLite, ChromaDB, sentence-transformers, TextBlob, and Ollama.

## What It Does

- Upload and validate survey, usage, and circulation CSV files.
- Store data locally in SQLite with provenance metadata.
- Query uploaded data with a local RAG pipeline using ChromaDB and Ollama.
- Run qualitative analysis: sentiment, themes, representative quotes.
- Run quantitative analysis: summaries, trends, comparisons, distributions.
- Create visualizations and Markdown/PDF reports.
- Detect and redact PII in retrieved context and generated answers.
- Require login by default, with optional demo login for development.

## Requirements

- Python 3.10+
- Ollama
- Local model: `llama3.2:3b`
- Recommended RAM: 16 GB+

## Quick Start

```bash
git clone https://github.com/synnbad/Library-Feedback-Sentiment-Analysis.git
cd Library-Feedback-Sentiment-Analysis

python -m venv .venv
.venv\Scripts\activate

pip install -r requirements.txt
python -m textblob.download_corpora
ollama pull llama3.2:3b
python scripts/init_app.py
streamlit run streamlit_app.py
```

Default login:

```text
username: admin
password: admin123
```

Change the default password before using real data.

## Configuration

Copy `.env.example` if you want local overrides. Important defaults:

```env
DATABASE_PATH=data/library.db
CHROMA_DB_PATH=data/chroma_db
OLLAMA_URL=http://localhost:11434
OLLAMA_MODEL=llama3.2:3b
EMBEDDING_MODEL=all-MiniLM-L6-v2
EMBEDDING_LOCAL_FILES_ONLY=true
LLM_GENERATION_TIMEOUT_SECONDS=90
ENABLE_DEMO_LOGIN=false
```

`EMBEDDING_LOCAL_FILES_ONLY=true` keeps embedding model loading local-first and avoids runtime Hugging Face network calls.

## CSV Inputs

Supported dataset types:

- Survey: `response_date`, `question`, `response_text`
- Usage: `date`, `metric_name`, `metric_value`
- Circulation: `checkout_date`, `material_type`, `patron_type`

The upload UI supports flexible column mapping, but these canonical columns are the safest path.

## Main Files

- `streamlit_app.py`: app entry point and navigation
- `ui/`: Streamlit pages
- `modules/`: auth, CSV handling, database, RAG, analysis, reporting, visualization, PII
- `config/settings.py`: environment-backed settings
- `data/`: local SQLite and ChromaDB storage
- `tests/`: unit, integration, property, and smoke tests

## Testing

```bash
pytest
```

Current verified baseline:

```text
201 passed
```

## Current Runtime Notes

- RAG uses `sentence-transformers/all-MiniLM-L6-v2` for embeddings.
- If that model cannot load, the app falls back to ChromaDB default embeddings.
- Ollama must be running for generated query answers.
- PDF export falls back to Markdown if `reportlab` is unavailable.
- Advanced quantitative/time-series features may require `statsmodels`.

## Docs

- `docs/DEPENDENCY_STRATEGY.md`: dependency and upgrade guidance
- `docs/MODULE_INTERFACES.md`: module-level API overview
- `docs/DATA_FORMAT_GUIDE.md`: data format guidance
- `docs/PROJECT_CONTEXT.md`: broader project context

## License

See `LICENSE`.

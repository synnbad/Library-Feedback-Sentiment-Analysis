# Personal System Report

Last updated: 2026-04-27

## Executive Summary

The Library Assessment Decision Support System is a local-first, small-team
Streamlit application for turning library assessment data into usable evidence,
analysis, and leadership-ready reports. It is best understood as a human-in-the-loop
assessment workbench rather than a generic chatbot, a spreadsheet replacement, or a
live business intelligence platform.

The system helps library staff import assessment data, validate and describe it,
index it for natural-language retrieval, analyze qualitative and quantitative
patterns, ask cited questions, and assemble findings into reports. Its strongest
design commitment is that sensitive assessment data remains under local or
institution-controlled custody.

The AI layer is not a single feature bolted onto the app. It is a set of coordinated
NLP capabilities: embeddings, semantic retrieval, RAG question answering, sentiment
analysis, theme extraction, query classification, evidence scoring, and narrative
drafting. The system uses AI to accelerate assessment reasoning while preserving
human review and professional judgment.

## Product Identity

The system is designed for library assessment professionals working with data such
as survey responses, usage statistics, circulation exports, event attendance,
instruction data, reference interactions, e-resource reports, collection data, and
benchmark comparisons.

Its core user need is not simply "ask a chatbot about a CSV." The deeper need is:

> Help an assessment team move from messy local evidence to trustworthy findings,
> recommendations, and reports that can be shared with library leadership.

That means the product must do several things well:

- Keep data local and auditable.
- Support multiple common library assessment data shapes.
- Help users understand whether data is ready for analysis.
- Provide both exploratory and structured analysis workflows.
- Prefer computed/statistical answers where possible.
- Use AI-generated prose as draft material, not final authority.
- Preserve citations, provenance, limitations, and evidence strength.
- Produce reports suitable for senior leadership.

The current Streamlit workflow shell reflects this identity. The primary sections are
Home, Data, Analyze, Ask, Reports, Governance, and Admin.

## System Architecture

At a high level, the app has four cooperating layers:

1. **Streamlit UI layer**
   Provides the workflow-oriented interface, role-aware navigation, dashboards,
   forms, analysis views, report previews, and admin surfaces.

2. **Business logic layer**
   Lives primarily in `modules/`. It handles importing, normalization, validation,
   analysis, RAG, reporting, logging, authentication, workflow guidance, and
   provenance.

3. **Persistence layer**
   Uses SQLite as the system of record. SQLite stores datasets, users, metadata,
   logs, query records, reports, analysis results, assessment projects, pinned
   insights, and workflow state.

4. **AI and retrieval layer**
   Uses ChromaDB for local vector storage, sentence-transformer embeddings for
   semantic representation, and Ollama for local LLM generation.

This architecture intentionally stays simple. It avoids microservices, hosted AI
APIs, managed databases, or external data pipelines. That simplicity is part of the
privacy and operational model.

## Workflow Overview

### Home

Home is an operational dashboard. It shows system status, quick counts, and the
attention queue: missing metadata, indexing gaps, unavailable inference, and
recommended next steps.

This matters because Streamlit apps can otherwise feel stateless. Home gives users a
clear sense of what the system needs before deeper work can continue.

### Data

Data is the control room for datasets. It includes import, dataset management,
metadata readiness, PII review, and indexing status.

The important workflow is:

1. Import a file.
2. Normalize it into an analysis-ready shape.
3. Validate and profile it.
4. Add FAIR/CARE metadata.
5. Index it into ChromaDB.
6. Confirm it is ready for Ask.

SQLite stores the canonical dataset and metadata. ChromaDB stores searchable vector
representations. The UI now shows whether each dataset is ready for Ask and can sync
stale local status from ChromaDB.

### Analyze

Analyze organizes analysis around user intent rather than implementation names:

- Text Feedback
- Metrics & Trends
- Comparisons
- Charts
- Modeling Readiness

This is important because most users think in assessment questions, not algorithms.
They want to know what patrons said, what changed over time, whether groups differ,
what visual explains a pattern, or whether data is suitable for a model.

### Ask

Ask is the natural-language question workbench. It retrieves relevant indexed
records, answers with local RAG, shows citations, and suggests follow-up questions.

The design direction is for Ask to become more structured over time: dataset scope,
question type, deterministic answer routing, evidence labels, and promotion into
reports.

### Reports

Reports is the destination for leadership-facing output. It combines datasets,
analysis summaries, visualizations, qualitative findings, pinned insights, citations,
and generated narrative.

The system's intended report style is not a raw analysis dump. It should produce
senior-leadership briefs with executive summaries, key findings, evidence,
limitations, implications, recommendations, methodology notes, and data sources.

### Governance

Governance tracks FAIR/CARE readiness and explains responsible data use. It connects
metadata quality, privacy, provenance, export controls, and auditability.

### Admin

Admin is the control plane for users, roles, model settings, PII rules, audit logs,
system health, and future backup/restore workflows. It is visible only to admins.

## Data Model And Persistence

SQLite is the system of record. The most important tables include:

- `datasets`: dataset metadata, file hash, row count, column names, FAIR/CARE fields,
  analysis capabilities, and indexing state.
- `survey_responses`: normalized text response records.
- `usage_statistics`: normalized metric/circulation-style records.
- `themes`: qualitative themes and representative quotes.
- `users`: named local accounts with hashed passwords and roles.
- `access_logs`: audit records.
- `query_logs`: RAG activity metadata.
- `reports`: report metadata and exported content hooks.
- `pinned_insights`: user-scoped query insights for report drafting.
- `assessment_projects`: project planning and assessment workflow records.

ChromaDB is not the system of record. It is the retrieval index. If ChromaDB and
SQLite disagree about indexing status, SQLite can be synchronized from ChromaDB when
documents already exist.

## The AI Layer

The AI layer is composed of several smaller NLP systems that work together. This is
one of the most important things to understand: the application does not simply send
everything to an LLM and hope for the best.

Instead, the system combines:

- structured data profiling
- deterministic statistics
- lexical NLP
- vector embeddings
- semantic search
- local LLM generation
- redaction and evidence controls

Each part has a different role.

## How NLP Is Applied

NLP appears throughout the system in different forms.

### 1. Text Normalization For Retrieval

When a dataset is indexed, rows are converted into text passages. Survey responses
become passages that include the question and response text. Usage or circulation
records become short semantic descriptions such as a metric, value, date, and
category.

This step is simple but crucial. Vector search works over text, so tabular rows must
be expressed as language before they can be embedded.

### 2. Sentence Embeddings

The system uses `sentence-transformers/all-MiniLM-L6-v2` by default. This model turns
text into dense numerical vectors. These vectors represent semantic meaning, not just
exact words.

For example, a user might ask:

> What are students frustrated about?

Relevant uploaded comments might not contain the word "frustrated." They might say
"the printers are always broken" or "study rooms are impossible to reserve." A
keyword search could miss those. Embeddings make it possible to retrieve semantically
related material even when the wording differs.

This is one of the main NLP foundations of the app.

### 3. ChromaDB Vector Retrieval

Once records are embedded, they are stored in ChromaDB. At query time, the question is
also embedded. ChromaDB compares the question vector to stored document vectors and
returns the closest matches.

This is retrieval, not generation. The system is finding local evidence that appears
semantically relevant to the user's question.

The retrieval result includes source metadata such as dataset ID, dataset type, row
ID, date, metric name, or question. That metadata becomes the basis for citations.

### 4. Retrieval-Augmented Generation

RAG is the bridge between retrieval and the local LLM.

The RAG pipeline is:

1. User asks a natural-language question.
2. The question is classified and sometimes rewritten with dataset context.
3. The question is embedded.
4. ChromaDB retrieves relevant local records.
5. Retrieved context is assembled with the question and conversation history.
6. The local Ollama model generates an answer.
7. PII redaction is applied.
8. Citations and evidence indicators are returned.

The important point is that the LLM is grounded in retrieved local evidence. The LLM
does not independently inspect SQLite. It receives curated text context from the RAG
pipeline.

### 5. Query Intelligence

The system has a query intelligence layer that works before and after RAG. It helps
classify questions into broad intents such as data inventory, data quality,
qualitative, quantitative, or reporting.

This enables better behavior than a plain chat box:

- Some questions can be answered from dataset profiles without the LLM.
- Some questions need indexed source rows.
- Some questions should be rewritten to include dataset context.
- Some answers should include stronger caveats because evidence is thin.
- Suggested follow-ups can be shaped by the available data.

This is NLP in a product sense: the system is interpreting what kind of language task
the user is performing and routing it accordingly.

### 6. Sentiment Analysis

For qualitative feedback, the baseline sentiment path uses TextBlob. TextBlob assigns
polarity scores and categories such as positive, neutral, and negative.

The repo also includes an enhanced transformer sentiment module based on RoBERTa,
but it is disabled by default. That design is sensible: transformer sentiment can be
more accurate, but it is heavier and may require more local resources.

Sentiment analysis is useful for summary patterns, but it should not be treated as
final interpretation. In assessment work, sentiment is a signal that helps direct
human attention.

### 7. Theme Extraction

The qualitative analysis layer extracts themes from open-ended responses. The current
approach uses traditional NLP and machine learning methods such as TF-IDF-style
keyword extraction and clustering.

This is different from LLM summarization. Theme extraction is more structured: it
tries to identify repeated patterns across many responses, count their frequency,
and connect them to representative quotes.

This is important for assessment because leaders need patterns, not isolated
comments.

### 8. Evidence Assessment

The system increasingly treats evidence quality as part of the answer. Retrieval
confidence, citation count, data shape, query type, and profile readiness can all
inform labels such as strong, moderate, limited, or insufficient evidence.

This is one of the most important trust mechanisms. LLM prose can sound confident
even when the underlying evidence is weak. Evidence labels make uncertainty visible.

### 9. Narrative Drafting

The LLM is most valuable when it turns structured results into readable narrative:

- executive summaries
- report paragraphs
- caveats
- recommendation drafts
- plain-language explanations of statistical results

But these outputs should remain drafts until reviewed. The system's direction is
clear: human analysts finalize recommendations and leadership-facing language.

## Relationship Between Deterministic Analysis And AI

The best version of this system does not ask the LLM to do everything.

For numeric questions, pandas, SQLite, scipy, statsmodels, or deterministic
statistics should answer first. The LLM should explain the result, not invent the
calculation.

For example:

- Count rows: use SQLite or pandas.
- Compute averages: use pandas.
- Run correlations: use statistical routines.
- Detect trends: use regression/time-series logic.
- Explain what the trend means: use AI drafting with caveats.

This distinction is central to trust. Deterministic computation provides accuracy and
repeatability. AI provides language, synthesis, and interpretive support.

## Local LLM Role

The local LLM currently runs through Ollama. The default model is `llama3.2:3b`.

The LLM is used for:

- answering RAG questions
- drafting report narratives
- generating interpretations
- helping turn findings into stakeholder-facing language
- suggesting next questions or recommendations

Because it runs locally, it supports the FERPA/privacy posture of the app. A future
institution-controlled VM can host the LLM for faster inference, but that VM should
remain inside the trust boundary and receive redacted context by default.

## Privacy And PII

The privacy model is layered:

- Data is stored locally in SQLite and ChromaDB.
- The system avoids hosted third-party AI APIs.
- PII detection and redaction protect generated outputs.
- Future upload-time PII blocking should prevent high-risk raw identifiers from
  entering the system unless an admin overrides.
- Query and report content should preserve citations and methodology notes.

The system should be conservative: over-redaction is usually safer than
under-redaction in library assessment contexts involving students or patrons.

## Roles And Governance

The role model is intentionally small:

- Admin
- Analyst
- Viewer

Admins govern the system. Analysts do the assessment work. Viewers consume approved
outputs.

This matters because not every user should see every workflow. Raw export, model
settings, user roles, backup/restore, PII override, and audit logs belong to admins.
Analysis and report preparation belong to analysts. Final report reading belongs to
viewers.

## Report Philosophy

Reports should be leadership-ready briefs, not analysis dumps.

A strong report should include:

- executive summary
- key findings
- evidence and limitations
- implications for service or strategy
- recommendations and actions
- supporting charts and metrics
- methodology notes
- data sources

AI can draft pieces of this, but an analyst should review and shape the final
message. Recommendations especially need human approval.

## Current Strengths

The system already has a strong foundation:

- local-first architecture
- modular Streamlit UI
- SQLite persistence
- ChromaDB vector retrieval
- Ollama-based local generation
- import and normalization support for many library assessment data types
- qualitative and quantitative analysis modules
- report generation
- PII redaction
- role-aware workflow shell
- governance documentation
- audit and logging surfaces

The overall direction is coherent. The repo is no longer just a course prototype; it
is moving toward a practical local assessment assistant.

## Current Limitations

Several areas are still emerging:

- Upload-time PII blocking is planned but not fully implemented.
- Admin user management UI is currently a placeholder/control-plane surface.
- Backup and restore are documented design decisions but not full workflows yet.
- Report lifecycle states such as draft, review, final, archived, and versioning need
  deeper implementation.
- Evidence drawers and project-linked promoted insights are still future work.
- Some visible Streamlit warnings mention `use_container_width`, which should be
  migrated to newer `width` parameters eventually.
- Some older documentation still reflects earlier feature names and should be updated
  over time.

## Best Next Implementation Steps

The best next steps are governance and workflow depth, not more model complexity.

Recommended order:

1. Build the upload wizard with PII review and redacted import.
2. Add real archive/delete/export role enforcement for datasets.
3. Implement admin user and role management.
4. Build explicit backup and overwrite-restore workflows.
5. Add report lifecycle states and section-by-section report editing.
6. Add report-specific evidence drawers.
7. Route deterministic/statistical questions before RAG generation.
8. Add stronger confidence/evidence labels across Ask and Reports.
9. Implement model endpoint allowlisting.
10. Continue cleaning old documentation and Streamlit deprecation warnings.

## Bottom Line

This system applies NLP in a grounded, practical way. It uses language models where
language models are useful: retrieval-grounded answering, synthesis, explanation,
and drafting. It uses traditional NLP where structure matters: embeddings, semantic
search, sentiment, theme extraction, query classification, and evidence routing. It
uses deterministic computation where accuracy matters: statistics, counts,
distributions, trends, and data profiling.

That balance is the core design strength.

The system should continue to grow as a local-first, human-reviewed assessment
assistant: one that helps library professionals reason faster, communicate better,
and preserve trust in the evidence behind their decisions.


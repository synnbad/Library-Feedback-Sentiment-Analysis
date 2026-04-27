# Local-First Small-Team Design Record

Last updated: 2026-04-27

## Purpose

This record captures the current product and architecture decisions for the Library
Assessment Decision Support System. It is intended to preserve the shared design
understanding before implementation work continues.

## North Star

The system remains a local-first workstation or small-team deployment. It is an
assessment workbench for library staff, not a hosted enterprise platform.

Local-first means:

- Core data stays on the workstation or approved local institutional storage.
- SQLite and ChromaDB remain local to the application machine.
- AI processing uses local or institution-controlled inference.
- No student or assessment data is sent to third-party hosted AI services.
- Manual human review remains part of upload, analysis, reporting, and sharing.

## Deployment Boundary

The application may later use a VM-hosted LLM to improve inference speed. A VM is
inside the trust boundary only when it is institution-controlled and reachable
through a private network or VPN.

The local app continues to own data storage. A VM may provide inference only. The
default behavior should send PII-redacted retrieved context to the VM, with any raw
context mode limited to admin-approved trusted deployments.

## Roles And Permissions

The system will use named user accounts with three roles:

- `admin`: manage users, roles, settings, model endpoints, backups, restore, delete
  datasets, override high-risk PII blocks, and govern finalized reports.
- `analyst`: upload data, edit metadata, run analyses, query data, generate drafts,
  prepare reports, and mark reports ready for review.
- `viewer`: read finalized reports and approved shared outputs only.

Shared accounts are not acceptable for normal use because they weaken auditability.
User and role management should live in an admin-only in-app settings page, with CLI
bootstrap retained as a fallback.

## Dataset Policy

Datasets are shared across the local team by default. This is a collaborative
assessment workspace, not a personal notebook.

Dataset lifecycle states:

- `active`: available for normal analysis, query, visualization, and reporting.
- `archived`: hidden from default workflows but preserved for provenance, old reports,
  audit, and possible admin restoration.
- `deleted`: rare, admin-only, and irreversible after confirmation.

Only admins can delete datasets. Analysts can upload datasets and edit metadata.
Raw dataset export is admin-only by default. Analysts may export reports, charts, and
aggregate analysis outputs.

## PII And Privacy

High-risk PII detection during upload blocks import by default. Admins may override a
block with a required logged reason. Analysts should normally import a redacted copy
instead.

When creating a redacted import:

- The original uploaded file is processed in memory only.
- The original file is not persisted by the app.
- Only the redacted dataset is stored.
- Provenance records the redaction types and counts.

Admins can configure institution-specific PII patterns, such as student IDs,
barcodes, or employee IDs. Custom patterns should include labels, severity, test
text, and change audit logs. They are included in backups.

## Query Policy

Viewers cannot run new natural-language queries by default. Querying is available to
admins and analysts.

Query outputs are private drafts unless intentionally promoted into a report or
shared artifact. Pinned query insights remain scoped to the user by default.

Query logs should store audit metadata rather than full question and answer text by
default. Useful metadata includes user, timestamp, datasets touched, confidence,
processing time, and broad outcome status.

Audit logs are retained for one year by default, configurable by admins. Pruning
should create a backup first and show admins what will be removed.

## Backup And Restore

Backups are explicit admin workflows, not only documentation telling users to copy
folders.

Backups include everything required for full restore:

- SQLite database
- ChromaDB index
- dataset records and metadata
- logs and provenance
- query metadata and pinned insights
- generated report metadata and snapshots
- PII pattern settings
- relevant configuration snapshot

Backup files are sensitive artifacts. They should be clearly named and governed as
sensitive local data. Encryption can be added later.

Restore overwrites the current system, with strong warnings. Before restore, the app
automatically creates a pre-restore backup of the current state.

## Model And Endpoint Governance

Only admins can change LLM endpoint/model settings or embedding model settings.
Analysts can view model status but cannot redirect inference.

The app should enforce an approved endpoint allowlist. `localhost`, loopback
addresses, and explicitly approved private-network hosts are allowed by default.
Unknown public endpoints are blocked unless an admin deliberately approves them with
a warning and logged reason.

The app should continue to work in degraded mode when the LLM is unavailable.
Upload, validation, PII scanning, metadata, quantitative analysis, visualizations,
backups, and non-LLM report structure should continue. LLM-dependent RAG generation
and narrative drafting should pause.

Whenever possible, deterministic or statistical answers take priority over
LLM-generated answers. The LLM should synthesize, explain, and draft narrative; it
should not perform arithmetic that SQLite, pandas, or statistical routines can answer
directly.

All AI-generated answers and report sections should include plain evidence labels:
`Strong evidence`, `Moderate evidence`, `Limited evidence`, or `Insufficient evidence`.

## Report Lifecycle

Reports are leadership-ready assessment briefs, not raw analysis dumps.

Default final report structure:

1. Title
2. Executive summary
3. Key findings
4. Evidence and limitations
5. Implications for service or strategy
6. Recommendations and actions
7. Supporting metrics and visuals
8. Methodology note
9. Data sources

Analysts and admins can edit AI-generated report narratives before finalization.
Reports should clearly distinguish analyst-reviewed recommendations from generated
draft text.

Each recommendation must link back to supporting evidence, such as datasets, metrics,
themes, confidence labels, or cited query insights.

Report lifecycle states:

- `draft`: editable working report.
- `ready_for_review`: prepared for approval.
- `final`: immutable approved snapshot visible to viewers.
- `archived`: preserved but hidden from default report lists.

Analysts and admins can mark reports ready for review. Finalization requires a named
approver and approval timestamp. A second reviewer is preferred by default, with
admin-configurable self-approval for very small teams.

Final reports are immutable snapshots. If source data or analysis changes, users
create a new report version rather than silently changing the finalized report.
Versioning should be simple: version number plus optional supersedes link. The latest
final version is shown by default while older versions remain preserved.

Every final report automatically preserves methodology notes, including datasets
used, row counts, analysis methods, model used, endpoint class, embedding model, PII
redaction status, confidence criteria, and known limitations.

## Dashboard And Ingestion Scope

Dashboard-building remains a planning and handoff feature, not a live BI dashboard
platform. The app may generate KPI plans, chart exports, dashboard blueprints, and
handoff material for tools such as Power BI or Tableau.

Data ingestion remains manual upload for the foreseeable future. This preserves
human review, metadata quality, PII scanning, and duplicate checks.

A watched local folder import queue may be added later. Files dropped into the
folder should still require analyst or admin review before import.

## Implementation Priority

The next implementation phase should prioritize governance and trust foundations
before new analysis features:

1. Roles and permission checks.
2. Admin user and role management UI.
3. Dataset archive/delete/export rules.
4. Upload-time PII blocking and redacted import.
5. Configurable institution-specific PII patterns.
6. Explicit admin backup and restore workflows.
7. Query log minimization and retention controls.
8. Report lifecycle, approval, immutable final snapshots, and versioning.
9. Model endpoint allowlist and admin-only model configuration.
10. Confidence/evidence labels across AI-generated outputs.


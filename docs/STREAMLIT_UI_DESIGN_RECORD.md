# Streamlit UI Design Record

Last updated: 2026-04-27

## Purpose

This record captures the agreed Streamlit UI direction for the local-first
small-team library assessment application.

## Navigation Model

The UI should be organized around assessment workflow stages rather than internal
feature modules.

Primary navigation:

- `Home`: operational dashboard and next actions.
- `Data`: import, dataset management, metadata, PII review, archive/export policy,
  and indexing status.
- `Analyze`: text feedback, metrics and trends, comparisons, charts, and modeling
  readiness.
- `Ask`: question workbench with chat, suggested questions, scope selection,
  evidence labels, citations, and promotion into reports.
- `Reports`: projects, evidence drawers, leadership report drafting, review,
  approval, versioning, and dashboard handoff.
- `Governance`: live governance readiness plus reference material.
- `Admin`: admin-only controls for users, roles, backups, model settings, PII rules,
  audit logs, and system health.

Viewers should see a simplified experience focused on finalized reports and
governance reference. Analysts should not see most admin-only actions.

## Page Behavior

Home should be an operational dashboard rather than a welcome page. It should show
what needs attention now: metadata gaps, unindexed datasets, PII review items, draft
reports awaiting review, backup freshness, model status, and recent activity.

Each major page should include a quiet current-context strip showing user, role,
active scope, model or backup status where relevant, and selected dataset/project or
report when applicable.

Long instructional text should move out of the main work surface into help expanders
or documentation links. Empty states should be task-oriented and include the next
action.

Warnings and errors should be grouped by severity:

- `Blocking`
- `Needs review`
- `Informational`

Each issue should include the recommended fix.

## Data Workflow

Upload should become a wizard-style flow:

1. Select file.
2. Preview and profile.
3. Review validation and PII findings.
4. Confirm metadata.
5. Import and index.

Indexing should happen automatically after import when possible. The UI should show a
background-style queue with states such as `Queued`, `Indexing`, `Ready`, `Failed`,
and `Skipped`, plus retry controls.

The Data section should be the single place for dataset state and actions.

## Analysis Workflow

Analysis should be organized by user question type:

- Text feedback
- Metrics and trends
- Comparisons
- Charts
- Modeling readiness

The app should recommend the best next analysis based on dataset profiles and
preselect sensible defaults. Advanced options should be hidden by default.

Analysis outputs should distinguish:

- `Result`: computed or statistical output.
- `Interpretation`: what the result means for assessment.
- `Recommendation`: reviewed or draft action.

Generated recommendations must be reviewed before inclusion in final reports.

## Ask Workflow

Ask should be a structured question workbench, not only a chat box.

Default scope is all active datasets, with controls for dataset, dataset type, saved
project, or report scope. Deterministic and statistical answers should be preferred
when possible, with LLM synthesis used for explanation and narrative.

Each answer should show evidence strength, citations, answer type, and a clear
promotion path into a report or project.

## Reports Workflow

Report creation should use stages:

1. Configure scope.
2. Generate draft.
3. Edit section-by-section.
4. Review evidence and recommendations.
5. Submit for review.
6. Finalize and export.

Reports should use a standardized senior-leadership brief structure. Charts, tables,
and insights should be selected as supporting artifacts rather than automatically
dumped into reports.

Promoted insights should live in a report-specific evidence drawer with source,
dataset, confidence, owner, and inclusion status.

Projects should be the organizing container for substantial assessment work:
datasets, research questions, queued queries, analyses, evidence, draft reports,
approvals, and final outputs. Projects remain optional but encouraged.

## Visual Tone

The app should feel quiet, professional, and assessment-oriented. Use restrained
colors, clear hierarchy, stable tables, polished report previews, concise microcopy,
and light iconography for wayfinding. Avoid decorative or marketing-style UI.

Action hierarchy should be consistent:

- One clear primary action per workflow panel.
- Secondary actions for alternatives.
- Danger actions only for destructive operations, with confirmation and role checks.

## Roadmap Priority

The first implementation slice is the workflow-oriented shell:

- grouped navigation
- role-aware Admin visibility
- operational Home
- Data, Analyze, Reports, and Admin section containers
- documentation and README updates

The next UI implementation slices should be:

1. Upload wizard with PII review and redacted import.
2. Dataset archive/export/indexing controls.
3. Report editor with evidence drawer and lifecycle states.
4. Project save/promote flows across Analyze and Ask.
5. Admin user/role management and backup/restore workflows.
6. Governance dashboard split from reference content.
7. Global search for datasets, projects, reports, and saved evidence.


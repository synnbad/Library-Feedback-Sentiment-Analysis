# Architecture Review — July 2026

## Scope

This review focused on the application boundary, configuration lifecycle, authentication session behavior, database integrity, and testability of the Library Assessment Decision Support System.

## Remediated in this change

### 1. Configuration imports performed filesystem writes

`config.settings` created repository-local runtime directories as soon as the module was imported. Import-time I/O makes tests order-dependent, complicates packaging, and can write to the wrong location before environment-specific startup logic runs.

**Fix:** directory creation now happens explicitly through `Settings.ensure_directories()` during application startup. The method honors `DATABASE_PATH`, `CHROMA_DB_PATH`, and `EXPORTS_DIR` overrides.

### 2. Configured session timeout was not enforced

`SESSION_TIMEOUT_MINUTES` existed in configuration, but authenticated Streamlit sessions had no idle-expiration policy.

**Fix:** a framework-light `modules.session_policy` module now owns idle-session timing. The Streamlit entry point checks expiration before protected pages render, clears session metadata on logout, and initializes activity for demo sessions.

### 3. Session logic was tightly coupled to Streamlit

Authentication state behavior could not be tested without importing Streamlit and database-backed authentication code.

**Fix:** timeout calculations are isolated behind pure helpers with an injectable clock. Focused tests cover initialization, boundary expiration, disabled timeout behavior, malformed timestamps, and cleanup.

## High-priority follow-up findings

### Database foreign-key enforcement is incomplete

The schema defines cascading foreign keys, but SQLite requires `PRAGMA foreign_keys = ON` for every connection. The current connection factory enables WAL and a busy timeout but does not enable foreign keys. This can allow orphaned rows and makes the documented cascade behavior unreliable.

**Recommended remediation:** centralize connection configuration in one private helper used by database initialization and `get_db_connection()`, enable `foreign_keys`, `journal_mode`, and `busy_timeout` there, and add an integration test proving a dataset delete cascades.

### Schema creation and migrations are duplicated

`init_database()` contains current schema definitions while `migrate_database()` separately replays historical changes. Broad exception handling hides migration failures and makes schema drift harder to detect.

**Recommended remediation:** move migrations into ordered, idempotent migration functions or SQL files; record each version only after its migration succeeds; catch only expected duplicate-column/index errors.

### The database module has too many responsibilities

The module combines connection policy, schema DDL, migrations, retry behavior, idempotency support, and generic query execution. Its size raises change risk and makes targeted testing harder.

**Recommended remediation:** split into `connection.py`, `migrations.py`, and repository/service modules while preserving a compatibility facade.

### Authentication rate limits are process-local

Failed-login tracking is stored in memory. It resets on restart and is not shared across multiple processes.

**Recommended remediation:** for a single-user local deployment, document this limitation. For shared deployment, persist lockout state or place authentication behind an external identity provider.

### Page loading catches exceptions too broadly

The application boundary displays raw exception text and catches all exceptions during dynamic imports. This can expose implementation details and blur dependency errors with application bugs.

**Recommended remediation:** log full exceptions through the logging service, show a stable user-facing message, and distinguish missing optional dependencies from defects in page code.

## Validation performed

Focused tests were executed against the extracted changed modules on Python 3.13.5:

- 8 tests passed
- idle-session timeout boundary and cleanup covered
- configured runtime directory paths covered
- negative timeout validation covered

A full repository test run should also execute in GitHub Actions because the connected environment did not provide a network-capable local checkout of the private dependency graph.

# Technical Guide - GAMLO

## 1. Description
GAMLO is a Tkinter desktop application for employee management and access reconciliation. It supports SQLite by default and SQL Server via `pyodbc`, providing CRUD for people and applications, process workflows (onboarding, offboarding, lateral movements, flex staff), reconciliation, history tracking, manual access logging, and Excel exports.

## 2. Scope
- Included: application architecture, data flow, key services, UI modules, reconciliation logic, export paths, and environment configuration for SQLite/SQL Server.
- Excluded: infra provisioning, AD/SSO integration, and new schema design (see `sql_server_setup.sql` and `config.py` for DB specifics).

## 3. Reference
- Main app: `app_empleados_refactorizada.py`
- Config: `config.py` (`USE_SQL_SERVER`, `SQL_SERVER_CONFIG`)
- Services: `services/` (`access_management_service.py`, `search_service.py`, `export_service.py`, `history_service.py`, `excel_importer.py`, `dropdown_service.py`)
- UI: `ui/` (`components.py`, `manual_access_component.py`, `styles.py`)
- SQL scripts: `sql_server_setup.sql`, `diagnostic_views.sql`, `samples/*.sql`
- Tests: `tests/test_offboarding.py`, `test_flex_staff*.py`
- Executable hints: `pyinstaller_command.txt`

## 4. Key Accountabilities
- Data integrity: normalize statuses (Active/Inactive), enforce SID uniqueness, and align unit/subunit combos with catalog data.
- Access safety: skip inactive applications when granting/revoking; ensure bulk actions are idempotent where possible.
- Export correctness: write Excel files to `Downloads` with descriptive names and required sheets; handle missing folder errors gracefully.
- Performance and UX: keep UI responsive (threaded operations where used), provide clear feedback on long-running tasks (bulk reconciliation).
- Auditability: persist history entries for created tickets and process changes; allow editing/deleting with confirmations.

## 5. Key Terms
- SID: unique employee identifier.
- Headcount: people catalog with unit/position metadata.
- Access status: application availability flag (Active/Inactive); inactive apps are skipped by reconciliation/grant logic.
- Lateral Movement: additive process that preserves current accesses and adds only missing ones.
- Flex Staff: temporary access assignments with planned revocation.
- Reconciliation: comparison of current vs. required accesses to produce grant/revoke actions.

## 6. General Information
- Default DB: SQLite file under `database/`; switch to SQL Server by setting `USE_SQL_SERVER=True` and populating `SQL_SERVER_CONFIG`.
- Downloads path: exports and reconciliation reports target the OS `Downloads` directory; ensure it exists and is writable.
- Threading: some long operations use threads to keep Tkinter responsive; avoid heavy work on the main thread.
- Logs/diagnostics: console prints (e.g., `[DEBUG] ...`) assist troubleshooting; check history data when reconciling or processing offboarding.

## 7. Front End
- Built with Tkinter/ttk, custom styles in `ui/styles.py`, and reusable widgets in `ui/components.py`.
- Navigation via a left side menu with modules: People, Applications, Processes (Onboarding/Offboarding/Lateral/Flex Staff), Reconciliation, History, Manual Access, Export.
- Tables support live search and multi-filtering; dialogs handle creation/editing/deletion with confirmation prompts.
- Manual access component lives in `ui/manual_access_component.py`.

## 8. The Code (High Level)
- Entry point `app_empleados_refactorizada.py`: initializes config, DB connection (SQLite/SQL Server), loads services, wires UI components, and starts the Tkinter main loop.
- Services encapsulate business logic:
  - `access_management_service.py`: onboarding/offboarding/lateral/flex logic; ensures only active apps are acted upon.
  - `search_service.py`: filtering/search across tables.
  - `export_service.py`: Excel exports to `Downloads` with structured sheets.
  - `history_service.py`: CRUD on historical records and ticket registration.
  - `excel_importer.py`: optional imports with column validation.
  - `dropdown_service.py`: populates combo data (units, positions, roles).
- SQL helpers and schemas are defined in `sql_server_setup.sql` and `diagnostic_views.sql`; SQLite mirrors structure where applicable.

## 9. Step-by-Step Logic (Core Flows)
- Launch: read `config.py` → choose DB (SQLite/SQL Server) → initialize services → build UI.
- People CRUD: UI form → validate required fields → call service → write to DB → refresh table → allow export.
- Applications CRUD: similar pattern; normalize `access_status` to Active/Inactive on save.
- Onboarding: fetch required apps by position/unit → calculate missing accesses → present summary → on confirm, write grants/history.
- Offboarding: list current accesses → filter out inactive apps → mark for revocation → persist results/history.
- Lateral Movement: compute delta (missing accesses only) → grant delta → leave existing accesses intact.
- Flex Staff: schedule temporary grants with end-date; revocation path removes only temporary grants.
- Reconciliation (per SID): fetch current vs. required apps → compute to-grant/to-revoke → optional ticket registration → export Excel.
- Reconciliation (bulk): iterate all SIDs → apply per-SID reconciliation → aggregate outputs; warn about runtime.
- History: list/edit/delete records; optional delete by `case_id` scope; export summaries/statistics.

## 10. Detailed Activities (By Module)
- People: create/edit/delete/inactivate headcount entries; maintain consistent unit/subunit/position; export headcount view.
- Applications: manage logical access catalog; ensure role/unit/subunit alignment; export catalog view.
- Processes: run onboarding/offboarding/lateral/flex flows; confirm summaries; respect Active-only rule for grants/revokes.
- Reconciliation: per SID or bulk; register tickets into history; export multi-sheet Excel to `Downloads`.
- History: review, edit, or delete records (single or by case); export stats.
- Manual Access: log exceptional access with position-aware filtering; capture comments/levels.
- Export/Import: generate Excel outputs; when import is enabled, validate columns before inserting; handle missing `Downloads` path gracefully.


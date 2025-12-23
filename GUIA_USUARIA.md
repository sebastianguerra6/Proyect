# User Guide - GAMLO

## 1. Introduction
- This guide explains how to use the GAMLO desktop app (Tkinter) to manage employees, applications, and access processes: onboarding, offboarding, lateral movements, and flex staff.
- It is written for operational users, team leads, and admins who need accurate people and access data without deep technical steps.

## 2. Purpose
- Standardize daily use, reduce errors, and speed up employee/access updates.
- Provide a quick reference for the most common tasks: create/edit/deactivate employees, reconcile access, register processes, and export reports.

## 3. Scope
- Included: launch/sign-in, side-menu navigation, People (headcount), Applications, Processes (onboarding/offboarding/lateral/flex staff), Access Reconciliation, History, Manual Access, search/filters, and Excel export/import (when available).
- Excluded: dependency installation, infrastructure changes, new module development, or database schema changes (see `README.md` for technical setup).

## 4. General Information
- Roles: Operations (updates data), Lead/Supervisor (validates/reviews), Admin (adjustments, diagnostics).
- Requirements: Python + dependencies installed or the packaged executable; database connection configured (SQLite by default, SQL Server via `config.py` with `USE_SQL_SERVER=True`).
- Security and good practices: use your own account, lock your session when away, keep exports within data-handling policies, and ensure the `Downloads` folder exists for exports.
- Data handled: employees (SID, name, email, position, unit), applications (role, unit/subunit, status), process history, and reconciliation tickets.

## 5. How to Use the Application

### 5.1 Launch and access
1. Run `python app_empleados_refactorizada.py` (or open the distributed executable).
2. Wait for the UI to load; the left side menu shows modules: People, Applications, Processes (Onboarding/Offboarding/Lateral/Flex Staff), Reconciliation, History, Manual Access, Export.
3. Use the side menu to move between modules; the main area shows the active table or form.

### 5.2 People (Headcount)
- Create: click “New person”; fill SID, name, email, position, unit/subunit; save.
- Edit: double-click or use “Edit” on a row; update fields and save.
- Deactivate/Delete: select the row and confirm the available action; states normalize to Active/Inactive.
- Search and filters: type in the search bar or add multiple filters (e.g., Unit=Technology, Status=Active); clear them from the active-filters list.
- Export: use the toolbar export to generate an Excel file with the current headcount view.

### 5.3 Applications
- Create: “New application”; set logical name, unit/subunit, required role, category, and status (normalized to Active).
- Edit/Delete: select a row and use the corresponding buttons; deletion requests confirmation.
- Filters and search: combine unit, category, status, role; quick search is supported on the table.
- Export: toolbar option exports an Excel file of the visible applications.

### 5.4 Processes (Onboarding, Offboarding, Lateral, Flex Staff)
- Onboarding: enter SID and required details; the app suggests accesses based on position/unit.
- Offboarding: enter SID; the service skips non-active accesses and shows details in the final message.
- Lateral Movement: additive logic—keeps current accesses and adds only missing ones.
- Flex Staff: manages temporary project accesses with automatic revocation at the end of the period.
- Confirmation: read on-screen messages; errors provide details or console logs for diagnosis.

### 5.5 Access Reconciliation
- Per SID: enter SID and click “Reconcile”; you will see Current access, To grant, and To revoke.
- Bulk: “Reconcile all” processes the full catalog (may take time; check console for progress).
- Register tickets: after a reconciliation, use “Register tickets” to insert detected actions into history.
- Export: generates `conciliacion_accesos_<SID>_<timestamp>.xlsx` with tabs per section in `Downloads`.

### 5.6 History
- View all: refreshes the table with all records (SID, case, process, app, dates, comments, status).
- Edit: select and open the edit dialog to adjust any field; save to persist.
- Delete: select one or multiple rows; delete a single record or all sharing the same `case_id` (confirmation required).
- Export/Stats: produces summaries by status, unit, and performance; Excel export available.

### 5.7 Manual Access
- Use this module to document accesses outside standard flows.
- Filter by position to show only relevant applications; capture level and comments if applicable.

### 5.8 Search, filters, and tables
- Live search: tables filter as you type.
- Multi-filters: add conditions, review the active-filters list, and apply/clear as needed.
- Case insensitivity: comparisons ignore casing and accept equivalents (`Active`, `Inactive`, `1`, `0`).

### 5.9 Export and import
- Excel export: available in People, Applications, History, and Reconciliation; files are saved to `Downloads` with descriptive names.
- Import (when enabled in your build): follow on-screen validation steps before inserting rows.

### 5.10 Session end and exit
- Close the main window when done; if your environment uses shared OS credentials, lock your session to avoid misuse.

## 6. Troubleshooting (quick)
- SQL Server connection: ensure the server is running, credentials in `config.py` are correct, port 1433 is open, and “ODBC Driver 17 for SQL Server” is installed.
- Exports or path errors: confirm `Downloads` exists and you have write permissions.
- Missing items in reconciliation: only applications with `access_status=Active` are considered; inactive ones are skipped.
- Slow bulk actions: bulk reconciliation can take time on large catalogs; watch console output for progress.

## 7. Contact Support
- Functional help (how-to, processes): soporte@tuempresa.com
- Technical help (errors, outages, exports): it@tuempresa.com
- Hours: Mon–Fri, 9:00–18:00 (local time).
- When reporting: include a screenshot, time of issue, module, affected SID/case, and steps taken.


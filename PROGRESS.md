# Build Progress

Purpose: if a Claude session or work session gets interrupted, read this
file first. It tells you exactly what's done and what the next concrete
step is, independent of chat history.

## Status: Phase 4 Step 1 (Local PostgreSQL) — DONE, CONFIRMED WORKING END-TO-END ON ELLE'S MACHINE
## Phase 4 Step 2 (Azure Database for PostgreSQL) — PAUSED, not started. Elle wants a break from Azure work for now — no urgency to resume.

## Setup issues hit on Elle's actual machine getting Phase 4 working (for reference)
- `.env` initially still pointed at the old SQLite URL — `flask db upgrade`
  ran against SQLite instead of Postgres, hit "table already exists"
  since those tables already existed there from Phases 1-3. Fixed by
  actually updating DATABASE_URL to the Postgres connection string.
- The `saas_app` Postgres role/database from the README instructions
  were never actually created on her machine — `psql postgres -c "\du"`
  showed only her own Mac superuser role. Created both with
  `CREATE ROLE` / `CREATE DATABASE` as documented in README.md.
- Postgres service itself was not running (`brew services list` showed
  `postgresql@16` status `none`) — needed `brew services start postgresql@16`.
- A `DATABASE_URL` with a password containing special characters caused
  `sqlalchemy.exc.ArgumentError: Could not parse SQLAlchemy URL` — she
  resolved this herself (likely by using a simpler password or
  URL-encoding it).
- All resolved; Phase 4 Step 1 confirmed fully working end-to-end on her
  actual Mac as of this session (dashboard loads at localhost:5001
  showing 12 seeded apps, backed by real local PostgreSQL).

## Phase 4 additions
- `requirements.txt`: added `Flask-Migrate==4.0.7`, `psycopg[binary]==3.2.10`
  (switched from `psycopg2-binary` after it failed to build on Elle's
  machine — no prebuilt wheel for her Python 3.14, and compiling from
  source needs Postgres build headers she didn't have. `psycopg` v3 has
  proper wheels for newer Python versions and is the actively maintained
  successor anyway).
- `app/__init__.py`: registers Flask-Migrate (`migrate.init_app(app, db)`);
  imports `app.models` before Migrate init so autogenerate sees every table.
- `migrations/` folder (Alembic) — initial migration generated and applied,
  covering all 7 tables (applications, integrations, application_integrations,
  audit_logs, software_requests, governance_reviews, request_answers).
- `run.py` / `seed.py`: `db.create_all()` removed — schema is now owned
  entirely by Alembic migrations (`flask db upgrade`), not implicit
  app-startup table creation.
- `.env.example`: `DATABASE_URL` now points at a local Postgres connection
  string using a dedicated `saas_app` role (not a superuser, not Elle's
  own Mac login) — least-privilege practice that also previews what an
  Azure Postgres connection string will look like in Step 2. Added
  `FLASK_APP=run.py` (required for `flask db ...` CLI commands).
- **Real bug found and fixed:** `config.py` gained a dedicated
  `TestingConfig` class, and all three test files' `app` fixtures were
  changed from `create_app("development")` + a late `app.config.update()`
  to `create_app("testing")`. Root cause: Flask-SQLAlchemy 3.x binds its
  engine eagerly inside `db.init_app()`, so overriding config *after*
  `create_app()` returns never actually took effect — tests were silently
  running against whatever `.env`'s `DATABASE_URL` pointed at. This was
  low-stakes while `.env` pointed at SQLite, but once it pointed at real
  Postgres, direct inspection confirmed tests were hitting the real
  database, and `db.drop_all()` in test teardown was wiping real seeded
  data every run (verified: 12 rows → 0 via direct `psql` check). Fixed
  properly at the root, not patched around. Full details in
  controls-mapping.md's Phase 4 section. This almost certainly also
  explains the "unreproducible" test flake noted in Phases 1–3 — tests
  were never actually isolated from each other.
- Verified end-to-end against a real local PostgreSQL 16 instance in
  Claude's own sandbox (not just described): `flask db init` / `migrate`
  / `upgrade` all ran clean, all 7 tables created correctly, `seed.py`
  populated real Postgres successfully, the live dashboard and
  application list both rendered correctly against it, and the full
  test suite (11/11) ran 5+ times with zero hangs and zero impact on
  the real seeded data.
- `controls-mapping.md` — Phase 4 section filled in with the bug above
  documented as a real finding, not a theoretical control.

## Not yet done for Phase 4
Step 2 — provisioning Azure Database for PostgreSQL Flexible Server,
pointing `.env` at it with `sslmode=require`, running the same Alembic
migration against it. Deliberately sequenced after Step 1 proved solid
locally, per the original two-step plan agreed with Elle.

## Phase 3 additions
- New Blueprint `app/routes/dashboard.py`, mounted at `/` and `/dashboard`
  (dashboard is now the app's home page — navbar brand links here).
- Metrics: total/active applications, no-business-owner, no-technical-owner,
  incomplete reviews, apps touching sensitive data, unknown SSO status,
  SSO-supported-but-not-enabled, estimated annual spend, renewal counts at
  30/60/90 days plus an actual table of the upcoming renewals, breakdowns by
  department/discovery source/review status (Chart.js bar charts via CDN),
  and a Pending Software Requests count linking to the Phase 2 queue.
- All metrics excludes archived applications; deterministic SQL only, no
  AI summarization (documented as such in controls-mapping.md).
- `tests/test_dashboard.py` — loads-with-no-data, root alias, and a
  metrics-correctness test (archived apps excluded, renewal shows in
  table, pending count reflects a real submitted request).
- Verified live: spend total cross-checked by hand against seed data
  ($375,600 — matches exactly), total/active counts verified against
  seed.py contents, pending-request count confirmed to update live after
  a real intake submission.
- `controls-mapping.md` — Phase 3 section filled in.

## Known test flakiness (observed, not fixed — see controls-mapping.md)
`test_list_applications_empty` has intermittently failed (~3 times across
40+ full-suite runs) in Claude's testing sandbox, across Phases 1–3.
Never reproducible in isolation or on demand despite deliberate attempts.
Likely a sandbox-specific timing artifact, not a real code defect — but
flagged honestly rather than dismissed. If Elle ever sees this fail on
her own machine, treat it as new information and investigate for real.

## UI note
Elle flagged the UI as plain/functional (default Bootstrap styling) —
agreed to defer a real UI/UX pass until after the data model and core
workflows settle (likely around Phase 4 or right before Phase 6), rather
than polish something that's still going to shift.

## Phase 2 additions
- New models: `SoftwareRequest`, `RequestAnswer`, `GovernanceReview` (+ 3 new
  enums: `CostType`, `RequestStatus`, `ReviewDecision`).
- New Blueprint `app/routes/requests.py` (`/requests` prefix): session-based
  name/email gate (`/requests/start`), public intake form (`/requests/new`),
  reviewer queue (`/requests/`), detail + follow-up Q&A + review decision
  (`/requests/<id>`), and convert-to-Application (`/requests/<id>/convert`).
- New templates: `requests/gate.html`, `intake_form.html`, `list.html`,
  `detail.html`. Nav links added to `base.html`.
- `tests/test_requests.py` — covers gate redirect, intake submission, full
  approve→convert flow, and rejecting conversion of an unapproved request.
  All 8 tests (4 Phase 1 + 4 Phase 2) pass reliably.
- Verified live end-to-end via real HTTP requests (not just pytest): gate →
  intake form → submission → detail page → review decision → convert to
  Application → new Application correctly shows derived data_classification.
- `controls-mapping.md` — Phase 2 section filled in.

## Design decisions specific to Phase 2
- `SoftwareRequest`'s own columns hold ONLY the requester's original
  self-reported answers — never edited after submission. Anything added
  during review (follow-up Q&A, decisions) goes in `RequestAnswer` /
  `GovernanceReview` instead. This separation is deliberate groundwork for
  Phase 7 (AI review) needing the same original-vs-reviewed distinction.
- `data_classification` on the resulting Application is derived by an
  explicit deterministic function (`_derive_data_classification` in
  routes/requests.py), documented as such — first concrete example of the
  "deterministic rules vs. AI observations" split Phase 9 will formalize.
- Name/email gate is session-based only, not real auth — explicitly a
  placeholder for Phase 6 (Entra ID).

Repo: https://github.com/aezechuk/saas-governance-registry
Local dev path: ~/projects/saas-governance-registry (moved off Downloads
due to macOS write-permission restrictions there — see "Gotchas" below).

## Decisions made
- Local development on Elle's Mac (MacBook Air) — no Azure VM for
  Phase 1–3. Azure VM/PostgreSQL/Container Apps deferred to Phase 4+
  where cloud infra is actually load-bearing (avoids unnecessary Azure
  credit spend).
- Infrastructure-as-code will use **Terraform**, not Bicep, once IaC is
  introduced (Phase 5+).
- Elle prefers Claude to write all code; she handles GitHub upload and
  deployment/ops steps herself.
- Local server default port is 5001, not 5000 (see Gotchas).

## What exists right now (Phase 1 — complete)
- `app/` — Flask app factory, models (Application, Integration,
  ApplicationIntegration, AuditLog), enums, routes (full CRUD +
  archive, search/filter), audit-log service, Bootstrap templates.
- `seed.py` — 12 sample applications + 2 sample integrations.
- `tests/test_applications.py` — pytest suite covering create, edit
  (+ audit log creation), archive (soft-delete), and list filtering.
  Passes reliably (5/5 repeated runs).
- `config.py`, `run.py`, `requirements.txt`, `.env.example`, `.gitignore`
- `controls-mapping.md` — framework/control mapping, Phase 1 section filled in.
- Confirmed in the browser: list, detail, create, edit (with audit
  log/Change History rendering correctly), and archive-not-delete all
  work as expected.

## Gotchas hit during Phase 1 setup (useful if similar issues recur)
1. **macOS write-permission restriction on ~/Downloads.** Running the
   project from ~/Downloads caused "unable to open database file" —
   macOS's TCC privacy protections block terminal apps from writing
   there by default. Fix: moved project to ~/projects/.
2. **venv breaks when the project folder is moved.** venv activation
   scripts hardcode absolute paths; moving the project folder requires
   deleting and recreating venv from scratch at the new location
   ("bad interpreter" error otherwise).
3. **Real root cause of the SQLite "unable to open database file"
   error (took several rounds to isolate):** `.env` had
   `DATABASE_URL=sqlite:///instance/app.db` (relative path). Flask-
   SQLAlchemy resolves relative SQLite URIs against `app.instance_path`,
   which is *already* the `instance/` folder — so the relative path
   doubled into `instance/instance/app.db`, which never existed. Fixed
   `.env` (and `.env.example`) to `DATABASE_URL=sqlite:///app.db`
   instead (no `instance/` prefix). Also hardened `config.py` to build
   an explicit absolute path and create the instance folder at import
   time (belt-and-suspenders, though the .env fix was the actual cause).
4. **Port 5000 conflict.** macOS's AirPlay Receiver commonly occupies
   port 5000. `run.py` now defaults to port 5001 (overridable via
   `PORT` env var).
5. **seed.py UNIQUE constraint failure on re-seed (hit during Phase 2
   setup).** `Application.query.delete()` / `Integration.query.delete()`
   are bulk deletes that bypass SQLAlchemy's ORM-level cascades, leaving
   orphaned `application_integrations` join-table rows behind. Re-seeding
   reused the same primary keys and collided with those orphaned rows.
   Fixed by explicitly deleting `ApplicationIntegration`, `AuditLog`,
   `GovernanceReview`, `RequestAnswer`, and `SoftwareRequest` first, in
   FK-safe order, before deleting `Application`/`Integration`.

## Not yet done (next steps)
Elle is pausing here for now — no urgency, she's just done with Azure-
adjacent work for the moment (Phase 4 Step 1 confirmed working was a
good stopping point after a bumpy setup). When she's ready to resume,
next is either Phase 4 Step 2 (Azure Postgres) or Phase 5
(Containerization) — her call which.

## Open questions for Elle
- None. Waiting on her to say when she wants to pick this back up.
# Build Progress

Purpose: if a Claude session or work session gets interrupted, read this
file first. It tells you exactly what's done and what the next concrete
step is, independent of chat history.

## Status: Phase 1 (Application Registry MVP) — DONE, CONFIRMED WORKING END-TO-END

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

## Not yet done (next steps)
Ready to start **Phase 2 — New Software Request Intake** whenever Elle
gives the go-ahead. Per her original instructions: propose the
SoftwareRequest / RequestAnswer / GovernanceReview data model and
relationships first, explain reasoning, before writing code — same
phased approach as Phase 1.

## Open questions for Elle
- None currently. Waiting on her signal to begin Phase 2.
# Build Progress

Purpose: if a Claude session or work session gets interrupted, read this
file first. It tells you exactly what's done and what the next concrete
step is, independent of chat history.

## Status: Phase 1 (Application Registry MVP) — CODE COMPLETE, NOT YET RUN/TESTED

## Decisions made
- Local development on Elle's Linux laptop — no Azure VM for Phase 1–3.
  Azure VM/PostgreSQL/Container Apps deferred to Phase 4+ where cloud
  infra is actually load-bearing (avoids unnecessary Azure credit spend).
- Infrastructure-as-code will use **Terraform**, not Bicep, once IaC is
  introduced (Phase 5+).
- Elle prefers Claude to write all code; she handles GitHub upload and
  deployment/ops steps herself.

## What exists right now
Full Phase 1 codebase, written but not yet run locally:
- `app/` — Flask app factory, models (Application, Integration,
  ApplicationIntegration, AuditLog), enums, routes (full CRUD +
  archive, search/filter), audit-log service, Bootstrap templates.
- `seed.py` — 12 sample applications + 2 sample integrations.
- `tests/test_applications.py` — pytest suite covering create, edit
  (+ audit log creation), archive (soft-delete), and list filtering.
- `config.py`, `run.py`, `requirements.txt`, `.env.example`, `.gitignore`
- `controls-mapping.md` — framework/control mapping, Phase 1 section filled in.

## Not yet done (next steps, in order)
1. Elle downloads the zipped project, unzips it locally, uploads to a
   new GitHub repo.
2. Local setup: create venv, `pip install -r requirements.txt`,
   copy `.env.example` to `.env`.
3. Run `python seed.py` to populate the database.
4. Run `python run.py`, verify the app loads at `http://localhost:5000/applications/`.
5. Run `python -m pytest tests/` to confirm tests pass.
6. Elle confirms Phase 1 works end-to-end → only then move to Phase 2
   (New Software Request Intake) per her explicit instruction not to
   proceed early.

## Open questions for Elle (ask before proceeding past Phase 1 confirmation)
- None currently — waiting on her to run and confirm Phase 1.

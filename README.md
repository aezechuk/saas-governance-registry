# SaaS / Application Governance Registry

An enterprise-style SaaS/Application Governance Registry built
progressively across 10 phases: inventory, intake workflow, dashboard,
PostgreSQL migration, containerized Azure deployment, Entra ID/RBAC,
AI-assisted (human-reviewed) governance review, discovery/imports, rule-based
governance intelligence, and RAG-grounded policy-aware AI.

Design decisions throughout are explicitly mapped to OWASP Web/API/LLM
Top 10, MITRE ATT&CK/ATLAS, NIST AI RMF, NIST 800-53, ISO 42001, and the
EU AI Act — see `controls-mapping.md`.

See `PROGRESS.md` for current build status and next steps.

## Phase 1 — Local Setup

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

cp .env.example .env
# edit .env if you want a different SECRET_KEY

python seed.py        # populates the database with sample applications
python run.py          # starts the app at http://localhost:5000
```

Visit `http://localhost:5000/applications/` in your browser.

Run tests with:

```bash
python -m pytest tests/
```

## Tech Stack (Phase 1)

- Python 3 / Flask
- SQLAlchemy ORM
- SQLite (development)
- Flask-WTF (CSRF protection)
- Bootstrap 5 (via CDN)

# Controls & Framework Mapping

This document maps design decisions in the SaaS Governance Registry to
specific controls/frameworks. It is updated at the end of each phase,
not written retroactively — the goal is to show *why* a design choice
was made, not to justify it after the fact.

Frameworks in scope: OWASP Web Top 10, OWASP API Top 10, OWASP LLM Top 10,
MITRE ATT&CK, MITRE ATLAS, NIST AI RMF, NIST 800-53, ISO 42001, EU AI Act.

---

## Phase 1 — Application Registry MVP

| Design decision | Framework / Control | Notes |
|---|---|---|
| SQLAlchemy ORM used for all queries (no raw SQL string interpolation) | OWASP Web Top 10 — A03 Injection | Parameterization is automatic via the ORM. |
| Flask-WTF CSRF protection enabled globally (`WTF_CSRF_ENABLED`) | OWASP Web Top 10 — A01 Broken Access Control (CSRF is a related risk) | Applied to every form (create/edit). |
| `AuditLog` table added in Phase 1, not deferred | NIST 800-53 — AU-3 (Content of Audit Records) | Tracks field-level changes: what changed, old/new value, who, when. |
| `created_at` / `updated_at` / `created_by` / `updated_by` on every Application row | NIST 800-53 — AU-3, AU-8 (Time Stamps) | `created_by`/`updated_by` are placeholder strings until Phase 6 introduces real user identity. |
| No hard delete — `is_archived` boolean instead | NIST 800-53 — AU-9 (Protection of Audit Information) / general data retention practice | Preserves history for audit and governance review even after an app is retired. |
| Controlled-vocabulary Enum fields instead of free text (status, discovery source, review status, YES/NO/UNKNOWN security fields) | NIST 800-53 — RA-3 (Risk Assessment) supportability | Free text would make Phase 3 dashboard queries and Phase 9 governance-intelligence rules unreliable. |
| Environment variables for `SECRET_KEY` / `DATABASE_URL`, `.env` gitignored | NIST 800-53 — SC-28 (Protection of Information at Rest), general secrets hygiene | No secrets committed to source control at any point. |
| `Application` ↔ `Integration` modeled as a proper many-to-many relationship (not a text field) | Groundwork for OWASP API Top 10 — API3 Broken Object Property Level Authorization (Phase 6+) | A queryable integrations table is what makes "which apps integrate with X" and later ownership/authorization checks possible. |

---

## Planned mapping for later phases (not yet built)

- **Phase 2 (Intake):** intake questions double as a lightweight risk-assessment intake — NIST 800-53 RA-2/RA-3.
- **Phase 4 (PostgreSQL):** TLS in transit, encryption at rest — NIST 800-53 SC-8, SC-28.
- **Phase 5 (Containers/Azure):** threat-model the deployment path against MITRE ATT&CK Cloud Matrix techniques (initial access via exposed endpoints, privilege escalation via misconfigured managed identity).
- **Phase 6 (Entra ID/RBAC):** role-scoped views become an API surface — OWASP API Top 10 (BOLA, excessive data exposure), NIST 800-53 AC-2/AC-3/IA-2.
- **Phase 7 (AI review):** OWASP LLM Top 10 (LLM01 Prompt Injection, LLM02 Insecure Output Handling, LLM06 Sensitive Information Disclosure, LLM08 Excessive Agency), MITRE ATLAS, NIST AI RMF (Govern/Map/Measure/Manage), ISO 42001, EU AI Act (expected classification: limited-risk, decision-support with mandatory human review — to be confirmed and documented explicitly when this phase is built).
- **Phase 8 (Imports/Discovery):** confidence/verification tracking on discovered records — NIST 800-53 CM-8(3).
- **Phase 9 (Governance Intelligence):** explicit separation of deterministic rules vs. AI-generated observations — NIST AI RMF Measure function.
- **Phase 10 (RAG):** poisoning risk on the retrieval corpus — MITRE ATLAS, OWASP LLM Top 10 (insecure plugin/tool design).

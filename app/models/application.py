"""
Application model — the core entity of the SaaS Governance Registry.

Design notes (see controls-mapping.md for framework alignment):

- Owner fields are split into name/email rather than a single free-text
  field, so that in Phase 6 (Entra ID) they can be converted to real
  foreign keys against a User table without a painful data migration.
- Status/source/classification fields use Python Enums instead of free
  text, per the project's "use dropdowns, not free text" requirement.
- `is_archived` is a dedicated boolean rather than an ApplicationStatus
  value, so archiving is orthogonal to workflow status (never a hard
  delete, per project requirements).
- `created_by` / `updated_by` are plain strings for now; they become
  real FKs to User once Entra ID auth exists in Phase 6.
"""

from datetime import datetime, timezone
from app import db
from app.models.enums import (
    ApplicationStatus,
    DiscoverySource,
    ReviewStatus,
    ContractStatus,
    YesNoUnknown,
    DataClassification,
)


class Application(db.Model):
    __tablename__ = "applications"

    id = db.Column(db.Integer, primary_key=True)

    # Core identity
    application_name = db.Column(db.String(200), nullable=False)
    vendor = db.Column(db.String(200), nullable=True)
    description = db.Column(db.Text, nullable=True)

    # Ownership (split name/email — see module docstring)
    business_owner_name = db.Column(db.String(150), nullable=True)
    business_owner_email = db.Column(db.String(200), nullable=True)
    technical_owner_name = db.Column(db.String(150), nullable=True)
    technical_owner_email = db.Column(db.String(200), nullable=True)
    department = db.Column(db.String(150), nullable=True)

    # Workflow / lifecycle
    application_status = db.Column(
        db.Enum(ApplicationStatus), default=ApplicationStatus.REQUESTED, nullable=False
    )
    discovery_source = db.Column(
        db.Enum(DiscoverySource), default=DiscoverySource.MANUAL, nullable=False
    )
    is_archived = db.Column(db.Boolean, default=False, nullable=False)

    # Usage / cost
    estimated_users = db.Column(db.Integer, nullable=True)
    license_count = db.Column(db.Integer, nullable=True)
    estimated_annual_cost = db.Column(db.Numeric(12, 2), nullable=True)
    renewal_date = db.Column(db.Date, nullable=True)
    contract_status = db.Column(
        db.Enum(ContractStatus), default=ContractStatus.NONE, nullable=True
    )

    # Security posture
    sso_supported = db.Column(db.Enum(YesNoUnknown), default=YesNoUnknown.UNKNOWN)
    sso_enabled = db.Column(db.Enum(YesNoUnknown), default=YesNoUnknown.UNKNOWN)
    mfa_supported = db.Column(db.Enum(YesNoUnknown), default=YesNoUnknown.UNKNOWN)
    mfa_enforced = db.Column(db.Enum(YesNoUnknown), default=YesNoUnknown.UNKNOWN)
    scim_supported = db.Column(db.Enum(YesNoUnknown), default=YesNoUnknown.UNKNOWN)

    data_classification = db.Column(
        db.Enum(DataClassification), default=DataClassification.UNKNOWN
    )

    # Governance
    review_status = db.Column(
        db.Enum(ReviewStatus), default=ReviewStatus.NOT_REVIEWED, nullable=False
    )
    first_seen = db.Column(db.Date, nullable=True)
    last_reviewed = db.Column(db.Date, nullable=True)

    # Audit-friendly timestamps
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )
    created_by = db.Column(db.String(150), nullable=True)
    updated_by = db.Column(db.String(150), nullable=True)

    # Relationships
    audit_logs = db.relationship(
        "AuditLog", backref="application", cascade="all, delete-orphan"
    )
    integration_links = db.relationship(
        "ApplicationIntegration", backref="application", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Application {self.application_name}>"

"""
Integration model + the join table linking Applications to Integrations.

This is a many-to-many relationship rather than a free-text field on
Application because Phase 9 (governance intelligence) needs to query
things like "applications with unknown integration ownership" and
"duplicate/overlapping tools" — that's not possible against a text blob.
"""

from datetime import datetime, timezone
from app import db
from app.models.enums import IntegrationCategory


class Integration(db.Model):
    __tablename__ = "integrations"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False, unique=True)
    category = db.Column(db.Enum(IntegrationCategory), nullable=True)
    notes = db.Column(db.Text, nullable=True)

    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    def __repr__(self):
        return f"<Integration {self.name}>"


class ApplicationIntegration(db.Model):
    """Join table between Application and Integration.

    `verified` distinguishes a confirmed integration from one that was
    discovered/assumed but not yet checked — important groundwork for
    Phase 8 (discovery/imports) confidence tracking.
    """

    __tablename__ = "application_integrations"

    id = db.Column(db.Integer, primary_key=True)
    application_id = db.Column(
        db.Integer, db.ForeignKey("applications.id"), nullable=False
    )
    integration_id = db.Column(
        db.Integer, db.ForeignKey("integrations.id"), nullable=False
    )
    verified = db.Column(db.Boolean, default=False, nullable=False)
    notes = db.Column(db.Text, nullable=True)

    integration = db.relationship("Integration", backref="application_links")

    __table_args__ = (
        db.UniqueConstraint(
            "application_id", "integration_id", name="uq_app_integration"
        ),
    )

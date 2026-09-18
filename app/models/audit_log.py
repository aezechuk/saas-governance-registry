"""
AuditLog model.

Added in Phase 1 rather than deferred to Phase 6, because retrofitting
audit history onto a database that already has real data in it is far
more painful than building it in from the start. This is also the
first concrete piece of evidence toward NIST 800-53 AU-3
(content of audit records) for this project.
"""

from datetime import datetime, timezone
from app import db


class AuditLog(db.Model):
    __tablename__ = "audit_logs"

    id = db.Column(db.Integer, primary_key=True)
    application_id = db.Column(
        db.Integer, db.ForeignKey("applications.id"), nullable=False
    )
    field_changed = db.Column(db.String(100), nullable=False)
    old_value = db.Column(db.Text, nullable=True)
    new_value = db.Column(db.Text, nullable=True)
    changed_by = db.Column(db.String(150), nullable=True)  # becomes a real FK to User in Phase 6
    changed_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    def __repr__(self):
        return f"<AuditLog app={self.application_id} field={self.field_changed}>"

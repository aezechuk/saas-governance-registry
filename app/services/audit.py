"""
Shared helper for writing AuditLog entries.

Kept as a service function (not scattered inline in routes) so that
every part of the app that changes an Application logs changes the
same way — this consistency matters for the AU-3 control evidence
this table is meant to provide.
"""

from app import db
from app.models import AuditLog


def log_changes(application_id, changes, changed_by=None):
    """changes: list of (field_name, old_value, new_value) tuples."""
    for field_name, old_value, new_value in changes:
        entry = AuditLog(
            application_id=application_id,
            field_changed=field_name,
            old_value=str(old_value) if old_value is not None else None,
            new_value=str(new_value) if new_value is not None else None,
            changed_by=changed_by,
        )
        db.session.add(entry)

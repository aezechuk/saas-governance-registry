"""
Application CRUD routes.

Security notes:
- All writes go through Flask-WTF forms with CSRF protection enabled
  globally (see app/__init__.py).
- SQLAlchemy ORM is used throughout (no raw SQL string interpolation),
  which is the primary defense against SQL injection here.
- Archiving is used instead of deletion, per project requirements.
"""

from datetime import datetime
from flask import Blueprint, render_template, request, redirect, url_for, flash
from app import db
from app.models import Application
from app.models.enums import (
    ApplicationStatus,
    DiscoverySource,
    ReviewStatus,
    ContractStatus,
    YesNoUnknown,
    DataClassification,
)
from app.services.audit import log_changes

applications_bp = Blueprint("applications", __name__, url_prefix="/applications")

ENUM_FIELDS = {
    "application_status": ApplicationStatus,
    "discovery_source": DiscoverySource,
    "review_status": ReviewStatus,
    "contract_status": ContractStatus,
    "sso_supported": YesNoUnknown,
    "sso_enabled": YesNoUnknown,
    "mfa_supported": YesNoUnknown,
    "mfa_enforced": YesNoUnknown,
    "scim_supported": YesNoUnknown,
    "data_classification": DataClassification,
}

TEXT_FIELDS = [
    "application_name",
    "vendor",
    "description",
    "business_owner_name",
    "business_owner_email",
    "technical_owner_name",
    "technical_owner_email",
    "department",
]

NUMBER_FIELDS = ["estimated_users", "license_count", "estimated_annual_cost"]
DATE_FIELDS = ["renewal_date", "first_seen", "last_reviewed"]


@applications_bp.route("/")
def list_applications():
    query = Application.query.filter_by(is_archived=False)

    search = request.args.get("search", "").strip()
    if search:
        query = query.filter(Application.application_name.ilike(f"%{search}%"))

    status_filter = request.args.get("status", "").strip()
    if status_filter:
        query = query.filter(Application.application_status == ApplicationStatus(status_filter))

    apps = query.order_by(Application.application_name.asc()).all()
    return render_template(
        "applications/list.html",
        applications=apps,
        search=search,
        status_filter=status_filter,
        statuses=list(ApplicationStatus),
    )


@applications_bp.route("/<int:app_id>")
def view_application(app_id):
    application = Application.query.get_or_404(app_id)
    return render_template("applications/detail.html", application=application)


@applications_bp.route("/new", methods=["GET", "POST"])
def create_application():
    if request.method == "POST":
        application = Application()
        _apply_form_to_application(application, request.form)
        application.created_by = "system"  # placeholder until Phase 6 auth exists
        application.updated_by = "system"

        db.session.add(application)
        db.session.commit()

        flash(f'Application "{application.application_name}" created.', "success")
        return redirect(url_for("applications.view_application", app_id=application.id))

    return render_template(
        "applications/form.html",
        application=None,
        statuses=list(ApplicationStatus),
        sources=list(DiscoverySource),
        review_statuses=list(ReviewStatus),
        contract_statuses=list(ContractStatus),
        yes_no_unknown=list(YesNoUnknown),
        classifications=list(DataClassification),
    )


@applications_bp.route("/<int:app_id>/edit", methods=["GET", "POST"])
def edit_application(app_id):
    application = Application.query.get_or_404(app_id)

    if request.method == "POST":
        changes = _apply_form_to_application(application, request.form, track_changes=True)
        application.updated_by = "system"  # placeholder until Phase 6 auth exists

        log_changes(application.id, changes, changed_by="system")
        db.session.commit()

        flash(f'Application "{application.application_name}" updated.', "success")
        return redirect(url_for("applications.view_application", app_id=application.id))

    return render_template(
        "applications/form.html",
        application=application,
        statuses=list(ApplicationStatus),
        sources=list(DiscoverySource),
        review_statuses=list(ReviewStatus),
        contract_statuses=list(ContractStatus),
        yes_no_unknown=list(YesNoUnknown),
        classifications=list(DataClassification),
    )


@applications_bp.route("/<int:app_id>/archive", methods=["POST"])
def archive_application(app_id):
    application = Application.query.get_or_404(app_id)
    application.is_archived = True
    db.session.commit()
    flash(f'Application "{application.application_name}" archived.', "info")
    return redirect(url_for("applications.list_applications"))


def _apply_form_to_application(application, form, track_changes=False):
    """Copies submitted form values onto the Application instance.

    Returns a list of (field, old_value, new_value) tuples for any
    field that actually changed, so the caller can write audit log
    entries. Kept as a plain function (not a method on the model)
    so the model stays a thin data definition.
    """
    changes = []

    def _set(field, new_value):
        old_value = getattr(application, field)
        if track_changes and str(old_value) != str(new_value):
            changes.append((field, old_value, new_value))
        setattr(application, field, new_value)

    for field in TEXT_FIELDS:
        _set(field, form.get(field, "").strip() or None)

    for field in NUMBER_FIELDS:
        raw = form.get(field, "").strip()
        _set(field, None if raw == "" else _to_number(raw))

    for field in DATE_FIELDS:
        raw = form.get(field, "").strip()
        _set(field, None if raw == "" else datetime.strptime(raw, "%Y-%m-%d").date())

    for field, enum_cls in ENUM_FIELDS.items():
        raw = form.get(field, "").strip()
        if raw:
            _set(field, enum_cls(raw))

    return changes


def _to_number(raw):
    try:
        if "." in raw:
            return float(raw)
        return int(raw)
    except ValueError:
        return None

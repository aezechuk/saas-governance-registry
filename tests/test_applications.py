"""
Basic CRUD tests for the Application model and routes.

Run with:
    python -m pytest tests/
"""

import pytest
from app import create_app, db
from app.models import Application


@pytest.fixture
def app():
    flask_app = create_app("development")
    flask_app.config.update(
        SQLALCHEMY_DATABASE_URI="sqlite:///:memory:",
        TESTING=True,
        WTF_CSRF_ENABLED=False,  # simplifies posting forms in tests
    )
    with flask_app.app_context():
        db.create_all()
        yield flask_app
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


def test_list_applications_empty(client):
    response = client.get("/applications/")
    assert response.status_code == 200
    assert b"No applications found" in response.data


def test_create_application(client, app):
    response = client.post(
        "/applications/new",
        data={"application_name": "Test App", "vendor": "Test Vendor"},
        follow_redirects=True,
    )
    assert response.status_code == 200
    with app.app_context():
        app_obj = Application.query.filter_by(application_name="Test App").first()
        assert app_obj is not None
        assert app_obj.vendor == "Test Vendor"
        assert app_obj.is_archived is False


def test_edit_application_creates_audit_log(client, app):
    with app.app_context():
        application = Application(application_name="Original Name")
        db.session.add(application)
        db.session.commit()
        app_id = application.id

    client.post(
        f"/applications/{app_id}/edit",
        data={"application_name": "Updated Name"},
        follow_redirects=True,
    )

    with app.app_context():
        updated = Application.query.get(app_id)
        assert updated.application_name == "Updated Name"
        assert len(updated.audit_logs) == 1
        assert updated.audit_logs[0].field_changed == "application_name"
        assert updated.audit_logs[0].old_value == "Original Name"
        assert updated.audit_logs[0].new_value == "Updated Name"


def test_archive_application_does_not_delete(client, app):
    with app.app_context():
        application = Application(application_name="To Archive")
        db.session.add(application)
        db.session.commit()
        app_id = application.id

    client.post(f"/applications/{app_id}/archive", follow_redirects=True)

    with app.app_context():
        archived = Application.query.get(app_id)
        assert archived is not None  # still exists
        assert archived.is_archived is True

    # Archived apps should not show in the default list view
    response = client.get("/applications/")
    assert b"To Archive" not in response.data

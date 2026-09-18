"""
Seeds the database with sample applications so the UI is useful
immediately, per Phase 1 requirements. Safe to re-run: it clears
existing Application rows first.

Usage:
    python seed.py
"""

from datetime import date
from app import create_app, db
from app.models import Application, Integration, ApplicationIntegration
from app.models.enums import (
    ApplicationStatus,
    DiscoverySource,
    ReviewStatus,
    ContractStatus,
    YesNoUnknown,
    DataClassification,
    IntegrationCategory,
)

app = create_app()

SAMPLE_APPS = [
    dict(
        application_name="Slack", vendor="Salesforce (Slack Technologies)",
        description="Team messaging and collaboration.",
        business_owner_name="Dana Reyes", business_owner_email="dana.reyes@example.com",
        technical_owner_name="Marcus Lee", technical_owner_email="marcus.lee@example.com",
        department="IT", application_status=ApplicationStatus.ACTIVE,
        discovery_source=DiscoverySource.ENTRA_ID, estimated_users=420, license_count=450,
        estimated_annual_cost=54000.00, renewal_date=date(2027, 3, 1),
        contract_status=ContractStatus.ACTIVE, sso_supported=YesNoUnknown.YES,
        sso_enabled=YesNoUnknown.YES, mfa_supported=YesNoUnknown.YES,
        mfa_enforced=YesNoUnknown.YES, scim_supported=YesNoUnknown.YES,
        data_classification=DataClassification.INTERNAL,
        review_status=ReviewStatus.APPROVED, first_seen=date(2022, 1, 15),
        last_reviewed=date(2026, 6, 1),
    ),
    dict(
        application_name="Canva", vendor="Canva Pty Ltd",
        description="Graphic design tool for marketing materials.",
        business_owner_name="Priya Nair", business_owner_email="priya.nair@example.com",
        technical_owner_name=None, technical_owner_email=None,
        department="Marketing", application_status=ApplicationStatus.ACTIVE,
        discovery_source=DiscoverySource.DEPARTMENT_INTERVIEW, estimated_users=12,
        license_count=15, estimated_annual_cost=1800.00, renewal_date=date(2026, 11, 20),
        contract_status=ContractStatus.ACTIVE, sso_supported=YesNoUnknown.YES,
        sso_enabled=YesNoUnknown.NO, mfa_supported=YesNoUnknown.YES,
        mfa_enforced=YesNoUnknown.UNKNOWN, scim_supported=YesNoUnknown.NO,
        data_classification=DataClassification.PUBLIC,
        review_status=ReviewStatus.INCOMPLETE, first_seen=date(2023, 5, 10),
        last_reviewed=None,
    ),
    dict(
        application_name="Zyston SOC Portal (Legacy)", vendor="Internal",
        description="Legacy internal SOC case management tool, being phased out.",
        business_owner_name="Tom Whitfield", business_owner_email="tom.whitfield@example.com",
        technical_owner_name="Elle Ezechukwu", technical_owner_email="elle@example.com",
        department="Security", application_status=ApplicationStatus.DEPRECATED,
        discovery_source=DiscoverySource.MANUAL, estimated_users=8, license_count=8,
        estimated_annual_cost=0.00, renewal_date=None, contract_status=ContractStatus.NONE,
        sso_supported=YesNoUnknown.NO, sso_enabled=YesNoUnknown.NO,
        mfa_supported=YesNoUnknown.NO, mfa_enforced=YesNoUnknown.NO,
        scim_supported=YesNoUnknown.NO, data_classification=DataClassification.CONFIDENTIAL,
        review_status=ReviewStatus.ADDITIONAL_REVIEW_REQUIRED, first_seen=date(2019, 2, 1),
        last_reviewed=date(2025, 1, 10),
    ),
    dict(
        application_name="Notion", vendor="Notion Labs",
        description="Docs, wiki, and project tracking.",
        business_owner_name=None, business_owner_email=None,
        technical_owner_name=None, technical_owner_email=None,
        department="Operations", application_status=ApplicationStatus.PILOT,
        discovery_source=DiscoverySource.MANUAL, estimated_users=25, license_count=30,
        estimated_annual_cost=3600.00, renewal_date=date(2027, 1, 5),
        contract_status=ContractStatus.ACTIVE, sso_supported=YesNoUnknown.YES,
        sso_enabled=YesNoUnknown.UNKNOWN, mfa_supported=YesNoUnknown.UNKNOWN,
        mfa_enforced=YesNoUnknown.UNKNOWN, scim_supported=YesNoUnknown.UNKNOWN,
        data_classification=DataClassification.INTERNAL,
        review_status=ReviewStatus.NOT_REVIEWED, first_seen=date(2026, 2, 1),
        last_reviewed=None,
    ),
    dict(
        application_name="ADP Workforce Now", vendor="ADP",
        description="Payroll and HR platform.",
        business_owner_name="Karen Ibe", business_owner_email="karen.ibe@example.com",
        technical_owner_name="Marcus Lee", technical_owner_email="marcus.lee@example.com",
        department="HR", application_status=ApplicationStatus.ACTIVE,
        discovery_source=DiscoverySource.CONTRACT_REVIEW, estimated_users=600,
        license_count=600, estimated_annual_cost=96000.00, renewal_date=date(2026, 12, 31),
        contract_status=ContractStatus.PENDING_RENEWAL, sso_supported=YesNoUnknown.YES,
        sso_enabled=YesNoUnknown.YES, mfa_supported=YesNoUnknown.YES,
        mfa_enforced=YesNoUnknown.YES, scim_supported=YesNoUnknown.YES,
        data_classification=DataClassification.EMPLOYEE_DATA,
        review_status=ReviewStatus.APPROVED, first_seen=date(2020, 6, 1),
        last_reviewed=date(2026, 5, 1),
    ),
    dict(
        application_name="Figma", vendor="Figma Inc.",
        description="UI/UX design and prototyping.",
        business_owner_name="Priya Nair", business_owner_email="priya.nair@example.com",
        technical_owner_name=None, technical_owner_email=None,
        department="Product", application_status=ApplicationStatus.ACTIVE,
        discovery_source=DiscoverySource.FINANCE, estimated_users=18, license_count=20,
        estimated_annual_cost=9600.00, renewal_date=date(2027, 4, 15),
        contract_status=ContractStatus.ACTIVE, sso_supported=YesNoUnknown.YES,
        sso_enabled=YesNoUnknown.YES, mfa_supported=YesNoUnknown.YES,
        mfa_enforced=YesNoUnknown.UNKNOWN, scim_supported=YesNoUnknown.YES,
        data_classification=DataClassification.INTERNAL,
        review_status=ReviewStatus.IN_REVIEW, first_seen=date(2023, 8, 20),
        last_reviewed=date(2025, 8, 1),
    ),
    dict(
        application_name="Random Free PDF Tool", vendor="Unknown",
        description="Found via endpoint scan, purpose unclear.",
        business_owner_name=None, business_owner_email=None,
        technical_owner_name=None, technical_owner_email=None,
        department=None, application_status=ApplicationStatus.REQUESTED,
        discovery_source=DiscoverySource.ENDPOINT_INVENTORY, estimated_users=None,
        license_count=None, estimated_annual_cost=None, renewal_date=None,
        contract_status=ContractStatus.NONE, sso_supported=YesNoUnknown.UNKNOWN,
        sso_enabled=YesNoUnknown.UNKNOWN, mfa_supported=YesNoUnknown.UNKNOWN,
        mfa_enforced=YesNoUnknown.UNKNOWN, scim_supported=YesNoUnknown.UNKNOWN,
        data_classification=DataClassification.UNKNOWN,
        review_status=ReviewStatus.NOT_REVIEWED, first_seen=date(2026, 8, 30),
        last_reviewed=None,
    ),
    dict(
        application_name="Salesforce Sales Cloud", vendor="Salesforce",
        description="CRM platform for sales pipeline management.",
        business_owner_name="Greg Talbot", business_owner_email="greg.talbot@example.com",
        technical_owner_name="Marcus Lee", technical_owner_email="marcus.lee@example.com",
        department="Sales", application_status=ApplicationStatus.ACTIVE,
        discovery_source=DiscoverySource.ENTRA_ID, estimated_users=85, license_count=90,
        estimated_annual_cost=162000.00, renewal_date=date(2027, 2, 28),
        contract_status=ContractStatus.ACTIVE, sso_supported=YesNoUnknown.YES,
        sso_enabled=YesNoUnknown.YES, mfa_supported=YesNoUnknown.YES,
        mfa_enforced=YesNoUnknown.YES, scim_supported=YesNoUnknown.YES,
        data_classification=DataClassification.CUSTOMER_DATA,
        review_status=ReviewStatus.APPROVED, first_seen=date(2021, 3, 1),
        last_reviewed=date(2026, 4, 15),
    ),
    dict(
        application_name="QuickBooks Online", vendor="Intuit",
        description="Accounting and bookkeeping platform.",
        business_owner_name="Karen Ibe", business_owner_email="karen.ibe@example.com",
        technical_owner_name=None, technical_owner_email=None,
        department="Finance", application_status=ApplicationStatus.ACTIVE,
        discovery_source=DiscoverySource.FINANCE, estimated_users=6, license_count=6,
        estimated_annual_cost=4200.00, renewal_date=date(2027, 1, 10),
        contract_status=ContractStatus.ACTIVE, sso_supported=YesNoUnknown.NO,
        sso_enabled=YesNoUnknown.NO, mfa_supported=YesNoUnknown.YES,
        mfa_enforced=YesNoUnknown.YES, scim_supported=YesNoUnknown.NO,
        data_classification=DataClassification.FINANCIAL_DATA,
        review_status=ReviewStatus.APPROVED, first_seen=date(2020, 1, 1),
        last_reviewed=date(2025, 12, 1),
    ),
    dict(
        application_name="Miro", vendor="Miro Inc.",
        description="Online whiteboard for workshops and planning.",
        business_owner_name=None, business_owner_email=None,
        technical_owner_name=None, technical_owner_email=None,
        department="Product", application_status=ApplicationStatus.RESTRICTED,
        discovery_source=DiscoverySource.DEPARTMENT_INTERVIEW, estimated_users=30,
        license_count=10, estimated_annual_cost=2400.00, renewal_date=date(2026, 10, 1),
        contract_status=ContractStatus.ACTIVE, sso_supported=YesNoUnknown.YES,
        sso_enabled=YesNoUnknown.NO, mfa_supported=YesNoUnknown.UNKNOWN,
        mfa_enforced=YesNoUnknown.UNKNOWN, scim_supported=YesNoUnknown.UNKNOWN,
        data_classification=DataClassification.INTERNAL,
        review_status=ReviewStatus.ADDITIONAL_REVIEW_REQUIRED, first_seen=date(2024, 6, 1),
        last_reviewed=date(2026, 1, 5),
    ),
    dict(
        application_name="Zoom", vendor="Zoom Video Communications",
        description="Video conferencing.",
        business_owner_name="Dana Reyes", business_owner_email="dana.reyes@example.com",
        technical_owner_name="Marcus Lee", technical_owner_email="marcus.lee@example.com",
        department="IT", application_status=ApplicationStatus.ACTIVE,
        discovery_source=DiscoverySource.ENTRA_ID, estimated_users=650, license_count=700,
        estimated_annual_cost=42000.00, renewal_date=date(2027, 5, 1),
        contract_status=ContractStatus.ACTIVE, sso_supported=YesNoUnknown.YES,
        sso_enabled=YesNoUnknown.YES, mfa_supported=YesNoUnknown.YES,
        mfa_enforced=YesNoUnknown.YES, scim_supported=YesNoUnknown.YES,
        data_classification=DataClassification.INTERNAL,
        review_status=ReviewStatus.APPROVED, first_seen=date(2020, 3, 15),
        last_reviewed=date(2026, 3, 1),
    ),
    dict(
        application_name="Trello", vendor="Atlassian",
        description="Lightweight project/task boards, used ad hoc by a few teams.",
        business_owner_name=None, business_owner_email=None,
        technical_owner_name=None, technical_owner_email=None,
        department=None, application_status=ApplicationStatus.REQUESTED,
        discovery_source=DiscoverySource.CSV_IMPORT, estimated_users=None,
        license_count=None, estimated_annual_cost=None, renewal_date=None,
        contract_status=ContractStatus.NONE, sso_supported=YesNoUnknown.UNKNOWN,
        sso_enabled=YesNoUnknown.UNKNOWN, mfa_supported=YesNoUnknown.UNKNOWN,
        mfa_enforced=YesNoUnknown.UNKNOWN, scim_supported=YesNoUnknown.UNKNOWN,
        data_classification=DataClassification.UNKNOWN,
        review_status=ReviewStatus.NOT_REVIEWED, first_seen=date(2026, 7, 1),
        last_reviewed=None,
    ),
]


def run():
    with app.app_context():
        db.create_all()

        # Bulk .delete() bypasses SQLAlchemy's ORM-level cascades, so
        # child/join tables must be cleared explicitly and in FK-safe
        # order, or re-seeding collides with orphaned rows from a
        # previous run (e.g. application_integrations rows left
        # pointing at IDs that get reused).
        from app.models import AuditLog, ApplicationIntegration
        from app.models import SoftwareRequest, RequestAnswer, GovernanceReview

        ApplicationIntegration.query.delete()
        AuditLog.query.delete()
        GovernanceReview.query.delete()
        RequestAnswer.query.delete()
        SoftwareRequest.query.delete()
        Application.query.delete()
        Integration.query.delete()
        db.session.commit()

        created = []
        for data in SAMPLE_APPS:
            application = Application(**data, created_by="seed_script", updated_by="seed_script")
            db.session.add(application)
            created.append(application)
        db.session.commit()

        # A couple of sample integrations, linked to a couple of apps,
        # to exercise the many-to-many relationship.
        email_integration = Integration(name="Company Email (M365)", category=IntegrationCategory.EMAIL)
        calendar_integration = Integration(name="Company Calendar (M365)", category=IntegrationCategory.CALENDAR)
        db.session.add_all([email_integration, calendar_integration])
        db.session.commit()

        slack = next(a for a in created if a.application_name == "Slack")
        zoom = next(a for a in created if a.application_name == "Zoom")

        db.session.add_all([
            ApplicationIntegration(application_id=slack.id, integration_id=email_integration.id, verified=True),
            ApplicationIntegration(application_id=zoom.id, integration_id=calendar_integration.id, verified=True),
        ])
        db.session.commit()

        print(f"Seeded {len(created)} applications and 2 integrations.")


if __name__ == "__main__":
    run()

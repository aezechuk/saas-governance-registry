"""
Enum definitions for controlled-vocabulary fields on Application.

Using Python Enums (rather than free text) keeps the data consistent
and makes dashboard/reporting queries (Phase 3) reliable — you cannot
group or filter cleanly on inconsistent free-text values like
"Active", "active", "ACTIVE ".
"""

import enum


class ApplicationStatus(enum.Enum):
    REQUESTED = "Requested"
    PILOT = "Pilot"
    APPROVED = "Approved"
    ACTIVE = "Active"
    RESTRICTED = "Restricted"
    DEPRECATED = "Deprecated"
    ARCHIVED = "Archived"


class DiscoverySource(enum.Enum):
    MANUAL = "Manual"
    ENTRA_ID = "Entra ID"
    ENDPOINT_INVENTORY = "Endpoint inventory"
    FINANCE = "Finance"
    PROCUREMENT = "Procurement"
    CONTRACT_REVIEW = "Contract review"
    DEPARTMENT_INTERVIEW = "Department interview"
    CSV_IMPORT = "CSV import"
    OTHER = "Other"


class ReviewStatus(enum.Enum):
    NOT_REVIEWED = "Not reviewed"
    INCOMPLETE = "Incomplete"
    IN_REVIEW = "In review"
    APPROVED = "Approved"
    ADDITIONAL_REVIEW_REQUIRED = "Additional review required"
    REJECTED = "Rejected"


class ContractStatus(enum.Enum):
    NONE = "No contract"
    ACTIVE = "Active contract"
    PENDING_RENEWAL = "Pending renewal"
    EXPIRED = "Expired"
    CANCELLED = "Cancelled"


class YesNoUnknown(enum.Enum):
    YES = "Yes"
    NO = "No"
    UNKNOWN = "Unknown"


class DataClassification(enum.Enum):
    PUBLIC = "Public"
    INTERNAL = "Internal"
    CONFIDENTIAL = "Confidential"
    CUSTOMER_DATA = "Customer data"
    EMPLOYEE_DATA = "Employee data"
    FINANCIAL_DATA = "Financial data"
    UNKNOWN = "Unknown"


class IntegrationCategory(enum.Enum):
    EMAIL = "Email"
    CALENDAR = "Calendar"
    FILES = "Files"
    DATABASE = "Database"
    API = "API"
    CLOUD_RESOURCES = "Cloud resources"
    OTHER = "Other"

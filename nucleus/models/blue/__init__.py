"""BLUE — advance-tax copilot (repo ``at-copilot``).

Clients email advance-tax documents to an intake mailbox. BLUE matches each
document to a client, extracts the figures, reviews the quarter against last
quarter, briefs the RM on Teams, drafts RM-approved client emails and writes
approved inputs into advance tax. These tables hold all of that state so the
agent itself stays stateless.

Design: https://github.com/Billion-BaseCamp/at-copilot/blob/main/docs/DESIGN.md

Generate the tables with Alembic autogenerate. Do not hand-write the migration.
"""

from nucleus.models.blue.constants import (
    BLUE_APPROVAL_KINDS,
    BLUE_APPROVAL_STATUSES,
    BLUE_DOCUMENT_TYPES,
    BLUE_EMAIL_STATUSES,
    BLUE_EXTRACTION_STATUSES,
    BLUE_MATCH_STATUSES,
    BLUE_REVIEW_READINESS,
)
from nucleus.models.blue.intake import BlueIntakeDocument, BlueIntakeMessage
from nucleus.models.blue.extraction import BlueExtractedField, BlueExtraction
from nucleus.models.blue.review import BlueQuarterReview
from nucleus.models.blue.outreach import BlueApproval, BlueClientEmail
from nucleus.models.blue.audit import BlueEvent, BlueRmIdentity

__all__ = [
    "BLUE_APPROVAL_KINDS",
    "BLUE_APPROVAL_STATUSES",
    "BLUE_DOCUMENT_TYPES",
    "BLUE_EMAIL_STATUSES",
    "BLUE_EXTRACTION_STATUSES",
    "BLUE_MATCH_STATUSES",
    "BLUE_REVIEW_READINESS",
    "BlueApproval",
    "BlueClientEmail",
    "BlueEvent",
    "BlueExtractedField",
    "BlueExtraction",
    "BlueIntakeDocument",
    "BlueIntakeMessage",
    "BlueQuarterReview",
    "BlueRmIdentity",
]

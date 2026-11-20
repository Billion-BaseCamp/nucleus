"""Allowed values for BLUE status columns.

Stored as plain strings with CHECK constraints (not native PG enums): adding a
value is a one-line constraint change instead of an ALTER TYPE, and
autogenerate handles CHECKs predictably.
"""


def check_in(column: str, values: tuple[str, ...]) -> str:
    """SQL for ``column IN (...)`` used by CheckConstraint."""
    quoted = ", ".join(f"'{v}'" for v in values)
    return f"{column} IN ({quoted})"


BLUE_DOCUMENT_TYPES = (
    "form16",
    "capital_gains_statement",
    "ais",
    "form26as",
    "interest_certificate",
    "rent_receipt",
    "email_body",
    "other",
    "unknown",
)

# matched: high-confidence, no RM step. needs_rm_confirm: low confidence or
# conflicting evidence. unmatched: no candidate. rejected: RM said "not ours".
BLUE_MATCH_STATUSES = ("pending", "matched", "needs_rm_confirm", "rm_confirmed", "unmatched", "rejected")

BLUE_EXTRACTION_STATUSES = ("queued", "running", "succeeded", "failed", "skipped", "superseded")

BLUE_REVIEW_READINESS = ("collecting", "needs_client_input", "needs_rm_review", "ready", "written_back")

BLUE_EMAIL_STATUSES = ("draft", "pending_approval", "approved", "sent", "discarded", "failed")

BLUE_APPROVAL_KINDS = ("client_match", "client_email", "write_back", "figure_correction")
BLUE_APPROVAL_STATUSES = ("pending", "approved", "rejected", "expired")

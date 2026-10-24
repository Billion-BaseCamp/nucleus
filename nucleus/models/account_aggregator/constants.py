"""Canonical status vocabularies for the Account Aggregator integration.

Finsense uses two different words for the same consent state depending on which
API you ask: the consent callback says ``ACTIVE`` while the status GET says
``ACCEPTED``. Normalising in exactly one place keeps that ambiguity out of every
other module — see ``normalize_consent_status``.
"""

from __future__ import annotations

# --- Consent lifecycle (our canonical vocabulary) ---------------------------
CONSENT_REQUESTED = "REQUESTED"  # row written before the API call
CONSENT_PENDING = "PENDING"  # handle issued, customer has not decided
CONSENT_ACTIVE = "ACTIVE"  # approved and usable
CONSENT_REJECTED = "REJECTED"  # customer declined
CONSENT_REVOKED = "REVOKED"  # withdrawn after approval
CONSENT_EXPIRED = "EXPIRED"  # past consent_expiry
CONSENT_FAILED = "FAILED"  # request could not be raised
CONSENT_RENEW_REQUIRED = "RENEW_REQUIRED"

CONSENT_STATUSES = frozenset(
    {
        CONSENT_REQUESTED,
        CONSENT_PENDING,
        CONSENT_ACTIVE,
        CONSENT_REJECTED,
        CONSENT_REVOKED,
        CONSENT_EXPIRED,
        CONSENT_FAILED,
        CONSENT_RENEW_REQUIRED,
    }
)

#: Consents that may still be used to fetch data.
CONSENT_USABLE_STATUSES = frozenset({CONSENT_ACTIVE})

#: Terminal states — never retry, never re-poll.
CONSENT_TERMINAL_STATUSES = frozenset(
    {CONSENT_REJECTED, CONSENT_REVOKED, CONSENT_EXPIRED, CONSENT_FAILED}
)

#: Vendor spelling -> ours. ``ACCEPTED`` and ``ACTIVE`` are the same state.
_CONSENT_ALIASES = {
    "ACCEPTED": CONSENT_ACTIVE,
    "ACTIVE": CONSENT_ACTIVE,
    "APPROVED": CONSENT_ACTIVE,
    "PENDING": CONSENT_PENDING,
    "REQUESTED": CONSENT_REQUESTED,
    "REJECTED": CONSENT_REJECTED,
    "DENIED": CONSENT_REJECTED,
    "REVOKED": CONSENT_REVOKED,
    "PAUSED": CONSENT_REVOKED,
    "EXPIRED": CONSENT_EXPIRED,
    "FAILED": CONSENT_FAILED,
    "RENEW_REQUIRED": CONSENT_RENEW_REQUIRED,
}


def normalize_consent_status(raw: str | None) -> str:
    """Map any vendor consent status onto our canonical vocabulary.

    Unknown values return ``PENDING`` rather than raising: a surprise status from
    the vendor must never crash a webhook handler, because Finsense will simply
    retry the callback and we would lose the notification entirely.
    """
    if not raw:
        return CONSENT_PENDING
    return _CONSENT_ALIASES.get(raw.strip().upper(), CONSENT_PENDING)


# --- Per-account consent status --------------------------------------------
ACCOUNT_ACTIVE = "ACTIVE"
ACCOUNT_FAILED = "FAILED"
ACCOUNT_REVOKED = "REVOKED"

ACCOUNT_STATUSES = frozenset({ACCOUNT_ACTIVE, ACCOUNT_FAILED, ACCOUNT_REVOKED})


# --- FI data-fetch session status ------------------------------------------
FI_REQUESTED = "REQUESTED"
FI_PENDING = "PENDING"
FI_READY = "READY"
FI_PARTIAL = "PARTIAL"  # some accounts READY, some FAILED
FI_FAILED = "FAILED"
FI_EXPIRED = "EXPIRED"

FI_SESSION_STATUSES = frozenset(
    {FI_REQUESTED, FI_PENDING, FI_READY, FI_PARTIAL, FI_FAILED, FI_EXPIRED}
)

_FI_ALIASES = {
    "REQUESTED": FI_REQUESTED,
    "PENDING": FI_PENDING,
    "ACTIVE": FI_PENDING,
    "READY": FI_READY,
    "DELIVERED": FI_READY,
    "COMPLETED": FI_READY,
    "PARTIAL": FI_PARTIAL,
    "FAILED": FI_FAILED,
    "TIMEOUT": FI_FAILED,
    "EXPIRED": FI_EXPIRED,
}


def normalize_fi_status(raw: str | None) -> str:
    """Map any vendor data-fetch status onto our canonical vocabulary."""
    if not raw:
        return FI_PENDING
    return _FI_ALIASES.get(raw.strip().upper(), FI_PENDING)


# --- Job queue --------------------------------------------------------------
JOB_QUEUED = "queued"
JOB_RUNNING = "running"
JOB_SUCCEEDED = "succeeded"
JOB_FAILED = "failed"
JOB_CANCELLED = "cancelled"

#: Statuses covered by the partial unique index — a consent may only have one
#: in-flight job of a given type at a time.
AA_JOB_ACTIVE_STATUSES = ("queued", "running")

# Job types. FI_REQUEST is always built even if Auto-FI is enabled on the
# channel: with a periodic consent, Auto-FI only covers the FIRST fetch, and
# every subsequent refresh still calls /FIRequest.
JOB_TYPE_FI_REQUEST = "FI_REQUEST"
JOB_TYPE_FI_FETCH = "FI_FETCH"
JOB_TYPE_REFRESH = "REFRESH"

JOB_TYPES = frozenset({JOB_TYPE_FI_REQUEST, JOB_TYPE_FI_FETCH, JOB_TYPE_REFRESH})


# --- Financial information types -------------------------------------------
FI_TYPE_DEPOSIT = "DEPOSIT"
FI_TYPE_TERM_DEPOSIT = "TERM_DEPOSIT"
FI_TYPE_RECURRING_DEPOSIT = "RECURRING_DEPOSIT"
FI_TYPE_MUTUAL_FUNDS = "MUTUAL_FUNDS"
FI_TYPE_EQUITIES = "EQUITIES"
FI_TYPE_INSURANCE_POLICIES = "INSURANCE_POLICIES"
FI_TYPE_NPS = "NPS"
FI_TYPE_GSTR1_3B = "GSTR1_3B"


# --- Who started the journey -----------------------------------------------
INITIATED_BY_CLIENT = "client"
INITIATED_BY_ADMIN = "admin"

"""Pure unit tests for the AA status normalisers.

No database required — these run anywhere, including CI. The vendor uses two
different words for the same consent state (``ACTIVE`` in the callback,
``ACCEPTED`` in the status GET); collapsing that ambiguity in one place is the
single most important correctness guarantee in the integration, so it is the
one thing tested without infrastructure.
"""

from __future__ import annotations

import pytest

from nucleus.models.account_aggregator import (
    CONSENT_ACTIVE,
    CONSENT_PENDING,
    CONSENT_REJECTED,
    CONSENT_REVOKED,
    FI_FAILED,
    FI_READY,
    normalize_consent_status,
    normalize_fi_status,
)


@pytest.mark.parametrize(
    "raw,expected",
    [
        # The two vendor spellings of the same state.
        ("ACTIVE", CONSENT_ACTIVE),
        ("ACCEPTED", CONSENT_ACTIVE),
        ("APPROVED", CONSENT_ACTIVE),
        # Case and whitespace must not matter.
        ("active", CONSENT_ACTIVE),
        (" Accepted ", CONSENT_ACTIVE),
        ("rejected", CONSENT_REJECTED),
        ("REVOKED", CONSENT_REVOKED),
        ("PAUSED", CONSENT_REVOKED),
    ],
)
def test_known_consent_statuses(raw: str, expected: str) -> None:
    assert normalize_consent_status(raw) == expected


@pytest.mark.parametrize("raw", ["WHO_KNOWS", "", None, "   "])
def test_unknown_consent_status_falls_back_to_pending(raw: str | None) -> None:
    """An unexpected vendor status must never raise.

    These values arrive inside a webhook handler. Raising would return a 5xx,
    Finsense would retry, and a persistently unknown status would mean the
    notification is lost entirely. Degrading to PENDING keeps the row alive and
    lets the status-GET fallback reconcile it.
    """
    assert normalize_consent_status(raw) == CONSENT_PENDING


@pytest.mark.parametrize(
    "raw,expected",
    [
        ("READY", FI_READY),
        ("DELIVERED", FI_READY),
        ("COMPLETED", FI_READY),
        ("TIMEOUT", FI_FAILED),
        ("FAILED", FI_FAILED),
    ],
)
def test_fi_status_aliases(raw: str, expected: str) -> None:
    assert normalize_fi_status(raw) == expected


def test_normalisers_are_total() -> None:
    """Neither normaliser may raise on arbitrary input."""
    for value in ["", "x", "123", "ACTIVE\n", None]:
        normalize_consent_status(value)
        normalize_fi_status(value)

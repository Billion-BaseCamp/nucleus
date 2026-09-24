"""AA consent — the spine of the whole integration.

Every later identifier hangs off ``consent_handle``: it exists from the moment
the journey is raised, survives rejection, and is the only id present at every
stage. ``consent_id`` appears *only* after approval, which is precisely why the
journey cannot be keyed on it.

Ordering rule: this row is INSERTed **before** calling ConsentRequestPlus. If
Finsense creates a consent and we crash before persisting, there is a live
consent on the AA network that we hold no record of — invisible to us,
impossible to revoke, and a compliance problem.
"""

from __future__ import annotations

from datetime import datetime
from typing import Any, Optional
from uuid import UUID, uuid4

from sqlalchemy import DateTime, ForeignKey, Index, LargeBinary, String, Text
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func
from sqlalchemy.types import UUID as SQLUUID

from nucleus.db.database import Base
from nucleus.models.account_aggregator.constants import CONSENT_REQUESTED


class AAConsent(Base):
    """One consent journey, from request through approval to revocation."""

    __tablename__ = "aa_consents"

    id: Mapped[UUID] = mapped_column(
        SQLUUID(as_uuid=True), primary_key=True, default=uuid4, index=True
    )
    aa_customer_id: Mapped[UUID] = mapped_column(
        SQLUUID(as_uuid=True),
        ForeignKey("aa_customers.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    # --- identifiers, in the order they come into existence -----------------
    # Our own rid, generated and persisted BEFORE the outbound call. This is the
    # correlation key Finsense echoes back as ``requestId`` in the callback.
    request_id: Mapped[UUID] = mapped_column(
        SQLUUID(as_uuid=True), nullable=False, unique=True, index=True, default=uuid4
    )
    # NULL until Finsense responds to ConsentRequestPlus.
    consent_handle: Mapped[Optional[str]] = mapped_column(
        String(64), nullable=True, unique=True, index=True
    )
    # NULL until the customer approves. Absent forever on rejection.
    consent_id: Mapped[Optional[str]] = mapped_column(
        String(64), nullable=True, unique=True, index=True
    )
    # Our mapping key for the redirect journey; echoed back on return.
    user_session_id: Mapped[UUID] = mapped_column(
        SQLUUID(as_uuid=True), nullable=False, default=uuid4, index=True
    )

    # --- lifecycle ----------------------------------------------------------
    status: Mapped[str] = mapped_column(
        String(32), nullable=False, default=CONSENT_REQUESTED, index=True
    )
    template_name: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    consent_description: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    purpose_code: Mapped[Optional[str]] = mapped_column(String(16), nullable=True)
    aa_id: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)

    # --- validity windows ---------------------------------------------------
    # All timezone-aware: Finsense sends ISO-8601 with offsets, and a naive
    # column silently drops the offset, shifting every timestamp by 5h30m.
    fi_from: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    fi_to: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    consent_start: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    consent_expiry: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True, index=True
    )

    # --- provenance / audit -------------------------------------------------
    initiated_by: Mapped[str] = mapped_column(String(16), nullable=False)
    initiated_by_user_id: Mapped[Optional[UUID]] = mapped_column(
        SQLUUID(as_uuid=True), nullable=True
    )
    redirect_url: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    # The Finvu-hosted journey URL we hand the browser.
    journey_url: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    revoked_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    error_code: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    error_message: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # Encrypted: vendor responses echo customer identifiers.
    raw_response_enc: Mapped[Optional[bytes]] = mapped_column(
        LargeBinary, nullable=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), onupdate=func.now(), nullable=True
    )

    __table_args__ = (
        Index("ix_aa_consents_customer_status", "aa_customer_id", "status"),
    )

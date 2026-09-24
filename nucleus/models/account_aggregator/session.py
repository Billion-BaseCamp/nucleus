"""Accounts linked under a consent, and the data-fetch sessions that pull them.

Consents are split account-wise on purpose (Finsense docs §4): isolating each
account lifts the overall success rate, so one failing bank does not sink the
whole consent. Both models below carry per-account state for that reason.
"""

from __future__ import annotations

from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4

from sqlalchemy import (
    DateTime,
    ForeignKey,
    Index,
    Integer,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func
from sqlalchemy.types import UUID as SQLUUID

from nucleus.db.database import Base
from nucleus.models.account_aggregator.constants import FI_REQUESTED


class AALinkedAccount(Base):
    """One bank/FIP account authorised under a consent."""

    __tablename__ = "aa_linked_accounts"

    id: Mapped[UUID] = mapped_column(
        SQLUUID(as_uuid=True), primary_key=True, default=uuid4, index=True
    )
    aa_consent_id: Mapped[UUID] = mapped_column(
        SQLUUID(as_uuid=True),
        ForeignKey("aa_consents.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    # The AA's reference for this account inside this consent. Stable across
    # fetches, so it is our natural upsert key.
    link_ref_number: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
    fip_id: Mapped[Optional[str]] = mapped_column(String(64), nullable=True, index=True)
    fip_name: Mapped[Optional[str]] = mapped_column(String(128), nullable=True)

    # Never the full number — the AA only ever returns a masked form.
    masked_account_number: Mapped[Optional[str]] = mapped_column(
        String(64), nullable=True
    )
    fi_type: Mapped[Optional[str]] = mapped_column(String(32), nullable=True, index=True)
    account_type: Mapped[Optional[str]] = mapped_column(String(32), nullable=True)

    status: Mapped[str] = mapped_column(String(32), nullable=False, index=True)
    error_code: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    error_message: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    last_fetched_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), onupdate=func.now(), nullable=True
    )

    __table_args__ = (
        UniqueConstraint(
            "aa_consent_id", "link_ref_number", name="uq_aa_linked_account_ref"
        ),
    )


class AAFISession(Base):
    """One data-fetch session — the result of a single /FIRequest call."""

    __tablename__ = "aa_fi_sessions"

    id: Mapped[UUID] = mapped_column(
        SQLUUID(as_uuid=True), primary_key=True, default=uuid4, index=True
    )
    aa_consent_id: Mapped[UUID] = mapped_column(
        SQLUUID(as_uuid=True),
        ForeignKey("aa_consents.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    session_id: Mapped[str] = mapped_column(
        String(64), nullable=False, unique=True, index=True
    )
    txn_id: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)

    status: Mapped[str] = mapped_column(
        String(32), nullable=False, default=FI_REQUESTED, index=True
    )

    # Per-account progress. The FI_FETCH job is only enqueued once every account
    # has resolved (READY or FAILED) — otherwise we fetch a partial payload and
    # silently miss accounts that were still in flight.
    accounts_total: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    accounts_ready: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    accounts_failed: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    requested_from: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    requested_to: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    fetched_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    error_code: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    error_message: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), onupdate=func.now(), nullable=True
    )

    __table_args__ = (
        Index("ix_aa_fi_sessions_consent_status", "aa_consent_id", "status"),
    )

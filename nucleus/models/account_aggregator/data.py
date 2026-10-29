"""Fetched financial data: account snapshots and transactions.

Two rules govern everything in this module.

**Money is NUMERIC, never float.** ``Float`` cannot represent 0.1 exactly; a
balance that round-trips through it will eventually be wrong by paise, and in a
tax product a wrong balance is a wrong filing. Parse with ``Decimal(str(value))``
— ``Decimal(float_value)`` reintroduces the same error it was meant to avoid.

**Customer financial detail is encrypted at column level.** Narration lines carry
counterparty names, UPI handles and account references. RDS disk encryption
protects against a stolen disk, not against a leaked query result or an
over-broad admin read, so the sensitive columns are sealed with the AA Fernet
key held only by the application.
"""

from __future__ import annotations

from datetime import date, datetime
from decimal import Decimal
from typing import Optional
from uuid import UUID, uuid4

from sqlalchemy import (
    Date,
    DateTime,
    ForeignKey,
    Index,
    LargeBinary,
    Numeric,
    String,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func
from sqlalchemy.types import UUID as SQLUUID

from nucleus.db.database import Base


class AAAccountSnapshot(Base):
    """Balance and holder profile for one account at one fetch.

    A new row per fetch rather than an update in place: the balance history is
    itself useful, and an overwrite would lose it.
    """

    __tablename__ = "aa_account_snapshots"

    id: Mapped[UUID] = mapped_column(
        SQLUUID(as_uuid=True), primary_key=True, default=uuid4, index=True
    )
    aa_linked_account_id: Mapped[UUID] = mapped_column(
        SQLUUID(as_uuid=True),
        ForeignKey("aa_linked_accounts.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    aa_fi_session_id: Mapped[UUID] = mapped_column(
        SQLUUID(as_uuid=True),
        ForeignKey("aa_fi_sessions.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    fi_type: Mapped[Optional[str]] = mapped_column(String(32), nullable=True, index=True)
    balance_amount: Mapped[Optional[Decimal]] = mapped_column(
        Numeric(20, 4), nullable=True
    )
    balance_as_of: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    currency: Mapped[Optional[str]] = mapped_column(String(8), nullable=True)

    # Encrypted JSONB blobs: the FI-type-specific Summary block and the account
    # holder's Profile (name, PAN, address, contact details).
    summary_enc: Mapped[Optional[bytes]] = mapped_column(LargeBinary, nullable=True)
    holder_profile_enc: Mapped[Optional[bytes]] = mapped_column(
        LargeBinary, nullable=True
    )

    fetched_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    __table_args__ = (
        Index(
            "ix_aa_snapshots_account_fetched",
            "aa_linked_account_id",
            "fetched_at",
        ),
    )


class AATransaction(Base):
    """A single financial transaction.

    Deduplication uses ``dedupe_key``, a hash over
    ``txnId | timestamp | amount | narration``.

    Narration is deliberately part of the hash. Both vendor sample payloads show
    ``"txnId": ""`` — banks frequently omit it — so timestamp and amount alone
    would merge two genuine 100 rupee UPI payments made on the same day into
    one. Including narration risks keeping a rare true duplicate; excluding it
    risks silently destroying a real transaction. Losing real financial data is
    the worse failure, so narration stays in.
    """

    __tablename__ = "aa_transactions"

    id: Mapped[UUID] = mapped_column(
        SQLUUID(as_uuid=True), primary_key=True, default=uuid4, index=True
    )
    aa_linked_account_id: Mapped[UUID] = mapped_column(
        SQLUUID(as_uuid=True),
        ForeignKey("aa_linked_accounts.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    aa_fi_session_id: Mapped[Optional[UUID]] = mapped_column(
        SQLUUID(as_uuid=True),
        ForeignKey("aa_fi_sessions.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )

    # --- promoted, indexed fields every FI type shares ----------------------
    txn_type: Mapped[Optional[str]] = mapped_column(
        String(16), nullable=True, index=True
    )  # CREDIT | DEBIT
    amount: Mapped[Decimal] = mapped_column(Numeric(20, 4), nullable=False)
    currency: Mapped[Optional[str]] = mapped_column(String(8), nullable=True)
    balance_after: Mapped[Optional[Decimal]] = mapped_column(
        Numeric(20, 4), nullable=True
    )
    txn_timestamp: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True, index=True
    )
    value_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    mode: Mapped[Optional[str]] = mapped_column(String(32), nullable=True)
    reference: Mapped[Optional[str]] = mapped_column(String(128), nullable=True)
    txn_id: Mapped[Optional[str]] = mapped_column(String(128), nullable=True)

    # --- encrypted detail ---------------------------------------------------
    narration_enc: Mapped[Optional[bytes]] = mapped_column(LargeBinary, nullable=True)
    # The full original object, so a parser fix can be replayed without
    # re-fetching from the FIP (consent windows expire; the raw payload does not).
    raw_enc: Mapped[Optional[bytes]] = mapped_column(LargeBinary, nullable=True)

    dedupe_key: Mapped[str] = mapped_column(String(64), nullable=False)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    __table_args__ = (
        UniqueConstraint(
            "aa_linked_account_id", "dedupe_key", name="uq_aa_txn_dedupe"
        ),
        # Serves the dashboard's default query: newest transactions per account.
        Index(
            "ix_aa_txn_account_ts",
            "aa_linked_account_id",
            "txn_timestamp",
        ),
    )

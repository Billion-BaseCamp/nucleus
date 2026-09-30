"""Investment data from SEBI-regulated FIPs: holdings and investment transactions.

Kept apart from ``aa_transactions`` on purpose. A bank feed is a cash ledger
(amount, debit/credit, running balance). A demat or mutual-fund feed is a
*position* (units of an ISIN at a price) plus trades against it. Forcing a
trade into the bank table would make ``amount`` mean different things per row,
leave ``balance_after`` permanently NULL and lose ``units`` — the one field
capital-gains work cannot do without.

Same two rules as ``data.py``: NUMERIC, never float; customer detail that could
identify a person or a portfolio line is encrypted at column level.
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

#: Asset classes we normalise vendor ``type`` values onto.
ASSET_EQUITY = "EQUITY"
ASSET_MUTUAL_FUND = "MUTUAL_FUND"
ASSET_ETF = "ETF"


class AAHolding(Base):
    """One line of a portfolio (an ISIN, or a scheme in a folio) at one fetch.

    A new set of rows per fetch session rather than an update in place: a
    holding that is sold simply stops appearing, and overwriting would turn
    "sold" into "still held at the old quantity". The latest session for an
    account is the current portfolio; older sessions are the history.
    """

    __tablename__ = "aa_holdings"

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

    asset_class: Mapped[str] = mapped_column(String(16), nullable=False, index=True)
    isin: Mapped[Optional[str]] = mapped_column(String(16), nullable=True, index=True)
    # Issuer (equities) or scheme name (mutual funds) — what a person reads.
    name: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    amc: Mapped[Optional[str]] = mapped_column(String(128), nullable=True)
    registrar: Mapped[Optional[str]] = mapped_column(String(32), nullable=True)
    amfi_code: Mapped[Optional[str]] = mapped_column(String(16), nullable=True)
    scheme_category: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    scheme_option: Mapped[Optional[str]] = mapped_column(String(32), nullable=True)

    units: Mapped[Optional[Decimal]] = mapped_column(Numeric(24, 6), nullable=True)
    lien_units: Mapped[Optional[Decimal]] = mapped_column(Numeric(24, 6), nullable=True)
    lockin_units: Mapped[Optional[Decimal]] = mapped_column(Numeric(24, 6), nullable=True)
    # NAV for funds, last traded price for equities.
    price: Mapped[Optional[Decimal]] = mapped_column(Numeric(20, 6), nullable=True)
    price_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    # units x price, computed in Decimal at parse time so every reader agrees.
    market_value: Mapped[Optional[Decimal]] = mapped_column(Numeric(20, 4), nullable=True)

    # Folio number identifies the investor at the AMC — encrypted.
    folio_enc: Mapped[Optional[bytes]] = mapped_column(LargeBinary, nullable=True)
    raw_enc: Mapped[Optional[bytes]] = mapped_column(LargeBinary, nullable=True)

    # isin + sha256(folio) — stable across fetches, never the folio in clear.
    holding_key: Mapped[str] = mapped_column(String(96), nullable=False)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    __table_args__ = (
        UniqueConstraint(
            "aa_fi_session_id",
            "aa_linked_account_id",
            "holding_key",
            name="uq_aa_holding_session_line",
        ),
        Index("ix_aa_holdings_account_session", "aa_linked_account_id", "aa_fi_session_id"),
    )


class AAInvestmentTransaction(Base):
    """A buy, sell, switch, dividend or similar event against a holding.

    ``units`` is nullable on purpose: mutual-fund feeds routinely send it empty
    and give only amount and NAV. Deriving units as amount / NAV here would
    invent a figure the RTA never stated (and exit loads, stamp duty and STT
    make it wrong anyway), so it is stored only when the FIP sends it.
    """

    __tablename__ = "aa_investment_transactions"

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

    asset_class: Mapped[str] = mapped_column(String(16), nullable=False, index=True)
    txn_type: Mapped[Optional[str]] = mapped_column(String(32), nullable=True, index=True)
    isin: Mapped[Optional[str]] = mapped_column(String(16), nullable=True, index=True)
    name: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    amfi_code: Mapped[Optional[str]] = mapped_column(String(16), nullable=True)
    exchange: Mapped[Optional[str]] = mapped_column(String(16), nullable=True)

    units: Mapped[Optional[Decimal]] = mapped_column(Numeric(24, 6), nullable=True)
    price: Mapped[Optional[Decimal]] = mapped_column(Numeric(20, 6), nullable=True)
    amount: Mapped[Optional[Decimal]] = mapped_column(Numeric(20, 4), nullable=True)

    txn_date: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True, index=True
    )
    nav_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    mode: Mapped[Optional[str]] = mapped_column(String(32), nullable=True)
    txn_id: Mapped[Optional[str]] = mapped_column(String(128), nullable=True)
    order_id: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    lock_in_days: Mapped[Optional[str]] = mapped_column(String(16), nullable=True)

    narration_enc: Mapped[Optional[bytes]] = mapped_column(LargeBinary, nullable=True)
    raw_enc: Mapped[Optional[bytes]] = mapped_column(LargeBinary, nullable=True)

    dedupe_key: Mapped[str] = mapped_column(String(64), nullable=False)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    __table_args__ = (
        UniqueConstraint(
            "aa_linked_account_id", "dedupe_key", name="uq_aa_inv_txn_dedupe"
        ),
        Index("ix_aa_inv_txn_account_date", "aa_linked_account_id", "txn_date"),
    )

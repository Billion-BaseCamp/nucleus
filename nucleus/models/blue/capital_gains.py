"""Capital-gains statements read by BLUE: one statement per document/broker, its trades, and every fix.

BLUE reads a CG statement (blue/readers/cg in at-copilot, vendored from tax-engine-backend), checks it
(totals vs the statement's own summary, per-row arithmetic and holding period, a second independent
read, cross-document duplicates), stores the result here, and only after RM approval pushes it to
advance-tax's at_cg_* tables. Column names for trades follow at_cg_india_eq_and_debt_mf_transactions /
at_cg_us_transactions so that push is a straight copy.

Original values are never overwritten: a fix writes the corrected value next to the original and a
row in blue_cg_corrections, so any automatic or RM change can be shown and undone.
"""

from __future__ import annotations

from datetime import date, datetime
from decimal import Decimal
from typing import Optional
from uuid import UUID, uuid4

from sqlalchemy import CheckConstraint, Date, DateTime, ForeignKey, Index, Integer, Numeric, String, Text, text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func
from sqlalchemy.types import UUID as SQLUUID

from nucleus.db.database import Base
from nucleus.models.blue.constants import (
    BLUE_CG_CORRECTION_SOURCES,
    BLUE_CG_GAIN_TYPES,
    BLUE_CG_SEGMENTS,
    BLUE_CG_STATEMENT_STATUSES,
    BLUE_CG_TXN_STATUSES,
    check_in,
)


class BlueCgStatement(Base):
    """One broker's statement read from one document (a workbook can hold several brokers)."""

    __tablename__ = "blue_cg_statements"
    __table_args__ = (
        CheckConstraint(check_in("status", BLUE_CG_STATEMENT_STATUSES), name="ck_blue_cg_statements_status"),
        Index("ix_blue_cg_statements_client_fy", "client_id", "financial_year"),
        Index("ix_blue_cg_statements_document", "document_id"),
        # Re-reading a document supersedes the previous statement for that broker: one current per pair.
        Index(
            "uq_blue_cg_statements_current",
            "document_id",
            "broker",
            unique=True,
            postgresql_where=text("status <> 'superseded'"),
        ),
    )

    id: Mapped[UUID] = mapped_column(SQLUUID(as_uuid=True), primary_key=True, default=uuid4)
    document_id: Mapped[UUID] = mapped_column(
        SQLUUID(as_uuid=True), ForeignKey("blue_intake_documents.id", ondelete="CASCADE"), nullable=False
    )
    client_id: Mapped[Optional[UUID]] = mapped_column(
        SQLUUID(as_uuid=True), ForeignKey("clients.id", ondelete="SET NULL"), nullable=True
    )
    financial_year: Mapped[Optional[str]] = mapped_column(String(7), nullable=True)  # "2025-26"
    broker: Mapped[str] = mapped_column(String(100), nullable=False)
    currency: Mapped[str] = mapped_column(String(3), nullable=False, default="INR")
    # deterministic | hybrid_ai | pdf_converted_* | ai_direct
    reader: Mapped[str] = mapped_column(String(48), nullable=False)
    parser_source: Mapped[Optional[str]] = mapped_column(String(128), nullable=True)
    # tax-engine-backend commit the vendored reader came from (UPSTREAM.json), for reproducibility.
    reader_version: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    status: Mapped[str] = mapped_column(String(24), nullable=False, default="read")
    trade_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    # Sums of the stored rows (as read) and the statement's own printed totals, per bucket,
    # e.g. {"Equity/STCG": "-80031.21", "MF/STCG": "200177.46"}; compared by check A.
    row_totals: Mapped[dict] = mapped_column(JSONB, nullable=False, default=dict)
    statement_totals: Mapped[Optional[dict]] = mapped_column(JSONB, nullable=True)
    # Every check that ran: [{"check": "totals_match", "ok": true, "detail": ...}, ...]
    checks: Mapped[list] = mapped_column(JSONB, nullable=False, default=list)
    warnings: Mapped[list] = mapped_column(JSONB, nullable=False, default=list)
    ai_calls: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    cost_usd: Mapped[Optional[Decimal]] = mapped_column(Numeric(10, 4), nullable=True)
    verified_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    approved_by_advisor_id: Mapped[Optional[UUID]] = mapped_column(
        SQLUUID(as_uuid=True), ForeignKey("advisors.id", ondelete="SET NULL"), nullable=True
    )
    approved_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    # Set when pushed to advance-tax (later); points at at_cg_*_brokers_data.id there.
    pushed_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    pushed_ref: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), onupdate=func.now(), nullable=True)


class BlueCgTransaction(Base):
    """One trade row, traceable to its sheet/row, with original and corrected values side by side."""

    __tablename__ = "blue_cg_transactions"
    __table_args__ = (
        CheckConstraint(check_in("segment", BLUE_CG_SEGMENTS), name="ck_blue_cg_transactions_segment"),
        CheckConstraint(check_in("gain_type", BLUE_CG_GAIN_TYPES), name="ck_blue_cg_transactions_gain_type"),
        CheckConstraint(
            "corrected_gain_type IS NULL OR " + check_in("corrected_gain_type", BLUE_CG_GAIN_TYPES),
            name="ck_blue_cg_transactions_corrected_gain_type",
        ),
        CheckConstraint(check_in("status", BLUE_CG_TXN_STATUSES), name="ck_blue_cg_transactions_status"),
        Index("ix_blue_cg_transactions_statement", "statement_id", "row_index"),
        Index("ix_blue_cg_transactions_client_sale", "client_id", "date_of_transfer"),
        Index("ix_blue_cg_transactions_isin", "isin"),
    )

    id: Mapped[UUID] = mapped_column(SQLUUID(as_uuid=True), primary_key=True, default=uuid4)
    statement_id: Mapped[UUID] = mapped_column(
        SQLUUID(as_uuid=True), ForeignKey("blue_cg_statements.id", ondelete="CASCADE"), nullable=False
    )
    # Denormalised for per-client queries (quarter split, duplicates across statements).
    client_id: Mapped[Optional[UUID]] = mapped_column(
        SQLUUID(as_uuid=True), ForeignKey("clients.id", ondelete="SET NULL"), nullable=True
    )
    row_index: Mapped[int] = mapped_column(Integer, nullable=False)  # order within the statement
    source_sheet: Mapped[Optional[str]] = mapped_column(String(128), nullable=True)
    source_row: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    segment: Mapped[str] = mapped_column(String(16), nullable=False)
    gain_type: Mapped[str] = mapped_column(String(16), nullable=False)
    status: Mapped[str] = mapped_column(String(16), nullable=False, default="ok")

    # As read. Names follow advance-tax's at_cg_* transaction tables.
    stock_scheme: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    isin: Mapped[Optional[str]] = mapped_column(String(12), nullable=True)
    quantity: Mapped[Optional[Decimal]] = mapped_column(Numeric(18, 4), nullable=True)
    date_of_purchase: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    date_of_transfer: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    holding_days: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    cost_of_acquisition: Mapped[Optional[Decimal]] = mapped_column(Numeric(18, 2), nullable=True)
    sale_value: Mapped[Optional[Decimal]] = mapped_column(Numeric(18, 2), nullable=True)
    sale_expenses: Mapped[Optional[Decimal]] = mapped_column(Numeric(18, 2), nullable=True)
    gain: Mapped[Optional[Decimal]] = mapped_column(Numeric(18, 2), nullable=True)
    stt_paid: Mapped[Optional[Decimal]] = mapped_column(Numeric(18, 2), nullable=True)
    grandfathering_fmv: Mapped[Optional[Decimal]] = mapped_column(Numeric(18, 4), nullable=True)
    indexed_cost: Mapped[Optional[Decimal]] = mapped_column(Numeric(18, 2), nullable=True)
    # Foreign statements: amounts above are in the statement currency; INR via rate below.
    exchange_rate: Mapped[Optional[Decimal]] = mapped_column(Numeric(12, 4), nullable=True)
    exchange_rate_source: Mapped[Optional[str]] = mapped_column(String(32), nullable=True)  # broker | rbi_ttbr
    sale_value_inr: Mapped[Optional[Decimal]] = mapped_column(Numeric(18, 2), nullable=True)
    cost_of_acquisition_inr: Mapped[Optional[Decimal]] = mapped_column(Numeric(18, 2), nullable=True)
    gain_inr: Mapped[Optional[Decimal]] = mapped_column(Numeric(18, 2), nullable=True)
    mf_fund_bucket: Mapped[Optional[str]] = mapped_column(String(16), nullable=True)  # EquityMF | DebtMF
    is_open_position: Mapped[bool] = mapped_column(nullable=False, default=False, server_default=text("false"))

    # Corrected values (automatic fix or RM). NULL = use the value as read.
    corrected_gain_type: Mapped[Optional[str]] = mapped_column(String(16), nullable=True)
    corrected_date_of_purchase: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    corrected_cost_of_acquisition: Mapped[Optional[Decimal]] = mapped_column(Numeric(18, 2), nullable=True)
    corrected_gain: Mapped[Optional[Decimal]] = mapped_column(Numeric(18, 2), nullable=True)
    corrected_grandfathering_fmv: Mapped[Optional[Decimal]] = mapped_column(Numeric(18, 4), nullable=True)
    # Whatever the reader returned for this row, unmodified, for audit/debugging.
    raw: Mapped[dict] = mapped_column(JSONB, nullable=False, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), onupdate=func.now(), nullable=True)


class BlueCgCorrection(Base):
    """Every change to a statement or trade: who/what, field, before, after, why. Append-only."""

    __tablename__ = "blue_cg_corrections"
    __table_args__ = (
        CheckConstraint(check_in("source", BLUE_CG_CORRECTION_SOURCES), name="ck_blue_cg_corrections_source"),
        CheckConstraint("transaction_id IS NOT NULL OR statement_id IS NOT NULL",
                        name="ck_blue_cg_corrections_target"),
        Index("ix_blue_cg_corrections_statement", "statement_id"),
        Index("ix_blue_cg_corrections_transaction", "transaction_id"),
    )

    id: Mapped[UUID] = mapped_column(SQLUUID(as_uuid=True), primary_key=True, default=uuid4)
    statement_id: Mapped[Optional[UUID]] = mapped_column(
        SQLUUID(as_uuid=True), ForeignKey("blue_cg_statements.id", ondelete="CASCADE"), nullable=True
    )
    transaction_id: Mapped[Optional[UUID]] = mapped_column(
        SQLUUID(as_uuid=True), ForeignKey("blue_cg_transactions.id", ondelete="CASCADE"), nullable=True
    )
    field: Mapped[str] = mapped_column(String(64), nullable=False)
    old_value: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    new_value: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    # auto: mechanical fix with one right answer. rm: RM approved/edited in Teams. revert: undo.
    source: Mapped[str] = mapped_column(String(16), nullable=False)
    rule: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)  # e.g. "holding_period_gain_type"
    reason: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    advisor_id: Mapped[Optional[UUID]] = mapped_column(
        SQLUUID(as_uuid=True), ForeignKey("advisors.id", ondelete="SET NULL"), nullable=True
    )
    approval_id: Mapped[Optional[UUID]] = mapped_column(
        SQLUUID(as_uuid=True), ForeignKey("blue_approvals.id", ondelete="SET NULL"), nullable=True
    )
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)

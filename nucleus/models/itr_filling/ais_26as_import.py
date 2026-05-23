"""Persisted AIS / 26AS import lines and reconciled unified entries per ITR return."""

from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from typing import Any, Optional
from uuid import UUID, uuid4

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from sqlalchemy.types import Numeric
from sqlalchemy import UUID as SQLUUID

from nucleus.db.database import Base


class ITRAisLine(Base):
    """One AIS Part B row (income / TDS view) — written by POST /import/ais."""

    __tablename__ = "itr_ais_lines"

    id: Mapped[UUID] = mapped_column(
        SQLUUID(as_uuid=True), primary_key=True, default=uuid4
    )
    itr_return_id: Mapped[UUID] = mapped_column(
        SQLUUID(as_uuid=True),
        ForeignKey("itr_returns.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    display_order: Mapped[int] = mapped_column(Integer, nullable=False, default=1)

    part: Mapped[str] = mapped_column(String(64), nullable=False, default="")
    info_code: Mapped[str] = mapped_column(String(128), nullable=False, default="")
    category_code: Mapped[str] = mapped_column(String(32), nullable=False, default="")
    part: Mapped[str] = mapped_column(String(32), nullable=False, default="")
    info_code: Mapped[str] = mapped_column(String(128), nullable=False, default="")
    category_code: Mapped[str] = mapped_column(String(32), nullable=False, default="")
    description: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    source_name: Mapped[Optional[str]] = mapped_column(String(125), nullable=True)
    source_tan_or_pan: Mapped[str] = mapped_column(String(10), nullable=False, default="")
    amount: Mapped[Decimal] = mapped_column(Numeric(20, 2), nullable=False, default=0)
    ais_tds_deducted: Mapped[Decimal] = mapped_column(
        Numeric(20, 2), nullable=False, default=0
    )
    ais_tds_deposited: Mapped[Decimal] = mapped_column(
        Numeric(20, 2), nullable=False, default=0
    )
    section_key: Mapped[str] = mapped_column(String(64), nullable=False, default="")
    section_code: Mapped[str] = mapped_column(String(32), nullable=False, default="")
    itr_schedule: Mapped[str] = mapped_column(String(8), nullable=False, default="")
    entry_type: Mapped[str] = mapped_column(String(16), nullable=False, default="INCOME")
    transaction_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    included_in_reconciliation: Mapped[bool] = mapped_column(
        nullable=False, default=True
    )
    skip_reason: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    itr_return: Mapped["ITRReturn"] = relationship(  # noqa: F821
        "ITRReturn", back_populates="ais_lines"
    )


class ITRForm26asLine(Base):
    """One 26AS summary line (Part I/IV/VI/VII/VIII) — written by POST /import/26as."""

    __tablename__ = "itr_form26as_lines"

    id: Mapped[UUID] = mapped_column(
        SQLUUID(as_uuid=True), primary_key=True, default=uuid4
    )
    itr_return_id: Mapped[UUID] = mapped_column(
        SQLUUID(as_uuid=True),
        ForeignKey("itr_returns.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    display_order: Mapped[int] = mapped_column(Integer, nullable=False, default=1)

    part: Mapped[str] = mapped_column(String(16), nullable=False, default="")
    deductor_or_collector_name: Mapped[str] = mapped_column(
        String(125), nullable=False, default=""
    )
    tan_or_pan: Mapped[str] = mapped_column(String(10), nullable=False, default="")
    section: Mapped[str] = mapped_column(String(16), nullable=False, default="")
    amount_paid_or_transaction: Mapped[Decimal] = mapped_column(
        Numeric(20, 2), nullable=False, default=0
    )
    tax_deducted_or_collected: Mapped[Decimal] = mapped_column(
        Numeric(20, 2), nullable=False, default=0
    )
    tds_or_tcs_deposited: Mapped[Decimal] = mapped_column(
        Numeric(20, 2), nullable=False, default=0
    )
    transaction_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    notes: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    itr_return: Mapped["ITRReturn"] = relationship(  # noqa: F821
        "ITRReturn", back_populates="form26as_lines"
    )


class ITRUnifiedEntry(Base):
    """Reconciled AIS+26AS row — rebuilt by POST /reconcile."""

    __tablename__ = "itr_unified_entries"

    id: Mapped[UUID] = mapped_column(
        SQLUUID(as_uuid=True), primary_key=True, default=uuid4
    )
    itr_return_id: Mapped[UUID] = mapped_column(
        SQLUUID(as_uuid=True),
        ForeignKey("itr_returns.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    display_order: Mapped[int] = mapped_column(Integer, nullable=False, default=1)

    info_code: Mapped[str] = mapped_column(String(128), nullable=False, default="")
    category_code: Mapped[str] = mapped_column(String(32), nullable=False, default="")
    section_code: Mapped[str] = mapped_column(String(32), nullable=False, default="")
    itr_schedule: Mapped[str] = mapped_column(String(8), nullable=False, default="")
    entry_type: Mapped[str] = mapped_column(String(16), nullable=False, default="INCOME")
    source_name: Mapped[Optional[str]] = mapped_column(String(125), nullable=True)
    source_tan_or_pan: Mapped[str] = mapped_column(String(10), nullable=False, default="")

    ais_amount: Mapped[Decimal] = mapped_column(Numeric(20, 2), nullable=False, default=0)
    ais_tds_deducted: Mapped[Decimal] = mapped_column(
        Numeric(20, 2), nullable=False, default=0
    )
    form26as_amount: Mapped[Decimal] = mapped_column(
        Numeric(20, 2), nullable=False, default=0
    )
    form26as_tds_deposited: Mapped[Decimal] = mapped_column(
        Numeric(20, 2), nullable=False, default=0
    )
    income_amount: Mapped[Decimal] = mapped_column(
        Numeric(20, 2), nullable=False, default=0
    )
    tds_credit: Mapped[Decimal] = mapped_column(Numeric(20, 2), nullable=False, default=0)
    tcs_credit: Mapped[Decimal] = mapped_column(Numeric(20, 2), nullable=False, default=0)
    source_document: Mapped[str] = mapped_column(String(8), nullable=False, default="")
    flags: Mapped[Optional[list[Any]]] = mapped_column(JSONB, nullable=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    itr_return: Mapped["ITRReturn"] = relationship(  # noqa: F821
        "ITRReturn", back_populates="unified_entries"
    )

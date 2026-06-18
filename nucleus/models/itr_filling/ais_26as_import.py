"""Persisted AIS / 26AS uploads, parsed rows, and reconciliation results."""

from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from typing import TYPE_CHECKING, Any, Optional
from uuid import UUID, uuid4

from sqlalchemy import CheckConstraint, DateTime, ForeignKey, Integer, String
from sqlalchemy import UUID as SQLUUID
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from sqlalchemy.types import Numeric

from nucleus.db.database import Base

if TYPE_CHECKING:
    from nucleus.models.itr_filling.itr_return import ITRReturn


class ITRAis26asUpload(Base):
    """One AIS or 26AS upload for an ITR return."""

    __tablename__ = "itr_ais_26as_uploads"

    id: Mapped[UUID] = mapped_column(
        SQLUUID(as_uuid=True), primary_key=True, default=uuid4
    )
    itr_return_id: Mapped[UUID] = mapped_column(
        SQLUUID(as_uuid=True),
        ForeignKey("itr_returns.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    document_type: Mapped[str] = mapped_column(String(8), nullable=False)
    original_filename: Mapped[str] = mapped_column(String(255), nullable=False)
    pan: Mapped[Optional[str]] = mapped_column(String(10), nullable=True, index=True)
    financial_year: Mapped[Optional[str]] = mapped_column(String(9), nullable=True)
    assessment_year: Mapped[Optional[str]] = mapped_column(String(10), nullable=True)
    status: Mapped[str] = mapped_column(String(32), nullable=False, default="uploaded")
    summary: Mapped[Optional[dict[str, Any]]] = mapped_column(JSONB, nullable=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    itr_return: Mapped["ITRReturn"] = relationship(  # noqa: F821
        "ITRReturn", back_populates="ais_26as_uploads"
    )
    ais_entries: Mapped[list["ITRAisEntry"]] = relationship(
        "ITRAisEntry",
        back_populates="upload",
        cascade="all, delete-orphan",
    )
    form26as_entries: Mapped[list["ITR26asEntry"]] = relationship(
        "ITR26asEntry",
        back_populates="upload",
        cascade="all, delete-orphan",
    )
    ais_sft_transactions: Mapped[list["ITRAisSftTransaction"]] = relationship(
        "ITRAisSftTransaction",
        back_populates="upload",
        cascade="all, delete-orphan",
    )

    __table_args__ = (
        CheckConstraint(
            "document_type IN ('AIS', '26AS')",
            name="ck_itr_ais_26as_uploads_document_type",
        ),
    )


class ITRAisEntry(Base):
    """One parsed AIS row for income, TDS section, or SFT summary income."""

    __tablename__ = "itr_ais_entries"

    id: Mapped[UUID] = mapped_column(
        SQLUUID(as_uuid=True), primary_key=True, default=uuid4
    )
    upload_id: Mapped[Optional[UUID]] = mapped_column(
        SQLUUID(as_uuid=True),
        ForeignKey("itr_ais_26as_uploads.id", ondelete="CASCADE"),
        nullable=True,
        index=True,
    )
    itr_return_id: Mapped[UUID] = mapped_column(
        SQLUUID(as_uuid=True),
        ForeignKey("itr_returns.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    display_order: Mapped[int] = mapped_column(Integer, nullable=False, default=1)

    part: Mapped[str] = mapped_column(String(64), nullable=False, default="")
    entry_level: Mapped[Optional[str]] = mapped_column(String(32), nullable=True)
    info_code: Mapped[str] = mapped_column(String(128), nullable=False, default="")
    category_code: Mapped[str] = mapped_column(String(32), nullable=False, default="")
    description: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    source_name: Mapped[Optional[str]] = mapped_column(String(125), nullable=True)
    source_tan_or_pan: Mapped[str] = mapped_column(
        String(10), nullable=False, default=""
    )
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
    entry_type: Mapped[str] = mapped_column(
        String(16), nullable=False, default="INCOME"
    )
    transaction_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    included_in_reconciliation: Mapped[bool] = mapped_column(
        nullable=False, default=True
    )
    skip_reason: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    raw_payload: Mapped[Optional[dict[str, Any]]] = mapped_column(
        JSONB, nullable=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    upload: Mapped["ITRAis26asUpload"] = relationship(
        "ITRAis26asUpload", back_populates="ais_entries"
    )
    itr_return: Mapped["ITRReturn"] = relationship(  # noqa: F821
        "ITRReturn", back_populates="ais_entries"
    )


class ITR26asEntry(Base):
    """One parsed 26AS summary row."""

    __tablename__ = "itr_26as_entries"

    id: Mapped[UUID] = mapped_column(
        SQLUUID(as_uuid=True), primary_key=True, default=uuid4
    )
    upload_id: Mapped[UUID] = mapped_column(
        SQLUUID(as_uuid=True),
        ForeignKey("itr_ais_26as_uploads.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
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
    raw_payload: Mapped[Optional[dict[str, Any]]] = mapped_column(JSONB, nullable=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    upload: Mapped["ITRAis26asUpload"] = relationship(
        "ITRAis26asUpload", back_populates="form26as_entries"
    )
    itr_return: Mapped["ITRReturn"] = relationship(  # noqa: F821
        "ITRReturn", back_populates="form26as_entries"
    )


class ITRAis26asReconciliation(Base):
    """Comparison result across AIS, 26AS, and final tax-credit values."""

    __tablename__ = "itr_ais_26as_reconciliations"

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
    entry_type: Mapped[str] = mapped_column(
        String(16), nullable=False, default="INCOME"
    )
    source_name: Mapped[Optional[str]] = mapped_column(String(125), nullable=True)
    source_tan_or_pan: Mapped[str] = mapped_column(
        String(10), nullable=False, default=""
    )

    ais_amount: Mapped[Decimal] = mapped_column(
        Numeric(20, 2), nullable=False, default=0
    )
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
    tds_credit: Mapped[Decimal] = mapped_column(
        Numeric(20, 2), nullable=False, default=0
    )
    tcs_credit: Mapped[Decimal] = mapped_column(
        Numeric(20, 2), nullable=False, default=0
    )
    source_document: Mapped[str] = mapped_column(String(8), nullable=False, default="")
    flags: Mapped[Optional[list[Any]]] = mapped_column(JSONB, nullable=True)
    reconciliation_status: Mapped[Optional[str]] = mapped_column(
        String(32), nullable=True, index=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    itr_return: Mapped["ITRReturn"] = relationship(  # noqa: F821
        "ITRReturn", back_populates="ais_26as_reconciliations"
    )


class ITRAisSftTransaction(Base):
    """AIS Part B2 SFT L1 transaction — one sale, off-market credit, or purchase row."""

    __tablename__ = "itr_ais_sft_transactions"

    id: Mapped[UUID] = mapped_column(
        SQLUUID(as_uuid=True), primary_key=True, default=uuid4
    )
    upload_id: Mapped[UUID] = mapped_column(
        SQLUUID(as_uuid=True),
        ForeignKey("itr_ais_26as_uploads.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    itr_return_id: Mapped[UUID] = mapped_column(
        SQLUUID(as_uuid=True),
        ForeignKey("itr_returns.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    display_order: Mapped[int] = mapped_column(Integer, nullable=False, default=1)

    # SALE = market sale / off-market credit; PURCHASE = SFT-17/18(Pur)
    transaction_kind: Mapped[str] = mapped_column(
        String(16), nullable=False, index=True
    )
    tsn_id: Mapped[Optional[str]] = mapped_column(String(64), nullable=True, index=True)

    info_code: Mapped[str] = mapped_column(String(128), nullable=False, default="")
    category_code: Mapped[str] = mapped_column(String(32), nullable=False, default="")
    source_name: Mapped[Optional[str]] = mapped_column(String(125), nullable=True)
    source_id: Mapped[str] = mapped_column(String(64), nullable=False, default="")
    amount: Mapped[Decimal] = mapped_column(Numeric(20, 2), nullable=False, default=0)
    display_name: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)

    # Sale / off-market credit (nullable for purchases)
    asset_type: Mapped[Optional[str]] = mapped_column(String(32), nullable=True)
    transaction_date: Mapped[Optional[str]] = mapped_column(String(16), nullable=True)
    security_name: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    nature_of_transfer: Mapped[Optional[str]] = mapped_column(String(128), nullable=True)
    holding_period: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    quantity: Mapped[Optional[str]] = mapped_column(String(32), nullable=True)
    counterparty: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)

    # Purchase (nullable for sales)
    quarter: Mapped[Optional[str]] = mapped_column(String(32), nullable=True)
    client_id: Mapped[Optional[str]] = mapped_column(String(32), nullable=True)
    amc_name: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    holder_flag: Mapped[Optional[str]] = mapped_column(String(16), nullable=True)
    sales_value: Mapped[Optional[Decimal]] = mapped_column(
        Numeric(20, 2), nullable=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    upload: Mapped[Optional["ITRAis26asUpload"]] = relationship(
        "ITRAis26asUpload", back_populates="ais_sft_transactions"
    )
    itr_return: Mapped["ITRReturn"] = relationship(  # noqa: F821
        "ITRReturn", back_populates="ais_sft_transactions"
    )


__all__ = [
    "ITRAis26asUpload",
    "ITRAisEntry",
    "ITR26asEntry",
    "ITRAis26asReconciliation",
    "ITRAisSftTransaction",
]

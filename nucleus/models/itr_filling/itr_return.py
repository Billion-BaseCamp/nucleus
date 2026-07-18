"""
Central ITR filing record — one row per client per FY per version_number.
Every schedule (salary, house property, capital gains, etc.) hangs off this.
"""

from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from typing import List, Optional
from uuid import UUID, uuid4

from sqlalchemy import (
    Boolean,
    DateTime,
    ForeignKey,
    Index,
    Integer,
    String,
    UniqueConstraint,
    UUID as SQLUUID,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func, text
from sqlalchemy.types import Numeric

from nucleus.db.database import Base


class ITRReturn(Base):
    __tablename__ = "itr_returns"

    id: Mapped[UUID] = mapped_column(
        SQLUUID(as_uuid=True), primary_key=True, default=uuid4
    )
    client_id: Mapped[UUID] = mapped_column(
        SQLUUID(as_uuid=True), nullable=False, index=True
    )
    financial_year_id: Mapped[UUID] = mapped_column(
        SQLUUID(as_uuid=True), nullable=False, index=True
    )
    version_number: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    parent_itr_return_id: Mapped[Optional[UUID]] = mapped_column(
        SQLUUID(as_uuid=True),
        ForeignKey("itr_returns.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    assessment_year: Mapped[str] = mapped_column(String(10), nullable=False)
    itr_form_type: Mapped[str] = mapped_column(String(10), default="ITR-2")
    regime: Mapped[str] = mapped_column(String(5), nullable=False, default="new")
    filing_status: Mapped[str] = mapped_column(String(20), default="not_started")
    filed_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    residential_status: Mapped[Optional[str]] = mapped_column(String(10), nullable=True)

    # Tax credits — Form 67 / Schedule TR1 (TaxPaidOutsideIndFlg)
    form67_enabled: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    # Advisor-confirmed: Form 67 filed on IT portal (Rule 128) when FTC is claimed
    form67_filed: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=False, server_default=text("false")
    )

    total_income: Mapped[Optional[Decimal]] = mapped_column(Numeric(18, 2), default=0)
    tax_payable: Mapped[Optional[Decimal]] = mapped_column(Numeric(18, 2), default=0)
    refund_due: Mapped[Optional[Decimal]] = mapped_column(Numeric(18, 2), default=0)
    is_huf:Mapped[Optional[bool]] = mapped_column(Boolean,default=False,nullable=True)

    salary: Mapped[Optional["ITRSalarySchedule"]] = relationship(
        "ITRSalarySchedule",
        back_populates="itr_return",
        cascade="all, delete-orphan",
        uselist=False,
    )
    house_property: Mapped[Optional["ITRHPSchedule"]] = relationship(
        "ITRHPSchedule",
        back_populates="itr_return",
        cascade="all, delete-orphan",
        uselist=False,
    )
    other_sources: Mapped[Optional["ITROSSchedule"]] = relationship(
        "ITROSSchedule",
        back_populates="itr_return",
        cascade="all, delete-orphan",
        uselist=False,
    )
    deductions: Mapped[Optional["ITRDedSchedule"]] = relationship(
        "ITRDedSchedule",
        back_populates="itr_return",
        cascade="all, delete-orphan",
        uselist=False,
    )
    disclosures: Mapped[Optional["ITRDisclosuresSchedule"]] = relationship(
        "ITRDisclosuresSchedule",
        back_populates="itr_return",
        cascade="all, delete-orphan",
        uselist=False,
    )
    cg_schedule: Mapped[Optional["ITRCGSchedule"]] = relationship(
        "ITRCGSchedule",
        back_populates="itr_return",
        cascade="all, delete-orphan",
        uselist=False,
    )

    tax_credit_schedule: Mapped[Optional["ITRTaxCreditSchedule"]] = relationship(
        "ITRTaxCreditSchedule",
        back_populates="itr_return",
        cascade="all, delete-orphan",
        uselist=False,
    )
    ais_26as_uploads: Mapped[List["ITRAis26asUpload"]] = relationship(  # noqa: F821
        "ITRAis26asUpload",
        back_populates="itr_return",
        cascade="all, delete-orphan",
    )
    ais_entries: Mapped[List["ITRAisEntry"]] = relationship(  # noqa: F821
        "ITRAisEntry",
        back_populates="itr_return",
        cascade="all, delete-orphan",
    )
    form26as_entries: Mapped[List["ITR26asEntry"]] = relationship(  # noqa: F821
        "ITR26asEntry",
        back_populates="itr_return",
        cascade="all, delete-orphan",
    )
    ais_26as_reconciliations: Mapped[
        List["ITRAis26asReconciliation"]
    ] = relationship(  # noqa: F821
        "ITRAis26asReconciliation",
        back_populates="itr_return",
        cascade="all, delete-orphan",
    )
    ais_sft_transactions: Mapped[List["ITRAisSftTransaction"]] = relationship(  # noqa: F821
        "ITRAisSftTransaction",
        back_populates="itr_return",
        cascade="all, delete-orphan",
    )
    cfl_schedule: Mapped[Optional["ITRCFLSchedule"]] = relationship(
        "ITRCFLSchedule",
        back_populates="itr_return",
        cascade="all, delete-orphan",
        uselist=False,
    )
    addresses: Mapped[list["ITRAddress"]] = relationship(
        "ITRAddress",
        back_populates="itr_return",
        cascade="all, delete-orphan",
    )
    refund_bank_accounts: Mapped[List["ITRRefundBankAccount"]] = relationship(
        "ITRRefundBankAccount",
        back_populates="itr_return",
        cascade="all, delete-orphan",
        order_by="ITRRefundBankAccount.display_order",
    )
    ais_json_archives: Mapped[List["ITRAisJsonArchive"]] = relationship(  # noqa: F821
        "ITRAisJsonArchive",
        back_populates="itr_return",
    )
    tis_summary_categories: Mapped[List["ITRTisSummaryCategory"]] = relationship(  # noqa: F821
        "ITRTisSummaryCategory",
        back_populates="itr_return",
        cascade="all, delete-orphan",
        order_by="ITRTisSummaryCategory.sr_no",
    )
    tis_pdf_archives: Mapped[List["ITRTisPdfArchive"]] = relationship(  # noqa: F821
        "ITRTisPdfArchive",
        back_populates="itr_return",
    )
    form_26as_archives: Mapped[List["ITRForm26asArchive"]] = relationship(  # noqa: F821
        "ITRForm26asArchive",
        back_populates="itr_return",
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), onupdate=func.now()
    )

    __table_args__ = (
        UniqueConstraint(
            "client_id",
            "financial_year_id",
            "version_number",
            name="uq_itr_return_client_fy_version",
        ),
        Index("ix_itr_return_client_fy", "client_id", "financial_year_id"),
    )

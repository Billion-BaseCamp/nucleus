"""
Central ITR filing record — one per client per financial year.
Every schedule (salary, house property, capital gains, etc.) hangs off this.
"""

from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from typing import List, Optional
from uuid import UUID, uuid4

from sqlalchemy import Boolean, DateTime, String, UniqueConstraint, UUID as SQLUUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from sqlalchemy.types import Numeric

from nucleus.db.database import Base


class ITRReturn(Base):
    __tablename__ = "itr_returns"

    id: Mapped[UUID] = mapped_column(SQLUUID(as_uuid=True), primary_key=True, default=uuid4)
    client_id: Mapped[UUID] = mapped_column(SQLUUID(as_uuid=True), nullable=False, index=True)
    financial_year_id: Mapped[UUID] = mapped_column(SQLUUID(as_uuid=True), nullable=False, index=True)
    assessment_year: Mapped[str] = mapped_column(String(10), nullable=False)
    itr_form_type: Mapped[str] = mapped_column(String(10), default="ITR-2")
    regime: Mapped[str] = mapped_column(String(5), nullable=False, default="new")
    filing_status: Mapped[str] = mapped_column(String(20), default="draft")
    residential_status: Mapped[Optional[str]] = mapped_column(String(10), nullable=True)

    # Tax credits — Form 67 / Schedule TR1 (TaxPaidOutsideIndFlg)
    form67_enabled: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    total_income: Mapped[Optional[Decimal]] = mapped_column(Numeric(18, 2), default=0)
    tax_payable: Mapped[Optional[Decimal]] = mapped_column(Numeric(18, 2), default=0)
    refund_due: Mapped[Optional[Decimal]] = mapped_column(Numeric(18, 2), default=0)

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
    cg_data: Mapped[Optional["ITRCGData"]] = relationship(
        "ITRCGData",
        back_populates="itr_return",
        uselist=False,
        cascade="all, delete-orphan",
    )

    tax_credit_schedule: Mapped[Optional["ITRTaxCreditSchedule"]] = relationship(
        "ITRTaxCreditSchedule",
        back_populates="itr_return",
        cascade="all, delete-orphan",
        uselist=False,
    )

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), onupdate=func.now())

    __table_args__ = (
        UniqueConstraint("client_id", "financial_year_id", name="uq_itr_return_client_fy"),
    )

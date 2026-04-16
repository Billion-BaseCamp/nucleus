"""
ITR filing layer: Tax credits (Schedule IT, TDS1/2/3, TCS, TR1, FSI).

All entries hang directly off itr_returns (no intermediate schedule table).
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
    Integer,
    String,
    UUID as SQLUUID,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from sqlalchemy.types import Numeric

from nucleus.db.database import Base

class ITRTaxCreditSchedule(Base):
    __tablename__ = "itr_tax_credit_schedule"
    id: Mapped[UUID] = mapped_column(SQLUUID(as_uuid=True), primary_key=True, default=uuid4)
    itr_return_id: Mapped[UUID] = mapped_column(SQLUUID(as_uuid=True), ForeignKey("itr_returns.id", ondelete="CASCADE"), nullable=False)
    total_advance_sa_tax_paid: Mapped[Decimal] = mapped_column(Numeric(20, 2), nullable=False, default=0)
    total_tds:Mapped[Decimal] = mapped_column(Numeric(20, 2), nullable=False, default=0)
    total_tds_on_salary:Mapped[Decimal] = mapped_column(Numeric(20, 2), nullable=False, default=0)
    total_tds_on_non_salary:Mapped[Decimal] = mapped_column(Numeric(20, 2), nullable=False, default=0)
    total_tcs:Mapped[Decimal] = mapped_column(Numeric(20, 2), nullable=False, default=0)
    total_form67_dtaa:Mapped[Decimal] = mapped_column(Numeric(20, 2), nullable=False, default=0)
    itr_return: Mapped["ITRReturn"] = relationship("ITRReturn", back_populates="tax_credit_schedule")



class ITRAdvanceTaxPayment(Base):
    """Advance / self-assessment tax payments → Schedule IT."""

    __tablename__ = "itr_advance_tax_payments"

    id: Mapped[UUID] = mapped_column(SQLUUID(as_uuid=True), primary_key=True, default=uuid4)
    itr_return_id: Mapped[UUID] = mapped_column(
        SQLUUID(as_uuid=True),
        ForeignKey("itr_returns.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    display_order: Mapped[int] = mapped_column(Integer, nullable=False, default=1)

    bank_name: Mapped[Optional[str]] = mapped_column(String(125), nullable=True)
    bsr_code: Mapped[str] = mapped_column(String(7), nullable=False)
    challan_no: Mapped[str] = mapped_column(String(5), nullable=False)
    date: Mapped[date] = mapped_column(Date, nullable=False)
    amount: Mapped[Decimal] = mapped_column(Numeric(20, 2), nullable=False, default=0)
    source: Mapped[Optional[str]] = mapped_column(String(30), nullable=True)

    itr_return: Mapped["ITRReturn"] = relationship("ITRReturn", back_populates="advance_tax_payments")

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), onupdate=func.now())


class ITRTDSSalary(Base):
    """TDS on salary → Schedule TDS1."""

    __tablename__ = "itr_tds_salary"

    id: Mapped[UUID] = mapped_column(SQLUUID(as_uuid=True), primary_key=True, default=uuid4)
    itr_return_id: Mapped[UUID] = mapped_column(
        SQLUUID(as_uuid=True),
        ForeignKey("itr_returns.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    display_order: Mapped[int] = mapped_column(Integer, nullable=False, default=1)

    employer_name: Mapped[str] = mapped_column(String(125), nullable=False)
    tan: Mapped[str] = mapped_column(String(10), nullable=False)
    tds_deducted: Mapped[Decimal] = mapped_column(Numeric(20, 2), nullable=False, default=0)
    tds_claimed: Mapped[Decimal] = mapped_column(Numeric(20, 2), nullable=False, default=0)
    income_chargeable: Mapped[Decimal] = mapped_column(Numeric(20, 2), nullable=False, default=0)

    itr_return: Mapped["ITRReturn"] = relationship("ITRReturn", back_populates="tds_salary")

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), onupdate=func.now())


class ITRTDSNonSalary(Base):
    """TDS other than salary → Schedule TDS2."""

    __tablename__ = "itr_tds_non_salary"

    id: Mapped[UUID] = mapped_column(SQLUUID(as_uuid=True), primary_key=True, default=uuid4)
    itr_return_id: Mapped[UUID] = mapped_column(
        SQLUUID(as_uuid=True),
        ForeignKey("itr_returns.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    display_order: Mapped[int] = mapped_column(Integer, nullable=False, default=1)

    deductor_name: Mapped[Optional[str]] = mapped_column(String(125), nullable=True)
    tan: Mapped[str] = mapped_column(String(10), nullable=False)
    section: Mapped[str] = mapped_column(String(10), nullable=False)
    head_of_income: Mapped[Optional[str]] = mapped_column(String(5), nullable=True)
    tds_deducted: Mapped[Decimal] = mapped_column(Numeric(20, 2), nullable=False, default=0)
    tds_claimed: Mapped[Decimal] = mapped_column(Numeric(20, 2), nullable=False, default=0)
    gross_amount: Mapped[Decimal] = mapped_column(Numeric(20, 2), nullable=False, default=0)
    balance_tds_cf: Mapped[Decimal] = mapped_column(Numeric(20, 2), nullable=False, default=0)
    gross_receipts_26as: Mapped[Decimal] = mapped_column(Numeric(20, 2), nullable=False, default=0)
    gross_receipt_offered: Mapped[Decimal] = mapped_column(Numeric(20, 2), nullable=False, default=0)

    itr_return: Mapped["ITRReturn"] = relationship("ITRReturn", back_populates="tds_non_salary")

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), onupdate=func.now())


class ITRTDSProperty(Base):
    """TDS on property (e.g. 194IA) → Schedule TDS3."""

    __tablename__ = "itr_tds_property"

    id: Mapped[UUID] = mapped_column(SQLUUID(as_uuid=True), primary_key=True, default=uuid4)
    itr_return_id: Mapped[UUID] = mapped_column(
        SQLUUID(as_uuid=True),
        ForeignKey("itr_returns.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    display_order: Mapped[int] = mapped_column(Integer, nullable=False, default=1)

    deductor_name: Mapped[Optional[str]] = mapped_column(String(125), nullable=True)
    pan: Mapped[str] = mapped_column(String(10), nullable=False)
    section: Mapped[str] = mapped_column(String(10), nullable=False, default="194IA")
    head_of_income: Mapped[Optional[str]] = mapped_column(String(5), nullable=True)
    tds_deducted: Mapped[Decimal] = mapped_column(Numeric(20, 2), nullable=False, default=0)
    tds_claimed: Mapped[Decimal] = mapped_column(Numeric(20, 2), nullable=False, default=0)
    balance_tds_cf: Mapped[Decimal] = mapped_column(Numeric(20, 2), nullable=False, default=0)
    gross_receipts_26as: Mapped[Decimal] = mapped_column(Numeric(20, 2), nullable=False, default=0)
    gross_receipt_offered: Mapped[Decimal] = mapped_column(Numeric(20, 2), nullable=False, default=0)

    itr_return: Mapped["ITRReturn"] = relationship("ITRReturn", back_populates="tds_property")

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), onupdate=func.now())


class ITRTCSEntry(Base):
    """Tax collected at source → Schedule TCS."""

    __tablename__ = "itr_tcs"

    id: Mapped[UUID] = mapped_column(SQLUUID(as_uuid=True), primary_key=True, default=uuid4)
    itr_return_id: Mapped[UUID] = mapped_column(
        SQLUUID(as_uuid=True),
        ForeignKey("itr_returns.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    display_order: Mapped[int] = mapped_column(Integer, nullable=False, default=1)

    collector_name: Mapped[Optional[str]] = mapped_column(String(125), nullable=True)
    tan: Mapped[str] = mapped_column(String(10), nullable=False)
    tcs_collected: Mapped[Decimal] = mapped_column(Numeric(20, 2), nullable=False, default=0)
    tcs_claimed: Mapped[Decimal] = mapped_column(Numeric(20, 2), nullable=False, default=0)
    balance_tcs_cf: Mapped[Decimal] = mapped_column(Numeric(20, 2), nullable=False, default=0)
    expenditure_26as: Mapped[Decimal] = mapped_column(Numeric(20, 2), nullable=False, default=0)

    itr_return: Mapped["ITRReturn"] = relationship("ITRReturn", back_populates="tcs_entries")

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), onupdate=func.now())


class ITRForm67Entry(Base):
    """Form 67 — foreign tax credit → Schedule TR1."""

    __tablename__ = "itr_form67_entries"

    id: Mapped[UUID] = mapped_column(SQLUUID(as_uuid=True), primary_key=True, default=uuid4)
    itr_return_id: Mapped[UUID] = mapped_column(
        SQLUUID(as_uuid=True),
        ForeignKey("itr_returns.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    display_order: Mapped[int] = mapped_column(Integer, nullable=False, default=1)

    country_name: Mapped[str] = mapped_column(String(55), nullable=False)
    country_code: Mapped[Optional[str]] = mapped_column(String(4), nullable=True)

    income: Mapped[Decimal] = mapped_column(Numeric(20, 2), nullable=False, default=0)
    tax_paid_outside_india: Mapped[Decimal] = mapped_column(Numeric(20, 2), nullable=False, default=0)
    tax_payable_in_india: Mapped[Decimal] = mapped_column(Numeric(20, 2), nullable=False, default=0)
    relief_claimed: Mapped[Decimal] = mapped_column(Numeric(20, 2), nullable=False, default=0)

    taxpayer_id_no: Mapped[Optional[str]] = mapped_column(String(75), nullable=True)
    head_of_income: Mapped[Optional[str]] = mapped_column(String(30), nullable=True)
    article_of_dtaa: Mapped[Optional[str]] = mapped_column(String(30), nullable=True)
    section_of_dtaa: Mapped[Optional[str]] = mapped_column(String(5), nullable=True)

    tax_rate: Mapped[Optional[Decimal]] = mapped_column(Numeric(8, 4), nullable=True)
    tax_under_it_act: Mapped[Decimal] = mapped_column(Numeric(20, 2), nullable=False, default=0)
    tax_us_115jc: Mapped[Decimal] = mapped_column(Numeric(20, 2), nullable=False, default=0)
    tax_rate_outside_india: Mapped[Optional[Decimal]] = mapped_column(Numeric(8, 4), nullable=True)
    nature_of_income: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)

    itr_return: Mapped["ITRReturn"] = relationship("ITRReturn", back_populates="form67_entries")

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), onupdate=func.now())


class ITRForm67Refund(Base):
    """Form 67 — tax refunded in prior years."""

    __tablename__ = "itr_form67_refunds"

    id: Mapped[UUID] = mapped_column(SQLUUID(as_uuid=True), primary_key=True, default=uuid4)
    itr_return_id: Mapped[UUID] = mapped_column(
        SQLUUID(as_uuid=True),
        ForeignKey("itr_returns.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    display_order: Mapped[int] = mapped_column(Integer, nullable=False, default=1)

    assessment_year: Mapped[Optional[str]] = mapped_column(String(10), nullable=True)
    tax_refunded: Mapped[Decimal] = mapped_column(Numeric(20, 2), nullable=False, default=0)

    itr_return: Mapped["ITRReturn"] = relationship("ITRReturn", back_populates="form67_refunds")

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), onupdate=func.now())


class ITRFSIEntry(Base):
    """Foreign source income → Schedule FSI."""

    __tablename__ = "itr_fsi_entries"

    id: Mapped[UUID] = mapped_column(SQLUUID(as_uuid=True), primary_key=True, default=uuid4)
    itr_return_id: Mapped[UUID] = mapped_column(
        SQLUUID(as_uuid=True),
        ForeignKey("itr_returns.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    display_order: Mapped[int] = mapped_column(Integer, nullable=False, default=1)

    country_code: Mapped[Optional[str]] = mapped_column(String(4), nullable=True)
    country_name: Mapped[str] = mapped_column(String(55), nullable=False)
    head_of_income: Mapped[str] = mapped_column(String(30), nullable=False)

    income_from_outside_india: Mapped[Decimal] = mapped_column(Numeric(20, 2), nullable=False, default=0)
    tax_paid_outside_india: Mapped[Decimal] = mapped_column(Numeric(20, 2), nullable=False, default=0)
    tax_payable_in_india: Mapped[Decimal] = mapped_column(Numeric(20, 2), nullable=False, default=0)
    relief_available: Mapped[Decimal] = mapped_column(Numeric(20, 2), nullable=False, default=0)

    section_of_relief: Mapped[Optional[str]] = mapped_column(String(5), nullable=True)
    article_of_dtaa: Mapped[Optional[str]] = mapped_column(String(30), nullable=True)

    itr_return: Mapped["ITRReturn"] = relationship("ITRReturn", back_populates="fsi_entries")

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), onupdate=func.now())

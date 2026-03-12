from __future__ import annotations

from datetime import date, datetime 
from typing import Optional
from uuid import UUID, uuid4

from sqlalchemy import Date, DateTime, ForeignKey, Numeric, SmallInteger, String, text, UUID as SQLUUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from nucleus.db.database import Base


# ---------------------------------------------------------------------------
# PART I - TDS on Salary / Dividend / Interest etc. (Aggregated per Deductor)
# ---------------------------------------------------------------------------
class Form26ASPart1(Base):
    __tablename__ = "form_26as_part1"

    id: Mapped[UUID] = mapped_column(SQLUUID(as_uuid=True), primary_key=True, default=uuid4, index=True)
    financial_year_id: Mapped[UUID] = mapped_column(SQLUUID(as_uuid=True), ForeignKey("financial_years.id", ondelete="CASCADE"), nullable=False, index=True)

    sr_no: Mapped[Optional[int]] = mapped_column(SmallInteger, nullable=True)
    name_of_deductor: Mapped[str] = mapped_column(String(255), nullable=False)
    tan_of_deductor: Mapped[str] = mapped_column(String(20), nullable=False, index=True)
    section: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)           # e.g. '192', '194', '194A'
    transaction_count: Mapped[int] = mapped_column(SmallInteger, nullable=False, default=0, server_default=text('0'))
    date_from: Mapped[Optional[date]] = mapped_column(Date, nullable=True)              # earliest transaction date
    date_to: Mapped[Optional[date]] = mapped_column(Date, nullable=True)                # latest transaction date
    total_amount_paid: Mapped[float] = mapped_column(Numeric(15, 2), nullable=False, default=0, server_default=text('0'))
    total_tax_deducted: Mapped[float] = mapped_column(Numeric(15, 2), nullable=False, default=0, server_default=text('0'))
    total_tds_deposited: Mapped[float] = mapped_column(Numeric(15, 2), nullable=False, default=0, server_default=text('0'))

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), onupdate=func.now(), nullable=True)

    financial_year: Mapped["FinancialYear"] = relationship("FinancialYear", back_populates="form_26as_part1")


# ---------------------------------------------------------------------------
# PART II - TDS with 15G / 15H Declarations (Aggregated per Deductor)
# ---------------------------------------------------------------------------
class Form26ASPart2(Base):
    __tablename__ = "form_26as_part2"

    id: Mapped[UUID] = mapped_column(SQLUUID(as_uuid=True), primary_key=True, default=uuid4, index=True)
    financial_year_id: Mapped[UUID] = mapped_column(SQLUUID(as_uuid=True), ForeignKey("financial_years.id", ondelete="CASCADE"), nullable=False, index=True)

    sr_no: Mapped[Optional[int]] = mapped_column(SmallInteger, nullable=True)
    name_of_deductor: Mapped[str] = mapped_column(String(255), nullable=False)
    tan_of_deductor: Mapped[str] = mapped_column(String(20), nullable=False, index=True)
    section: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    transaction_count: Mapped[int] = mapped_column(SmallInteger, nullable=False, default=0, server_default=text('0'))
    date_from: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    date_to: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    total_amount_paid: Mapped[float] = mapped_column(Numeric(15, 2), nullable=False, default=0, server_default=text('0'))
    total_tax_deducted: Mapped[float] = mapped_column(Numeric(15, 2), nullable=False, default=0, server_default=text('0'))
    total_tds_deposited: Mapped[float] = mapped_column(Numeric(15, 2), nullable=False, default=0, server_default=text('0'))

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), onupdate=func.now(), nullable=True)

    financial_year: Mapped["FinancialYear"] = relationship("FinancialYear", back_populates="form_26as_part2")


# ---------------------------------------------------------------------------
# PART III - TDS u/s 194B / 194R / 194S / 194BA
# (Lottery, Perquisites, VDA, Online Gaming) - Aggregated per Deductor
# ---------------------------------------------------------------------------
class Form26ASPart3(Base):
    __tablename__ = "form_26as_part3"

    id: Mapped[UUID] = mapped_column(SQLUUID(as_uuid=True), primary_key=True, default=uuid4, index=True)
    financial_year_id: Mapped[UUID] = mapped_column(SQLUUID(as_uuid=True), ForeignKey("financial_years.id", ondelete="CASCADE"), nullable=False, index=True)

    sr_no: Mapped[Optional[int]] = mapped_column(SmallInteger, nullable=True)
    name_of_deductor: Mapped[str] = mapped_column(String(255), nullable=False)
    tan_of_deductor: Mapped[str] = mapped_column(String(20), nullable=False, index=True)
    section: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    transaction_count: Mapped[int] = mapped_column(SmallInteger, nullable=False, default=0, server_default=text('0'))
    date_from: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    date_to: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    total_amount_paid: Mapped[float] = mapped_column(Numeric(15, 2), nullable=False, default=0, server_default=text('0'))
    total_tax_deducted: Mapped[float] = mapped_column(Numeric(15, 2), nullable=False, default=0, server_default=text('0'))
    total_tds_deposited: Mapped[float] = mapped_column(Numeric(15, 2), nullable=False, default=0, server_default=text('0'))

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), onupdate=func.now(), nullable=True)

    financial_year: Mapped["FinancialYear"] = relationship("FinancialYear", back_populates="form_26as_part3")


# ---------------------------------------------------------------------------
# PART IV - TDS u/s 194IA / 194IB / 194M / 194S
# For Seller / Landlord / Professional receiving payment (Aggregated)
# ---------------------------------------------------------------------------
class Form26ASPart4(Base):
    __tablename__ = "form_26as_part4"

    id: Mapped[UUID] = mapped_column(SQLUUID(as_uuid=True), primary_key=True, default=uuid4, index=True)
    financial_year_id: Mapped[UUID] = mapped_column(SQLUUID(as_uuid=True), ForeignKey("financial_years.id", ondelete="CASCADE"), nullable=False, index=True)

    sr_no: Mapped[Optional[int]] = mapped_column(SmallInteger, nullable=True)
    name_of_deductor: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    pan_of_deductor: Mapped[Optional[str]] = mapped_column(String(20), nullable=True, index=True)
    section: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)           # e.g. '194IA', '194IB'
    transaction_count: Mapped[int] = mapped_column(SmallInteger, nullable=False, default=0, server_default=text('0'))
    date_from: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    date_to: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    total_transaction_amount: Mapped[float] = mapped_column(Numeric(15, 2), nullable=False, default=0, server_default=text('0'))
    total_tds_deposited: Mapped[float] = mapped_column(Numeric(15, 2), nullable=False, default=0, server_default=text('0'))

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), onupdate=func.now(), nullable=True)

    financial_year: Mapped["FinancialYear"] = relationship("FinancialYear", back_populates="form_26as_part4")


# ---------------------------------------------------------------------------
# PART V - Transactions u/s 194S via Form 26QE
# For Seller of Virtual Digital Asset (Aggregated)
# ---------------------------------------------------------------------------
class Form26ASPart5(Base):
    __tablename__ = "form_26as_part5"

    id: Mapped[UUID] = mapped_column(SQLUUID(as_uuid=True), primary_key=True, default=uuid4, index=True)
    financial_year_id: Mapped[UUID] = mapped_column(SQLUUID(as_uuid=True), ForeignKey("financial_years.id", ondelete="CASCADE"), nullable=False, index=True)

    sr_no: Mapped[Optional[int]] = mapped_column(SmallInteger, nullable=True)
    name_of_buyer: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    pan_of_buyer: Mapped[Optional[str]] = mapped_column(String(20), nullable=True, index=True)
    transaction_count: Mapped[int] = mapped_column(SmallInteger, nullable=False, default=0, server_default=text('0'))
    date_from: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    date_to: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    total_transaction_amount: Mapped[float] = mapped_column(Numeric(15, 2), nullable=False, default=0, server_default=text('0'))

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), onupdate=func.now(), nullable=True)

    financial_year: Mapped["FinancialYear"] = relationship("FinancialYear", back_populates="form_26as_part5")


# ---------------------------------------------------------------------------
# PART VI - TCS (Tax Collected at Source) - Aggregated per Collector
# ---------------------------------------------------------------------------
class Form26ASPart6(Base):
    __tablename__ = "form_26as_part6"

    id: Mapped[UUID] = mapped_column(SQLUUID(as_uuid=True), primary_key=True, default=uuid4, index=True)
    financial_year_id: Mapped[UUID] = mapped_column(SQLUUID(as_uuid=True), ForeignKey("financial_years.id", ondelete="CASCADE"), nullable=False, index=True)

    sr_no: Mapped[Optional[int]] = mapped_column(SmallInteger, nullable=True)
    name_of_collector: Mapped[str] = mapped_column(String(255), nullable=False)
    tan_of_collector: Mapped[str] = mapped_column(String(20), nullable=False, index=True)
    section: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)           # e.g. '206CT', '206C'
    transaction_count: Mapped[int] = mapped_column(SmallInteger, nullable=False, default=0, server_default=text('0'))
    date_from: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    date_to: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    total_amount_paid: Mapped[float] = mapped_column(Numeric(15, 2), nullable=False, default=0, server_default=text('0'))
    total_tax_collected: Mapped[float] = mapped_column(Numeric(15, 2), nullable=False, default=0, server_default=text('0'))
    total_tcs_deposited: Mapped[float] = mapped_column(Numeric(15, 2), nullable=False, default=0, server_default=text('0'))

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), onupdate=func.now(), nullable=True)

    financial_year: Mapped["FinancialYear"] = relationship("FinancialYear", back_populates="form_26as_part6")


# ---------------------------------------------------------------------------
# PART VII - Tax Refunds (Aggregated per Assessment Year)
# ---------------------------------------------------------------------------
class Form26ASPart7(Base):
    __tablename__ = "form_26as_part7"

    id: Mapped[UUID] = mapped_column(SQLUUID(as_uuid=True), primary_key=True, default=uuid4, index=True)
    financial_year_id: Mapped[UUID] = mapped_column(SQLUUID(as_uuid=True), ForeignKey("financial_years.id", ondelete="CASCADE"), nullable=False, index=True)

    sr_no: Mapped[Optional[int]] = mapped_column(SmallInteger, nullable=True)
    assessment_year: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    mode: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)              # e.g. 'ECS', 'Cheque'
    nature_of_refund: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    date_from: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    date_to: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    total_amount_of_refund: Mapped[float] = mapped_column(Numeric(15, 2), nullable=False, default=0, server_default=text('0'))
    total_interest: Mapped[float] = mapped_column(Numeric(15, 2), nullable=False, default=0, server_default=text('0'))

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), onupdate=func.now(), nullable=True)

    financial_year: Mapped["FinancialYear"] = relationship("FinancialYear", back_populates="form_26as_part7")


# ---------------------------------------------------------------------------
# PART VIII - TDS u/s 194IA / 194IB / 194M / 194S
# For Buyer / Tenant / Person making payment (Aggregated per Deductee)
# ---------------------------------------------------------------------------
class Form26ASPart8(Base):
    __tablename__ = "form_26as_part8"

    id: Mapped[UUID] = mapped_column(SQLUUID(as_uuid=True), primary_key=True, default=uuid4, index=True)
    financial_year_id: Mapped[UUID] = mapped_column(SQLUUID(as_uuid=True), ForeignKey("financial_years.id", ondelete="CASCADE"), nullable=False, index=True)

    sr_no: Mapped[Optional[int]] = mapped_column(SmallInteger, nullable=True)
    name_of_deductee: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    pan_of_deductee: Mapped[Optional[str]] = mapped_column(String(20), nullable=True, index=True)
    section: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)           # e.g. '194IA', '194IB'
    transaction_count: Mapped[int] = mapped_column(SmallInteger, nullable=False, default=0, server_default=text('0'))
    date_from: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    date_to: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    total_transaction_amount: Mapped[float] = mapped_column(Numeric(15, 2), nullable=False, default=0, server_default=text('0'))
    total_tds_deposited: Mapped[float] = mapped_column(Numeric(15, 2), nullable=False, default=0, server_default=text('0'))
    total_amount_other_than_tds: Mapped[float] = mapped_column(Numeric(15, 2), nullable=False, default=0, server_default=text('0'))

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), onupdate=func.now(), nullable=True)

    financial_year: Mapped["FinancialYear"] = relationship("FinancialYear", back_populates="form_26as_part8")


# ---------------------------------------------------------------------------
# PART IX - Transactions u/s 194S via Form 26QE
# For Buyer of Virtual Digital Asset (Aggregated)
# ---------------------------------------------------------------------------
class Form26ASPart9(Base):
    __tablename__ = "form_26as_part9"

    id: Mapped[UUID] = mapped_column(SQLUUID(as_uuid=True), primary_key=True, default=uuid4, index=True)
    financial_year_id: Mapped[UUID] = mapped_column(SQLUUID(as_uuid=True), ForeignKey("financial_years.id", ondelete="CASCADE"), nullable=False, index=True)

    sr_no: Mapped[Optional[int]] = mapped_column(SmallInteger, nullable=True)
    name_of_seller: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    pan_of_seller: Mapped[Optional[str]] = mapped_column(String(20), nullable=True, index=True)
    transaction_count: Mapped[int] = mapped_column(SmallInteger, nullable=False, default=0, server_default=text('0'))
    date_from: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    date_to: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    total_transaction_amount: Mapped[float] = mapped_column(Numeric(15, 2), nullable=False, default=0, server_default=text('0'))
    total_amount_other_than_tds: Mapped[float] = mapped_column(Numeric(15, 2), nullable=False, default=0, server_default=text('0'))

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), onupdate=func.now(), nullable=True)

    financial_year: Mapped["FinancialYear"] = relationship("FinancialYear", back_populates="form_26as_part9")


# ---------------------------------------------------------------------------
# PART X - TDS / TCS Defaults (per Financial Year)
# ---------------------------------------------------------------------------
class Form26ASPart10(Base):
    __tablename__ = "form_26as_part10"

    id: Mapped[UUID] = mapped_column(SQLUUID(as_uuid=True), primary_key=True, default=uuid4, index=True)
    financial_year_id: Mapped[UUID] = mapped_column(SQLUUID(as_uuid=True), ForeignKey("financial_years.id", ondelete="CASCADE"), nullable=False, index=True)

    sr_no: Mapped[Optional[int]] = mapped_column(SmallInteger, nullable=True)
    short_payment: Mapped[float] = mapped_column(Numeric(15, 2), nullable=False, default=0, server_default=text('0'))
    short_deduction_collection: Mapped[float] = mapped_column(Numeric(15, 2), nullable=False, default=0, server_default=text('0'))
    interest_on_tds_payment_default: Mapped[float] = mapped_column(Numeric(15, 2), nullable=False, default=0, server_default=text('0'))
    interest_on_tds_deduction_default: Mapped[float] = mapped_column(Numeric(15, 2), nullable=False, default=0, server_default=text('0'))
    late_filing_fee_234e: Mapped[float] = mapped_column(Numeric(15, 2), nullable=False, default=0, server_default=text('0'))
    interest_220_2: Mapped[float] = mapped_column(Numeric(15, 2), nullable=False, default=0, server_default=text('0'))
    total_default: Mapped[float] = mapped_column(Numeric(15, 2), nullable=False, default=0, server_default=text('0'))

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), onupdate=func.now(), nullable=True)

    financial_year: Mapped["FinancialYear"] = relationship("FinancialYear", back_populates="form_26as_part10")

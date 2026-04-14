"""
ITR filing layer: Schedule OS (income from other sources) persistence.

itr_returns → itr_os_schedule (1:1) → 7 child tables
"""

from __future__ import annotations

from datetime import date, datetime
from decimal import Decimal
from typing import List, Optional
from uuid import UUID, uuid4

from sqlalchemy import (
    Date,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text,
    UUID as SQLUUID,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from sqlalchemy.types import Numeric

from nucleus.db.database import Base


class ITROSSchedule(Base):
    """Schedule OS — one-to-one child of ITRReturn."""

    __tablename__ = "itr_os_schedule"

    id: Mapped[UUID] = mapped_column(SQLUUID(as_uuid=True), primary_key=True, default=uuid4)
    itr_return_id: Mapped[UUID] = mapped_column(
        SQLUUID(as_uuid=True),
        ForeignKey("itr_returns.id", ondelete="CASCADE"),
        nullable=False,
        unique=True,
        index=True,
    )

    total_ios_income: Mapped[Optional[Decimal]] = mapped_column(Numeric(15, 2), default=0)
    total_net_ios_income: Mapped[Optional[Decimal]] = mapped_column(Numeric(15, 2), default=0)
    total_pti_income: Mapped[Optional[Decimal]] = mapped_column(Numeric(15, 2), default=0)
    grand_total_income: Mapped[Optional[Decimal]] = mapped_column(Numeric(15, 2), default=0)
    total_savings_interest: Mapped[Optional[Decimal]] = mapped_column(Numeric(15, 2), default=0)
    total_fd_interest: Mapped[Optional[Decimal]] = mapped_column(Numeric(15, 2), default=0)
    total_dividend_income: Mapped[Optional[Decimal]] = mapped_column(Numeric(15, 2), default=0)
    total_other_income: Mapped[Optional[Decimal]] = mapped_column(Numeric(15, 2), default=0)
    total_income_lines: Mapped[Optional[Decimal]] = mapped_column(Numeric(15, 2), default=0)
    total_tds: Mapped[Optional[Decimal]] = mapped_column(Numeric(15, 2), default=0)

    
    # ── Relationships ──
    itr_return: Mapped["ITRReturn"] = relationship("ITRReturn", back_populates="other_sources")
    income_lines: Mapped[List["ITROSIncomeLine"]] = relationship(
        back_populates="os_schedule",
        cascade="all, delete-orphan"
    )
    interest_details: Mapped[List["ITROSInterestDetail"]] = relationship(
        back_populates="os_schedule",
        cascade="all, delete-orphan",
        order_by="ITROSInterestDetail.display_order",
    )
    dividend_details: Mapped[List["ITROSDividendDetail"]] = relationship(
        back_populates="os_schedule",
        cascade="all, delete-orphan",
        order_by="ITROSDividendDetail.display_order",
    )
    pti_entities: Mapped[List["ITROSPTIEntity"]] = relationship(
        back_populates="os_schedule",
        cascade="all, delete-orphan",
        order_by="ITROSPTIEntity.display_order",
    )
    buyback_shares: Mapped[List["ITROSBuybackShare"]] = relationship(
        back_populates="os_schedule",
        cascade="all, delete-orphan",
        order_by="ITROSBuybackShare.display_order",
    )
    clubbing_entries: Mapped[List["ITROSClubbingEntry"]] = relationship(
        back_populates="os_schedule",
        cascade="all, delete-orphan",
        order_by="ITROSClubbingEntry.display_order",
    )
    other_income: Mapped[List["ITROSOtherIncome"]] = relationship(
        back_populates="os_schedule",
        cascade="all, delete-orphan",
        order_by="ITROSOtherIncome.display_order",
    )

    #one to one relationship with ITRTaxExemptIncome
    tax_exempt_income: Mapped["ITRTaxExemptIncome"] = relationship(back_populates="os_schedule")
    deemed_income: Mapped["ITRDeemedIncome"] = relationship(back_populates="os_schedule")

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), onupdate=func.now())

class ITRDeemedIncome(Base):
    __tablename__ = "itr_deemed_income"
    id: Mapped[UUID] = mapped_column(SQLUUID(as_uuid=True), primary_key=True, default=uuid4)
    os_schedule_id: Mapped[UUID] = mapped_column(
        SQLUUID(as_uuid=True),
        ForeignKey("itr_os_schedule.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    immovable_without_cons: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False, default=0)
    immovable_inadequate_cons: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False, default=0)
    movable_without_cons: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False, default=0)
    movable_inadequate_cons: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False, default=0)
    gross_rent_from_machinery: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False, default=0)
    deduction_us57: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False, default=0)

    os_schedule: Mapped["ITROSSchedule"] = relationship(back_populates="deemed_income")

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), onupdate=func.now())

class ITRTaxExemptIncome(Base):
    __tablename__ = "itr_tax_exempt_income"
    id: Mapped[UUID] = mapped_column(SQLUUID(as_uuid=True), primary_key=True, default=uuid4)
    os_schedule_id: Mapped[UUID] = mapped_column(
        SQLUUID(as_uuid=True),
        ForeignKey("itr_os_schedule.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
   # ── Tax Exempt Income — fixed 6-row structure ──
    exempt_interest_income: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False, default=0)
    exempt_not_chargeable: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False, default=0)
    exempt_pti_not_chargeable: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False, default=0)
    exempt_10_10d: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False, default=0)
    exempt_10_11: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False, default=0)
    exempt_10_12: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False, default=0)

    os_schedule: Mapped["ITROSSchedule"] = relationship(back_populates="tax_exempt_income")

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), onupdate=func.now())


class ITROSIncomeLine(Base):
    """Fixed income-nature rows (22 rows: savingsInterest, fdInterest, familyPension, etc.)."""

    __tablename__ = "itr_os_income_lines"

    id: Mapped[UUID] = mapped_column(SQLUUID(as_uuid=True), primary_key=True, default=uuid4)
    os_schedule_id: Mapped[UUID] = mapped_column(
        SQLUUID(as_uuid=True),
        ForeignKey("itr_os_schedule.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    nature_of_income: Mapped[str] = mapped_column(String(200), nullable=False)
    code: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    reference_source: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    amount: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False, default=0)
    tds: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False, default=0)

    os_schedule: Mapped["ITROSSchedule"] = relationship(back_populates="income_lines")

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), onupdate=func.now())


class ITROSInterestDetail(Base):
    """Bank-wise SB + FD interest breakdowns."""

    __tablename__ = "itr_os_interest_details"

    id: Mapped[UUID] = mapped_column(SQLUUID(as_uuid=True), primary_key=True, default=uuid4)
    os_schedule_id: Mapped[UUID] = mapped_column(
        SQLUUID(as_uuid=True),
        ForeignKey("itr_os_schedule.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    display_order: Mapped[int] = mapped_column(Integer, nullable=False, default=1)

    detail_type: Mapped[str] = mapped_column(String(10), nullable=False)
    bank_name: Mapped[Optional[str]] = mapped_column(String(200), nullable=True)
    account_no: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    amount: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False, default=0)
    source: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    comment: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    os_schedule: Mapped["ITROSSchedule"] = relationship(back_populates="interest_details")

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), onupdate=func.now())


class ITROSDividendDetail(Base):
    """Company-wise Indian + Foreign dividend breakdowns."""

    __tablename__ = "itr_os_dividend_details"

    id: Mapped[UUID] = mapped_column(SQLUUID(as_uuid=True), primary_key=True, default=uuid4)
    os_schedule_id: Mapped[UUID] = mapped_column(
        SQLUUID(as_uuid=True),
        ForeignKey("itr_os_schedule.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    display_order: Mapped[int] = mapped_column(Integer, nullable=False, default=1)

    dividend_type: Mapped[str] = mapped_column(String(10), nullable=False)
    company_name: Mapped[Optional[str]] = mapped_column(String(200), nullable=True)
    amount: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False, default=0)
    source: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    comment: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    os_schedule: Mapped["ITROSSchedule"] = relationship(back_populates="dividend_details")

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), onupdate=func.now())


class ITROSPTIEntity(Base):
    """Pass Through Income entity entries."""

    __tablename__ = "itr_os_pti_entities"

    id: Mapped[UUID] = mapped_column(SQLUUID(as_uuid=True), primary_key=True, default=uuid4)
    os_schedule_id: Mapped[UUID] = mapped_column(
        SQLUUID(as_uuid=True),
        ForeignKey("itr_os_schedule.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    display_order: Mapped[int] = mapped_column(Integer, nullable=False, default=1)

    trust_name: Mapped[Optional[str]] = mapped_column(String(200), nullable=True)
    income: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False, default=0)
    tds: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False, default=0)
    pan: Mapped[Optional[str]] = mapped_column(String(10), nullable=True)
    head_of_income: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    schema_head: Mapped[Optional[str]] = mapped_column(String(30), nullable=True)
    investment_entity: Mapped[Optional[str]] = mapped_column(String(30), nullable=True)

    # CG-specific fields (nullable, relevant when head_of_income relates to capital gains)
    nature_of_gains: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    invested_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    invested_amount: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False, default=0)
    cg_scheme_deposit: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False, default=0)
    exempt_gains: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False, default=0)
    net_taxable_gains_ltcg: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False, default=0)

    # OS-specific
    expense_us57: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False, default=0)

    os_schedule: Mapped["ITROSSchedule"] = relationship(back_populates="pti_entities")

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), onupdate=func.now())


class ITROSBuybackShare(Base):
    """Buyback of Shares entries."""

    __tablename__ = "itr_os_buyback_shares"

    id: Mapped[UUID] = mapped_column(SQLUUID(as_uuid=True), primary_key=True, default=uuid4)
    os_schedule_id: Mapped[UUID] = mapped_column(
        SQLUUID(as_uuid=True),
        ForeignKey("itr_os_schedule.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    display_order: Mapped[int] = mapped_column(Integer, nullable=False, default=1)

    stock_name: Mapped[Optional[str]] = mapped_column(String(200), nullable=True)
    nature_of_gains: Mapped[Optional[str]] = mapped_column(String(10), nullable=True)
    rate_of_tax: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    date_of_buyback: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    date_of_acquisition: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    total_sale_price: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False, default=0)
    acquisition_cost_per_unit: Mapped[Decimal] = mapped_column(Numeric(15, 4), nullable=False, default=0)
    total_acquisition_cost: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False, default=0)
    loss_amount: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False, default=0)

    os_schedule: Mapped["ITROSSchedule"] = relationship(back_populates="buyback_shares")

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), onupdate=func.now())


class ITROSClubbingEntry(Base):
    """Minor + Other Person income clubbing (Schedule SPI)."""

    __tablename__ = "itr_os_clubbing_entries"

    id: Mapped[UUID] = mapped_column(SQLUUID(as_uuid=True), primary_key=True, default=uuid4)
    os_schedule_id: Mapped[UUID] = mapped_column(
        SQLUUID(as_uuid=True),
        ForeignKey("itr_os_schedule.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    display_order: Mapped[int] = mapped_column(Integer, nullable=False, default=1)

    clubbing_type: Mapped[str] = mapped_column(String(15), nullable=False)
    name: Mapped[Optional[str]] = mapped_column(String(200), nullable=True)
    pan: Mapped[Optional[str]] = mapped_column(String(10), nullable=True)
    relationship_type: Mapped[Optional[str]] = mapped_column(String(30), nullable=True)
    amount: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False, default=0)
    head_of_income: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    head_of_income_code: Mapped[Optional[str]] = mapped_column(String(5), nullable=True)
    remark: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    os_schedule: Mapped["ITROSSchedule"] = relationship(back_populates="clubbing_entries")

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), onupdate=func.now())


class ITROSOtherIncome(Base):
    """Other Interest + Any Other Income (unified via income_type discriminator)."""

    __tablename__ = "itr_os_other_income"

    id: Mapped[UUID] = mapped_column(SQLUUID(as_uuid=True), primary_key=True, default=uuid4)
    os_schedule_id: Mapped[UUID] = mapped_column(
        SQLUUID(as_uuid=True),
        ForeignKey("itr_os_schedule.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    display_order: Mapped[int] = mapped_column(Integer, nullable=False, default=1)

    income_type: Mapped[str] = mapped_column(String(20), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(String(300), nullable=True)
    amount: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False, default=0)

    os_schedule: Mapped["ITROSSchedule"] = relationship(back_populates="other_income")

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), onupdate=func.now())

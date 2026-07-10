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
    Boolean,
    Date,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text,
    UUID as SQLUUID,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func, text
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

    computation_status: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        server_default="NOT_STARTED",
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
        cascade="all, delete-orphan",
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
    special_rates: Mapped[List["ITROSSpecialRate"]] = relationship(
        back_populates="os_schedule",
        cascade="all, delete-orphan",
        order_by="ITROSSpecialRate.display_order",
    )
    dtaa_income_rows: Mapped[List["ITROSDtaaIncome"]] = relationship(
        back_populates="os_schedule",
        cascade="all, delete-orphan",
        order_by="ITROSDtaaIncome.display_order",
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
    machinery_rent_expenses: Mapped[Optional[Decimal]] = mapped_column(Numeric(15, 2), nullable=True, default=0)      # Sec 57 — expenses against machinery rent
    machinery_rent_depreciation: Mapped[Optional[Decimal]] = mapped_column(Numeric(15, 2), nullable=True, default=0)  # Sec 57 — depreciation on plant / machinery
    deduction_us57: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False, default=0)
    # Itemized Sec 57 deductions — deduction_us57 stays the persisted total.
    # Nullable: pre-itemization rows exist; NULL is treated as 0 by consumers.
    us57_commission_paid: Mapped[Optional[Decimal]] = mapped_column(Numeric(15, 2), nullable=True, default=0)        # Sec 57(i)
    us57_interest_expense: Mapped[Optional[Decimal]] = mapped_column(Numeric(15, 2), nullable=True, default=0)       # Sec 57(i) interest on borrowed capital
    us57_bank_charges: Mapped[Optional[Decimal]] = mapped_column(Numeric(15, 2), nullable=True, default=0)           # Sec 57(iii) bank / service charges
    us57_professional_fees: Mapped[Optional[Decimal]] = mapped_column(Numeric(15, 2), nullable=True, default=0)      # Sec 57(iii) professional / legal fees
    us57_aif_expenses: Mapped[Optional[Decimal]] = mapped_column(Numeric(15, 2), nullable=True, default=0)           # AIF (Investment Fund PTI) expenses
    us57_other_expenses: Mapped[Optional[Decimal]] = mapped_column(Numeric(15, 2), nullable=True, default=0)       # Sec 57 — other allowable expenses

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
    """Fixed Other Income grid rows (Nature, Code, Source, Amount, TDS)."""

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
    quarter: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)

    os_schedule: Mapped["ITROSSchedule"] = relationship(back_populates="income_lines")
    details: Mapped[List["ITROSIncomeLineDetail"]] = relationship(
        back_populates="income_line",
        cascade="all, delete-orphan",
        order_by="ITROSIncomeLineDetail.display_order",
    )

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), onupdate=func.now())


class ITROSIncomeLineDetail(Base):
    """Breakdown rows under a fixed Other Income line (description + amount)."""

    __tablename__ = "itr_os_income_line_details"

    id: Mapped[UUID] = mapped_column(SQLUUID(as_uuid=True), primary_key=True, default=uuid4)
    income_line_id: Mapped[UUID] = mapped_column(
        SQLUUID(as_uuid=True),
        ForeignKey("itr_os_income_lines.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    display_order: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    description: Mapped[str] = mapped_column(String(200), nullable=False, default="")
    amount: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False, default=0)
    tds: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False, default=0)

    income_line: Mapped["ITROSIncomeLine"] = relationship(back_populates="details")

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
    # Foreign dividends only — qualified vs ordinary (US tax classification).
    income_dividend_type: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    # Foreign dividends only — foreign tax credit (Sec 90/91 relief) auto-filled
    # from the linked Form 67 row when the preparer clicks "Claim DTAA".
    ftc: Mapped[Optional[Decimal]] = mapped_column(Numeric(15, 2), nullable=True)
    # CBDT ``AccruOrRecOfCG.DateRange`` key — drives Sec 234C proviso
    # deferral of dividend tax. NULL = quarter not specified (compute
    # treats the row as accruing before Q1, i.e. no deferral).
    # Allowed values: Upto15Of6, Upto15Of9, Up16Of9To15Of12,
    # Up16Of12To15Of3, Up16Of3To31Of3.
    quarter: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    # Foreign dividends only — average USD→INR rate the preparer used to
    # convert the dividend (prefilled with the FY average TTBR, editable).
    exchange_rate_avg: Mapped[Optional[Decimal]] = mapped_column(
        Numeric(15, 6), nullable=True
    )
    # Foreign dividends only — dividend amount in foreign currency (USD).
    # ``amount`` stays the INR value = amount_usd × exchange_rate_avg.
    amount_usd: Mapped[Optional[Decimal]] = mapped_column(Numeric(15, 2), nullable=True)

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
    investment_entity: Mapped[Optional[str]] = mapped_column(String(30), nullable=True)

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
    sale_price_per_unit: Mapped[Optional[Decimal]] = mapped_column(Numeric(15, 4), nullable=True, default=0)
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
    # CBDT DateRange quarter slot (Q1–Q4 + Post-Q4).
    # Upto15Of6 | Upto15Of9 | Up16Of9To15Of12 | Up16Of12To15Of3 | Up16Of3To31Of3
    quarter: Mapped[str] = mapped_column(String(20), nullable=False, server_default="Upto15Of6")

    os_schedule: Mapped["ITROSSchedule"] = relationship(back_populates="clubbing_entries")

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), onupdate=func.now())


class ITROSSpecialRate(Base):
    """NRI OS income at statutory special rates (UI capture; not wired to ITR export yet)."""

    __tablename__ = "itr_os_special_rate"

    id: Mapped[UUID] = mapped_column(SQLUUID(as_uuid=True), primary_key=True, default=uuid4)
    os_schedule_id: Mapped[UUID] = mapped_column(
        SQLUUID(as_uuid=True),
        ForeignKey("itr_os_schedule.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    display_order: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    section_code: Mapped[str] = mapped_column(String(20), nullable=False)
    income: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False, default=0)
    # Sec 111 only — PF accumulated in the assessment year.
    pf_accumulated_in_ay: Mapped[Optional[Decimal]] = mapped_column(Numeric(15, 2), nullable=True)
    # Pass-through income u/s 115U / 115UA / 115UB.
    pass_through_income: Mapped[Optional[bool]] = mapped_column(Boolean, nullable=True)
    # Sec 234C proviso quarter slot (CBDT DateRange key).
    quarter: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)

    os_schedule: Mapped["ITROSSchedule"] = relationship(back_populates="special_rates")

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), onupdate=func.now())


class ITROSDtaaIncome(Base):
    """DTAA-rate income for Non-residents (Sec 90(2) beneficial rate).

    Income taxed at the applicable rate = lower of (I.T. Act rate, DTAA rate),
    with NO surcharge and NO cess (the treaty rate is the ceiling on Indian tax).
    ``applicable_rate`` and ``tax`` are computed in the engine, not persisted.
    """

    __tablename__ = "itr_os_dtaa_income"

    id: Mapped[UUID] = mapped_column(SQLUUID(as_uuid=True), primary_key=True, default=uuid4)
    os_schedule_id: Mapped[UUID] = mapped_column(
        SQLUUID(as_uuid=True),
        ForeignKey("itr_os_schedule.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    display_order: Mapped[Optional[int]] = mapped_column(Integer, nullable=True, default=1)
    nature_of_income: Mapped[Optional[str]] = mapped_column(String(255), nullable=True, default="")
    # "Section of I.T. Act" dropdown code (see app.config.dtaa_income).
    section_of_it_act: Mapped[Optional[str]] = mapped_column(String(40), nullable=True)
    it_act_rate_pct: Mapped[Optional[Decimal]] = mapped_column(Numeric(5, 2), nullable=True, default=0)
    dtaa_rate_pct: Mapped[Optional[Decimal]] = mapped_column(Numeric(5, 2), nullable=True, default=0)
    income: Mapped[Optional[Decimal]] = mapped_column(Numeric(15, 2), nullable=True, default=0)
    # CBDT numeric ISD country code (1–4 digits, e.g. 91=India, 971=UAE, 1264).
    # The CountryName for the filing JSON is resolved from this code.
    country_code: Mapped[Optional[str]] = mapped_column(String(4), nullable=True)
    article_of_dtaa: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    # Tax Residency Certificate obtained (Sec 90(4)) — drives CBDT
    # TaxRescertifiedFlag. NULL is treated as 'Y' (claiming a treaty rate
    # presupposes a TRC) until the preparer answers in the UI.
    is_trc_obtained: Mapped[Optional[bool]] = mapped_column(Boolean, nullable=True, default=True)
    # Pass-through income u/s 115U / 115UA / 115UB.
    is_pass_through: Mapped[Optional[bool]] = mapped_column(Boolean, nullable=True, default=False)
    # Sec 234C proviso quarter slot (CBDT DateRange key).
    quarter: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)

    os_schedule: Mapped["ITROSSchedule"] = relationship(back_populates="dtaa_income_rows")

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
    source_of_income: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    amount: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False, default=0)

    os_schedule: Mapped["ITROSSchedule"] = relationship(back_populates="other_income")

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), onupdate=func.now())

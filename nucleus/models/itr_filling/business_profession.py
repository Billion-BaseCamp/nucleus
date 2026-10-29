"""
ITR filing layer: Schedule BP (presumptive business and profession).

itr_returns → itr_bp_schedule (1:1) → nature-of-business, 44AE goods, GSTIN rows.
"""

from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from typing import List, Optional
from uuid import UUID, uuid4

from sqlalchemy import (
    CheckConstraint,
    DateTime,
    ForeignKey,
    Integer,
    String,
    UniqueConstraint,
    UUID as SQLUUID,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from sqlalchemy.types import Numeric

from nucleus.db.database import Base

_AD_MAX = 30_000_000
_ADA_MAX = 7_500_000


def _rupees(column: str, *, upper: int | None = None) -> Mapped[Optional[Decimal]]:
    if upper is None:
        expr = f"{column} >= 0"
    else:
        expr = f"{column} BETWEEN 0 AND {upper}"
    return mapped_column(
        Numeric(18, 2),
        CheckConstraint(expr, name=f"ck_bp_{column}"),
        nullable=True,
    )


class ITRBPSchedule(Base):
    """Schedule BP — one-to-one child of ITRReturn."""

    __tablename__ = "itr_bp_schedule"

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
    verification_status: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)

    # Income % used for 44AD / 44ADA (statutory minimum is the default)
    ad_income_pct_digital: Mapped[Optional[Decimal]] = mapped_column(
        Numeric(9, 6),
        CheckConstraint(
            "ad_income_pct_digital BETWEEN 6 AND 100", name="ck_bp_ad_income_pct_digital"
        ),
        nullable=True,
        server_default="6",
    )
    ad_income_pct_other: Mapped[Optional[Decimal]] = mapped_column(
        Numeric(9, 6),
        CheckConstraint(
            "ad_income_pct_other BETWEEN 8 AND 100", name="ck_bp_ad_income_pct_other"
        ),
        nullable=True,
        server_default="8",
    )
    ada_income_pct: Mapped[Optional[Decimal]] = mapped_column(
        Numeric(9, 6),
        CheckConstraint("ada_income_pct BETWEEN 50 AND 100", name="ck_bp_ada_income_pct"),
        nullable=True,
        server_default="50",
    )

    # PersumptiveInc44AD
    grs_total_trn_over: Mapped[Optional[Decimal]] = _rupees("grs_total_trn_over", upper=_AD_MAX)
    grs_trn_over_bank: Mapped[Optional[Decimal]] = _rupees("grs_trn_over_bank", upper=_AD_MAX)
    grs_total_trn_over_in_cash: Mapped[Optional[Decimal]] = _rupees(
        "grs_total_trn_over_in_cash", upper=_AD_MAX
    )
    grs_trn_over_any_oth_mode: Mapped[Optional[Decimal]] = _rupees(
        "grs_trn_over_any_oth_mode", upper=_AD_MAX
    )
    persumptive_inc_44ad_6_per: Mapped[Optional[Decimal]] = _rupees(
        "persumptive_inc_44ad_6_per", upper=_AD_MAX
    )
    persumptive_inc_44ad_8_per: Mapped[Optional[Decimal]] = _rupees(
        "persumptive_inc_44ad_8_per", upper=_AD_MAX
    )
    tot_persumptive_inc_44ad: Mapped[Optional[Decimal]] = _rupees(
        "tot_persumptive_inc_44ad", upper=_AD_MAX
    )

    # PersumptiveInc44ADA
    grs_receipt: Mapped[Optional[Decimal]] = _rupees("grs_receipt", upper=_ADA_MAX)
    grs_trn_over_bank_44ada: Mapped[Optional[Decimal]] = _rupees(
        "grs_trn_over_bank_44ada", upper=_ADA_MAX
    )
    grs_total_trn_over_in_cash_44ada: Mapped[Optional[Decimal]] = _rupees(
        "grs_total_trn_over_in_cash_44ada", upper=_ADA_MAX
    )
    grs_trn_over_any_oth_mode_44ada: Mapped[Optional[Decimal]] = _rupees(
        "grs_trn_over_any_oth_mode_44ada", upper=_ADA_MAX
    )
    tot_persumptive_inc_44ada: Mapped[Optional[Decimal]] = _rupees(
        "tot_persumptive_inc_44ada", upper=_ADA_MAX
    )

    # PersumptiveInc44AE
    tot_persum_inc_44ae: Mapped[Optional[Decimal]] = _rupees("tot_persum_inc_44ae")
    sal_interest_by_firm: Mapped[Optional[Decimal]] = _rupees("sal_interest_by_firm")
    total_persumptive_inc: Mapped[Optional[Decimal]] = _rupees("total_persumptive_inc")
    inc_chargeable_under_bus: Mapped[Optional[Decimal]] = mapped_column(
        Numeric(18, 2), nullable=True
    )

    total_turnover_grs_rcpt_gstin: Mapped[Optional[Decimal]] = _rupees(
        "total_turnover_grs_rcpt_gstin"
    )

    # FinanclPartclrOfBusiness
    partner_member_own_capital: Mapped[Optional[Decimal]] = _rupees("partner_member_own_capital")
    secured_loans: Mapped[Optional[Decimal]] = _rupees("secured_loans")
    un_secured_loans: Mapped[Optional[Decimal]] = _rupees("un_secured_loans")
    advances: Mapped[Optional[Decimal]] = _rupees("advances")
    sundry_creditors: Mapped[Optional[Decimal]] = _rupees("sundry_creditors")
    othr_curr_liab: Mapped[Optional[Decimal]] = _rupees("othr_curr_liab")
    tot_cap_liabilities: Mapped[Optional[Decimal]] = _rupees("tot_cap_liabilities")
    fixed_assets: Mapped[Optional[Decimal]] = _rupees("fixed_assets")
    investments: Mapped[Optional[Decimal]] = _rupees("investments")
    inventories: Mapped[Optional[Decimal]] = _rupees("inventories")
    sundry_debtors: Mapped[Optional[Decimal]] = _rupees("sundry_debtors")
    bal_with_banks: Mapped[Optional[Decimal]] = _rupees("bal_with_banks")
    cash_in_hand: Mapped[Optional[Decimal]] = _rupees("cash_in_hand")
    loans_and_advances: Mapped[Optional[Decimal]] = _rupees("loans_and_advances")
    other_assets: Mapped[Optional[Decimal]] = _rupees("other_assets")
    total_assets: Mapped[Optional[Decimal]] = _rupees("total_assets")

    itr_return: Mapped["ITRReturn"] = relationship(back_populates="bp_schedule")
    nat_of_bus_44ad: Mapped[List["ITRBPNatOfBus44AD"]] = relationship(
        back_populates="bp_schedule",
        cascade="all, delete-orphan",
        order_by="ITRBPNatOfBus44AD.line_no",
    )
    nat_of_bus_44ada: Mapped[List["ITRBPNatOfBus44ADA"]] = relationship(
        back_populates="bp_schedule",
        cascade="all, delete-orphan",
        order_by="ITRBPNatOfBus44ADA.line_no",
    )
    nat_of_bus_44ae: Mapped[List["ITRBPNatOfBus44AE"]] = relationship(
        back_populates="bp_schedule",
        cascade="all, delete-orphan",
        order_by="ITRBPNatOfBus44AE.line_no",
    )
    goods_44ae: Mapped[List["ITRBPGoods44AE"]] = relationship(
        back_populates="bp_schedule",
        cascade="all, delete-orphan",
        order_by="ITRBPGoods44AE.line_no",
    )
    gstin_turnovers: Mapped[List["ITRBPGstinTurnover"]] = relationship(
        back_populates="bp_schedule",
        cascade="all, delete-orphan",
        order_by="ITRBPGstinTurnover.line_no",
    )

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), onupdate=func.now())


class ITRBPNatOfBus44AD(Base):
    __tablename__ = "itr_bp_nat_of_bus_44ad"
    __table_args__ = (
        UniqueConstraint("bp_schedule_id", "line_no", name="uq_bp_44ad_schedule_line"),
    )

    id: Mapped[UUID] = mapped_column(SQLUUID(as_uuid=True), primary_key=True, default=uuid4)
    bp_schedule_id: Mapped[UUID] = mapped_column(
        SQLUUID(as_uuid=True),
        ForeignKey("itr_bp_schedule.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    line_no: Mapped[int] = mapped_column(Integer, nullable=False)
    name_of_business: Mapped[str] = mapped_column(String(75), nullable=False)
    code_ad: Mapped[str] = mapped_column(String(10), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(String(75), nullable=True)

    bp_schedule: Mapped["ITRBPSchedule"] = relationship(back_populates="nat_of_bus_44ad")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class ITRBPNatOfBus44ADA(Base):
    __tablename__ = "itr_bp_nat_of_bus_44ada"
    __table_args__ = (
        UniqueConstraint("bp_schedule_id", "line_no", name="uq_bp_44ada_schedule_line"),
    )

    id: Mapped[UUID] = mapped_column(SQLUUID(as_uuid=True), primary_key=True, default=uuid4)
    bp_schedule_id: Mapped[UUID] = mapped_column(
        SQLUUID(as_uuid=True),
        ForeignKey("itr_bp_schedule.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    line_no: Mapped[int] = mapped_column(Integer, nullable=False)
    name_of_business: Mapped[str] = mapped_column(String(75), nullable=False)
    code_ada: Mapped[str] = mapped_column(String(10), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(String(75), nullable=True)

    bp_schedule: Mapped["ITRBPSchedule"] = relationship(back_populates="nat_of_bus_44ada")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class ITRBPNatOfBus44AE(Base):
    __tablename__ = "itr_bp_nat_of_bus_44ae"
    __table_args__ = (
        UniqueConstraint("bp_schedule_id", "line_no", name="uq_bp_44ae_schedule_line"),
        CheckConstraint(
            "code_ae IN ('08001', '11002', '11008', '11010', '11011', '11012', '11015')",
            name="ck_bp_44ae_code",
        ),
    )

    id: Mapped[UUID] = mapped_column(SQLUUID(as_uuid=True), primary_key=True, default=uuid4)
    bp_schedule_id: Mapped[UUID] = mapped_column(
        SQLUUID(as_uuid=True),
        ForeignKey("itr_bp_schedule.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    line_no: Mapped[int] = mapped_column(Integer, nullable=False)
    name_of_business: Mapped[str] = mapped_column(String(75), nullable=False)
    code_ae: Mapped[str] = mapped_column(String(10), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(String(75), nullable=True)

    bp_schedule: Mapped["ITRBPSchedule"] = relationship(back_populates="nat_of_bus_44ae")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class ITRBPGoods44AE(Base):
    __tablename__ = "itr_bp_goods_44ae"
    __table_args__ = (
        UniqueConstraint("bp_schedule_id", "line_no", name="uq_bp_goods_44ae_schedule_line"),
        CheckConstraint("line_no BETWEEN 1 AND 10", name="ck_bp_goods_44ae_line_no"),
        CheckConstraint(
            "owned_leased_hired_flag IN ('OWN', 'LEASE', 'HIRED')",
            name="ck_bp_goods_44ae_owned_flag",
        ),
        CheckConstraint(
            "tonnage_capacity BETWEEN 0 AND 100",
            name="ck_bp_goods_44ae_tonnage",
        ),
        CheckConstraint(
            "holding_period BETWEEN 1 AND 12",
            name="ck_bp_goods_44ae_holding_period",
        ),
        CheckConstraint(
            "presumptive_income BETWEEN 7500 AND 99999999999999",
            name="ck_bp_goods_44ae_presumptive_income",
        ),
    )

    id: Mapped[UUID] = mapped_column(SQLUUID(as_uuid=True), primary_key=True, default=uuid4)
    bp_schedule_id: Mapped[UUID] = mapped_column(
        SQLUUID(as_uuid=True),
        ForeignKey("itr_bp_schedule.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    line_no: Mapped[int] = mapped_column(Integer, nullable=False)
    reg_number_goods_carriage: Mapped[str] = mapped_column(String(11), nullable=False)
    owned_leased_hired_flag: Mapped[str] = mapped_column(String(5), nullable=False)
    tonnage_capacity: Mapped[int] = mapped_column(Integer, nullable=False)
    holding_period: Mapped[int] = mapped_column(Integer, nullable=False)
    presumptive_income: Mapped[Decimal] = mapped_column(Numeric(18, 2), nullable=False)

    bp_schedule: Mapped["ITRBPSchedule"] = relationship(back_populates="goods_44ae")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class ITRBPGstinTurnover(Base):
    __tablename__ = "itr_bp_gstin_turnover"
    __table_args__ = (
        UniqueConstraint("bp_schedule_id", "line_no", name="uq_bp_gstin_schedule_line"),
        CheckConstraint(
            "gstin_no ~ '^[0-9]{2}[A-Z]{5}[0-9]{4}[A-Z][0-9A-Z]{3}$'",
            name="ck_bp_gstin_no",
        ),
        CheckConstraint(
            "amt_turn_gross_rcpt_gstin >= 0",
            name="ck_bp_gstin_turnover_non_negative",
        ),
    )

    id: Mapped[UUID] = mapped_column(SQLUUID(as_uuid=True), primary_key=True, default=uuid4)
    bp_schedule_id: Mapped[UUID] = mapped_column(
        SQLUUID(as_uuid=True),
        ForeignKey("itr_bp_schedule.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    line_no: Mapped[int] = mapped_column(Integer, nullable=False)
    gstin_no: Mapped[str] = mapped_column(String(15), nullable=False)
    amt_turn_gross_rcpt_gstin: Mapped[Decimal] = mapped_column(Numeric(18, 2), nullable=False)

    bp_schedule: Mapped["ITRBPSchedule"] = relationship(back_populates="gstin_turnovers")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

"""
ITR filing: Capital gains (Schedule CG) persistence.

Root `itr_cg_data` is 1:1 with `itr_returns`. High-volume trade rows and
HP CG detail trees hang off the root.
"""

from __future__ import annotations

from datetime import date, datetime
from decimal import Decimal
from typing import TYPE_CHECKING, List, Optional
from uuid import UUID, uuid4

if TYPE_CHECKING:
    from nucleus.models.itr_filling.itr_return import ITRReturn

from sqlalchemy import (
    Boolean,
    Date,
    DateTime,
    ForeignKey,
    Index,
    Integer,
    String,
    UniqueConstraint,
    UUID as SQLUUID,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from sqlalchemy.types import Numeric

from nucleus.db.database import Base


class ITRCGData(Base):
    __tablename__ = "itr_cg_data"

    id: Mapped[UUID] = mapped_column(SQLUUID(as_uuid=True), primary_key=True, default=uuid4)
    itr_return_id: Mapped[UUID] = mapped_column(
        SQLUUID(as_uuid=True),
        ForeignKey("itr_returns.id", ondelete="CASCADE"),
        nullable=False,
        unique=True,
        index=True,
    )

    computed_stcg_111a: Mapped[Optional[Decimal]] = mapped_column(Numeric(15, 2), nullable=True)
    computed_stcg_other_assets: Mapped[Optional[Decimal]] = mapped_column(Numeric(15, 2), nullable=True)
    computed_stcg_land_building: Mapped[Optional[Decimal]] = mapped_column(Numeric(15, 2), nullable=True)
    computed_stcg_deemed: Mapped[Optional[Decimal]] = mapped_column(Numeric(15, 2), nullable=True)
    computed_stcg_pti: Mapped[Optional[Decimal]] = mapped_column(Numeric(15, 2), nullable=True)
    computed_total_stcg: Mapped[Optional[Decimal]] = mapped_column(Numeric(15, 2), nullable=True)

    computed_ltcg_112a: Mapped[Optional[Decimal]] = mapped_column(Numeric(15, 2), nullable=True)
    computed_ltcg_bonds_debentures: Mapped[Optional[Decimal]] = mapped_column(Numeric(15, 2), nullable=True)
    computed_ltcg_land_building: Mapped[Optional[Decimal]] = mapped_column(Numeric(15, 2), nullable=True)
    computed_ltcg_other_assets: Mapped[Optional[Decimal]] = mapped_column(Numeric(15, 2), nullable=True)
    computed_ltcg_deemed: Mapped[Optional[Decimal]] = mapped_column(Numeric(15, 2), nullable=True)
    computed_ltcg_pti: Mapped[Optional[Decimal]] = mapped_column(Numeric(15, 2), nullable=True)
    computed_total_ltcg: Mapped[Optional[Decimal]] = mapped_column(Numeric(15, 2), nullable=True)

    computed_total_exemption_54: Mapped[Optional[Decimal]] = mapped_column(Numeric(15, 2), nullable=True)
    computed_total_exemption_54b: Mapped[Optional[Decimal]] = mapped_column(Numeric(15, 2), nullable=True)
    computed_total_exemption_54ec: Mapped[Optional[Decimal]] = mapped_column(Numeric(15, 2), nullable=True)
    computed_total_exemption_54f: Mapped[Optional[Decimal]] = mapped_column(Numeric(15, 2), nullable=True)
    computed_total_exemptions: Mapped[Optional[Decimal]] = mapped_column(Numeric(15, 2), nullable=True)

    computed_vda_income: Mapped[Optional[Decimal]] = mapped_column(Numeric(15, 2), nullable=True)

    computed_sum_cg_income: Mapped[Optional[Decimal]] = mapped_column(Numeric(15, 2), nullable=True)
    computed_total_schedule_cg: Mapped[Optional[Decimal]] = mapped_column(Numeric(15, 2), nullable=True)

    computed_buyback_loss_stcg: Mapped[Optional[Decimal]] = mapped_column(Numeric(15, 2), nullable=True)
    computed_buyback_loss_ltcg: Mapped[Optional[Decimal]] = mapped_column(Numeric(15, 2), nullable=True)

    computed_112a_sale_value: Mapped[Optional[Decimal]] = mapped_column(Numeric(15, 2), nullable=True)
    computed_112a_cost_acq: Mapped[Optional[Decimal]] = mapped_column(Numeric(15, 2), nullable=True)
    computed_112a_acq_cost: Mapped[Optional[Decimal]] = mapped_column(Numeric(15, 2), nullable=True)
    computed_112a_fmv: Mapped[Optional[Decimal]] = mapped_column(Numeric(15, 2), nullable=True)
    computed_112a_expenses: Mapped[Optional[Decimal]] = mapped_column(Numeric(15, 2), nullable=True)
    computed_112a_deductions: Mapped[Optional[Decimal]] = mapped_column(Numeric(15, 2), nullable=True)
    computed_112a_balance: Mapped[Optional[Decimal]] = mapped_column(Numeric(15, 2), nullable=True)
    computed_112a_balance_be: Mapped[Optional[Decimal]] = mapped_column(Numeric(15, 2), nullable=True)
    computed_112a_balance_ae: Mapped[Optional[Decimal]] = mapped_column(Numeric(15, 2), nullable=True)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), onupdate=func.now())

    itr_return: Mapped["ITRReturn"] = relationship("ITRReturn", back_populates="cg_data")
    india_eq_entries: Mapped[List["ITRCGIndiaEQEntry"]] = relationship(
        back_populates="cg_data",
        cascade="all, delete-orphan",
        order_by="ITRCGIndiaEQEntry.display_order",
    )
    debt_mf_entries: Mapped[List["ITRCGDebtMFEntry"]] = relationship(
        back_populates="cg_data",
        cascade="all, delete-orphan",
        order_by="ITRCGDebtMFEntry.display_order",
    )
    us_entries: Mapped[List["ITRCGUSEntry"]] = relationship(
        back_populates="cg_data",
        cascade="all, delete-orphan",
        order_by="ITRCGUSEntry.display_order",
    )
    unlisted_entries: Mapped[List["ITRCGUnlistedEntry"]] = relationship(
        back_populates="cg_data",
        cascade="all, delete-orphan",
        order_by="ITRCGUnlistedEntry.display_order",
    )
    hp_entries: Mapped[List["ITRCGHPEntry"]] = relationship(
        back_populates="cg_data",
        cascade="all, delete-orphan",
        order_by="ITRCGHPEntry.display_order",
    )
    vda_entries: Mapped[List["ITRCGVDAEntry"]] = relationship(
        back_populates="cg_data",
        cascade="all, delete-orphan",
        order_by="ITRCGVDAEntry.display_order",
    )
    exemptions_54f: Mapped[List["ITRCGExemption54F"]] = relationship(
        back_populates="cg_data",
        cascade="all, delete-orphan",
        order_by="ITRCGExemption54F.display_order",
    )
    exemptions_54ec: Mapped[List["ITRCGExemption54EC"]] = relationship(
        back_populates="cg_data",
        cascade="all, delete-orphan",
        order_by="ITRCGExemption54EC.display_order",
    )
    bfl_years: Mapped[List["ITRCGBFLYear"]] = relationship(
        back_populates="cg_data",
        cascade="all, delete-orphan",
        order_by="ITRCGBFLYear.display_order",
    )
    broker_summaries: Mapped[List["ITRCGBrokerSummary"]] = relationship(
        back_populates="cg_data",
        cascade="all, delete-orphan",
    )


class ITRCGIndiaEQEntry(Base):
    __tablename__ = "itr_cg_india_eq_entries"

    id: Mapped[UUID] = mapped_column(SQLUUID(as_uuid=True), primary_key=True, default=uuid4)
    cg_data_id: Mapped[UUID] = mapped_column(
        SQLUUID(as_uuid=True),
        ForeignKey("itr_cg_data.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    display_order: Mapped[int] = mapped_column(Integer, nullable=False, default=1)

    broker: Mapped[str] = mapped_column(String(100), nullable=False)
    stock_scheme: Mapped[Optional[str]] = mapped_column(String(200), nullable=True)
    nature_of_asset: Mapped[str] = mapped_column(String(30), nullable=False, default="Equity")
    isin_code: Mapped[Optional[str]] = mapped_column(String(12), nullable=True)

    quantity: Mapped[Decimal] = mapped_column(Numeric(15, 4), nullable=False, default=0)
    date_of_purchase: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    date_of_transfer: Mapped[Optional[date]] = mapped_column(Date, nullable=True)

    sale_consideration: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False, default=0)
    selling_expenses: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False, default=0)
    net_sale_consideration: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False, default=0)
    cost_of_acquisition: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False, default=0)

    fmv_per_share: Mapped[Optional[Decimal]] = mapped_column(Numeric(15, 4), nullable=True)
    fmv_value: Mapped[Optional[Decimal]] = mapped_column(Numeric(15, 2), nullable=True)

    holding_period: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    long_short: Mapped[str] = mapped_column(String(5), nullable=False, default="Short")

    ltcg_112a: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False, default=0)
    stcg_111a: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False, default=0)

    share_on_or_before: Mapped[Optional[str]] = mapped_column(String(2), nullable=True)
    share_transferred_on_or_before: Mapped[Optional[str]] = mapped_column(String(2), nullable=True)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), onupdate=func.now())

    cg_data: Mapped["ITRCGData"] = relationship("ITRCGData", back_populates="india_eq_entries")

    __table_args__ = (
        Index("ix_cg_india_eq_broker_ls", "cg_data_id", "broker", "long_short"),
        Index("ix_cg_india_eq_long_short", "cg_data_id", "long_short"),
        Index("ix_cg_india_eq_date", "cg_data_id", "date_of_transfer"),
    )


class ITRCGDebtMFEntry(Base):
    __tablename__ = "itr_cg_debt_mf_entries"

    id: Mapped[UUID] = mapped_column(SQLUUID(as_uuid=True), primary_key=True, default=uuid4)
    cg_data_id: Mapped[UUID] = mapped_column(
        SQLUUID(as_uuid=True),
        ForeignKey("itr_cg_data.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    display_order: Mapped[int] = mapped_column(Integer, nullable=False, default=1)

    rta: Mapped[str] = mapped_column(String(20), nullable=False, default="CAMS")
    mf_category: Mapped[str] = mapped_column(String(20), nullable=False, default="Equity")

    particulars: Mapped[Optional[str]] = mapped_column(String(200), nullable=True)
    listed_unlisted: Mapped[str] = mapped_column(String(10), nullable=False, default="Listed")
    isin_code: Mapped[Optional[str]] = mapped_column(String(12), nullable=True)

    quantity: Mapped[Decimal] = mapped_column(Numeric(15, 4), nullable=False, default=0)
    date_of_purchase: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    date_of_transfer: Mapped[Optional[date]] = mapped_column(Date, nullable=True)

    sale_consideration: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False, default=0)
    selling_expenses: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False, default=0)
    net_sale_consideration: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False, default=0)
    cost_of_acquisition: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False, default=0)

    fmv_value: Mapped[Optional[Decimal]] = mapped_column(Numeric(15, 2), nullable=True)
    year_of_acquisition: Mapped[Optional[str]] = mapped_column(String(10), nullable=True)
    cii: Mapped[Optional[Decimal]] = mapped_column(Numeric(10, 2), nullable=True)
    indexed_cost: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False, default=0)
    actual_cost: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False, default=0)

    holding_period: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    long_short: Mapped[str] = mapped_column(String(5), nullable=False, default="Short")

    stcg: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False, default=0)
    ltcg_20: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False, default=0)
    ltcg_12_5: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False, default=0)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), onupdate=func.now())

    cg_data: Mapped["ITRCGData"] = relationship("ITRCGData", back_populates="debt_mf_entries")

    __table_args__ = (
        Index("ix_cg_debt_mf_rta_cat_ls", "cg_data_id", "rta", "mf_category", "long_short"),
        Index("ix_cg_debt_mf_long_short", "cg_data_id", "long_short"),
    )


class ITRCGUSEntry(Base):
    __tablename__ = "itr_cg_us_entries"

    id: Mapped[UUID] = mapped_column(SQLUUID(as_uuid=True), primary_key=True, default=uuid4)
    cg_data_id: Mapped[UUID] = mapped_column(
        SQLUUID(as_uuid=True),
        ForeignKey("itr_cg_data.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    display_order: Mapped[int] = mapped_column(Integer, nullable=False, default=1)

    broker: Mapped[str] = mapped_column(String(100), nullable=False)
    stock_name: Mapped[Optional[str]] = mapped_column(String(200), nullable=True)

    quantity: Mapped[Decimal] = mapped_column(Numeric(15, 4), nullable=False, default=0)
    date_of_sale: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    date_of_purchase: Mapped[Optional[date]] = mapped_column(Date, nullable=True)

    sale_value_per_share: Mapped[Decimal] = mapped_column(Numeric(15, 4), nullable=False, default=0)
    sale_value_usd: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False, default=0)
    purchase_value_per_share: Mapped[Decimal] = mapped_column(Numeric(15, 4), nullable=False, default=0)
    purchase_value_usd: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False, default=0)
    capital_gain_usd: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False, default=0)

    exchange_rate_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    exchange_rate: Mapped[Decimal] = mapped_column(Numeric(10, 4), nullable=False, default=0)

    sale_value_inr: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False, default=0)
    fmv: Mapped[Optional[Decimal]] = mapped_column(Numeric(15, 2), nullable=True)
    full_consideration_50ca: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False, default=0)
    purchase_value_inr: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False, default=0)

    year_of_purchase: Mapped[Optional[str]] = mapped_column(String(10), nullable=True)
    indexation_rate: Mapped[Optional[Decimal]] = mapped_column(Numeric(10, 4), nullable=True)
    indexed_cost: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False, default=0)
    actual_cost: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False, default=0)

    holding_period: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    long_short: Mapped[str] = mapped_column(String(5), nullable=False, default="Short")

    stcg_inr: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False, default=0)
    ltcg_inr: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False, default=0)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), onupdate=func.now())

    cg_data: Mapped["ITRCGData"] = relationship("ITRCGData", back_populates="us_entries")

    __table_args__ = (
        Index("ix_cg_us_broker_ls", "cg_data_id", "broker", "long_short"),
        Index("ix_cg_us_long_short", "cg_data_id", "long_short"),
    )


class ITRCGUnlistedEntry(Base):
    __tablename__ = "itr_cg_unlisted_entries"

    id: Mapped[UUID] = mapped_column(SQLUUID(as_uuid=True), primary_key=True, default=uuid4)
    cg_data_id: Mapped[UUID] = mapped_column(
        SQLUUID(as_uuid=True),
        ForeignKey("itr_cg_data.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    display_order: Mapped[int] = mapped_column(Integer, nullable=False, default=1)

    stock_name: Mapped[Optional[str]] = mapped_column(String(200), nullable=True)

    quantity: Mapped[Decimal] = mapped_column(Numeric(15, 4), nullable=False, default=0)
    date_of_sale: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    date_of_purchase: Mapped[Optional[date]] = mapped_column(Date, nullable=True)

    sale_value_per_share: Mapped[Decimal] = mapped_column(Numeric(15, 4), nullable=False, default=0)
    selling_expenses: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False, default=0)
    purchase_value_per_share: Mapped[Decimal] = mapped_column(Numeric(15, 4), nullable=False, default=0)

    exchange_rate_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    exchange_rate: Mapped[Optional[Decimal]] = mapped_column(Numeric(10, 4), nullable=True, default=0)

    sale_value: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False, default=0)
    fmv: Mapped[Optional[Decimal]] = mapped_column(Numeric(15, 2), nullable=True)
    full_consideration_50ca: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False, default=0)
    purchase_value: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False, default=0)

    year_of_purchase: Mapped[Optional[str]] = mapped_column(String(10), nullable=True)
    indexation_rate: Mapped[Optional[Decimal]] = mapped_column(Numeric(10, 4), nullable=True)
    indexed_cost: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False, default=0)
    actual_cost: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False, default=0)

    holding_period: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    long_short: Mapped[str] = mapped_column(String(5), nullable=False, default="Short")

    stcg: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False, default=0)
    ltcg: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False, default=0)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), onupdate=func.now())

    cg_data: Mapped["ITRCGData"] = relationship("ITRCGData", back_populates="unlisted_entries")


class ITRCGHPEntry(Base):
    __tablename__ = "itr_cg_hp_entries"

    id: Mapped[UUID] = mapped_column(SQLUUID(as_uuid=True), primary_key=True, default=uuid4)
    cg_data_id: Mapped[UUID] = mapped_column(
        SQLUUID(as_uuid=True),
        ForeignKey("itr_cg_data.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    display_order: Mapped[int] = mapped_column(Integer, nullable=False, default=1)

    property_type: Mapped[str] = mapped_column(String(50), nullable=False, default="Residential Property")
    ownership_pct: Mapped[Decimal] = mapped_column(Numeric(5, 2), nullable=False, default=100)

    address_line: Mapped[Optional[str]] = mapped_column(String(250), nullable=True)
    state: Mapped[Optional[str]] = mapped_column(String(5), nullable=True)
    pin: Mapped[Optional[str]] = mapped_column(String(6), nullable=True)

    date_of_acquisition: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    date_of_transfer: Mapped[Optional[date]] = mapped_column(Date, nullable=True)

    sale_consideration: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False, default=0)
    stamp_duty_value_50c: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False, default=0)
    property_valuation: Mapped[Optional[Decimal]] = mapped_column(Numeric(15, 2), nullable=True)

    capital_gain_without_idx: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False, default=0)
    capital_gain_with_idx: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False, default=0)
    share_of_cg_without_idx: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False, default=0)
    share_of_cg_with_idx: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False, default=0)
    net_capital_gain_without_idx: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False, default=0)
    net_capital_gain_with_idx: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False, default=0)
    tax_on_cg_without_idx: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False, default=0)
    tax_on_cg_with_idx: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False, default=0)
    taxable_capital_gain: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False, default=0)

    deemed_full_value_50c: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False, default=0)
    net_consideration_for_54f: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False, default=0)

    claim_sec_54: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    sec54_new_house_address: Mapped[Optional[str]] = mapped_column(String(250), nullable=True)
    sec54_new_house_date_of_purchase: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    sec54_new_house_date_of_construction: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    sec54_cost_of_new_house: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False, default=0)
    sec54_amount_deposited: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False, default=0)
    sec54_date_of_deposit: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    sec54_cgas_account_no: Mapped[Optional[str]] = mapped_column(String(30), nullable=True)
    sec54_cgas_bank_name: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    sec54_cgas_ifsc: Mapped[Optional[str]] = mapped_column(String(11), nullable=True)
    sec54_total_invested: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False, default=0)
    sec54_exempt_amount: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False, default=0)
    sec54_balance_taxable_gain: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False, default=0)

    balance_for_eib: Mapped[Optional[Decimal]] = mapped_column(Numeric(15, 2), nullable=True)
    total_dedn_for_eib: Mapped[Optional[Decimal]] = mapped_column(Numeric(15, 2), nullable=True)
    tax_sec_1121a_ii_b: Mapped[Optional[Decimal]] = mapped_column(Numeric(15, 2), nullable=True)
    tax_sec_1121a: Mapped[Optional[Decimal]] = mapped_column(Numeric(15, 2), nullable=True)
    excess_amt_sec_1121a: Mapped[Optional[Decimal]] = mapped_column(Numeric(15, 2), nullable=True)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), onupdate=func.now())

    cg_data: Mapped["ITRCGData"] = relationship("ITRCGData", back_populates="hp_entries")
    acquisition_details: Mapped[List["ITRCGHPAcquisitionDetail"]] = relationship(
        back_populates="hp_entry",
        cascade="all, delete-orphan",
        order_by="ITRCGHPAcquisitionDetail.display_order",
    )
    improvements: Mapped[List["ITRCGHPImprovement"]] = relationship(
        back_populates="hp_entry",
        cascade="all, delete-orphan",
        order_by="ITRCGHPImprovement.display_order",
    )
    transfer_expenses: Mapped[List["ITRCGHPTransferExpense"]] = relationship(
        back_populates="hp_entry",
        cascade="all, delete-orphan",
        order_by="ITRCGHPTransferExpense.display_order",
    )
    buyers: Mapped[List["ITRCGHPBuyer"]] = relationship(
        back_populates="hp_entry",
        cascade="all, delete-orphan",
        order_by="ITRCGHPBuyer.display_order",
    )


class ITRCGHPAcquisitionDetail(Base):
    __tablename__ = "itr_cg_hp_acquisition_details"

    id: Mapped[UUID] = mapped_column(SQLUUID(as_uuid=True), primary_key=True, default=uuid4)
    hp_entry_id: Mapped[UUID] = mapped_column(
        SQLUUID(as_uuid=True),
        ForeignKey("itr_cg_hp_entries.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    display_order: Mapped[int] = mapped_column(Integer, nullable=False, default=1)

    description: Mapped[Optional[str]] = mapped_column(String(200), nullable=True)
    financial_year: Mapped[Optional[str]] = mapped_column(String(10), nullable=True)
    cost_without_indexation: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False, default=0)
    cost_with_indexation: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False, default=0)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), onupdate=func.now())

    hp_entry: Mapped["ITRCGHPEntry"] = relationship("ITRCGHPEntry", back_populates="acquisition_details")


class ITRCGHPImprovement(Base):
    __tablename__ = "itr_cg_hp_improvements"

    id: Mapped[UUID] = mapped_column(SQLUUID(as_uuid=True), primary_key=True, default=uuid4)
    hp_entry_id: Mapped[UUID] = mapped_column(
        SQLUUID(as_uuid=True),
        ForeignKey("itr_cg_hp_entries.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    display_order: Mapped[int] = mapped_column(Integer, nullable=False, default=1)

    description: Mapped[Optional[str]] = mapped_column(String(200), nullable=True)
    financial_year: Mapped[Optional[str]] = mapped_column(String(10), nullable=True)
    cost_without_indexation: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False, default=0)
    cost_with_indexation: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False, default=0)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), onupdate=func.now())

    hp_entry: Mapped["ITRCGHPEntry"] = relationship("ITRCGHPEntry", back_populates="improvements")


class ITRCGHPTransferExpense(Base):
    __tablename__ = "itr_cg_hp_transfer_expenses"

    id: Mapped[UUID] = mapped_column(SQLUUID(as_uuid=True), primary_key=True, default=uuid4)
    hp_entry_id: Mapped[UUID] = mapped_column(
        SQLUUID(as_uuid=True),
        ForeignKey("itr_cg_hp_entries.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    display_order: Mapped[int] = mapped_column(Integer, nullable=False, default=1)

    description: Mapped[Optional[str]] = mapped_column(String(200), nullable=True)
    amount: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False, default=0)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), onupdate=func.now())

    hp_entry: Mapped["ITRCGHPEntry"] = relationship("ITRCGHPEntry", back_populates="transfer_expenses")


class ITRCGHPBuyer(Base):
    __tablename__ = "itr_cg_hp_buyers"

    id: Mapped[UUID] = mapped_column(SQLUUID(as_uuid=True), primary_key=True, default=uuid4)
    hp_entry_id: Mapped[UUID] = mapped_column(
        SQLUUID(as_uuid=True),
        ForeignKey("itr_cg_hp_entries.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    display_order: Mapped[int] = mapped_column(Integer, nullable=False, default=1)

    name: Mapped[Optional[str]] = mapped_column(String(125), nullable=True)
    pan: Mapped[Optional[str]] = mapped_column(String(10), nullable=True)
    aadhaar: Mapped[Optional[str]] = mapped_column(String(12), nullable=True)
    ownership_pct: Mapped[Decimal] = mapped_column(Numeric(5, 2), nullable=False, default=0)
    ownership_amount: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False, default=0)

    address_of_property: Mapped[Optional[str]] = mapped_column(String(250), nullable=True)
    state_code: Mapped[Optional[str]] = mapped_column(String(5), nullable=True)
    country_code: Mapped[Optional[str]] = mapped_column(String(5), nullable=True, default="91")
    pin_code: Mapped[Optional[str]] = mapped_column(String(6), nullable=True)
    zip_code: Mapped[Optional[str]] = mapped_column(String(8), nullable=True)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), onupdate=func.now())

    hp_entry: Mapped["ITRCGHPEntry"] = relationship("ITRCGHPEntry", back_populates="buyers")


class ITRCGVDAEntry(Base):
    __tablename__ = "itr_cg_vda_entries"

    id: Mapped[UUID] = mapped_column(SQLUUID(as_uuid=True), primary_key=True, default=uuid4)
    cg_data_id: Mapped[UUID] = mapped_column(
        SQLUUID(as_uuid=True),
        ForeignKey("itr_cg_data.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    display_order: Mapped[int] = mapped_column(Integer, nullable=False, default=1)

    date_of_acquisition: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    date_of_transfer: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    head_und_inc_taxed: Mapped[str] = mapped_column(String(5), nullable=False, default="CG")
    cost_of_acquisition: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False, default=0)
    consideration_received: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False, default=0)
    income: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False, default=0)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), onupdate=func.now())

    cg_data: Mapped["ITRCGData"] = relationship("ITRCGData", back_populates="vda_entries")


class ITRCGExemption54F(Base):
    __tablename__ = "itr_cg_exemptions_54f"

    id: Mapped[UUID] = mapped_column(SQLUUID(as_uuid=True), primary_key=True, default=uuid4)
    cg_data_id: Mapped[UUID] = mapped_column(
        SQLUUID(as_uuid=True),
        ForeignKey("itr_cg_data.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    display_order: Mapped[int] = mapped_column(Integer, nullable=False, default=1)

    source: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    description: Mapped[Optional[str]] = mapped_column(String(200), nullable=True)
    date_of_transfer: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    net_sale_consideration: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False, default=0)
    capital_gain: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False, default=0)

    new_house_address: Mapped[Optional[str]] = mapped_column(String(250), nullable=True)
    date_of_purchase: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    date_of_construction: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    cost_of_new_house: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False, default=0)

    cg_scheme_deposit: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False, default=0)
    date_of_deposit: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    cgas_account_no: Mapped[Optional[str]] = mapped_column(String(30), nullable=True)
    cgas_bank_name: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    cgas_ifsc: Mapped[Optional[str]] = mapped_column(String(11), nullable=True)

    total_invested: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False, default=0)
    exempt_amount: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False, default=0)
    net_taxable_gain: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False, default=0)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), onupdate=func.now())

    cg_data: Mapped["ITRCGData"] = relationship("ITRCGData", back_populates="exemptions_54f")


class ITRCGExemption54EC(Base):
    __tablename__ = "itr_cg_exemptions_54ec"

    id: Mapped[UUID] = mapped_column(SQLUUID(as_uuid=True), primary_key=True, default=uuid4)
    cg_data_id: Mapped[UUID] = mapped_column(
        SQLUUID(as_uuid=True),
        ForeignKey("itr_cg_data.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    display_order: Mapped[int] = mapped_column(Integer, nullable=False, default=1)

    source: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    description: Mapped[Optional[str]] = mapped_column(String(200), nullable=True)
    date_of_transfer: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    capital_gain: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False, default=0)
    bond_type: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    date_of_investment: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    amount_invested: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False, default=0)
    exempt_amount: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False, default=0)
    net_taxable_gain: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False, default=0)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), onupdate=func.now())

    cg_data: Mapped["ITRCGData"] = relationship("ITRCGData", back_populates="exemptions_54ec")


class ITRCGBFLYear(Base):
    __tablename__ = "itr_cg_bfl_years"

    id: Mapped[UUID] = mapped_column(SQLUUID(as_uuid=True), primary_key=True, default=uuid4)
    cg_data_id: Mapped[UUID] = mapped_column(
        SQLUUID(as_uuid=True),
        ForeignKey("itr_cg_data.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    display_order: Mapped[int] = mapped_column(Integer, nullable=False, default=1)

    assessment_year: Mapped[str] = mapped_column(String(10), nullable=False)
    date_of_return: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    hp_loss: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False, default=0)
    speculation_loss: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False, default=0)
    specified_business_loss: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False, default=0)
    ordinary_business_loss: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False, default=0)
    depreciation: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False, default=0)
    sec35_4: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False, default=0)
    ltcg_loss: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False, default=0)
    stcg_loss: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False, default=0)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), onupdate=func.now())

    cg_data: Mapped["ITRCGData"] = relationship("ITRCGData", back_populates="bfl_years")


class ITRCGBrokerSummary(Base):
    __tablename__ = "itr_cg_broker_summaries"

    id: Mapped[UUID] = mapped_column(SQLUUID(as_uuid=True), primary_key=True, default=uuid4)
    cg_data_id: Mapped[UUID] = mapped_column(
        SQLUUID(as_uuid=True),
        ForeignKey("itr_cg_data.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    asset_class: Mapped[str] = mapped_column(String(20), nullable=False)
    broker_name: Mapped[str] = mapped_column(String(100), nullable=False)
    sub_category: Mapped[Optional[str]] = mapped_column(String(30), nullable=True)

    total_trades: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    short_term_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    long_term_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    total_sale_consideration: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False, default=0)
    total_cost_of_acquisition: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False, default=0)
    total_stcg: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False, default=0)
    total_ltcg: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False, default=0)
    net_gain: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False, default=0)

    last_refreshed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    cg_data: Mapped["ITRCGData"] = relationship("ITRCGData", back_populates="broker_summaries")

    __table_args__ = (
        UniqueConstraint(
            "cg_data_id",
            "asset_class",
            "broker_name",
            "sub_category",
            name="uq_cg_broker_summary",
        ),
        Index("ix_cg_broker_summary_class", "cg_data_id", "asset_class"),
    )

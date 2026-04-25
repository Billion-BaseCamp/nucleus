"""
ITR filing: Capital gains (Schedule CG) persistence.

Root `itr_cg_schedule` is 1:1 with `itr_returns`. High-volume trade rows and
HP CG detail trees hang off the schedule.
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
    Integer,
    String,
    UUID as SQLUUID,
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from sqlalchemy.types import Numeric

from nucleus.db.database import Base


class ITRCGSchedule(Base):
    __tablename__ = "itr_cg_schedule"

    id: Mapped[UUID] = mapped_column(SQLUUID(as_uuid=True), primary_key=True, default=uuid4)
    itr_return_id: Mapped[UUID] = mapped_column(
        SQLUUID(as_uuid=True),
        ForeignKey("itr_returns.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    stcg_india_eq: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False, default=0)
    stcg_mutual_funds: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False, default=0)
    stcg_us_foreign: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False, default=0)
    stcg_unlisted: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False, default=0)
    total_stcg: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False, default=0)
    ltcg_india_eq: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False, default=0)
    ltcg_mutual_funds: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False, default=0)
    ltcg_us_foreign: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False, default=0)
    ltcg_unlisted: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False, default=0)
    total_ltcg: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False, default=0)

    total_hp_gain: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False, default=0)
    total_exempt_gain: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False, default=0)
    total_bf_loss: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False, default=0)
    total_vda_gain: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False, default=0)

    total_capital_gain: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False, default=0)

    quarterly_breakdown: Mapped[Optional[dict]] = mapped_column(JSONB, nullable=True)
    """Per-quarter STCG/LTCG summary extracted from broker CG statements.

    Shape:
        {
          "equity_listed": {"Q1": {"stcg": 50000, "ltcg": 120000}, "Q2": {...}, "Q3": {...}, "Q4": {...}},
          "debt_mf": {...},
          "unlisted": {...}
        }
    V1 stores it without compute; V1.1 consumes it for Sec 234C advance-tax
    deficit interest calculation.
    """

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), onupdate=func.now())


    india_eq_and_debt_mf_brokers: Mapped[List["ITRCGIndiaEQAndDebtMFBroker"]] = relationship(
        back_populates="cg_schedule",
        cascade="all, delete-orphan",
        order_by="ITRCGIndiaEQAndDebtMFBroker.display_order",
    )
    us_brokers: Mapped[List["ITRCGUSBroker"]] = relationship(
        back_populates="cg_schedule",
        cascade="all, delete-orphan",
        order_by="ITRCGUSBroker.display_order",
    )

    unlisted_transactions: Mapped[List["ITRCGUnlistedTransaction"]] = relationship(
        back_populates="cg_schedule",
        cascade="all, delete-orphan",
        order_by="ITRCGUnlistedTransaction.display_order",
    )

    vda_transactions: Mapped[List["ITRCGVDATransaction"]] = relationship(
        back_populates="cg_schedule",
        cascade="all, delete-orphan",
        order_by="ITRCGVDATransaction.display_order",
    )

    exemptions_54: Mapped[List["ITRCGExemption54"]] = relationship(
        back_populates="cg_schedule",
        cascade="all, delete-orphan",
        order_by="ITRCGExemption54.display_order",
    )
    exemptions_54f: Mapped[List["ITRCGExemption54F"]] = relationship(
        back_populates="cg_schedule",
        cascade="all, delete-orphan",
        order_by="ITRCGExemption54F.created_at",
    )
    hp_entries: Mapped[List["ITRCGHPEntry"]] = relationship(
        back_populates="cg_schedule",
        cascade="all, delete-orphan",
        order_by="ITRCGHPEntry.display_order",
    )

    bond_entries: Mapped[List["ITRCGBondEntry"]] = relationship(
        back_populates="cg_schedule",
        cascade="all, delete-orphan",
        order_by="ITRCGBondEntry.display_order",
    )

    itr_return: Mapped["ITRReturn"] = relationship("ITRReturn", back_populates="cg_schedule")
   

class ITRCGIndiaEQAndDebtMFBroker(Base):
    __tablename__ = "itr_cg_india_eq_and_debt_mf_brokers_data"
    id: Mapped[UUID] = mapped_column(SQLUUID(as_uuid=True), primary_key=True, default=uuid4)
    cg_schedule_id: Mapped[UUID] = mapped_column(
        SQLUUID(as_uuid=True),
        ForeignKey("itr_cg_schedule.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    display_order: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    cg_type: Mapped[str] = mapped_column(String(20), nullable=False)
    broker: Mapped[str] = mapped_column(String(100), nullable=False)
    total_sale_value: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False, default=0)
    total_sale_expenses: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False, default=0)
    total_net_sale_value: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False, default=0)
    total_cost_of_acquisition: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False, default=0)
    total_gain: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False, default=0)
    total_stcg: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False, default=0)
    total_ltcg: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False, default=0)
    source_document_id: Mapped[Optional[UUID]] = mapped_column(
        SQLUUID(as_uuid=True),
        nullable=True,
        index=True,
    )
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), onupdate=func.now())
    india_eq_and_debt_mf_transactions: Mapped[List["ITRCGIndiaEQAndDebtMFTransaction"]] = relationship(
        back_populates="cg_india_eq_broker",
        cascade="all, delete-orphan",
        order_by="ITRCGIndiaEQAndDebtMFTransaction.display_order",
    )
    cg_schedule: Mapped["ITRCGSchedule"] = relationship(
        "ITRCGSchedule",
        back_populates="india_eq_and_debt_mf_brokers",
    )

class ITRCGIndiaEQAndDebtMFTransaction(Base):
    __tablename__ = "itr_cg_india_eq_and_debt_mf_transactions"

    id: Mapped[UUID] = mapped_column(SQLUUID(as_uuid=True), primary_key=True, default=uuid4)
    cg_india_eq_id: Mapped[UUID] = mapped_column(
        SQLUUID(as_uuid=True),
        ForeignKey("itr_cg_india_eq_and_debt_mf_brokers_data.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    display_order: Mapped[int] = mapped_column(Integer, nullable=False, default=1)

    stock_scheme: Mapped[Optional[str]] = mapped_column(String(200), nullable=True)
    quantity: Mapped[Decimal] = mapped_column(Numeric(15, 4), nullable=False, default=0)
    date_of_purchase: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    date_of_transfer: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    sale_value: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False, default=0)
    sale_expenses: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False, default=0)
    net_sale_value: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False, default=0)
    cost_of_acquisition: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False, default=0)
    gain_type: Mapped[str] = mapped_column(String(20), nullable=False, default="Short")
    gain: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False, default=0)
    isin: Mapped[Optional[str]] = mapped_column(String(12), nullable=True)
    stt_paid: Mapped[Optional[Decimal]] = mapped_column(Numeric(15, 2), nullable=True)
    grandfathering_fmv: Mapped[Optional[Decimal]] = mapped_column(Numeric(15, 4), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), onupdate=func.now())

    cg_india_eq_broker: Mapped["ITRCGIndiaEQAndDebtMFBroker"] = relationship(
        "ITRCGIndiaEQAndDebtMFBroker",
        back_populates="india_eq_and_debt_mf_transactions",
    )


class ITRCGUSBroker(Base):
    __tablename__ = "itr_cg_us_brokers_data"
    id: Mapped[UUID] = mapped_column(SQLUUID(as_uuid=True), primary_key=True, default=uuid4)
    cg_schedule_id: Mapped[UUID] = mapped_column(
        SQLUUID(as_uuid=True),
        ForeignKey("itr_cg_schedule.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    display_order: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    broker: Mapped[str] = mapped_column(String(100), nullable=False)
    total_sale_value: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False, default=0)
    total_cost_value: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False, default=0)
    total_gain: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False, default=0)
    total_stcg: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False, default=0)
    total_ltcg: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False, default=0)
    source_document_id: Mapped[Optional[UUID]] = mapped_column(
        SQLUUID(as_uuid=True),
        nullable=True,
        index=True,
    )
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), onupdate=func.now())
    us_transactions: Mapped[List["ITRCGUSTransaction"]] = relationship(
        back_populates="cg_us_broker",
        cascade="all, delete-orphan",
        order_by="ITRCGUSTransaction.display_order",
    )
    cg_schedule: Mapped["ITRCGSchedule"] = relationship("ITRCGSchedule", back_populates="us_brokers")



class ITRCGUSTransaction(Base):
    __tablename__ = "itr_cg_us_transactions"

    id: Mapped[UUID] = mapped_column(SQLUUID(as_uuid=True), primary_key=True, default=uuid4)
    cg_us_broker_id: Mapped[UUID] = mapped_column(
        SQLUUID(as_uuid=True),
        ForeignKey("itr_cg_us_brokers_data.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    display_order: Mapped[int] = mapped_column(Integer, nullable=False, default=1)

    stock_name: Mapped[Optional[str]] = mapped_column(String(200), nullable=True)

    quantity: Mapped[Decimal] = mapped_column(Numeric(15, 4), nullable=False, default=0)
    date_of_purchase: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    date_of_sale: Mapped[Optional[date]] = mapped_column(Date, nullable=True)

    purchase_value_usd: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False, default=0)
    sale_value_usd: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False, default=0)
    exchange_rate: Mapped[Decimal] = mapped_column(Numeric(10, 4), nullable=False, default=0)
    sale_value_inr: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False, default=0)
    purchase_value_inr: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False, default=0)
    gain_type: Mapped[str] = mapped_column(String(20), nullable=False)
    gain_inr: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False, default=0)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), onupdate=func.now())

    cg_us_broker: Mapped["ITRCGUSBroker"] = relationship("ITRCGUSBroker", back_populates="us_transactions")


class ITRCGUnlistedTransaction(Base):
    __tablename__ = "itr_cg_unlisted_transactions"

    id: Mapped[UUID] = mapped_column(SQLUUID(as_uuid=True), primary_key=True, default=uuid4)
    cg_schedule_id: Mapped[UUID] = mapped_column(
        SQLUUID(as_uuid=True),
        ForeignKey("itr_cg_schedule.id", ondelete="CASCADE"),
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
    fmv: Mapped[Optional[Decimal]] = mapped_column(Numeric(15, 2), nullable=True)
    indexed_cost_of_acquisition: Mapped[Optional[Decimal]] = mapped_column(Numeric(15, 2), nullable=True)

    gain_type: Mapped[str] = mapped_column(String(20), nullable=False)
    gain_inr: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False, default=0)
    source_document_id: Mapped[Optional[UUID]] = mapped_column(
        SQLUUID(as_uuid=True),
        nullable=True,
        index=True,
    )
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), onupdate=func.now())

    cg_schedule: Mapped["ITRCGSchedule"] = relationship("ITRCGSchedule", back_populates="unlisted_transactions")



class ITRCGHPEntry(Base):
    __tablename__ = "itr_cg_hp_entries"

    id: Mapped[UUID] = mapped_column(SQLUUID(as_uuid=True), primary_key=True, default=uuid4)
    cg_schedule_id: Mapped[UUID] = mapped_column(
        SQLUUID(as_uuid=True),
        ForeignKey("itr_cg_schedule.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    display_order: Mapped[int] = mapped_column(Integer, nullable=False, default=1)

    property_type: Mapped[str] = mapped_column(String(50), nullable=False, default="Residential Property")
    share_percentage: Mapped[Decimal] = mapped_column(Numeric(5, 2), nullable=False, default=0)
    acquisition_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    transfer_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    sale_consideration: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False, default=0)
    stamp_duty_and_registration_fees: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False, default=0)
    address: Mapped[Optional[str]] = mapped_column(String(250), nullable=True)
    state_code: Mapped[Optional[str]] = mapped_column(String(5), nullable=True)
    state: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    town_district: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    country_code: Mapped[Optional[str]] = mapped_column(String(5), nullable=True)
    pin_code: Mapped[Optional[str]] = mapped_column(String(6), nullable=True)
    deemed_full_value: Mapped[Optional[Decimal]] = mapped_column(Numeric(15, 2), nullable=True)
    net_consideration: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False, default=0)
    total_transfer_expenses: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False, default=0)
    total_acquisition_cost: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False, default=0)
    total_improvements: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False, default=0)
    capital_gain_without_indexation: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False, default=0)
    capital_gain_with_indexation: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False, default=0)
    share_of_capital_gain_without_indexation: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False, default=0)
    share_of_capital_gain_with_indexation: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False, default=0)
    net_capital_gain_without_indexation: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False, default=0)
    net_capital_gain_with_indexation: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False, default=0)
    tax_on_capital_gain_without_indexation: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False, default=0)
    tax_on_capital_gain_with_indexation: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False, default=0)
    taxable_capital_gain: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False, default=0)
    source_document_id: Mapped[Optional[UUID]] = mapped_column(
        SQLUUID(as_uuid=True),
        nullable=True,
        index=True,
    )

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), onupdate=func.now())

    transfer_expenses: Mapped[List["ITRCGHPTransferExpense"]] = relationship(
        back_populates="hp_entry",
        cascade="all, delete-orphan",
        order_by="ITRCGHPTransferExpense.display_order",
    )

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

    buyers: Mapped[List["ITRCGHPBuyer"]] = relationship(
        back_populates="hp_entry",
        cascade="all, delete-orphan",
        order_by="ITRCGHPBuyer.display_order",
    )

    cg_schedule: Mapped["ITRCGSchedule"] = relationship("ITRCGSchedule", back_populates="hp_entries")


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

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), onupdate=func.now())

    hp_entry: Mapped["ITRCGHPEntry"] = relationship("ITRCGHPEntry", back_populates="buyers")


class ITRCGBondEntry(Base):
    __tablename__ = "itr_cg_bond_entries"

    id: Mapped[UUID] = mapped_column(SQLUUID(as_uuid=True), primary_key=True, default=uuid4)
    cg_schedule_id: Mapped[UUID] = mapped_column(
        SQLUUID(as_uuid=True),
        ForeignKey("itr_cg_schedule.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    display_order: Mapped[int] = mapped_column(Integer, nullable=False, default=1)

    issuer_name: Mapped[str] = mapped_column(String(200), nullable=False)
    isin: Mapped[Optional[str]] = mapped_column(String(12), nullable=True)
    date_of_purchase: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    date_of_sale: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    quantity: Mapped[Decimal] = mapped_column(Numeric(15, 4), nullable=False, default=0)
    sale_consideration: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False, default=0)
    purchase_cost: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False, default=0)
    indexed_cost: Mapped[Optional[Decimal]] = mapped_column(Numeric(15, 2), nullable=True)
    transfer_expenses: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False, default=0)
    gain_type: Mapped[str] = mapped_column(String(20), nullable=False, default="Long")
    stcg: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False, default=0)
    ltcg_20: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False, default=0)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), onupdate=func.now())

    cg_schedule: Mapped["ITRCGSchedule"] = relationship("ITRCGSchedule", back_populates="bond_entries")


class ITRCGExemption54F(Base):
    __tablename__ = "itr_cg_exemptions_54f"

    id: Mapped[UUID] = mapped_column(SQLUUID(as_uuid=True), primary_key=True, default=uuid4)
    cg_schedule_id: Mapped[UUID] = mapped_column(
        SQLUUID(as_uuid=True),
        ForeignKey("itr_cg_schedule.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    is_eligible: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
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
    source_document_id: Mapped[Optional[UUID]] = mapped_column(
        SQLUUID(as_uuid=True),
        nullable=True,
        index=True,
    )
    net_sale_consideration: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False, default=0)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), onupdate=func.now())

    cg_schedule: Mapped["ITRCGSchedule"] = relationship("ITRCGSchedule", back_populates="exemptions_54f")



class ITRCGVDATransaction(Base):
    __tablename__ = "itr_cg_vda_transactions"

    id: Mapped[UUID] = mapped_column(SQLUUID(as_uuid=True), primary_key=True, default=uuid4)
    cg_schedule_id: Mapped[UUID] = mapped_column(
        SQLUUID(as_uuid=True),
        ForeignKey("itr_cg_schedule.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    display_order: Mapped[int] = mapped_column(Integer, nullable=False, default=1)

    date_of_acquisition: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    date_of_transfer: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    cost_of_acquisition: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False, default=0)
    consideration_received: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False, default=0)
    income: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False, default=0)
    source_document_id: Mapped[Optional[UUID]] = mapped_column(
        SQLUUID(as_uuid=True),
        nullable=True,
        index=True,
    )

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), onupdate=func.now())

    cg_schedule: Mapped["ITRCGSchedule"] = relationship("ITRCGSchedule", back_populates="vda_transactions")





class ITRCGExemption54(Base):
    __tablename__ = "itr_cg_exemptions_54"

    id: Mapped[UUID] = mapped_column(SQLUUID(as_uuid=True), primary_key=True, default=uuid4)

    cg_schedule_id: Mapped[UUID] = mapped_column(
        SQLUUID(as_uuid=True),
        ForeignKey("itr_cg_schedule.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    display_order: Mapped[int] = mapped_column(Integer, nullable=False, default=1)

    source: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    description: Mapped[Optional[str]] = mapped_column(String(200), nullable=True)
    date_of_transfer: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    net_taxable_gain: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False, default=0)
    capital_gain: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False, default=0)
    date_of_purchase: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    cost_of_house: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False, default=0)
    cgas_deposit: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False, default=0)
    total_invested: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False, default=0)
    exempt_amount: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False, default=0)
    net_taxable_gain: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False, default=0)
    new_house_address: Mapped[Optional[str]] = mapped_column(String(250), nullable=True)
    construction_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    cgas_deposit_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    cgas_account_no: Mapped[Optional[str]] = mapped_column(String(30), nullable=True)
    bank_name: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    ifsc: Mapped[Optional[str]] = mapped_column(String(11), nullable=True)
    source_document_id: Mapped[Optional[UUID]] = mapped_column(
        SQLUUID(as_uuid=True),
        nullable=True,
        index=True,
    )

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), onupdate=func.now())

    cg_schedule: Mapped["ITRCGSchedule"] = relationship("ITRCGSchedule", back_populates="exemptions_54")


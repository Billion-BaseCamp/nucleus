"""Advance-tax capital-gains transaction store.

Replica of ITR Schedule CG trade tables, 1:1 with ``quarters`` via
``quarter_id`` (instead of ``itr_return_id``). HP / bonds / other assets /
DTAA / 54 / 54F are intentionally not replicated — those stay on existing
advance-tax models.

Populated when the request is ``request_portal=adv_tax`` with a compulsory
``quarter_id``.
"""

from __future__ import annotations

from datetime import date, datetime
from decimal import Decimal
from typing import TYPE_CHECKING, List, Optional
from uuid import UUID, uuid4

from sqlalchemy import (
    Boolean,
    Date,
    DateTime,
    ForeignKey,
    Integer,
    String,
    UUID as SQLUUID,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func, text
from sqlalchemy.types import Numeric

from nucleus.db.database import Base

if TYPE_CHECKING:
    from nucleus.models.advance_tax_models.quarter import Quarter
    from nucleus.models.common_models.client import Client


class ATCGSchedule(Base):
    __tablename__ = "at_cg_schedule"

    id: Mapped[UUID] = mapped_column(SQLUUID(as_uuid=True), primary_key=True, default=uuid4)
    quarter_id: Mapped[UUID] = mapped_column(
        SQLUUID(as_uuid=True),
        ForeignKey("quarters.id", ondelete="CASCADE"),
        nullable=False,
        unique=True,
        index=True,
    )
    client_id: Mapped[UUID] = mapped_column(
        SQLUUID(as_uuid=True),
        ForeignKey("clients.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    computation_status: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        server_default="NOT_STARTED",
    )
    verification_status: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)

    stcg_india_eq: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False, default=0)
    stcg_fno: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=True, default=0)
    stcg_mutual_funds: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False, default=0)
    stcg_us_foreign: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False, default=0)
    stcg_unlisted: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False, default=0)
    total_stcg: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False, default=0)
    ltcg_india_eq: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False, default=0)
    ltcg_fno: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=True, default=0)
    ltcg_mutual_funds: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False, default=0)
    ltcg_us_foreign: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False, default=0)
    ltcg_unlisted: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False, default=0)
    total_ltcg: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False, default=0)

    total_bf_loss: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False, default=0)
    total_vda_gain: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False, default=0)
    total_capital_gain: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False, default=0)

    fno_opted_business_last_year: Mapped[bool] = mapped_column(
        Boolean, nullable=True, server_default=text("false"), default=False
    )
    fno_opted_44ad_last_year: Mapped[bool] = mapped_column(
        Boolean, nullable=True, server_default=text("false"), default=False
    )
    fno_has_slab_rate_stcg_elsewhere: Mapped[bool] = mapped_column(
        Boolean, nullable=True, server_default=text("false"), default=False
    )

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), onupdate=func.now())

    india_eq_and_debt_mf_brokers: Mapped[List["ATCGIndiaEQAndDebtMFBroker"]] = relationship(
        back_populates="cg_schedule",
        cascade="all, delete-orphan",
        order_by="ATCGIndiaEQAndDebtMFBroker.display_order",
    )
    us_brokers: Mapped[List["ATCGUSBroker"]] = relationship(
        back_populates="cg_schedule",
        cascade="all, delete-orphan",
        order_by="ATCGUSBroker.display_order",
    )
    unlisted_transactions: Mapped[List["ATCGUnlistedTransaction"]] = relationship(
        back_populates="cg_schedule",
        cascade="all, delete-orphan",
        order_by="ATCGUnlistedTransaction.display_order",
    )
    vda_transactions: Mapped[List["ATCGVDATransaction"]] = relationship(
        back_populates="cg_schedule",
        cascade="all, delete-orphan",
        order_by="ATCGVDATransaction.display_order",
    )

    quarter: Mapped["Quarter"] = relationship("Quarter", back_populates="cg_schedule")
    client: Mapped["Client"] = relationship("Client")


class ATCGIndiaEQAndDebtMFBroker(Base):
    __tablename__ = "at_cg_india_eq_and_debt_mf_brokers_data"

    id: Mapped[UUID] = mapped_column(SQLUUID(as_uuid=True), primary_key=True, default=uuid4)
    cg_schedule_id: Mapped[UUID] = mapped_column(
        SQLUUID(as_uuid=True),
        ForeignKey("at_cg_schedule.id", ondelete="CASCADE"),
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
    pms_expenses: Mapped[Optional[Decimal]] = mapped_column(Numeric(15, 2), nullable=True, default=0)
    source_document_id: Mapped[Optional[UUID]] = mapped_column(
        SQLUUID(as_uuid=True),
        nullable=True,
        index=True,
    )
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), onupdate=func.now())

    india_eq_and_debt_mf_transactions: Mapped[List["ATCGIndiaEQAndDebtMFTransaction"]] = relationship(
        back_populates="cg_india_eq_broker",
        cascade="all, delete-orphan",
        order_by="ATCGIndiaEQAndDebtMFTransaction.display_order",
    )
    cg_schedule: Mapped["ATCGSchedule"] = relationship(
        "ATCGSchedule",
        back_populates="india_eq_and_debt_mf_brokers",
    )


class ATCGIndiaEQAndDebtMFTransaction(Base):
    __tablename__ = "at_cg_india_eq_and_debt_mf_transactions"

    id: Mapped[UUID] = mapped_column(SQLUUID(as_uuid=True), primary_key=True, default=uuid4)
    cg_india_eq_id: Mapped[UUID] = mapped_column(
        SQLUUID(as_uuid=True),
        ForeignKey("at_cg_india_eq_and_debt_mf_brokers_data.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    source_document_id: Mapped[Optional[UUID]] = mapped_column(
        SQLUUID(as_uuid=True),
        ForeignKey("at_cg_documents.id", ondelete="CASCADE"),
        nullable=True,
        index=True,
    )
    display_order: Mapped[int] = mapped_column(Integer, nullable=False, default=1)

    stock_scheme: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
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

    cg_india_eq_broker: Mapped["ATCGIndiaEQAndDebtMFBroker"] = relationship(
        "ATCGIndiaEQAndDebtMFBroker",
        back_populates="india_eq_and_debt_mf_transactions",
    )


class ATCGUSBroker(Base):
    __tablename__ = "at_cg_us_brokers_data"

    id: Mapped[UUID] = mapped_column(SQLUUID(as_uuid=True), primary_key=True, default=uuid4)
    cg_schedule_id: Mapped[UUID] = mapped_column(
        SQLUUID(as_uuid=True),
        ForeignKey("at_cg_schedule.id", ondelete="CASCADE"),
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

    us_transactions: Mapped[List["ATCGUSTransaction"]] = relationship(
        back_populates="cg_us_broker",
        cascade="all, delete-orphan",
        order_by="ATCGUSTransaction.display_order",
    )
    cg_schedule: Mapped["ATCGSchedule"] = relationship("ATCGSchedule", back_populates="us_brokers")


class ATCGUSTransaction(Base):
    __tablename__ = "at_cg_us_transactions"

    id: Mapped[UUID] = mapped_column(SQLUUID(as_uuid=True), primary_key=True, default=uuid4)
    cg_us_broker_id: Mapped[UUID] = mapped_column(
        SQLUUID(as_uuid=True),
        ForeignKey("at_cg_us_brokers_data.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    source_document_id: Mapped[Optional[UUID]] = mapped_column(
        SQLUUID(as_uuid=True),
        ForeignKey("at_cg_documents.id", ondelete="CASCADE"),
        nullable=True,
        index=True,
    )
    display_order: Mapped[int] = mapped_column(Integer, nullable=False, default=1)

    stock_name: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
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

    cg_us_broker: Mapped["ATCGUSBroker"] = relationship("ATCGUSBroker", back_populates="us_transactions")


class ATCGUnlistedTransaction(Base):
    __tablename__ = "at_cg_unlisted_transactions"

    id: Mapped[UUID] = mapped_column(SQLUUID(as_uuid=True), primary_key=True, default=uuid4)
    cg_schedule_id: Mapped[UUID] = mapped_column(
        SQLUUID(as_uuid=True),
        ForeignKey("at_cg_schedule.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    display_order: Mapped[int] = mapped_column(Integer, nullable=False, default=1)

    stock_name: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
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
        ForeignKey("at_cg_documents.id", ondelete="CASCADE"),
        nullable=True,
        index=True,
    )
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), onupdate=func.now())

    cg_schedule: Mapped["ATCGSchedule"] = relationship("ATCGSchedule", back_populates="unlisted_transactions")


class ATCGVDATransaction(Base):
    __tablename__ = "at_cg_vda_transactions"

    id: Mapped[UUID] = mapped_column(SQLUUID(as_uuid=True), primary_key=True, default=uuid4)
    cg_schedule_id: Mapped[UUID] = mapped_column(
        SQLUUID(as_uuid=True),
        ForeignKey("at_cg_schedule.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    display_order: Mapped[int] = mapped_column(Integer, nullable=False, default=1)

    crypto_name: Mapped[Optional[str]] = mapped_column(String(200), nullable=True)
    date_of_acquisition: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    date_of_transfer: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    cost_of_acquisition: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False, default=0)
    consideration_received: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False, default=0)
    income: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False, default=0)
    source_document_id: Mapped[Optional[UUID]] = mapped_column(
        SQLUUID(as_uuid=True),
        ForeignKey("at_cg_documents.id", ondelete="CASCADE"),
        nullable=True,
        index=True,
    )

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), onupdate=func.now())

    cg_schedule: Mapped["ATCGSchedule"] = relationship("ATCGSchedule", back_populates="vda_transactions")

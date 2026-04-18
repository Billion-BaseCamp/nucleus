"""
ITR filing layer: Schedule HP (house property) persistence.

itr_returns → itr_hp_schedule (1:1) → itr_hp_properties (1:N) → children
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
    UUID as SQLUUID,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from sqlalchemy.types import Numeric

from nucleus.db.database import Base


class ITRHPSchedule(Base):
    """Schedule HP — one-to-one child of ITRReturn."""

    __tablename__ = "itr_hp_schedule"

    id: Mapped[UUID] = mapped_column(SQLUUID(as_uuid=True), primary_key=True, default=uuid4)
    itr_return_id: Mapped[UUID] = mapped_column(
        SQLUUID(as_uuid=True),
        ForeignKey("itr_returns.id", ondelete="CASCADE"),
        nullable=False,
        unique=True,
        index=True,
    )

    total_hp_income: Mapped[Optional[Decimal]] = mapped_column(Numeric(15, 2), default=0)
    # brought_forward_loss: Mapped[Optional[Decimal]] = mapped_column(Numeric(15, 2), default=0)
    # income_under_head_hp: Mapped[Optional[Decimal]] = mapped_column(Numeric(15, 2), default=0)

    itr_return: Mapped["ITRReturn"] = relationship("ITRReturn", back_populates="house_property")
    properties: Mapped[List["ITRHPProperty"]] = relationship(
        back_populates="hp_schedule",
        cascade="all, delete-orphan",
        order_by="ITRHPProperty.display_order",
    )

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), onupdate=func.now())


class ITRHPProperty(Base):
    """One row per property in Schedule HP."""

    __tablename__ = "itr_hp_properties"

    id: Mapped[UUID] = mapped_column(SQLUUID(as_uuid=True), primary_key=True, default=uuid4)
    hp_schedule_id: Mapped[UUID] = mapped_column(
        SQLUUID(as_uuid=True),
        ForeignKey("itr_hp_schedule.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    display_order: Mapped[int] = mapped_column(Integer, nullable=False, default=1)

    short_name: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)

    # ── Address (AddressDetailWithZipCode) ──
    flat_door_no: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    premises: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    road: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    locality: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    town_district: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    state: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    state_code: Mapped[Optional[str]] = mapped_column(String(2), nullable=True)
    country: Mapped[Optional[str]] = mapped_column(String(50), nullable=True, default="India")
    country_code: Mapped[Optional[str]] = mapped_column(String(2), nullable=True, default="91")
    pin: Mapped[Optional[str]] = mapped_column(String(6), nullable=True)
    zipcode: Mapped[Optional[str]] = mapped_column(String(10), nullable=True)

    # ── Classification ──
    nature_of_property: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    type_of_property: Mapped[str] = mapped_column(String(20), nullable=False)
    type_of_property_code: Mapped[Optional[str]] = mapped_column(String(2), nullable=True)

    # ── Ownership ──
    property_owner: Mapped[Optional[str]] = mapped_column(String(50), nullable=True, default="Self")
    property_owner_code: Mapped[Optional[str]] = mapped_column(String(2), nullable=True)
    is_co_owned: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    ownership_percent: Mapped[Decimal] = mapped_column(Numeric(5, 2), nullable=False, default=100)

    # ── Income inputs (user-entered) ──
    annual_letable_value: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False, default=0)
    actual_rent_received: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False, default=0)
    vacancy_allowance: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False, default=0)
    property_taxes_paid: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False, default=0)

    # ── Interest on borrowed capital (display-level total) ──
    interest_on_borrowed_capital: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False, default=0)

    # ── Arrears / unrealized rent u/s 25A ──
    arrears_unrealized_rent: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False, default=0)
    unrealized_rent_allowed: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False, default=0)

    # ── Pre-construction interest ──
    pre_construction_interest_total: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False, default=0)
    fy_of_completion: Mapped[Optional[str]] = mapped_column(String(7), nullable=True)

    # ── Computed fields (backend calc engine) ──
    computed_gav: Mapped[Optional[Decimal]] = mapped_column(Numeric(15, 2), nullable=True)
    computed_nav: Mapped[Optional[Decimal]] = mapped_column(Numeric(15, 2), nullable=True)
    computed_share_of_nav: Mapped[Optional[Decimal]] = mapped_column(Numeric(15, 2), nullable=True)
    computed_std_deduction_30: Mapped[Optional[Decimal]] = mapped_column(Numeric(15, 2), nullable=True)
    computed_interest_allowed: Mapped[Optional[Decimal]] = mapped_column(Numeric(15, 2), nullable=True)
    computed_pre_const_deductible: Mapped[Optional[Decimal]] = mapped_column(Numeric(15, 2), nullable=True)
    computed_pre_const_cf: Mapped[Optional[Decimal]] = mapped_column(Numeric(15, 2), nullable=True)
    computed_net_hp_income: Mapped[Optional[Decimal]] = mapped_column(Numeric(15, 2), nullable=True)

    # ── Relationships ──
    hp_schedule: Mapped["ITRHPSchedule"] = relationship(back_populates="properties")
    co_owners: Mapped[List["ITRHPCoOwner"]] = relationship(
        back_populates="property",
        cascade="all, delete-orphan",
        order_by="ITRHPCoOwner.display_order",
    )
    loans: Mapped[List["ITRHPLoan"]] = relationship(
        back_populates="property",
        cascade="all, delete-orphan",
        order_by="ITRHPLoan.display_order",
    )
    tenants: Mapped[List["ITRHPTenant"]] = relationship(
        back_populates="property",
        cascade="all, delete-orphan",
        order_by="ITRHPTenant.display_order",
    )

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), onupdate=func.now())


class ITRHPCoOwner(Base):
    """Co-owner entry for a property (CoOwners in ITR JSON)."""

    __tablename__ = "itr_hp_co_owners"

    id: Mapped[UUID] = mapped_column(SQLUUID(as_uuid=True), primary_key=True, default=uuid4)
    property_id: Mapped[UUID] = mapped_column(
        SQLUUID(as_uuid=True),
        ForeignKey("itr_hp_properties.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    display_order: Mapped[int] = mapped_column(Integer, nullable=False, default=1)

    name: Mapped[str] = mapped_column(String(125), nullable=False)
    pan: Mapped[Optional[str]] = mapped_column(String(10), nullable=True)
    aadhaar: Mapped[Optional[str]] = mapped_column(String(12), nullable=True)
    share_percent: Mapped[Decimal] = mapped_column(Numeric(5, 2), nullable=False, default=0)

    property: Mapped["ITRHPProperty"] = relationship(back_populates="co_owners")

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), onupdate=func.now())


class ITRHPLoan(Base):
    """Loan detail for Section 24B (Section24BDtls in ITR JSON)."""

    __tablename__ = "itr_hp_loans"

    id: Mapped[UUID] = mapped_column(SQLUUID(as_uuid=True), primary_key=True, default=uuid4)
    property_id: Mapped[UUID] = mapped_column(
        SQLUUID(as_uuid=True),
        ForeignKey("itr_hp_properties.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    display_order: Mapped[int] = mapped_column(Integer, nullable=False, default=1)

    loan_taken_from: Mapped[Optional[str]] = mapped_column(String(25), nullable=True)
    loan_taken_code: Mapped[Optional[str]] = mapped_column(String(1), nullable=True)
    lender_name: Mapped[Optional[str]] = mapped_column(String(125), nullable=True)
    loan_account_no: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    sanction_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    total_loan_amount: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False, default=0)
    closing_balance: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False, default=0)
    interest_payable: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False, default=0)
    interest_paid: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False, default=0)
    principal_repaid: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False, default=0)

    property: Mapped["ITRHPProperty"] = relationship(back_populates="loans")

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), onupdate=func.now())


class ITRHPTenant(Base):
    """Tenant details for let-out properties (TenantDetails in ITR JSON)."""

    __tablename__ = "itr_hp_tenants"

    id: Mapped[UUID] = mapped_column(SQLUUID(as_uuid=True), primary_key=True, default=uuid4)
    property_id: Mapped[UUID] = mapped_column(
        SQLUUID(as_uuid=True),
        ForeignKey("itr_hp_properties.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    display_order: Mapped[int] = mapped_column(Integer, nullable=False, default=1)

    name: Mapped[Optional[str]] = mapped_column(String(125), nullable=True)
    pan: Mapped[Optional[str]] = mapped_column(String(10), nullable=True)
    aadhaar: Mapped[Optional[str]] = mapped_column(String(12), nullable=True)
    tan: Mapped[Optional[str]] = mapped_column(String(10), nullable=True)

    property: Mapped["ITRHPProperty"] = relationship(back_populates="tenants")

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), onupdate=func.now())

"""
ITR filing layer: Deductions (Chapter VI-A) persistence.

itr_returns → itr_ded_schedule (1:1) → 5 child tables
"""

from __future__ import annotations

from datetime import date, datetime
from decimal import Decimal
from typing import Any, List, Optional
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
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from sqlalchemy.types import Numeric

from nucleus.db.database import Base


class ITRDedSchedule(Base):
    """Deductions (Chapter VI-A) — one-to-one child of ITRReturn."""

    __tablename__ = "itr_ded_schedule"

    id: Mapped[UUID] = mapped_column(SQLUUID(as_uuid=True), primary_key=True, default=uuid4)
    itr_return_id: Mapped[UUID] = mapped_column(
        SQLUUID(as_uuid=True),
        ForeignKey("itr_returns.id", ondelete="CASCADE"),
        nullable=False,
        unique=True,
        index=True,
    )

    # ── 80C — fixed 16 items as JSONB ──
    # Each: { id, label, docIdNo, amount, comment }
    sec_80c_items: Mapped[Optional[list[dict[str, Any]]]] = mapped_column(JSONB, nullable=False, default=list)

    # ── 80CCC — Pension Fund ──
    ccc_amount: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False, default=0)
    ccc_comment: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)

    # ── 80CCD — NPS ──
    ccd_self_or_employed: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False, default=0)
    ccd_employer_contribution: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False, default=0)
    ccd_pran: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    ccd_voluntary_1b: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False, default=0)

    # ── 80D — Medical Insurance (flags + JSONB breakup) ──
    d_self_senior_citizen: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    d_parents_senior_citizen: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    d_self_breakup: Mapped[Optional[list[dict[str, Any]]]] = mapped_column(JSONB, nullable=False, default=list)
    d_parents_breakup: Mapped[Optional[list[dict[str, Any]]]] = mapped_column(JSONB, nullable=False, default=list)

    # ── 80DD — Handicapped Dependant ──
    dd_severe_disability: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    dd_eligible_deduction: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False, default=0)
    dd_dependant_pan: Mapped[Optional[str]] = mapped_column(String(10), nullable=True)
    dd_dependant_aadhaar: Mapped[Optional[str]] = mapped_column(String(12), nullable=True)
    dd_relation: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    dd_relation_id: Mapped[Optional[str]] = mapped_column(String(2), nullable=True)
    dd_disability_type: Mapped[Optional[str]] = mapped_column(String(2), nullable=True)
    dd_udid_no: Mapped[Optional[str]] = mapped_column(String(18), nullable=True)
    dd_form10ia_date_filing: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    dd_form10ia_ack_no: Mapped[Optional[str]] = mapped_column(String(15), nullable=True)

    # ── 80DDB — Specified Diseases (JSONB — 2 fixed rows) ──
    ddb_entries: Mapped[Optional[list[dict[str, Any]]]] = mapped_column(JSONB, nullable=False, default=list)

    # ── 80U — Own Disability ──
    u_severe_disability: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    u_eligible_deduction: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False, default=0)
    u_disability_type: Mapped[Optional[str]] = mapped_column(String(2), nullable=True)
    u_udid_no: Mapped[Optional[str]] = mapped_column(String(18), nullable=True)
    u_form10ia_date_filing: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    u_form10ia_ack_no: Mapped[Optional[str]] = mapped_column(String(15), nullable=True)

    # ── Simple Deductions ──
    amt_80gg: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False, default=0)
    amt_80qqb: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False, default=0)
    amt_80rrb: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False, default=0)
    amt_80tta: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False, default=0)
    amt_80ttb: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False, default=0)
    amt_80cch: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False, default=0)

    # ── Form Acknowledgement Numbers ──
    form10ba_ack_no: Mapped[Optional[str]] = mapped_column(String(15), nullable=True)
    form10ccd_ack_no: Mapped[Optional[str]] = mapped_column(String(15), nullable=True)
    form10cce_ack_no: Mapped[Optional[str]] = mapped_column(String(15), nullable=True)

    # ── Computed totals (backend calc engine) ──
    computed_80c_capped: Mapped[Optional[Decimal]] = mapped_column(Numeric(15, 2), nullable=True)
    computed_total_nps: Mapped[Optional[Decimal]] = mapped_column(Numeric(15, 2), nullable=True)
    computed_80d_total: Mapped[Optional[Decimal]] = mapped_column(Numeric(15, 2), nullable=True)
    computed_80g_total: Mapped[Optional[Decimal]] = mapped_column(Numeric(15, 2), nullable=True)
    computed_total_chapter_via: Mapped[Optional[Decimal]] = mapped_column(Numeric(15, 2), nullable=True)

    # ── Relationships ──
    itr_return: Mapped["ITRReturn"] = relationship("ITRReturn", back_populates="deductions")
    donations_80g: Mapped[List["ITRDed80GDonation"]] = relationship(
        back_populates="ded_schedule",
        cascade="all, delete-orphan",
        order_by="ITRDed80GDonation.display_order",
    )
    policies_80d: Mapped[List["ITRDed80DPolicy"]] = relationship(
        back_populates="ded_schedule",
        cascade="all, delete-orphan",
        order_by="ITRDed80DPolicy.display_order",
    )
    loans: Mapped[List["ITRDedLoan"]] = relationship(
        back_populates="ded_schedule",
        cascade="all, delete-orphan",
        order_by="ITRDedLoan.display_order",
    )
    entries_80gga: Mapped[List["ITRDed80GGAEntry"]] = relationship(
        back_populates="ded_schedule",
        cascade="all, delete-orphan",
        order_by="ITRDed80GGAEntry.display_order",
    )
    entries_80ggc: Mapped[List["ITRDed80GGCEntry"]] = relationship(
        back_populates="ded_schedule",
        cascade="all, delete-orphan",
        order_by="ITRDed80GGCEntry.display_order",
    )

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), onupdate=func.now())


class ITRDed80GDonation(Base):
    """80G donation entries (across 4 categories)."""

    __tablename__ = "itr_ded_80g_donations"

    id: Mapped[UUID] = mapped_column(SQLUUID(as_uuid=True), primary_key=True, default=uuid4)
    ded_schedule_id: Mapped[UUID] = mapped_column(
        SQLUUID(as_uuid=True),
        ForeignKey("itr_ded_schedule.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    display_order: Mapped[int] = mapped_column(Integer, nullable=False, default=1)

    category: Mapped[str] = mapped_column(String(30), nullable=False)
    name_of_donee: Mapped[str] = mapped_column(String(125), nullable=False, default="")
    donation_amount: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False, default=0)
    pan: Mapped[Optional[str]] = mapped_column(String(10), nullable=True)
    address: Mapped[Optional[str]] = mapped_column(String(250), nullable=True)
    city: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    state: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    state_code: Mapped[Optional[str]] = mapped_column(String(3), nullable=True)
    pin_code: Mapped[Optional[str]] = mapped_column(String(6), nullable=True)
    paid_in_cash: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    arn: Mapped[Optional[str]] = mapped_column(String(25), nullable=True)

    computed_eligible_amount: Mapped[Optional[Decimal]] = mapped_column(Numeric(15, 2), nullable=True)

    ded_schedule: Mapped["ITRDedSchedule"] = relationship(back_populates="donations_80g")

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), onupdate=func.now())


class ITRDed80DPolicy(Base):
    """80D medical insurance policy entries (self + parent)."""

    __tablename__ = "itr_ded_80d_policies"

    id: Mapped[UUID] = mapped_column(SQLUUID(as_uuid=True), primary_key=True, default=uuid4)
    ded_schedule_id: Mapped[UUID] = mapped_column(
        SQLUUID(as_uuid=True),
        ForeignKey("itr_ded_schedule.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    display_order: Mapped[int] = mapped_column(Integer, nullable=False, default=1)

    policy_for: Mapped[str] = mapped_column(String(10), nullable=False)
    insurance_company: Mapped[str] = mapped_column(String(125), nullable=False, default="")
    policy_no: Mapped[Optional[str]] = mapped_column(String(30), nullable=True)
    premium_paid: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False, default=0)
    
    ded_schedule: Mapped["ITRDedSchedule"] = relationship(back_populates="policies_80d")

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), onupdate=func.now())


class ITRDedLoan(Base):
    """Unified loan entries for 80E / 80EE / 80EEA / 80EEB."""

    __tablename__ = "itr_ded_loans"

    id: Mapped[UUID] = mapped_column(SQLUUID(as_uuid=True), primary_key=True, default=uuid4)
    ded_schedule_id: Mapped[UUID] = mapped_column(
        SQLUUID(as_uuid=True),
        ForeignKey("itr_ded_schedule.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    display_order: Mapped[int] = mapped_column(Integer, nullable=False, default=1)

    section: Mapped[str] = mapped_column(String(5), nullable=False)
    loan_taken_from: Mapped[Optional[str]] = mapped_column(String(1), nullable=True)
    bank_or_institution_name: Mapped[str] = mapped_column(String(125), nullable=False, default="")
    loan_account_no: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    date_of_loan: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    total_loan_amount: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False, default=0)
    loan_outstanding_amount: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False, default=0)
    interest_claimed: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False, default=0)

    # 80EEB-specific
    vehicle_reg_no: Mapped[Optional[str]] = mapped_column(String(11), nullable=True)

    # 80EEA-specific
    prop_stamp_duty_value: Mapped[Optional[Decimal]] = mapped_column(Numeric(15, 2), nullable=True)

    ded_schedule: Mapped["ITRDedSchedule"] = relationship(back_populates="loans")

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), onupdate=func.now())


class ITRDed80GGAEntry(Base):
    """80GGA — Donations for scientific research / rural development."""

    __tablename__ = "itr_ded_80gga_entries"

    id: Mapped[UUID] = mapped_column(SQLUUID(as_uuid=True), primary_key=True, default=uuid4)
    ded_schedule_id: Mapped[UUID] = mapped_column(
        SQLUUID(as_uuid=True),
        ForeignKey("itr_ded_schedule.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    display_order: Mapped[int] = mapped_column(Integer, nullable=False, default=1)

    name_of_donee: Mapped[str] = mapped_column(String(125), nullable=False, default="")
    pan: Mapped[Optional[str]] = mapped_column(String(10), nullable=True)
    donation_amount: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False, default=0)
    eligible_amount: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False, default=0)
    nature_of_donation: Mapped[Optional[str]] = mapped_column(String(60), nullable=True)

    ded_schedule: Mapped["ITRDedSchedule"] = relationship(back_populates="entries_80gga")

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), onupdate=func.now())


class ITRDed80GGCEntry(Base):
    """80GGC — Donations to political parties."""

    __tablename__ = "itr_ded_80ggc_entries"

    id: Mapped[UUID] = mapped_column(SQLUUID(as_uuid=True), primary_key=True, default=uuid4)
    ded_schedule_id: Mapped[UUID] = mapped_column(
        SQLUUID(as_uuid=True),
        ForeignKey("itr_ded_schedule.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    display_order: Mapped[int] = mapped_column(Integer, nullable=False, default=1)

    particulars: Mapped[str] = mapped_column(String(125), nullable=False, default="")
    amount: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False, default=0)
    donation_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    ifs_code: Mapped[Optional[str]] = mapped_column(String(11), nullable=True)
    txn_ref_no: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    paid_in_cash: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    computed_eligible_amount: Mapped[Optional[Decimal]] = mapped_column(Numeric(15, 2), nullable=True)

    ded_schedule: Mapped["ITRDedSchedule"] = relationship(back_populates="entries_80ggc")

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), onupdate=func.now())

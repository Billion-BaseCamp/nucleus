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
    UniqueConstraint,
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

    id: Mapped[UUID] = mapped_column(
        SQLUUID(as_uuid=True), primary_key=True, default=uuid4
    )
    itr_return_id: Mapped[UUID] = mapped_column(
        SQLUUID(as_uuid=True),
        ForeignKey("itr_returns.id", ondelete="CASCADE"),
        nullable=False,
        unique=True,
        index=True,
    )

    sec_80c_capped: Mapped[Decimal] = mapped_column(
        Numeric(15, 2), nullable=False, default=0
    )
    nps_total: Mapped[Decimal] = mapped_column(
        Numeric(15, 2), nullable=False, default=0
    )
    total_80d_80g: Mapped[Decimal] = mapped_column(
        Numeric(15, 2), nullable=False, default=0
    )
    total_chapter_via: Mapped[Decimal] = mapped_column(
        Numeric(15, 2), nullable=False, default=0
    )
    sec_80dMedical_total: Mapped[Decimal] = mapped_column(
        Numeric(15, 2), nullable=False, default=0
    )
    sec_80gDonation_total: Mapped[Decimal] = mapped_column(
        Numeric(15, 2), nullable=False, default=0
    )
    sec_80ddHandicapped_total: Mapped[Decimal] = mapped_column(
        Numeric(15, 2), nullable=False, default=0
    )
    sec_80ddbDiseases_total: Mapped[Decimal] = mapped_column(
        Numeric(15, 2), nullable=False, default=0
    )
    sec_80ggcPolitical_total: Mapped[Decimal] = mapped_column(
        Numeric(15, 2), nullable=False, default=0
    )
    sec_80uDisability_total: Mapped[Decimal] = mapped_column(
        Numeric(15, 2), nullable=False, default=0
    )
    sec_80eeducation_total: Mapped[Decimal] = mapped_column(
        Numeric(15, 2), nullable=False, default=0
    )
    sec_80eebVehicle_total: Mapped[Decimal] = mapped_column(
        Numeric(15, 2), nullable=False, default=0
    )
    sec_other_total: Mapped[Decimal] = mapped_column(
        Numeric(15, 2), nullable=False, default=0
    )

    # ── Relationships ──
    # one to one relationship with ITRReturn
    itr_return: Mapped["ITRReturn"] = relationship(
        "ITRReturn", back_populates="deductions"
    )
    # one to one relationship with ITRDed80C80CCD
    ded_80c_80ccd: Mapped["ITRDed_80C_80CCD"] = relationship(
        back_populates="ded_schedule"
    )
    ded_80d_meta: Mapped["ITRDed80DMeta"] = relationship(
        back_populates="ded_schedule"
    )

    ded_80d_details: Mapped[List["ITRDed80DDetail"]] = relationship(
        back_populates="ded_schedule", cascade="all, delete-orphan"
    )
    ded_80d_policies: Mapped[List["ITRDed80DPolicy"]] = relationship(
        back_populates="ded_schedule", cascade="all, delete-orphan"
    )
    ded_80c: Mapped[List["ITRDed80C"]] = relationship(
        back_populates="ded_schedule", cascade="all, delete-orphan"
    )
    ded_80g_donations: Mapped[List["ITRDed80GDonation"]] = relationship(
        back_populates="ded_schedule", cascade="all, delete-orphan"
    )
    ded_80d_80u: Mapped["ITRDed80DD80U"] = relationship(
        back_populates="ded_schedule"
    )

    ded_80ddb: Mapped[List["ITRDed80DDB"]] = relationship(
        back_populates="ded_schedule", cascade="all, delete-orphan"
    )
    ded_80gga_entries: Mapped[List["ITRDed80GGAEntry"]] = relationship(
        back_populates="ded_schedule", cascade="all, delete-orphan"
    )
    ded_80ggc_entries: Mapped[List["ITRDed80GGCEntry"]] = relationship(
        back_populates="ded_schedule",
        cascade="all, delete-orphan",
        order_by="ITRDed80GGCEntry.display_order",
    )
    ded_80e_loans: Mapped[List["ITRDed80ELoan"]] = relationship(
        back_populates="ded_schedule",
        cascade="all, delete-orphan",
        order_by="ITRDed80ELoan.display_order",
    )
    ded_80eeb_loans: Mapped[List["ITRDed80EEBLoan"]] = relationship(
        back_populates="ded_schedule",
        cascade="all, delete-orphan",
        order_by="ITRDed80EEBLoan.display_order",
    )
    ded_other_lines: Mapped[List["ITRDedOtherLine"]] = relationship(
        back_populates="ded_schedule",
        cascade="all, delete-orphan",
        order_by="ITRDedOtherLine.display_order",
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), onupdate=func.now()
    )


class ITRDed80C(Base):
    __tablename__ = "itr_ded_80c"
    id: Mapped[UUID] = mapped_column(
        SQLUUID(as_uuid=True), primary_key=True, default=uuid4
    )
    ded_schedule_id: Mapped[UUID] = mapped_column(
        SQLUUID(as_uuid=True),
        ForeignKey("itr_ded_schedule.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    description: Mapped[str] = mapped_column(String, nullable=False)
    doc_id_no: Mapped[str | None] = mapped_column(String, nullable=True)
    amount: Mapped[float] = mapped_column(Numeric(12, 2), default=0)
    comments: Mapped[str | None] = mapped_column(String, nullable=True)

    ded_schedule: Mapped["ITRDedSchedule"] = relationship(back_populates="ded_80c")

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), onupdate=func.now()
    )


class ITRDed_80C_80CCD(Base):
    __tablename__ = "itr_ded_80c_80ccd"
    id: Mapped[UUID] = mapped_column(
        SQLUUID(as_uuid=True), primary_key=True, default=uuid4
    )
    ded_schedule_id: Mapped[UUID] = mapped_column(
        SQLUUID(as_uuid=True),
        ForeignKey("itr_ded_schedule.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    sec_80ccc_pension_amount: Mapped[float] = mapped_column(Numeric(12, 2), default=0)
    sec_80ccc_pension_comment: Mapped[str | None] = mapped_column(String, nullable=True)
    sec_80ccd1_nps_amount: Mapped[float] = mapped_column(Numeric(12, 2), default=0)
    sec_80ccd2_nps_amount: Mapped[float] = mapped_column(Numeric(12, 2), default=0)
    pran_number: Mapped[str | None] = mapped_column(String, nullable=True)
    sec80ccd1b_voluntary_amount: Mapped[float] = mapped_column(
        Numeric(12, 2), default=0
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), onupdate=func.now()
    )

    ded_schedule: Mapped["ITRDedSchedule"] = relationship(
        back_populates="ded_80c_80ccd"
    )


class ITRDed80DDetail(Base):
    __tablename__ = "itr_80d_details"

    id: Mapped[UUID] = mapped_column(
        SQLUUID(as_uuid=True), primary_key=True, default=uuid4
    )
    ded_schedule_id: Mapped[UUID] = mapped_column(
        SQLUUID(as_uuid=True),
        ForeignKey("itr_ded_schedule.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    # 👇 which section
    section: Mapped[str] = mapped_column(String)
    # values: "SELF_FAMILY", "PARENTS"

    # 👇 category
    category: Mapped[str] = mapped_column(String)
    # values: "SENIOR", "OTHERS"

    insurance_premium: Mapped[float] = mapped_column(Numeric(12, 2), default=0)
    medical_expenses: Mapped[float] = mapped_column(Numeric(12, 2), default=0)
    health_checkup: Mapped[float] = mapped_column(Numeric(12, 2), default=0)

    deductible: Mapped[float] = mapped_column(Numeric(12, 2), default=0)

    ded_schedule: Mapped["ITRDedSchedule"] = relationship(
        back_populates="ded_80d_details"
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), onupdate=func.now()
    )


class ITRDed80DMeta(Base):
    __tablename__ = "itr_80d_meta"

    id: Mapped[UUID] = mapped_column(
        SQLUUID(as_uuid=True), primary_key=True, default=uuid4
    )

    ded_schedule_id: Mapped[UUID] = mapped_column(
        SQLUUID(as_uuid=True),
        ForeignKey("itr_ded_schedule.id", ondelete="CASCADE"),
        nullable=False,
        unique=True,
        index=True,
    )

    self_family_senior: Mapped[bool] = mapped_column(Boolean, default=False)
    parents_senior: Mapped[bool] = mapped_column(Boolean, default=False)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), onupdate=func.now()
    )

    ded_schedule: Mapped["ITRDedSchedule"] = relationship(back_populates="ded_80d_meta")


class ITRDed80DPolicy(Base):
    __tablename__ = "itr_ded_80d_policies"
    id: Mapped[UUID] = mapped_column(
        SQLUUID(as_uuid=True), primary_key=True, default=uuid4
    )
    ded_schedule_id: Mapped[UUID] = mapped_column(
        SQLUUID(as_uuid=True),
        ForeignKey("itr_ded_schedule.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    display_order: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    type: Mapped[str] = mapped_column(String, nullable=False)
    insurance_company: Mapped[str] = mapped_column(String, nullable=False)
    policy_no: Mapped[str | None] = mapped_column(String, nullable=True)
    premium_paid: Mapped[float] = mapped_column(Numeric(12, 2), default=0)

    ded_schedule: Mapped["ITRDedSchedule"] = relationship(
        back_populates="ded_80d_policies"
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), onupdate=func.now()
    )


class ITRDed80GDonation(Base):
    __tablename__ = "itr_80g_donation"
    id: Mapped[UUID] = mapped_column(
        SQLUUID(as_uuid=True), primary_key=True, default=uuid4
    )
    ded_schedule_id: Mapped[UUID] = mapped_column(
        SQLUUID(as_uuid=True),
        ForeignKey("itr_ded_schedule.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    type: Mapped[str] = mapped_column(String, nullable=False)
    donation_name: Mapped[str] = mapped_column(String, nullable=False)
    donation_amount: Mapped[float] = mapped_column(Numeric(12, 2), default=0)
    donation_pan: Mapped[str | None] = mapped_column(String, nullable=True)
    donation_city: Mapped[str | None] = mapped_column(String, nullable=True)
    donation_state: Mapped[str | None] = mapped_column(String, nullable=True)
    donation_pincode: Mapped[str | None] = mapped_column(String, nullable=True)
    is_cash_donation: Mapped[bool] = mapped_column(Boolean, default=False)
    donation_arn: Mapped[str | None] = mapped_column(String, nullable=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), onupdate=func.now()
    )

    ded_schedule: Mapped["ITRDedSchedule"] = relationship(
        back_populates="ded_80g_donations"
    )


class ITRDed80DD80U(Base):
    __tablename__ = "itr_80d_80u"
    id: Mapped[UUID] = mapped_column(
        SQLUUID(as_uuid=True), primary_key=True, default=uuid4
    )
    ded_schedule_id: Mapped[UUID] = mapped_column(
        SQLUUID(as_uuid=True),
        ForeignKey("itr_ded_schedule.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    is_servere_disability: Mapped[bool] = mapped_column(Boolean, default=False)
    eligible_deduction: Mapped[float] = mapped_column(Numeric(12, 2), default=0)
    dependant_pan: Mapped[str | None] = mapped_column(String, nullable=True)
    dependant_aadhar: Mapped[str | None] = mapped_column(String, nullable=True)
    relation: Mapped[str] = mapped_column(String, nullable=False)
    uudid_number: Mapped[str | None] = mapped_column(String, nullable=True)
    form10_number: Mapped[str | None] = mapped_column(String, nullable=True)
    form10_date: Mapped[date | None] = mapped_column(Date, nullable=True)

    is_80u_eligible: Mapped[bool] = mapped_column(Boolean, default=False)
    sec_80u_deduction: Mapped[float] = mapped_column(Numeric(12, 2), default=0)
    sec_80u_uudid_number: Mapped[str | None] = mapped_column(String, nullable=True)
    sec_80u_form10_number: Mapped[str | None] = mapped_column(String, nullable=True)
    sec_80u_form10_date: Mapped[date | None] = mapped_column(Date, nullable=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), onupdate=func.now()
    )

    ded_schedule: Mapped["ITRDedSchedule"] = relationship(back_populates="ded_80d_80u")


class ITRDed80DDB(Base):
    __tablename__ = "itr_80ddb"
    id: Mapped[UUID] = mapped_column(
        SQLUUID(as_uuid=True), primary_key=True, default=uuid4
    )
    ded_schedule_id: Mapped[UUID] = mapped_column(
        SQLUUID(as_uuid=True),
        ForeignKey("itr_ded_schedule.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    type: Mapped[str] = mapped_column(String, nullable=False)
    diseases_details: Mapped[str] = mapped_column(String, nullable=False)
    disease_id: Mapped[str] = mapped_column(String, nullable=False)
    disease_expenditure: Mapped[float] = mapped_column(Numeric(12, 2), default=0)
    disease_claimed: Mapped[float] = mapped_column(Numeric(12, 2), default=0)
    disease_deduction: Mapped[float] = mapped_column(Numeric(12, 2), default=0)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), onupdate=func.now()
    )

    ded_schedule: Mapped["ITRDedSchedule"] = relationship(back_populates="ded_80ddb")


class ITRDed80ELoan(Base):
    """80E — interest on education loan (repeatable rows)."""

    __tablename__ = "itr_80e_loans"

    id: Mapped[UUID] = mapped_column(
        SQLUUID(as_uuid=True), primary_key=True, default=uuid4
    )
    ded_schedule_id: Mapped[UUID] = mapped_column(
        SQLUUID(as_uuid=True),
        ForeignKey("itr_ded_schedule.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    display_order: Mapped[int] = mapped_column(Integer, nullable=False, default=1)

    # "From" — lender category (e.g. B = bank; match your UI / ITR codes)
    loan_taken_from: Mapped[Optional[str]] = mapped_column(String(1), nullable=True)
    bank_or_institution_name: Mapped[str] = mapped_column(
        String(125), nullable=False, default=""
    )
    loan_account_no: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    date_of_loan: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    total_loan_amount: Mapped[Decimal] = mapped_column(
        Numeric(15, 2), nullable=False, default=0
    )
    loan_outstanding_amount: Mapped[Decimal] = mapped_column(
        Numeric(15, 2), nullable=False, default=0
    )
    interest_claimed: Mapped[Decimal] = mapped_column(
        Numeric(15, 2), nullable=False, default=0
    )

    ded_schedule: Mapped["ITRDedSchedule"] = relationship(
        back_populates="ded_80e_loans"
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), onupdate=func.now()
    )


class ITRDed80EEBLoan(Base):
    """80EEB — interest on electric vehicle loan (repeatable rows)."""

    __tablename__ = "itr_80eeb_loans"

    id: Mapped[UUID] = mapped_column(
        SQLUUID(as_uuid=True), primary_key=True, default=uuid4
    )
    ded_schedule_id: Mapped[UUID] = mapped_column(
        SQLUUID(as_uuid=True),
        ForeignKey("itr_ded_schedule.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    display_order: Mapped[int] = mapped_column(Integer, nullable=False, default=1)

    loan_taken_from: Mapped[Optional[str]] = mapped_column(String(1), nullable=True)
    bank_or_institution_name: Mapped[str] = mapped_column(
        String(125), nullable=False, default=""
    )
    loan_account_no: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    date_of_loan: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    total_loan_amount: Mapped[Decimal] = mapped_column(
        Numeric(15, 2), nullable=False, default=0
    )
    loan_outstanding_amount: Mapped[Decimal] = mapped_column(
        Numeric(15, 2), nullable=False, default=0
    )
    vehicle_reg_no: Mapped[Optional[str]] = mapped_column(String(11), nullable=True)
    interest_claimed: Mapped[Decimal] = mapped_column(
        Numeric(15, 2), nullable=False, default=0
    )

    ded_schedule: Mapped["ITRDedSchedule"] = relationship(
        back_populates="ded_80eeb_loans"
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), onupdate=func.now()
    )


class ITRDedOtherLine(Base):
    """Fixed 'Other Deductions' rows: 80GG, 80QQB, 80RRB, 80TTA, 80TTB.

    Seed five rows per schedule (unique section per ded_schedule_id), e.g.:
    (1, 80GG,  House Rent Paid, ...),
    (2, 80QQB, Royalty Income of Authors, ...),
    (3, 80RRB, Royalty on Patents, ...),
    (4, 80TTA, Interest on Savings A/c's (max ₹10,000), ...),
    (5, 80TTB, Interest on Savings/Deposit A/c's (Sr. Citizen, max ₹50,000), ...).
    Total → ITRDedSchedule.sec_other_total (sum of amounts or capped total).
    """

    __tablename__ = "itr_ded_other_lines"
    __table_args__ = (
        UniqueConstraint(
            "ded_schedule_id",
            "section",
            name="uq_itr_ded_other_lines_schedule_section",
        ),
    )

    id: Mapped[UUID] = mapped_column(
        SQLUUID(as_uuid=True), primary_key=True, default=uuid4
    )
    ded_schedule_id: Mapped[UUID] = mapped_column(
        SQLUUID(as_uuid=True),
        ForeignKey("itr_ded_schedule.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    display_order: Mapped[int] = mapped_column(Integer, nullable=False, default=1)

    # e.g. 80GG, 80QQB, 80RRB, 80TTA, 80TTB
    section: Mapped[str] = mapped_column(String(10), nullable=False)
    description: Mapped[str] = mapped_column(String(300), nullable=False, default="")
    amount: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False, default=0)
    comments: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)

    ded_schedule: Mapped["ITRDedSchedule"] = relationship(
        back_populates="ded_other_lines"
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), onupdate=func.now()
    )


class ITRDed80GGAEntry(Base):
    __tablename__ = "itr_ded_80gga_entries"
    id: Mapped[UUID] = mapped_column(
        SQLUUID(as_uuid=True), primary_key=True, default=uuid4
    )
    ded_schedule_id: Mapped[UUID] = mapped_column(
        SQLUUID(as_uuid=True),
        ForeignKey("itr_ded_schedule.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    name: Mapped[str] = mapped_column(String, nullable=False)
    pan: Mapped[str] = mapped_column(String, nullable=False)
    nature_of_description: Mapped[str] = mapped_column(String, nullable=False)
    amount: Mapped[float] = mapped_column(Numeric(12, 2), default=0)
    is_eligible: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), onupdate=func.now()
    )

    ded_schedule: Mapped["ITRDedSchedule"] = relationship(
        back_populates="ded_80gga_entries"
    )


class ITRDed80GGCEntry(Base):
    """80GGC — contributions to political parties (repeatable rows)."""

    __tablename__ = "itr_ded_80ggc_entries"

    id: Mapped[UUID] = mapped_column(
        SQLUUID(as_uuid=True), primary_key=True, default=uuid4
    )
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

    computed_eligible_amount: Mapped[Optional[Decimal]] = mapped_column(
        Numeric(15, 2), nullable=True
    )

    ded_schedule: Mapped["ITRDedSchedule"] = relationship(
        back_populates="ded_80ggc_entries"
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), onupdate=func.now()
    )

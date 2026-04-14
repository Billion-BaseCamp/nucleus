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

    sec_80c_capped: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False, default=0)
    nps_total: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False, default=0)
    total_80d_80g: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False, default=0)
    total_chapter_via: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False, default=0)
    sec_80dMedical_total: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False, default=0)
    sec_80gDonation_total: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False, default=0)
    sec_80ddHandicapped_total: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False, default=0)
    sec_80ddbDiseases_total: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False, default=0)
    sec_80ggcPolitical_total: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False, default=0)
    sec_80uDisability_total: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False, default=0)
    sec_80eeducation_total: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False, default=0)
    sec_80eebVehicle_total: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False, default=0)
    sec_other_total: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False, default=0)

     # ── Relationships ──
     #one to one relationship with ITRReturn
    itr_return: Mapped["ITRReturn"] = relationship("ITRReturn", back_populates="deductions")
    #one to one relationship with ITRDed80C80CCD
    ded_80c_80ccd: Mapped["ITRDed_80C_80CCD"] = relationship(back_populates="ded_schedule")
    #one to one relationship with ITR80DMeta
    ded_80d_meta: Mapped["ITR80DMeta"] = relationship(back_populates="ded_schedule")

    #one to many relationship with ITR80DDetail
    ded_80d_details: Mapped[List["ITR80DDetail"]] = relationship(back_populates="ded_schedule", cascade="all, delete-orphan")
    #one to many relationship with ITR80DPolicy
    ded_80d_policies: Mapped[List["ITR80DPolicy"]] = relationship(back_populates="ded_schedule", cascade="all, delete-orphan")
    #one to many relationship with ITRDed80C
    ded_80c: Mapped[List["ITRDed80C"]] = relationship(back_populates="ded_schedule", cascade="all, delete-orphan")

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), onupdate=func.now())


class ITRDed80C(Base):
    __tablename__ = "itr_ded_80c"
    id: Mapped[UUID] = mapped_column(SQLUUID(as_uuid=True), primary_key=True, default=uuid4)
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
    
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), onupdate=func.now())

class ITRDed_80C_80CCD(Base):
    __tablename__ = "itr_ded_80c_80ccd"
    id: Mapped[UUID] = mapped_column(SQLUUID(as_uuid=True), primary_key=True, default=uuid4)
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
    sec80ccd1b_voluntary_amount: Mapped[float] = mapped_column(Numeric(12, 2), default=0)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), onupdate=func.now())

    ded_schedule: Mapped["ITRDedSchedule"] = relationship(back_populates="ded_80c_80ccd")


class ITR80DDetail(Base):
    __tablename__ = "itr_80d_details"

    id: Mapped[UUID] = mapped_column(SQLUUID(as_uuid=True), primary_key=True, default=uuid4)
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

    ded_schedule: Mapped["ITRDedSchedule"] = relationship(back_populates="80d_details")

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), onupdate=func.now())

class ITR80DMeta(Base):
    __tablename__ = "itr_80d_meta"

    id: Mapped[UUID] = mapped_column(SQLUUID(as_uuid=True), primary_key=True, default=uuid4)

    itr_return_id: Mapped[UUID] = mapped_column(
        SQLUUID(as_uuid=True),
        ForeignKey("itr_returns.id"),
        unique=True
    )

    self_family_senior: Mapped[bool] = mapped_column(Boolean, default=False)
    parents_senior: Mapped[bool] = mapped_column(Boolean, default=False)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), onupdate=func.now())

    ded_schedule: Mapped["ITRDedSchedule"] = relationship(back_populates="80d_meta")

class ITR80DPolicy(Base):
    __tablename__ = "itr_80d_policies"
    id: Mapped[UUID] = mapped_column(SQLUUID(as_uuid=True), primary_key=True, default=uuid4)
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

    ded_schedule: Mapped["ITRDedSchedule"] = relationship(back_populates="80d_policies")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), onupdate=func.now())

"""
ITR filing layer: Step 2 wizard persistence (salary row, other info Q&A, residency).

Maps to itr_step2_salary, itr_step2_salary_deductions, itr_step2_other_info,
itr_step2_other_info_data, itr_step2_residency.
"""

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Any, List, Optional
from uuid import UUID, uuid4

if TYPE_CHECKING:
    from nucleus.models.itr_filling.itr_document_slot import ITRDocumentSlot

from sqlalchemy import (
    UUID as SQLUUID,
    Boolean,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from nucleus.db.database import Base


class ITRStep2Salary(Base):
    __tablename__ = "itr_step2_salary"

    id: Mapped[UUID] = mapped_column(
        SQLUUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
        index=True,
    )
    client_id: Mapped[UUID] = mapped_column(
        SQLUUID(as_uuid=True),
        ForeignKey("clients.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    financial_year_id: Mapped[UUID] = mapped_column(
        SQLUUID(as_uuid=True),
        ForeignKey("financial_years.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    employer_name: Mapped[str] = mapped_column(String, nullable=False, default="")
    sequence: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    job_change_during_year: Mapped[Optional[str]] = mapped_column(
        String, nullable=True
    )
    f16_employer_from: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    f16_employer_to: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    comment: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    source: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    is_current: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    f16_uploaded: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=False, server_default="FALSE"
    )
    f16_has_12ba: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=False, server_default="FALSE"
    )
    f16_has_annexure: Mapped[bool] = mapped_column(
        Boolean, nullable=True, default=False, server_default="FALSE"
    )
    f16_regime: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    f16_period: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    cascade_step: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    cascade_12ba: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    cascade_itcs: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    cascade_slip: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    cascade_comment: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    fnf_uploaded: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=False, server_default="FALSE"
    )

    client: Mapped["Client"] = relationship("Client")
    financial_year: Mapped["FinancialYear"] = relationship("FinancialYear")


class ITRStep2SalaryTrigger(Base):
    __tablename__ = "itr_step2_salary_trigger"

    id: Mapped[UUID] = mapped_column(
        SQLUUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
        index=True,
    )
    client_id: Mapped[UUID] = mapped_column(
        SQLUUID(as_uuid=True),
        ForeignKey("clients.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    financial_year_id: Mapped[UUID] = mapped_column(
        SQLUUID(as_uuid=True),
        ForeignKey("financial_years.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    trigger_id: Mapped[str] = mapped_column(String, nullable=False)
    enabled: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=False, server_default="FALSE"
    )
    comment: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    slot_id: Mapped[Optional[UUID]] = mapped_column(
        SQLUUID(as_uuid=True),
        ForeignKey("itr_document_slots.id", ondelete="SET NULL"),
        nullable=True,
    )

    client: Mapped["Client"] = relationship("Client")
    financial_year: Mapped["FinancialYear"] = relationship("FinancialYear")
    attachment_slot: Mapped[Optional["ITRDocumentSlot"]] = relationship(
        "ITRDocumentSlot",
        foreign_keys=[slot_id],
    )

    __table_args__ = (
        UniqueConstraint(
            "client_id",
            "financial_year_id",
            "trigger_id",
            name="uq_itr_step2_salary_trigger",
        ),
    )


class ITRStep2SalaryDeductionDetail(Base):
    __tablename__ = "itr_step2_salary_deduction_detail"

    id: Mapped[UUID] = mapped_column(
        SQLUUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
        index=True,
    )
    client_id: Mapped[UUID] = mapped_column(
        SQLUUID(as_uuid=True),
        ForeignKey("clients.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    financial_year_id: Mapped[UUID] = mapped_column(
        SQLUUID(as_uuid=True),
        ForeignKey("financial_years.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    deduction_id: Mapped[str] = mapped_column(String, nullable=False)
    enabled: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=False, server_default="FALSE"
    )
    comment: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    slot_id: Mapped[Optional[UUID]] = mapped_column(
        SQLUUID(as_uuid=True),
        ForeignKey("itr_document_slots.id", ondelete="SET NULL"),
        nullable=True,
    )

    client: Mapped["Client"] = relationship("Client")
    financial_year: Mapped["FinancialYear"] = relationship("FinancialYear")
    attachment_slot: Mapped[Optional["ITRDocumentSlot"]] = relationship(
        "ITRDocumentSlot",
        foreign_keys=[slot_id],
    )

    __table_args__ = (
        UniqueConstraint(
            "client_id",
            "financial_year_id",
            "deduction_id",
            name="uq_itr_step2_salary_deduction_detail",
        ),
    )


class ITRStep2SalaryDeductions(Base):
    __tablename__ = "itr_step2_salary_deductions"

    id: Mapped[UUID] = mapped_column(
        SQLUUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
        index=True,
    )
    client_id: Mapped[UUID] = mapped_column(
        SQLUUID(as_uuid=True),
        ForeignKey("clients.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    financial_year_id: Mapped[UUID] = mapped_column(
        SQLUUID(as_uuid=True),
        ForeignKey("financial_years.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    health: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=False, server_default="FALSE"
    )
    donations: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=False, server_default="FALSE"
    )
    education: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=False, server_default="FALSE"
    )
    nps: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=False, server_default="FALSE"
    )
    other_80c: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=False, server_default="FALSE"
    )

    client: Mapped["Client"] = relationship("Client")
    financial_year: Mapped["FinancialYear"] = relationship("FinancialYear")


class ITRStep2OtherInfo(Base):
    __tablename__ = "itr_step2_other_info"

    id: Mapped[UUID] = mapped_column(
        SQLUUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
        index=True,
    )
    client_id: Mapped[UUID] = mapped_column(
        SQLUUID(as_uuid=True),
        ForeignKey("clients.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    financial_year_id: Mapped[UUID] = mapped_column(
        SQLUUID(as_uuid=True),
        ForeignKey("financial_years.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    section: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    question_type: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    question_code: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    answer: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    filtered_in: Mapped[Optional[bool]] = mapped_column(Boolean, nullable=True)
    reason: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    comment: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    override: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=False, server_default="FALSE"
    )

    client: Mapped["Client"] = relationship("Client")
    financial_year: Mapped["FinancialYear"] = relationship("FinancialYear")
    data_rows: Mapped[List["ITRStep2OtherInfoData"]] = relationship(
        "ITRStep2OtherInfoData",
        back_populates="other_info",
        cascade="all, delete-orphan",
    )


class ITRStep2OtherInfoData(Base):
    __tablename__ = "itr_step2_other_info_data"

    id: Mapped[UUID] = mapped_column(
        SQLUUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
        index=True,
    )
    other_info_id: Mapped[UUID] = mapped_column(
        SQLUUID(as_uuid=True),
        ForeignKey("itr_step2_other_info.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    from_last_year: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=False, server_default="FALSE"
    )
    data: Mapped[Optional[Any]] = mapped_column(JSONB, nullable=True)

    other_info: Mapped["ITRStep2OtherInfo"] = relationship(
        "ITRStep2OtherInfo",
        back_populates="data_rows",
    )


class ITRStep2Residency(Base):
    __tablename__ = "itr_step2_residency"

    id: Mapped[UUID] = mapped_column(
        SQLUUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
        index=True,
    )
    client_id: Mapped[UUID] = mapped_column(
        SQLUUID(as_uuid=True),
        ForeignKey("clients.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    financial_year_id: Mapped[UUID] = mapped_column(
        SQLUUID(as_uuid=True),
        ForeignKey("financial_years.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    # Card 1: Last year's residency status
    last_year_status: Mapped[Optional[str]] = mapped_column(
        String(10), nullable=True
    )  # ROR | RNOR | NR
    is_residency_detected: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
        server_default="FALSE",
    )

    # Card 2: Days in India this FY
    days_current_fy: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    fy_bucket: Mapped[Optional[str]] = mapped_column(
        String(20), nullable=True
    )  # <60 | 60-119 | 120-181 | 182+

    # Card 3: Citizenship (conditional)
    citizenship: Mapped[Optional[str]] = mapped_column(
        String(20), nullable=True
    )  # Indian | OCI-PIO | Foreign

    # Card 4a: Employment scenario (conditional)
    employment_scenario: Mapped[Optional[str]] = mapped_column(
        String(20), nullable=True
    )  # inIndia | movedThisYear | movedEarlier

    # Card 4b: Visit or moved back (conditional)
    visit_or_moved: Mapped[Optional[str]] = mapped_column(
        String(10), nullable=True
    )  # visiting | moved

    # Card 5: Indian income above ₹15L (conditional)
    income_above_15l: Mapped[Optional[bool]] = mapped_column(Boolean, nullable=True)

    # Card 5b: Prior 4 FY day counts (conditional)
    prior4_days: Mapped[Optional[Any]] = mapped_column(JSONB, nullable=True)

    # Card 6: Deep test (conditional)
    deep_test_days7: Mapped[Optional[Any]] = mapped_column(JSONB, nullable=True)
    deep_test_resident10: Mapped[Optional[Any]] = mapped_column(JSONB, nullable=True)

    # Computed result (e.g. written by client PUT at terminal state)
    computed_status: Mapped[Optional[str]] = mapped_column(
        String(10), nullable=True
    )  # ROR | RNOR | NR
    computed_path: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # Overrides & notes
    residency_confirmed: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=False, server_default="FALSE"
    )
    confirmed_same: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=False, server_default="FALSE"
    )
    override_status: Mapped[Optional[str]] = mapped_column(
        String(10), nullable=True
    )  # ROR | RNOR | NR (e.g. RM override)
    comment: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
    updated_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        onupdate=func.now(),
        nullable=True,
    )

    client: Mapped["Client"] = relationship("Client")
    financial_year: Mapped["FinancialYear"] = relationship("FinancialYear")

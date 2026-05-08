"""
ITR filing layer: Step 2 wizard persistence (salary row, other info Q&A, residency).

Maps to itr_step2_salary, itr_step2_salary_deductions, itr_step2_other_info,
itr_step2_other_info_data, itr_step2_residency.
"""

from __future__ import annotations

from typing import Any, List, Optional
from uuid import UUID, uuid4

from sqlalchemy import Boolean, ForeignKey, String, Text, UUID as SQLUUID
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

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
    source: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    is_current: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    f16_uploaded: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=False, server_default="FALSE"
    )
    f16_has_12ba: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=False, server_default="FALSE"
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
    question_code: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    answer: Mapped[Optional[str]] = mapped_column(String, nullable=True)
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

    current_year_status: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    confirmed_same: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=False, server_default="FALSE"
    )
    override_status: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    days_in_india: Mapped[Optional[Any]] = mapped_column(JSONB, nullable=True)
    comment: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    client: Mapped["Client"] = relationship("Client")
    financial_year: Mapped["FinancialYear"] = relationship("FinancialYear")

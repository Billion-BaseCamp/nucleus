"""
ITR filing layer: Schedule S (salary) persistence.

Hangs off the central ITRReturn via itr_salary_schedule (1:1).
Child tables for employers, components, allowances, perquisites,
foreign salary, and other salary.
"""

from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from typing import Any, List, Optional
from uuid import UUID, uuid4

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text, UUID as SQLUUID
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from sqlalchemy.types import Numeric

from nucleus.db.database import Base


class ITRSalarySchedule(Base):
    """Schedule S — one-to-one child of ITRReturn."""

    __tablename__ = "itr_salary_schedule"

    id: Mapped[UUID] = mapped_column(SQLUUID(as_uuid=True), primary_key=True, default=uuid4)
    itr_return_id: Mapped[UUID] = mapped_column(
        SQLUUID(as_uuid=True),
        ForeignKey("itr_returns.id", ondelete="CASCADE"),
        nullable=False,
        unique=True,
        index=True,
    )

    total_gross_salary: Mapped[Optional[Decimal]] = mapped_column(Numeric(18, 2), default=0)
    total_exempt_us10: Mapped[Optional[Decimal]] = mapped_column(Numeric(18, 2), default=0)
    net_salary: Mapped[Optional[Decimal]] = mapped_column(Numeric(18, 2), default=0)
    total_deduction_us16: Mapped[Optional[Decimal]] = mapped_column(Numeric(18, 2), default=0)
    total_net_taxable: Mapped[Optional[Decimal]] = mapped_column(Numeric(18, 2), default=0)
    total_tds: Mapped[Optional[Decimal]] = mapped_column(Numeric(18, 2), default=0)

    itr_return: Mapped["ITRReturn"] = relationship("ITRReturn", back_populates="salary")
    employers: Mapped[List["ITRSalaryEmployer"]] = relationship(
        back_populates="salary_schedule",
        cascade="all, delete-orphan",
        order_by="ITRSalaryEmployer.sort_order",
    )
    foreign_salaries: Mapped[List["ITRForeignSalary"]] = relationship(
        back_populates="salary_schedule",
        cascade="all, delete-orphan",
        order_by="ITRForeignSalary.sort_order",
    )
    other_salaries: Mapped[List["ITROtherSalary"]] = relationship(
        back_populates="salary_schedule",
        cascade="all, delete-orphan",
        order_by="ITROtherSalary.sort_order",
    )

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), onupdate=func.now())


class ITRSalaryEmployer(Base):
    """Per-employer salary (ScheduleS.Salaries[])."""

    __tablename__ = "itr_salary_employers"

    id: Mapped[UUID] = mapped_column(SQLUUID(as_uuid=True), primary_key=True, default=uuid4)
    salary_schedule_id: Mapped[UUID] = mapped_column(
        SQLUUID(as_uuid=True),
        ForeignKey("itr_salary_schedule.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    sort_order: Mapped[int] = mapped_column(Integer, default=0)

    source_employer_id: Mapped[Optional[UUID]] = mapped_column(
        SQLUUID(as_uuid=True),
        ForeignKey("employers.id", ondelete="SET NULL"),
        nullable=True,
    )

    employer_name: Mapped[str] = mapped_column(String(125), nullable=False, default="")
    tan: Mapped[str] = mapped_column(String(10), nullable=False, default="")
    address: Mapped[Optional[str]] = mapped_column(String(200), nullable=True)
    city: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    state: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    state_code: Mapped[Optional[str]] = mapped_column(String(5), nullable=True)
    pin: Mapped[Optional[str]] = mapped_column(String(6), nullable=True)

    nature_of_employment: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)

    ais_tan: Mapped[Optional[str]] = mapped_column(String(10), nullable=True)
    ais_tds: Mapped[Optional[Decimal]] = mapped_column(Numeric(18, 2), default=0)

    profits_in_lieu_of_salary: Mapped[Optional[Decimal]] = mapped_column(Numeric(18, 2), default=0)
    previous_employer_income: Mapped[Optional[Decimal]] = mapped_column(Numeric(18, 2), default=0)

    income_notified_89a: Mapped[Optional[Decimal]] = mapped_column(Numeric(18, 2), default=0)
    income_notified_other_89a: Mapped[Optional[Decimal]] = mapped_column(Numeric(18, 2), default=0)
    country_notified_89a: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)

    entertainment_allowance: Mapped[Optional[Decimal]] = mapped_column(Numeric(18, 2), default=0)
    professional_tax: Mapped[Optional[Decimal]] = mapped_column(Numeric(18, 2), default=0)
    standard_deduction: Mapped[Optional[Decimal]] = mapped_column(Numeric(18, 2), default=0)

    housing_loan_interest: Mapped[Optional[Decimal]] = mapped_column(Numeric(18, 2), default=0)
    ios_reported_by_employer: Mapped[Optional[Decimal]] = mapped_column(Numeric(18, 2), default=0)

    tds_deducted: Mapped[Optional[Decimal]] = mapped_column(Numeric(18, 2), default=0)

    gross_salary_17_1: Mapped[Optional[Decimal]] = mapped_column(Numeric(18, 2), default=0)
    total_perquisites: Mapped[Optional[Decimal]] = mapped_column(Numeric(18, 2), default=0)
    total_gross_salary: Mapped[Optional[Decimal]] = mapped_column(Numeric(18, 2), default=0)
    total_exempt_us10: Mapped[Optional[Decimal]] = mapped_column(Numeric(18, 2), default=0)
    income_from_salary: Mapped[Optional[Decimal]] = mapped_column(Numeric(18, 2), default=0)

    salary_schedule: Mapped["ITRSalarySchedule"] = relationship(back_populates="employers")
    components: Mapped[List["ITRSalaryComponent"]] = relationship(
        back_populates="employer",
        cascade="all, delete-orphan",
        order_by="ITRSalaryComponent.sort_order",
    )
    allowances: Mapped[List["ITRSalaryAllowance"]] = relationship(
        back_populates="employer",
        cascade="all, delete-orphan",
        order_by="ITRSalaryAllowance.sort_order",
    )
    perquisites: Mapped[List["ITRSalaryPerquisite"]] = relationship(
        back_populates="employer",
        cascade="all, delete-orphan",
        order_by="ITRSalaryPerquisite.sort_order",
    )

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), onupdate=func.now())


class ITRSalaryComponent(Base):
    """u/s 17(1) salary line (NatureOfSalary / OthersIncDtls)."""

    __tablename__ = "itr_salary_components"

    id: Mapped[UUID] = mapped_column(SQLUUID(as_uuid=True), primary_key=True, default=uuid4)
    employer_id: Mapped[UUID] = mapped_column(
        SQLUUID(as_uuid=True),
        ForeignKey("itr_salary_employers.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    sort_order: Mapped[int] = mapped_column(Integer, default=0)

    component: Mapped[str] = mapped_column(String(100), nullable=False, default="")
    nature_code: Mapped[Optional[str]] = mapped_column(String(5), nullable=True)

    received: Mapped[Decimal] = mapped_column(Numeric(18, 2), default=0)
    exempt: Mapped[Decimal] = mapped_column(Numeric(18, 2), default=0)
    taxable: Mapped[Decimal] = mapped_column(Numeric(18, 2), default=0)
    exempt_section: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)

    employer: Mapped["ITRSalaryEmployer"] = relationship(back_populates="components")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class ITRSalaryAllowance(Base):
    """Allowance with optional calculator inputs (JSONB)."""

    __tablename__ = "itr_salary_allowances"

    id: Mapped[UUID] = mapped_column(SQLUUID(as_uuid=True), primary_key=True, default=uuid4)
    employer_id: Mapped[UUID] = mapped_column(
        SQLUUID(as_uuid=True),
        ForeignKey("itr_salary_employers.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    sort_order: Mapped[int] = mapped_column(Integer, default=0)

    allowance_type: Mapped[str] = mapped_column(String(100), nullable=False, default="")
    exempt_section: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)

    received: Mapped[Decimal] = mapped_column(Numeric(18, 2), default=0)
    exempt: Mapped[Decimal] = mapped_column(Numeric(18, 2), default=0)
    taxable: Mapped[Decimal] = mapped_column(Numeric(18, 2), default=0)

    calc_inputs: Mapped[Optional[dict[str, Any]]] = mapped_column(JSONB, nullable=True)

    employer: Mapped["ITRSalaryEmployer"] = relationship(back_populates="allowances")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class ITRSalaryPerquisite(Base):
    """u/s 17(2) perquisite line."""

    __tablename__ = "itr_salary_perquisites"

    id: Mapped[UUID] = mapped_column(SQLUUID(as_uuid=True), primary_key=True, default=uuid4)
    employer_id: Mapped[UUID] = mapped_column(
        SQLUUID(as_uuid=True),
        ForeignKey("itr_salary_employers.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    sort_order: Mapped[int] = mapped_column(Integer, default=0)

    perquisite_type: Mapped[str] = mapped_column(String(100), nullable=False, default="")
    nature_code: Mapped[Optional[str]] = mapped_column(String(5), nullable=True)

    value: Mapped[Decimal] = mapped_column(Numeric(18, 2), default=0)

    employer: Mapped["ITRSalaryEmployer"] = relationship(back_populates="perquisites")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class ITRForeignSalary(Base):
    __tablename__ = "itr_foreign_salaries"

    id: Mapped[UUID] = mapped_column(SQLUUID(as_uuid=True), primary_key=True, default=uuid4)
    salary_schedule_id: Mapped[UUID] = mapped_column(
        SQLUUID(as_uuid=True),
        ForeignKey("itr_salary_schedule.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    sort_order: Mapped[int] = mapped_column(Integer, default=0)

    employer_name: Mapped[str] = mapped_column(String(125), nullable=False, default="")
    taxable_salary: Mapped[Decimal] = mapped_column(Numeric(18, 2), default=0)
    comments: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    period_from: Mapped[Optional[str]] = mapped_column(String(10), nullable=True)
    period_to: Mapped[Optional[str]] = mapped_column(String(10), nullable=True)

    salary_schedule: Mapped["ITRSalarySchedule"] = relationship(back_populates="foreign_salaries")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class ITROtherSalary(Base):
    __tablename__ = "itr_other_salaries"

    id: Mapped[UUID] = mapped_column(SQLUUID(as_uuid=True), primary_key=True, default=uuid4)
    salary_schedule_id: Mapped[UUID] = mapped_column(
        SQLUUID(as_uuid=True),
        ForeignKey("itr_salary_schedule.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    sort_order: Mapped[int] = mapped_column(Integer, default=0)

    employer_name: Mapped[str] = mapped_column(String(125), nullable=False, default="")
    taxable_salary: Mapped[Decimal] = mapped_column(Numeric(18, 2), default=0)
    comments: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    period_from: Mapped[Optional[str]] = mapped_column(String(10), nullable=True)
    period_to: Mapped[Optional[str]] = mapped_column(String(10), nullable=True)

    salary_schedule: Mapped["ITRSalarySchedule"] = relationship(back_populates="other_salaries")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

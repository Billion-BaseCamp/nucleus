from __future__ import annotations

from datetime import date, datetime
from typing import List, Optional
from uuid import UUID, uuid4

from sqlalchemy import Boolean, Date, DateTime, ForeignKey, Integer, String, UUID as SQLUUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from nucleus.db.database import Base



class Quarter(Base):
    __tablename__ = "quarters"
    id: Mapped[UUID] = mapped_column(SQLUUID(as_uuid=True), primary_key=True, default=uuid4, index=True)
    
    # Foreign key to financial year
    financial_year_id: Mapped[UUID] = mapped_column(SQLUUID(as_uuid=True), ForeignKey("financial_years.id", ondelete="CASCADE"), nullable=False)
    
    quarter_number: Mapped[int] = mapped_column(Integer, nullable=False)
    start_date: Mapped[date] = mapped_column(Date, nullable=False)
    end_date: Mapped[date] = mapped_column(Date, nullable=False)
    is_locked: Mapped[bool] = mapped_column(Boolean, default=False)
    status: Mapped[str] = mapped_column(String, nullable=False)
    is_liability: Mapped[bool] = mapped_column(Boolean, nullable=True)  # legacy; use liability_status
    liability_status: Mapped[str | None] = mapped_column(String, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), onupdate=func.now(), nullable=True)
    is_json_imported: Mapped[bool] = mapped_column(Boolean, default=False, nullable=True)
    
    # Relationships
    # 26AS uploads own the link via AdvanceTax26asUpload.quarter_id (unique) —
    # no reverse FK here, to avoid a cycle with advance_tax_26as_uploads.
    financial_year: Mapped["FinancialYear"] = relationship("FinancialYear", back_populates="quarters")
    
    # Financial data relationships
    interest_details: Mapped[List["InterestDetails"]] = relationship("InterestDetails", back_populates="quarter")
    dividends: Mapped[List["Dividends"]] = relationship("Dividends", back_populates="quarter")
    capital_gains: Mapped[List["CapitalGains"]] = relationship("CapitalGains", back_populates="quarter")
    cg_document_slots: Mapped[List["ATCGDocumentSlot"]] = relationship(
        "ATCGDocumentSlot",
        back_populates="quarter",
        cascade="all, delete-orphan",
    )
    cg_schedule: Mapped[Optional["ATCGSchedule"]] = relationship(
        "ATCGSchedule",
        back_populates="quarter",
        cascade="all, delete-orphan",
        uselist=False,
    )
    other_income: Mapped[List["OtherIncome"]] = relationship("OtherIncome", back_populates="quarter")
    rentals: Mapped[List["Rental"]] = relationship("Rental", back_populates="quarter")
    excemptions: Mapped[List["Excemption"]] = relationship("Excemption", back_populates="quarter", cascade="all, delete-orphan")
    rule_validations: Mapped[List["RuleValidations"]] = relationship("RuleValidations", back_populates="quarter", cascade="all, delete-orphan")


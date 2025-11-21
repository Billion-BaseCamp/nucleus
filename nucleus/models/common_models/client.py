from sqlalchemy import Integer, String, DateTime, Boolean, ForeignKey, UUID as SQLUUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from datetime import datetime, date
from nucleus.db.database import Base
from typing import List
from uuid import UUID, uuid4
from nucleus.core.constants import ResidenceType
from sqlalchemy import Enum, Date   

class Client(Base):
    __tablename__ = "clients"
    id: Mapped[UUID] = mapped_column(SQLUUID(as_uuid=True), primary_key=True, default=uuid4, index=True)
    first_name: Mapped[str] = mapped_column(String, nullable=False)
    last_name: Mapped[str] = mapped_column(String, nullable=False)
    adhar_number: Mapped[str] = mapped_column(String, nullable=True)
    pan_number: Mapped[str] = mapped_column(String, nullable=True)
    gender: Mapped[str] = mapped_column(String, nullable=True)
    date_of_birth: Mapped[date] = mapped_column(Date, nullable=True)
    is_family_member: Mapped[bool] = mapped_column(Boolean, default=False)
    parent_id: Mapped[UUID] = mapped_column(SQLUUID[UUID](as_uuid=True), nullable=True)
    family_relationship: Mapped[str] = mapped_column(String, nullable=True)
    is_advance_tax_payer: Mapped[bool] = mapped_column(Boolean, default=True)
    residence_type: Mapped[ResidenceType] = mapped_column(Enum(ResidenceType), nullable=True)
    
    # Foreign key to advisor
    advisor_id: Mapped[UUID] = mapped_column(SQLUUID[UUID](as_uuid=True), ForeignKey("advisors.id"), nullable=True)
    
    # Relationships
    logins: Mapped[List["Login"]] = relationship("Login", back_populates="client")
    advisor: Mapped["Advisor"] = relationship("Advisor", back_populates="clients")
    financial_years: Mapped[List["FinancialYear"]] = relationship("FinancialYear", back_populates="client")
    
    
    # Financial data relationships
    interest_details: Mapped[List["InterestDetails"]] = relationship("InterestDetails", back_populates="client")
    dividends: Mapped[List["Dividends"]] = relationship("Dividends", back_populates="client")
    capital_gains: Mapped[List["CapitalGains"]] = relationship("CapitalGains", back_populates="client")
    other_income: Mapped[List["OtherIncome"]] = relationship("OtherIncome", back_populates="client")
    rentals: Mapped[List["Rental"]] = relationship("Rental", back_populates="client")
    
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), onupdate=func.now(), nullable=True)
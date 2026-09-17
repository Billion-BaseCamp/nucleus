from __future__ import annotations

from datetime import date, datetime
from typing import List
from uuid import UUID, uuid4

from sqlalchemy import (
    Boolean,
    CheckConstraint,
    Date,
    DateTime,
    Enum,
    ForeignKey,
    Index,
    String,
    UniqueConstraint,
    UUID as SQLUUID,
    text,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from nucleus.core.constants import ResidenceType
from nucleus.db.database import Base
  


class ClientPhoneMapping(Base):
    """Alternate phone numbers for a client. TSM resolves inbound calls through this."""
    __tablename__ = "client_phone_mappings"
    __table_args__ = (UniqueConstraint("client_id", "phone_number", name="uix_client_phone_mapping"),)
    id: Mapped[UUID] = mapped_column(SQLUUID(as_uuid=True), primary_key=True, default=uuid4, index=True)
    client_id: Mapped[UUID] = mapped_column(SQLUUID(as_uuid=True), ForeignKey("clients.id", ondelete="CASCADE"), nullable=False)
    phone_number: Mapped[str] = mapped_column(String, nullable=False)


class ClientEmailMapping(Base):
    """Alternate email addresses for a client.

    Deliberately its own table rather than an ``email`` column on ``ClientPhoneMapping``:
    that one is shared with TSM, and holding an email there would mean making
    ``phone_number`` nullable, which changes what TSM's own queries see.

    The primary address stays on ``logins.email``, which is the sign-in identity — these
    are extra ways to reach someone, not credentials.
    """
    __tablename__ = "client_email_mappings"
    __table_args__ = (
        UniqueConstraint("client_id", "email", name="uix_client_email_mapping"),
        CheckConstraint("email <> ''", name="ck_client_email_mappings_email_nonempty"),
        # Case-insensitive guard, so foo@x.com can't be added again as Foo@X.com.
        Index("uix_client_email_mapping_lower", "client_id", text("lower(email)"), unique=True),
    )
    id: Mapped[UUID] = mapped_column(SQLUUID(as_uuid=True), primary_key=True, default=uuid4)
    client_id: Mapped[UUID] = mapped_column(SQLUUID(as_uuid=True), ForeignKey("clients.id", ondelete="CASCADE"), nullable=False, index=True)
    email: Mapped[str] = mapped_column(String, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), onupdate=func.now(), nullable=True)


class Client(Base):
    __tablename__ = "clients"
    __table_args__ = (
        # One non-empty PAN among *active* clients. Soft-deleted rows keep
        # their PAN so a later re-register can reuse it. NULL is_active is
        # treated as active (legacy rows). Multiple NULLs/blanks allowed.
        Index(
            "uix_clients_pan_number",
            text("upper(btrim(pan_number))"),
            unique=True,
            postgresql_where=text(
                "pan_number IS NOT NULL AND btrim(pan_number) <> '' "
                "AND is_active IS NOT FALSE"
            ),
        ),
    )
    id: Mapped[UUID] = mapped_column(SQLUUID(as_uuid=True), primary_key=True, default=uuid4, index=True)
    first_name: Mapped[str] = mapped_column(String, nullable=False)
    middle_name: Mapped[str] = mapped_column(String, nullable=True)
    last_name: Mapped[str] = mapped_column(String, nullable=False)
    father_name: Mapped[str] = mapped_column(String, nullable=True)
    adhar_number: Mapped[str] = mapped_column(String, nullable=True)
    pan_number: Mapped[str] = mapped_column(String, nullable=True)
    gender: Mapped[str] = mapped_column(String, nullable=True)
    date_of_birth: Mapped[date] = mapped_column(Date, nullable=True)
    is_family_member: Mapped[bool] = mapped_column(Boolean, default=False)
    parent_id: Mapped[UUID] = mapped_column(SQLUUID[UUID](as_uuid=True), nullable=True)
    family_relationship: Mapped[str] = mapped_column(String, nullable=True)
    is_advance_tax_payer: Mapped[bool] = mapped_column(Boolean, default=True)
    residence_type: Mapped[ResidenceType] = mapped_column(Enum(ResidenceType), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=True)  
    deactivated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)
    it_portal_username: Mapped[str] = mapped_column(String, nullable=True)
    it_portal_pass: Mapped[str] = mapped_column(String, nullable=True)

    
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
    excemptions: Mapped[List["Excemption"]] = relationship("Excemption", back_populates="client", cascade="all, delete-orphan")
    
    # Client profiling relationships
    personal_information: Mapped["PersonalInformation"] = relationship("PersonalInformation", back_populates="client")
    addresses: Mapped["Address"] = relationship("Address", back_populates="client")
    employment: Mapped[List["Employment"]] = relationship("Employment", back_populates="client")
    residencies: Mapped[List["Residency"]] = relationship("Residency", back_populates="client")
    citizenships: Mapped[List["Citizenship"]] = relationship("Citizenship", back_populates="client")
    loans: Mapped[List["LoanRecord"]] = relationship("LoanRecord", back_populates="client")
    insurances: Mapped[List["Insurance"]] = relationship("Insurance", back_populates="client")
    real_estate: Mapped[List["RealEstate"]] = relationship("RealEstate", back_populates="client")

    
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), onupdate=func.now(), nullable=True)
from nucleus.db.database import Base
from sqlalchemy import String, ForeignKey, UUID as SQLUUID, Integer, Boolean, DECIMAL, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Optional
from uuid import UUID, uuid4
from datetime import datetime
from decimal import Decimal


class SeparatelyOwnedAccounts(Base):
    __tablename__ = "separately_owned_accounts"

    id: Mapped[UUID] = mapped_column(SQLUUID(as_uuid=True), primary_key=True, default=uuid4, index=True)
    
    financial_year_id: Mapped[Optional[UUID]] = mapped_column(SQLUUID(as_uuid=True), ForeignKey("financial_years.id", ondelete="CASCADE"),nullable=True,index=True)
    financial_year: Mapped[Optional["FinancialYear"]] = relationship("FinancialYear")
    
    country_code_name: Mapped[Optional[str]] = mapped_column(String, nullable=True,index=True)

    sl_no: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    
    maximum_account_value: Mapped[Optional[Decimal]] = mapped_column(DECIMAL(15, 2), nullable=True)
    
    maximum_account_value_unknown: Mapped[Optional[bool]] = mapped_column(Boolean, nullable=True, default=False)
        
    type_of_account: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    
    name_of_financial_institution: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    
    account_number: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    
    mailing_address: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    
    city: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    
    state: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    
    foreign_postal_code: Mapped[Optional[str]] = mapped_column(String, nullable=True)

    hash_key: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    
    comment: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    
    created_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True, server_default=func.now())
    
    updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True, server_default=func.now(), onupdate=func.now())

    

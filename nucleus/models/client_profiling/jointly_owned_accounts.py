from nucleus.db.database import Base
from sqlalchemy import String, ForeignKey, UUID as SQLUUID, Integer, Boolean, DECIMAL, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Optional
from uuid import UUID, uuid4
from datetime import datetime
from decimal import Decimal

class JointlyOwnedAccounts(Base):
    __tablename__ = "jointly_owned_accounts"

    id: Mapped[UUID] = mapped_column(SQLUUID(as_uuid=True), primary_key=True, default=uuid4, index=True)

    financial_year_id: Mapped[Optional[UUID]] = mapped_column(SQLUUID(as_uuid=True), ForeignKey("financial_years.id"),nullable=True,index=True)

    financial_year: Mapped[Optional["FinancialYear"]] = relationship("FinancialYear")

    # Account details
    maximum_account_value: Mapped[Optional[Decimal]] = mapped_column(DECIMAL(15, 2), nullable=True)
    
    type_of_account: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    
    financial_institution: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    
    account_number: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    
    # Mailing address details
    mailing_address: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    
    city: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    
    postal_code: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    
    country_code_name: Mapped[Optional[str]] = mapped_column(String, nullable=True,index=True)
    
    # Joint owner details
    joint_owners: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    
    # Principal details
    principal_tin: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    
    tin_type: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    
    principal_last_name: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    
    principal_first_name: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    
    principal_address: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    
    principal_city: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    
    principal_zip: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    
    principal_country: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    
    # Timestamps
    created_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True, server_default=func.now())
    
    updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True, server_default=func.now(), onupdate=func.now())

    
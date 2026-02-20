from nucleus.db.database import Base
from sqlalchemy import BigInteger, String, DateTime, ForeignKey,func,Date,DECIMAL, UUID as SQLUUID, Boolean 
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import date, datetime
from decimal import Decimal
from typing import Optional
from uuid import UUID, uuid4



class ForeignCustodialAccounts(Base):
    __tablename__ = "foreign_custodial_accounts"

    id: Mapped[UUID] = mapped_column(SQLUUID(as_uuid=True), primary_key=True, default=uuid4, index=True)

    financial_year_id: Mapped[Optional[UUID]] = mapped_column(SQLUUID(as_uuid=True), ForeignKey("financial_years.id", ondelete="CASCADE"),nullable=True,index=True)
    financial_year: Mapped[Optional["FinancialYear"]] = relationship("FinancialYear")

    #country details
    country_id: Mapped[Optional[UUID]] = mapped_column(SQLUUID(as_uuid=True), ForeignKey("country_lookup.id"),nullable=True,index=True)
    
    country: Mapped[Optional["CountryLookup"]] = relationship("CountryLookup", back_populates="foreign_custodial_accounts")

    #institution details
    name_of_institution: Mapped[str] = mapped_column(String, nullable=True)

    address_of_institution: Mapped[str] = mapped_column(String, nullable=True)

    zip_code_of_institution: Mapped[str] = mapped_column(String, nullable=True)

    account_number: Mapped[str] = mapped_column(String, nullable=True)

    status: Mapped[str] = mapped_column(String, nullable=True)

    account_opened_date: Mapped[date] = mapped_column(Date, nullable=True)

    peak_balance: Mapped[Decimal] = mapped_column(DECIMAL(15, 2), nullable=True)

    closing_balance: Mapped[Decimal] = mapped_column(DECIMAL(15, 2), nullable=True)

    gross_interest:Mapped[Decimal] = mapped_column(DECIMAL(15, 2), nullable=True)
    
    comment: Mapped[Optional[str]] = mapped_column(String, nullable=True)

    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=True,server_default=func.now())

    updated_at: Mapped[datetime] = mapped_column(DateTime, nullable=True,server_default=func.now(),onupdate=func.now())
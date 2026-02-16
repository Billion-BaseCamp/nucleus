from uuid import UUID, uuid4
from sqlalchemy import ForeignKey, String, DateTime, Boolean, DECIMAL
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from datetime import datetime
from typing import Optional
from nucleus.db.database import Base
from nucleus.models.advance_tax_models.financial_year import FinancialYear
from nucleus.models.client_profiling.country_lookup import CountryLookup
from sqlalchemy.dialects.postgresql import UUID as SQLUUID

class ForeignSigningAuthorityAccounts(Base):
    __tablename__ = "foreign_signing_authority_accounts"

    id: Mapped[UUID] = mapped_column(SQLUUID(as_uuid=True), primary_key=True, default=uuid4, index=True)

    financial_year_id: Mapped[Optional[UUID]] = mapped_column(SQLUUID(as_uuid=True), ForeignKey("financial_years.id", ondelete="CASCADE"),nullable=True,index=True)
    financial_year: Mapped[Optional["FinancialYear"]] = relationship("FinancialYear")

    #country details
    country_id: Mapped[Optional[UUID]] = mapped_column(SQLUUID(as_uuid=True), ForeignKey("country_lookup.id"),nullable=True,index=True)
    country: Mapped[Optional["CountryLookup"]] = relationship("CountryLookup", back_populates="foreign_signing_authority_accounts")

    name_of_institution: Mapped[str] = mapped_column(String, nullable=True)
    zip_code_of_institution: Mapped[str] = mapped_column(String, nullable=True)
    name_of_account_holder: Mapped[str] = mapped_column(String, nullable=True)
    account_number: Mapped[str] = mapped_column(String, nullable=True)
    peak_balance: Mapped[float] = mapped_column(DECIMAL(15, 2), nullable=True)
    income_accrued_taxable: Mapped[float] = mapped_column(DECIMAL(15, 2), nullable=True)
    income_accrued_in_account: Mapped[bool] = mapped_column(Boolean, nullable=True)
    amount_taxed_on_income: Mapped[float] = mapped_column(DECIMAL(15, 2), nullable=True)
    schedule_offered: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    item_number_schedule: Mapped[str] = mapped_column(String, nullable=True)
    
    comment: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    
    is_mutual_fund: Mapped[Optional[bool]] = mapped_column(Boolean, nullable=True)
    
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=True,server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, nullable=True,server_default=func.now(),onupdate=func.now())
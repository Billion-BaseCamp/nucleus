from nucleus.db.database import Base
from sqlalchemy import String, ForeignKey, UUID as SQLUUID, Integer, Boolean, DECIMAL, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Optional
from uuid import UUID, uuid4
from datetime import datetime
from decimal import Decimal


class ForeignDepositCustodialAccounts(Base):
    __tablename__ = "foreign_deposit_custodial_accounts"

    id: Mapped[UUID] = mapped_column(SQLUUID(as_uuid=True), primary_key=True, default=uuid4, index=True)

    financial_year_id: Mapped[Optional[UUID]] = mapped_column(SQLUUID(as_uuid=True), ForeignKey("financial_years.id", ondelete="CASCADE"), nullable=True, index=True)
    
    financial_year: Mapped[Optional["FinancialYear"]] = relationship("FinancialYear")
    # Serial number
    sl_no: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)

    # Account type and details
    account_type: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    
    account_number: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    # Account status flags
    account_opened_during_tax_year: Mapped[Optional[bool]] = mapped_column(Boolean, nullable=True, default=False)
    
    account_closed_during_tax_year: Mapped[Optional[bool]] = mapped_column(Boolean, nullable=True, default=False)
    
    account_jointly_owned_with_spouse: Mapped[Optional[bool]] = mapped_column(Boolean, nullable=True, default=False)
    
    no_tax_item_reported: Mapped[Optional[bool]] = mapped_column(Boolean, nullable=True, default=False)
    # Account value
    maximum_value_during_tax_year: Mapped[Optional[Decimal]] = mapped_column(DECIMAL(15, 2), nullable=True)
    # Currency and exchange rate details
    used_foreign_currency_exchange_rate: Mapped[Optional[bool]] = mapped_column(Boolean, nullable=True, default=False)
    
    foreign_currency: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    
    exchange_rate: Mapped[Optional[Decimal]] = mapped_column(DECIMAL(15, 6), nullable=True)
    
    exchange_rate_source:    Mapped[Optional[str]] = mapped_column(String, nullable=True)
    # Institution details
    name_of_financial_institution: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    
    giin: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    # Address details
    mailing_address: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    
    city_state_country_zip: Mapped[Optional[str]] = mapped_column(String, nullable=True)

    hash_key: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    # Timestamps
    created_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True, server_default=func.now())
    
    updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True, server_default=func.now(), onupdate=func.now())


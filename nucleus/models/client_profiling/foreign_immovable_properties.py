from nucleus.db.database import Base
from sqlalchemy import BigInteger, String, DateTime, ForeignKey,func,Date,DECIMAL, UUID as SQLUUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime, date
from decimal import Decimal
from typing import Optional
from uuid import UUID, uuid4


class ForeignImmovableProperties(Base):
    __tablename__ = "foreign_immovable_properties"

    id: Mapped[UUID] = mapped_column(SQLUUID(as_uuid=True), primary_key=True, default=uuid4, index=True)

    financial_year_id: Mapped[Optional[UUID]] = mapped_column(SQLUUID(as_uuid=True), ForeignKey("financial_years.id", ondelete="CASCADE"),nullable=True,index=True)
    financial_year: Mapped[Optional["FinancialYear"]] = relationship("FinancialYear")

    #country details
    country_id: Mapped[Optional[UUID]] = mapped_column(SQLUUID(as_uuid=True), ForeignKey("country_lookup.id"),nullable=True,index=True)
    country: Mapped[Optional["CountryLookup"]] = relationship("CountryLookup", back_populates="foreign_immovable_properties")

    zip_code: Mapped[str] = mapped_column(String, nullable=True)

    #property details
    address_of_property: Mapped[str] = mapped_column(String, nullable=True)

    ownership_details: Mapped[str] = mapped_column(String, nullable=True)

    date_of_acquisition: Mapped[date] = mapped_column(Date, nullable=True)

    total_investment: Mapped[Decimal] = mapped_column(DECIMAL(15, 2), nullable=True)

    income_derived_from_property: Mapped[Decimal] = mapped_column(DECIMAL(15, 2), nullable=True)

    nature_of_income: Mapped[str] = mapped_column(String, nullable=True)

    income_taxable_amount: Mapped[Decimal] = mapped_column(DECIMAL(15, 2), nullable=True)

    schedule_offered: Mapped[Optional[str]] = mapped_column(String, nullable=True)

    item_number_schedule: Mapped[str] = mapped_column(String, nullable=True)

    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=True,server_default=func.now())

    updated_at: Mapped[datetime] = mapped_column(DateTime, nullable=True,server_default=func.now(),onupdate=func.now())


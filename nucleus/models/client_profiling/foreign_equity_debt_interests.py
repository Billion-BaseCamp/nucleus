from nucleus.db.database import Base
from sqlalchemy import BigInteger, String, DateTime, ForeignKey,func,Date,DECIMAL, UUID as SQLUUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime, date
from decimal import Decimal
from typing import Optional
from uuid import UUID, uuid4



class ForeignEquityDebtInterests(Base):
    __tablename__ = "foreign_equity_debt_interests"

    id: Mapped[UUID] = mapped_column(SQLUUID(as_uuid=True), primary_key=True, default=uuid4, index=True)

    financial_year_id: Mapped[Optional[UUID]] = mapped_column(SQLUUID(as_uuid=True), ForeignKey("financial_years.id", ondelete="CASCADE"),nullable=True,index=True)
    financial_year: Mapped[Optional["FinancialYear"]] = relationship("FinancialYear")

    #country details
    country_id: Mapped[Optional[UUID]] = mapped_column(SQLUUID(as_uuid=True), ForeignKey("country_lookup.id"),nullable=True,index=True)
    country: Mapped[Optional["CountryLookup"]] = relationship("CountryLookup", back_populates="foreign_equity_debt_interests")

    #institution details
    name_of_entity: Mapped[str] = mapped_column(String, nullable=True)

    address_of_entity: Mapped[str] = mapped_column(String, nullable=True)

    zip_code: Mapped[str] = mapped_column(String, nullable=True)

    nature_of_entity: Mapped[str] = mapped_column(String, nullable=True)

    date_of_acquiring_the_interest: Mapped[date] = mapped_column(Date, nullable=True)

    initial_value_of_interest: Mapped[Decimal] = mapped_column(DECIMAL(15, 2), nullable=True)

    peak_value_of_investment: Mapped[Decimal] = mapped_column(DECIMAL(15, 2), nullable=True)

    closing_value_of_investment: Mapped[Decimal] = mapped_column(DECIMAL(15, 2), nullable=True)

    gross_interest: Mapped[Decimal] = mapped_column(DECIMAL(15, 2), nullable=True)

    total_gross_sale_proceeds: Mapped[Decimal] = mapped_column(DECIMAL(15, 2), nullable=True)

    comment: Mapped[Optional[str]] = mapped_column(String, nullable=True)
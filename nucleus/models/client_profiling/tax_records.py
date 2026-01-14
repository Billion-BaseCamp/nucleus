from sqlalchemy import BigInteger, String, DateTime, ForeignKey,func,Boolean, UUID as SQLUUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from nucleus.db.database import Base
from datetime import datetime
from uuid import UUID, uuid4

# Tax Records Schema
# while creating the schema make sure to use the enum values for the jurisdiction
class TaxRecords(Base):
    __tablename__ = "tax_records"
    id: Mapped[UUID] = mapped_column(SQLUUID(as_uuid=True), primary_key=True, default=uuid4, index=True)

    financial_year_id: Mapped[UUID] = mapped_column(SQLUUID(as_uuid=True), ForeignKey("financial_years.id", ondelete="CASCADE"),nullable=True,index=True)
    financial_year: Mapped["FinancialYear"] = relationship("FinancialYear")

    jurisdiction:Mapped[str] = mapped_column(String, nullable=True)

    last_three_returns_filed:Mapped[bool] = mapped_column(Boolean, nullable=True)

    advanced_tax_paid:Mapped[bool] = mapped_column(Boolean, nullable=True)

    filing_portal_credentials:Mapped[str] = mapped_column(String, nullable=True)

    outstanding_issues:Mapped[str] = mapped_column(String, nullable=True)

    foreign_asset_reporting_india:Mapped[bool] = mapped_column(Boolean, nullable=True)

    foreign_asset_reporting_global:Mapped[bool] = mapped_column(Boolean, nullable=True)

    notes:Mapped[str] = mapped_column(String, nullable=True)

    created_at:Mapped[datetime] = mapped_column(DateTime, nullable=True,server_default=func.now())

    updated_at:Mapped[datetime] = mapped_column(DateTime, nullable=True,server_default=func.now(),onupdate=func.now())
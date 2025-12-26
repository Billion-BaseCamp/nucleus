from nucleus.db.database import Base
from sqlalchemy import BigInteger, String, DateTime, ForeignKey,DECIMAL,func, UUID as SQLUUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from uuid import UUID, uuid4



# Income Schema 
# while creating the schema make sure to use the enum values for the income type, currency, frequency, holder type
class income(Base):
    __tablename__ = "incomes"
    id: Mapped[UUID] = mapped_column(SQLUUID(as_uuid=True), primary_key=True, default=uuid4, index=True)

    financial_year_id: Mapped[UUID] = mapped_column(SQLUUID(as_uuid=True), ForeignKey("financial_years.id"),nullable=True,index=True)
    financial_year: Mapped["FinancialYear"] = relationship("FinancialYear")

    income_type:Mapped[str] = mapped_column(String, nullable=True)

    description:Mapped[str] = mapped_column(String, nullable=True)

    currency:Mapped[str] = mapped_column(String, nullable=True)

    gross_amount:Mapped[float] = mapped_column(DECIMAL(15, 2), nullable=True)

    frequency:Mapped[str] = mapped_column(String, nullable=True)

    holder_type:Mapped[str] = mapped_column(String, nullable=True)

    created_at:Mapped[datetime] = mapped_column(DateTime, nullable=True,server_default=func.now())

    updated_at:Mapped[datetime] = mapped_column(DateTime, nullable=True,server_default=func.now(),onupdate=func.now())
from sqlalchemy import String, DateTime, ForeignKey, UUID as SQLUUID, Float
from nucleus.db.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from uuid import UUID, uuid4
from sqlalchemy.sql import func
from datetime import datetime
from decimal import Decimal
from sqlalchemy.types import Numeric



class Employer(Base):
    __tablename__ = "employers"
    id: Mapped[UUID] = mapped_column(SQLUUID(as_uuid=True), primary_key=True, default=uuid4, index=True)
    financial_year_id: Mapped[UUID] = mapped_column(SQLUUID(as_uuid=True), ForeignKey("financial_years.id", ondelete="CASCADE"), nullable=False)
    employer_name: Mapped[str] = mapped_column(String, nullable=False)
    gross_salary: Mapped[Float] = mapped_column(Numeric[Decimal](18,2), default=0,nullable=True)
    income_under_the_head_salary: Mapped[Float] = mapped_column(Numeric[Decimal](18,2), default=0,nullable=True)
    basic_salary: Mapped[Float] = mapped_column(Numeric[Decimal](18,2), default=0,nullable=True)
    employer_contribution_to_pf: Mapped[Float] = mapped_column(Numeric[Decimal](18,2), default=0,nullable=True)
    employer_contribution_to_nps: Mapped[Float] = mapped_column(Numeric[Decimal](18,2), default=0,nullable=True)
    standard_deduction: Mapped[Float] = mapped_column(Numeric[Decimal](18,2), default=0,nullable=True)
    professional_tax:Mapped[Float] = mapped_column(Numeric[Decimal](18,2), default=0,nullable=True)  # not more than 2500
    employer_contribution_to_pf_percentage:Mapped[Float] = mapped_column(Numeric[Decimal](18,2), default=0,nullable=True)
    gratuity:Mapped[Float] = mapped_column(Numeric[Decimal](18,2), default=0,nullable=True)
    leave_encashment:Mapped[Float] = mapped_column(Numeric[Decimal](18,2), default=0,nullable=True)
    hra:Mapped[Float] = mapped_column(Numeric[Decimal](18,2), default=0,nullable=True)
    other_allowances:Mapped[Float] = mapped_column(Numeric[Decimal](18,2), default=0,nullable=True)
    tds: Mapped[Float] = mapped_column(Numeric[Decimal](18,2), default=0,nullable=True)

    # Relationships (string-based to avoid circular imports)
    financial_year: Mapped["FinancialYear"] = relationship("FinancialYear", back_populates="employers")

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), onupdate=func.now(), nullable=True)



#





#1 sum of gross salary
#2 sum of all (gratuity+leave_encashment)
#3 sum of all standard deduction (not more than 750000)
#4  sum of all professional tax (not more than 3200)
#5 income under head salary max((1-2-3-4),0))
#6 nps deduction Min(sum of all nps,14% of all basic salary)
#7 net salary=Max((5-6),0)
#tds sum all of tds




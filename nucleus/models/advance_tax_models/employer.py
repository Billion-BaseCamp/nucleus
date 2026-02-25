from sqlalchemy import String, DateTime, ForeignKey, UUID as SQLUUID, Float
from nucleus.db.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from uuid import UUID, uuid4
from sqlalchemy.sql import func
from datetime import datetime

from nucleus.models.advance_tax_models import financial_year


class Employer(Base):
    __tablename__ = "employers"
    id: Mapped[UUID] = mapped_column(SQLUUID(as_uuid=True), primary_key=True, default=uuid4, index=True)
    financial_year_id: Mapped[UUID] = mapped_column(SQLUUID(as_uuid=True), ForeignKey("tax_profile.id", ondelete="CASCADE"), nullable=False)
    employer_name: Mapped[str] = mapped_column(String, nullable=False)
    income_under_the_head_salary: Mapped[float] = mapped_column(Float, nullable=False)
    basic_salary: Mapped[float] = mapped_column(Float, nullable=False)
    employer_contribution_to_pf: Mapped[float] = mapped_column(Float, nullable=False)
    employer_contribution_to_nps: Mapped[float] = mapped_column(Float, nullable=False)

    # Relationships
    financial_year: Mapped["FinancialYear"] = relationship("FinancialYear", back_populates="employers")

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), onupdate=func.now(), nullable=True)


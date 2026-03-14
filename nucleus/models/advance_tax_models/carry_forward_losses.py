from sqlalchemy import ForeignKey, UUID as SQLUUID, Date, Numeric
from uuid import UUID, uuid4
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from datetime import date
from nucleus.db.database import Base


class CarryForwardLosses(Base):
    __tablename__ = "carry_forward_losses"
    id: Mapped[UUID] = mapped_column(SQLUUID(as_uuid=True), primary_key=True, default=uuid4, index=True)
    
    # Foreign keys
    financial_year_id: Mapped[UUID] = mapped_column(SQLUUID(as_uuid=True), ForeignKey("financial_years.id", ondelete="CASCADE"), nullable=False)

    date_of_loss: Mapped[date] = mapped_column(Date, nullable=False)
    short_term_loss_brought_forward: Mapped[float] = mapped_column(Numeric(18, 2), nullable=True)
    long_term_loss_brought_forward: Mapped[float] = mapped_column(Numeric(18, 2), nullable=True)
    housing_loan_loss_brought_forward: Mapped[float] = mapped_column(Numeric(18, 2), nullable=True)
    other_source_loss_brought_forward: Mapped[float] = mapped_column(Numeric(18, 2), nullable=True)

    # Relationships
    financial_year: Mapped["FinancialYear"] = relationship("FinancialYear", back_populates="carry_forward_losses")


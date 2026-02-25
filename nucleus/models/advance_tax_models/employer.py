from sqlalchemy import String, DateTime, ForeignKey, UUID as SQLUUID, Float
from nucleus.db.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from uuid import UUID, uuid4
from sqlalchemy.sql import func
from datetime import datetime


class Employer(Base):
    __tablename__ = "employers"
    id: Mapped[UUID] = mapped_column(SQLUUID(as_uuid=True), primary_key=True, default=uuid4, index=True)
    tax_profile_id: Mapped[UUID] = mapped_column(SQLUUID(as_uuid=True), ForeignKey("tax_profiles.id", ondelete="CASCADE"), nullable=False)
    employer_name: Mapped[str] = mapped_column(String, nullable=False)
    income_under_the_head_salary: Mapped[float] = mapped_column(Float, nullable=False)
    basic_salary: Mapped[float] = mapped_column(Float, nullable=False)
    employer_contribution_to_pf: Mapped[float] = mapped_column(Float, nullable=False)
    employer_contribution_to_nps: Mapped[float] = mapped_column(Float, nullable=False)

    # Relationships
    tax_profile: Mapped["TaxProfile"] = relationship("TaxProfile", back_populates="employers")

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), onupdate=func.now(), nullable=True)


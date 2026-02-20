import json
from typing import Dict
from sqlalchemy import String, DateTime, Float, ForeignKey, UUID as SQLUUID, Boolean, text
from sqlalchemy.dialects.postgresql import JSONB
from uuid import UUID, uuid4
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from datetime import datetime
from nucleus.db.database import Base
from typing import Dict

class TaxProfile(Base):
    __tablename__ = "tax_profile"
    id: Mapped[UUID] = mapped_column(SQLUUID(as_uuid=True), primary_key=True, default=uuid4, index=True)
    
    # Foreign keys
    financial_year_id: Mapped[UUID] = mapped_column(SQLUUID(as_uuid=True), ForeignKey("financial_years.id", ondelete="CASCADE"), nullable=False)
    client_id: Mapped[UUID] = mapped_column(SQLUUID(as_uuid=True), ForeignKey("clients.id", ondelete="CASCADE"), nullable=False)
    
    expected_current_year_income: Mapped[float] = mapped_column(Float, nullable=False)
    tax_rate: Mapped[float] = mapped_column(Float, nullable=False)
    advance_tax_paid_Q1: Mapped[float] = mapped_column(Float, nullable=True)
    advance_tax_paid_Q2: Mapped[float] = mapped_column(Float, nullable=True)
    advance_tax_paid_Q3: Mapped[float] = mapped_column(Float, nullable=True)
    advance_tax_paid_Q4: Mapped[float] = mapped_column(Float, nullable=True)
    gross_salary: Mapped[Dict[str, float]] = mapped_column(JSONB, nullable=True)
    tds: Mapped[Dict[str, float]] = mapped_column(JSONB, nullable=True)
    is_india_tax_payer: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False, server_default=text('false'))
    is_us_tax_payer: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False, server_default=text('false'))

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), onupdate=func.now(), nullable=True)

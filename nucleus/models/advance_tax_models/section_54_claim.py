from __future__ import annotations

from datetime import date, datetime
from uuid import UUID, uuid4

from sqlalchemy import Date, DateTime, Numeric, String, UUID as SQLUUID
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func

from nucleus.db.database import Base


class Section54Claim(Base):
    __tablename__ = "section_54_claim"

    id: Mapped[UUID] = mapped_column(SQLUUID(as_uuid=True), primary_key=True, default=uuid4)


    #cost of property
    agreement_value: Mapped[float] = mapped_column(Numeric(18,2), default=0, nullable=True)
    stamp_duty: Mapped[float] = mapped_column(Numeric(18,2), default=0, nullable=True)
    registration: Mapped[float] = mapped_column(Numeric(18,2), default=0, nullable=True)
    gst: Mapped[float] = mapped_column(Numeric(18,2), default=0, nullable=True)


    #additional costs
    cost_of_improvement: Mapped[float] = mapped_column(Numeric(18,2), default=0, nullable=True)
    broker_commission: Mapped[float] = mapped_column(Numeric(18,2), default=0, nullable=True)
    travel_expenses: Mapped[float] = mapped_column(Numeric(18,2), default=0, nullable=True)
    legal_fees: Mapped[float] = mapped_column(Numeric(18,2), default=0, nullable=True)
    carry_forward_loan_interest: Mapped[float] = mapped_column(Numeric(18,2), default=0, nullable=True)

    #cost of property===> agreement value + stamp duty + registration + gst+ additional costs
    cost_of_property: Mapped[float] = mapped_column(Numeric(18,2), default=0, nullable=True)
    
    #sale value of property===> cost of property + additional costs-expenses on sale of property
    sale_value_of_property: Mapped[float] = mapped_column(Numeric(18,2), default=0, nullable=True)
   
   #expenses on sale of property
    expenses_brokerage: Mapped[float] = mapped_column(Numeric(18,2), default=0, nullable=True)
    expenses_legal: Mapped[float] = mapped_column(Numeric(18,2), default=0, nullable=True)
    expenses_travel: Mapped[float] = mapped_column(Numeric(18,2), default=0, nullable=True)

    date_of_acquisition: Mapped[date] = mapped_column(Date, nullable=True)
    type_of_acquisition: Mapped[str] = mapped_column(String, nullable=True)

    #normal gain===> sale value of property - cost of property
    normal_gain: Mapped[float] = mapped_column(Numeric(18,2), default=0, nullable=True)

    #indexed gain===> normal gain * indexation factor
    indexed_gain: Mapped[float] = mapped_column(Numeric(18,2), default=0, nullable=True)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), onupdate=func.now(), nullable=True)

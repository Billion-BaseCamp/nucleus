from __future__ import annotations

from datetime import date, datetime
from uuid import UUID, uuid4

from sqlalchemy import Date, DateTime, Numeric, UniqueConstraint, UUID as SQLUUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from nucleus.db.database import Base



class Section54FClaim(Base):

    __tablename__ = "section_54f_claim"

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
    

    registration_date: Mapped[date] = mapped_column(Date, nullable=True)
    allocation_date: Mapped[date] = mapped_column(Date, nullable=True)
    booking_date: Mapped[date] = mapped_column(Date, nullable=True)

    #normal gain===> cost of property - sale value of property
    normal_gain: Mapped[float] = mapped_column(Numeric(18,2), default=0, nullable=True)

    #indexed gain===> normal gain * indexation factor
    indexed_gain: Mapped[float] = mapped_column(Numeric(18,2), default=0, nullable=True)

    # One Section54FClaim can have multiple Section54FAssets (one-to-many; FK on child only)
    section_54f_assets: Mapped[list["Section54FAssets"]] = relationship(
        "Section54FAssets",
        back_populates="section_54f_claim",
        cascade="all, delete-orphan",
    )

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), onupdate=func.now(), nullable=True)


from nucleus.db.database import Base
from sqlalchemy import (
    String,
    Date,
    DateTime,
    Boolean,
    ForeignKey,
    DECIMAL,
    Integer,
    func,
    UUID as SQLUUID,
    Text,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime, date
from uuid import UUID, uuid4
from nucleus.models.common_models.client import Client
from sqlalchemy import text
from enum import Enum as PyEnum


class RealEstate(Base):
    __tablename__ = "real_estate"

    id: Mapped[UUID] = mapped_column(
        SQLUUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
        index=True,
    )

    client_id: Mapped[UUID] = mapped_column(
        SQLUUID(as_uuid=True),
        ForeignKey("clients.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    client: Mapped["Client"] = relationship("Client", back_populates="real_estate")

    property_type: Mapped[str] = mapped_column(
        String,
        nullable=True
    )

    estimated_value: Mapped[float] = mapped_column(
        DECIMAL(15, 2),
        nullable=True,
    )

    cost_of_acquisition: Mapped[float] = mapped_column(
        DECIMAL(15, 2),
        nullable=True,
    )

    year_of_acquisition: Mapped[int] = mapped_column(
        Integer,
        nullable=True,
    )

    owners:Mapped[int] = mapped_column(
        Integer,
        nullable=True,
    )

    state:Mapped[str] = mapped_column(
        String,
        nullable=True,
    )

    country:Mapped[str] = mapped_column(
        String,
        nullable=True,
    )

    loan_closed:Mapped[bool] = mapped_column(
        Boolean,
        nullable=True,
    )

    loan_attached:Mapped[bool] = mapped_column(
        Boolean,
        nullable=True,
    )

    loan_starting_date:Mapped[date] = mapped_column(
        Date,
        nullable=True,
    )

    outStanding_loan_amount:Mapped[float] = mapped_column(
        DECIMAL(15, 2),
        nullable=True,
    )

    interest_rate:Mapped[float] = mapped_column(
        DECIMAL(15, 2),
        nullable=True,
    )

    emi_amount:Mapped[float] = mapped_column(
        DECIMAL(15, 2),
        nullable=True,
    )

    rent_amount:Mapped[float] = mapped_column(
        DECIMAL(15, 2),
        nullable=True,
    )

    property_tax_amount:Mapped[float] = mapped_column(
        DECIMAL(15, 2),
        nullable=True,
    )

    insured:Mapped[bool] = mapped_column(
        Boolean,
        nullable=True,
        default=False,
        server_default="false",
    )

    insured_details:Mapped[str] = mapped_column(
        Text,
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True),onupdate=func.now(), nullable=True)
    
    
    

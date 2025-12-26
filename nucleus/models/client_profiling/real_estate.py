from nucleus.db.database import Base
from sqlalchemy import (
    BigInteger,
    String,
    Text,
    Date,
    DateTime,
    Boolean,
    ForeignKey,
    DECIMAL,
    func,
    UUID as SQLUUID,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime, date
from uuid import UUID, uuid4


class RealEstate(Base):
    __tablename__ = "real_estate"

    id: Mapped[UUID] = mapped_column(
        SQLUUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
        index=True,
    )

    financial_year_id: Mapped[UUID] = mapped_column(
        SQLUUID(as_uuid=True),
        ForeignKey("financial_years.id"),
        nullable=False,
        index=True,
    )
    financial_year: Mapped["FinancialYear"] = relationship("FinancialYear")

    usage_type: Mapped[str] = mapped_column(
        String,
        nullable=False,
    )

    details: Mapped[str] = mapped_column(
        Text,
        nullable=True,
    )

    market_value: Mapped[float] = mapped_column(
        DECIMAL(15, 2),
        nullable=True,
    )

    cost_of_acquisition: Mapped[float] = mapped_column(
        DECIMAL(15, 2),
        nullable=True,
    )

    owners: Mapped[str] = mapped_column(
        Text,
        nullable=True,
    )

    state_country: Mapped[str] = mapped_column(
        String(255),
        nullable=True,
    )

    loan_attached: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        server_default=func.now(),
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),    

    )
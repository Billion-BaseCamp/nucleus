from sqlalchemy import Date
from nucleus.db.database import Base
from sqlalchemy import BigInteger, Text, DateTime, ForeignKey,DECIMAL,func,String, UUID as SQLUUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from uuid import UUID, uuid4


class RSUVesting(Base):
    __tablename__ = "rsu_vesting"

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

    vesting_date: Mapped[datetime.date] = mapped_column(
        Date,
        nullable=False,
    )

    # Stored as VARCHAR, validated via Currency enum
    currency: Mapped[str] = mapped_column(
        String,
        nullable=False,
    )

    amount: Mapped[float] = mapped_column(
        DECIMAL(15, 2),
        nullable=False,
    )

    description: Mapped[str] = mapped_column(
        Text,
        nullable=True,
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

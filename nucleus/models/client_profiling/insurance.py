from nucleus.db.database import Base
from sqlalchemy import (
    BigInteger,
    String,
    Text,
    Date,
    DateTime,
    Boolean,
    ForeignKey,
    Integer,
    DECIMAL,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime, date
from uuid import UUID, uuid4
from sqlalchemy import UUID as SQLUUID


class Insurance(Base):
    __tablename__ = "insurance"

    id: Mapped[UUID] = mapped_column(
        SQLUUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
        index=True,
    )

    client_profile_id: Mapped[UUID] = mapped_column(SQLUUID(as_uuid=True), ForeignKey("client_profiles.id", ondelete="CASCADE"), nullable=False)

    # Stored as VARCHAR, validated via InsuranceCategory enum
    category: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
    )

    sum_assured: Mapped[float] = mapped_column(
        DECIMAL(15, 2),
        nullable=True,
    )

    premium_amount: Mapped[float] = mapped_column(
        DECIMAL(15, 2),
        nullable=True,
    )

    frequency: Mapped[str] = mapped_column(
        String(50),   # Monthly / Quarterly / Annual etc.
        nullable=True,
    )

    start_date: Mapped[date] = mapped_column(
        Date,
        nullable=True,
    )

    end_date: Mapped[date] = mapped_column(
        Date,
        nullable=True,
    )

    tenure_months: Mapped[int] = mapped_column(
        Integer,
        nullable=True,
    )

    annuity_plan: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
    )

    annuity_receivable: Mapped[float] = mapped_column(
        DECIMAL(15, 2),
        nullable=True,
    )

    annuity_start_date: Mapped[date] = mapped_column(
        Date,
        nullable=True,
    )

    annuity_end_date: Mapped[date] = mapped_column(
        Date,
        nullable=True,
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

from nucleus.db.database import Base
from sqlalchemy import (
    BigInteger,
    String,
    Text,
    Date,
    DateTime,
    ForeignKey,
    Integer,
    DECIMAL,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime, date
from uuid import UUID, uuid4
from sqlalchemy import UUID as SQLUUID


class LoanRecord(Base):
    __tablename__ = "loan_records"

    id: Mapped[UUID] = mapped_column(
        SQLUUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
        index=True,
    )

    client_profile_id: Mapped[UUID] = mapped_column(SQLUUID(as_uuid=True), ForeignKey("client_profiles.id", ondelete="CASCADE"), nullable=False)

    # Stored as VARCHAR, validated using LoanType enum in app layer
    loan_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    lender_issuer: Mapped[str] = mapped_column(
        String(255),
        nullable=True,
    )

    principal_outstanding: Mapped[float] = mapped_column(
        DECIMAL(15, 2),
        nullable=True,
    )

    interest_rate: Mapped[float] = mapped_column(
        DECIMAL(5, 2),   # e.g. 9.25
        nullable=True,
    )

    emi: Mapped[float] = mapped_column(
        DECIMAL(15, 2),
        nullable=True,
    )

    owner: Mapped[str] = mapped_column(
        String(255),
        nullable=True,
    )

    notes: Mapped[str] = mapped_column(
        Text,
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

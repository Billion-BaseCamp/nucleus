from nucleus.db.database import Base
from sqlalchemy import (
    BigInteger,
    String,
    Text,
    DateTime,
    ForeignKey,
    Integer,
    DECIMAL,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
from uuid import UUID, uuid4
from sqlalchemy import UUID as SQLUUID


class OtherLoan(Base):
    __tablename__ = "other_loans"

    id: Mapped[UUID] = mapped_column(
        SQLUUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
        index=True,
    )

    client_id: Mapped[UUID] = mapped_column(SQLUUID(as_uuid=True), ForeignKey("clients.id"), nullable=False)

    # Stored as VARCHAR, validated via LoanCategory enum
    category: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    principal_outstanding: Mapped[float] = mapped_column(
        DECIMAL(15, 2),
        nullable=True,
    )

    tenure_months: Mapped[int] = mapped_column(
        Integer,
        nullable=True,
    )

    rate_of_interest: Mapped[float] = mapped_column(
        DECIMAL(5, 2),
        nullable=True,
    )

    description: Mapped[str] = mapped_column(
        Text,
        nullable=True,
    )

    deposit_against_loan: Mapped[float] = mapped_column(
        DECIMAL(15, 2),
        nullable=True,
    )

    deposit_rate: Mapped[float] = mapped_column(
        DECIMAL(5, 2),
        nullable=True,
    )

    soa_line_item: Mapped[str] = mapped_column(
        String(255),
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

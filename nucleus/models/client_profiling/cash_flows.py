from nucleus.db.database import Base
from sqlalchemy import (
    BigInteger,
    String,
    DateTime,
    ForeignKey,
    DECIMAL,
    func,
    UUID as SQLUUID,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from uuid import UUID, uuid4


class CashFlow(Base):
    __tablename__ = "cash_flows"

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

    # Stored as VARCHAR, validated via enums
    period: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
    )

    flow_type: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
    )

    category: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    label: Mapped[str] = mapped_column(
        String(255),
        nullable=True,
    )

    amount: Mapped[float] = mapped_column(
        DECIMAL(15, 2),
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

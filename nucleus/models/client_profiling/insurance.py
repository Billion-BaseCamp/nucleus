from nucleus.db.database import Base
from sqlalchemy import (
    String,
    Date,
    DateTime,
    Boolean,
    ForeignKey,
    Integer,
    DECIMAL,
    func,
    Text
)
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime, date
from uuid import UUID, uuid4
from sqlalchemy import UUID as SQLUUID
from sqlalchemy.orm import relationship

class Insurance(Base):
    __tablename__ = "insurances"

    id: Mapped[UUID] = mapped_column(
        SQLUUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
        index=True,
    )

    client_id: Mapped[UUID] = mapped_column(SQLUUID(as_uuid=True), ForeignKey("clients.id", ondelete="CASCADE"), nullable=False)

    client: Mapped["Client"] = relationship("Client", back_populates="insurances")

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

    annuity_plan: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
    )

    annuity_receivable: Mapped[float] = mapped_column(
        DECIMAL(15, 2),
        nullable=True,
    )

    annuity_receivable_start_date: Mapped[date] = mapped_column(
        Date,
        nullable=True,
    )

    annuity_receivable_end_date: Mapped[date] = mapped_column(
        Date,
        nullable=True,
    )

    description: Mapped[str] = mapped_column(
        Text,
        nullable=True,
    )

    members_count: Mapped[int] = mapped_column(
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

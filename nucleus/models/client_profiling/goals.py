from nucleus.db.database import Base
from sqlalchemy import (
    BigInteger,
    String,
    Text,
    Date,
    DateTime,
    ForeignKey,
    DECIMAL,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime, date
from uuid import UUID, uuid4
from sqlalchemy import UUID as SQLUUID


class Goal(Base):
    __tablename__ = "goals"

    id: Mapped[UUID] = mapped_column(
        SQLUUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
        index=True,
    )

    client_profile_id: Mapped[UUID] = mapped_column(SQLUUID(as_uuid=True), ForeignKey("client_profiles.id", ondelete="CASCADE"), nullable=False)

    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    description: Mapped[str] = mapped_column(
        Text,
        nullable=True,
    )

    start_date: Mapped[date] = mapped_column(
        Date,
        nullable=True,
    )

    target_date: Mapped[date] = mapped_column(
        Date,
        nullable=True,
    )

    # Stored as VARCHAR, validated via Currency enum
    currency: Mapped[str] = mapped_column(
        String(10),
        nullable=False,
    )

    cost_at_pv: Mapped[float] = mapped_column(
        DECIMAL(15, 2),
        nullable=True,
    )

    cost_at_pv_inr: Mapped[float] = mapped_column(
        DECIMAL(15, 2),
        nullable=True,
    )

    # Stored as VARCHAR, validated via GoalTerm enum
    goal_term: Mapped[str] = mapped_column(
        String(20),
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

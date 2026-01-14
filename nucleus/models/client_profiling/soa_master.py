from nucleus.db.database import Base
from sqlalchemy import (
    BigInteger,
    String,
    Text,
    DateTime,
    ForeignKey,
    DECIMAL,
    func,
    UUID as SQLUUID,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from uuid import UUID, uuid4


class SOAMaster(Base):
    __tablename__ = "soa_master"

    id: Mapped[UUID] = mapped_column(
        SQLUUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
        index=True,
    )

    financial_year_id: Mapped[UUID] = mapped_column(
        SQLUUID(as_uuid=True),
        ForeignKey("financial_years.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    financial_year: Mapped["FinancialYear"] = relationship("FinancialYear")

    # Stored as VARCHAR, validated via AssetClass enum
    type: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    # Stored as VARCHAR, validated via AssetSubClass enum
    asset_class: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    allocation_self: Mapped[float] = mapped_column(
        DECIMAL(15, 2),
        nullable=True,
    )

    allocation_spouse: Mapped[float] = mapped_column(
        DECIMAL(15, 2),
        nullable=True,
    )

    allocation_parents: Mapped[float] = mapped_column(
        DECIMAL(15, 2),
        nullable=True,
    )

    total_self_spouse: Mapped[float] = mapped_column(
        DECIMAL(15, 2),
        nullable=True,
    )

    percent_within_type: Mapped[float] = mapped_column(
        DECIMAL(5, 2),   # e.g. 32.45 %
        nullable=True,
    )

    percent_overall: Mapped[float] = mapped_column(
        DECIMAL(5, 2),   # e.g. 12.30 %
        nullable=True,
    )

    notes: Mapped[str] = mapped_column(
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

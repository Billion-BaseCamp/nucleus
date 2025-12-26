from nucleus.db.database import Base
from sqlalchemy import BigInteger, Text, DateTime, ForeignKey,DECIMAL,func,String,Date,UUID as SQLUUID
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
from uuid import UUID, uuid4


class AssetWithMaturity(Base):
    __tablename__ = "assets_with_maturity"

    id: Mapped[UUID] = mapped_column(
        SQLUUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
        index=True,
    )

    client_id: Mapped[UUID] = mapped_column(SQLUUID(as_uuid=True), ForeignKey("clients.id"), nullable=False)

    details: Mapped[str] = mapped_column(
        Text,
        nullable=True,
    )

    maturity_value: Mapped[float] = mapped_column(
        DECIMAL(15, 2),
        nullable=True,
    )

    maturity_date: Mapped[datetime.date] = mapped_column(
        Date,
        nullable=True,
    )

    rate_of_interest: Mapped[float] = mapped_column(
        DECIMAL(5, 2),
        nullable=True,
    )

    amount_in_soa: Mapped[float] = mapped_column(
        DECIMAL(15, 2),
        nullable=True,
    )

    soa_line_item: Mapped[str] = mapped_column(
        String(255),
        nullable=True,
    )

    income_earned: Mapped[float] = mapped_column(
        DECIMAL(15, 2),
        nullable=True,
    )

    cashflow_frequency: Mapped[str] = mapped_column(
        String(50),   # Monthly / Quarterly / Annual
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

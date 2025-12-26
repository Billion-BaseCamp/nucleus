from nucleus.db.database import Base
from sqlalchemy import (
    BigInteger,
    String,
    DateTime,
    ForeignKey,
    Boolean,
    Integer,
    DECIMAL,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
from uuid import UUID, uuid4
from sqlalchemy import UUID as SQLUUID


class RealEstatePlan(Base):
    __tablename__ = "real_estate_plans"

    id: Mapped[UUID] = mapped_column(
        SQLUUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
        index=True,
    )

    client_id: Mapped[UUID] = mapped_column(SQLUUID(as_uuid=True), ForeignKey("clients.id"), nullable=False)

    property_name: Mapped[str] = mapped_column(
        String(255),
        nullable=True,
    )

    plan_to_sell: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
    )

    year_to_sell: Mapped[int] = mapped_column(
        Integer,
        nullable=True,
    )

    expected_value: Mapped[float] = mapped_column(
        DECIMAL(15, 2),
        nullable=True,
    )

    inheritance_share: Mapped[float] = mapped_column(
        DECIMAL(5, 2),   # percentage share
        nullable=True,
    )

    soa_line_item: Mapped[str] = mapped_column(
        String(255),
        nullable=True,
    )

    value_not_in_soa: Mapped[float] = mapped_column(
        DECIMAL(15, 2),
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

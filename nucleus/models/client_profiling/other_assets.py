from sqlalchemy import Date
from nucleus.db.database import Base
from sqlalchemy import BigInteger, Text, DateTime, ForeignKey,DECIMAL,func
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
from uuid import UUID, uuid4
from sqlalchemy import UUID as SQLUUID

class OtherAsset(Base):
    __tablename__ = "other_assets"

    id: Mapped[UUID] = mapped_column(
        SQLUUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
        index=True,
    )

    client_profile_id: Mapped[UUID] = mapped_column(SQLUUID(as_uuid=True), ForeignKey("client_profiles.id", ondelete="CASCADE"), nullable=False)

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

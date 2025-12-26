from sqlalchemy import Integer, String
from nucleus.db.database import Base
from sqlalchemy import BigInteger, Text, DateTime, ForeignKey,func
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
from uuid import UUID, uuid4

from sqlalchemy import UUID as SQLUUID


class ChildInfo(Base):
    __tablename__ = "children_info"

    id: Mapped[UUID] = mapped_column(
        SQLUUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
        index=True,
    )

    client_id: Mapped[UUID] = mapped_column(SQLUUID(as_uuid=True), ForeignKey("clients.id"), nullable=False)

    child_name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    current_age: Mapped[int] = mapped_column(
        Integer,
        nullable=True,
    )

    undergrad_goal: Mapped[str] = mapped_column(
        Text,
        nullable=True,
    )

    postgrad_goal: Mapped[str] = mapped_column(
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

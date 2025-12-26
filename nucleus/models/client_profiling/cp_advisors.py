from nucleus.db.database import Base
from sqlalchemy import (
    BigInteger,
    String,
    Text,
    DateTime,
    ForeignKey,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
from uuid import UUID, uuid4
from sqlalchemy import UUID as SQLUUID


class CPAdvisor(Base):
    __tablename__ = "cp_advisors"

    id: Mapped[UUID] = mapped_column(
        SQLUUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
        index=True,
    )

    client_id: Mapped[UUID] = mapped_column(SQLUUID(as_uuid=True), ForeignKey("clients.id"), nullable=False)

    # Stored as VARCHAR, validated using AdvisorType enum
    advisor_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    # Assuming Jurisdiction is an enum or lookup → store as string
    jurisdiction: Mapped[str] = mapped_column(
        String(100),
        nullable=True,
    )

    # Stored as VARCHAR, validated using ContactType enum
    contact_type: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
    )

    contact_value: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    relationship_timing: Mapped[str] = mapped_column(
        String(100),
        nullable=True,
    )

    expertise_area: Mapped[str] = mapped_column(
        String(255),
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

"""Stored prior-year return data extracted from XML for a client+tax_year."""

from __future__ import annotations

from datetime import datetime
from typing import Any
from uuid import UUID, uuid4

from sqlalchemy import UUID as SQLUUID
from sqlalchemy import DateTime, Integer, String, UniqueConstraint, func
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from nucleus.db.database import Base


class ClientPriorReturn(Base):
    __tablename__ = "client_prior_returns"
    __table_args__ = (
        UniqueConstraint(
            "client_email",
            "tax_year",
            name="uq_client_prior_return_email_year",
        ),
    )

    id: Mapped[UUID] = mapped_column(
        SQLUUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
    )
    client_email: Mapped[str] = mapped_column(String(255), nullable=False)
    tax_year: Mapped[int] = mapped_column(Integer, nullable=False)
    extracted_data: Mapped[dict[str, Any]] = mapped_column(
        JSONB,
        nullable=False,
    )
    source_filename: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        server_default=func.now(),
    )

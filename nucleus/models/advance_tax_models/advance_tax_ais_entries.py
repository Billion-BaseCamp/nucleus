"""Parsed AIS flat entries for advance-tax Numbers.

Raw file metadata stays on ``itr_ais_json_archives``. This table stores the
parse result (name / amount / tds / type) keyed by that archive.
"""

from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from typing import Optional
from uuid import UUID, uuid4

from sqlalchemy import DateTime, ForeignKey, Numeric, String, UUID as SQLUUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from nucleus.db.database import Base


class AdvanceTaxAisEntry(Base):
    """Flat AIS row from one ``ITRAisJsonArchive`` parse."""

    __tablename__ = "advance_tax_ais_entries"

    id: Mapped[UUID] = mapped_column(
        SQLUUID(as_uuid=True), primary_key=True, default=uuid4, index=True
    )
    archive_id: Mapped[UUID] = mapped_column(
        SQLUUID(as_uuid=True),
        ForeignKey("itr_ais_json_archives.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    client_id: Mapped[UUID] = mapped_column(
        SQLUUID(as_uuid=True),
        ForeignKey("clients.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    # Optional AT period filters when the same archive is used for a quarter view.
    financial_year_id: Mapped[Optional[UUID]] = mapped_column(
        SQLUUID(as_uuid=True),
        ForeignKey("financial_years.id", ondelete="CASCADE"),
        nullable=True,
        index=True,
    )
    quarter_id: Mapped[Optional[UUID]] = mapped_column(
        SQLUUID(as_uuid=True),
        ForeignKey("quarters.id", ondelete="CASCADE"),
        nullable=True,
        index=True,
    )

    name: Mapped[str] = mapped_column(String(512), nullable=False)
    amount: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False, default=0)
    tds: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False, default=0)
    # dividend | savings | fd | salary | salary_tds
    type: Mapped[str] = mapped_column(String(32), nullable=False, index=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), onupdate=func.now(), nullable=True
    )

    archive: Mapped["ITRAisJsonArchive"] = relationship(  # noqa: F821
        "ITRAisJsonArchive",
    )


__all__ = ["AdvanceTaxAisEntry"]

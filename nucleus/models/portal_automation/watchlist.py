"""Clients checked by the weekly e-Proceedings run.

Rows with a ``batch_id`` were chosen by that monthly run. The weekly run reads
only the latest monthly batch whose status is ``completed``, so a running or
failed month never replaces the previous list.

Rows without a ``batch_id`` were added by hand. They are not tied to a month
and stay until ``removed_at`` is set.

Generate the table with Alembic autogenerate. Do not hand-write the migration.
"""

from __future__ import annotations

from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4

from sqlalchemy import DateTime, ForeignKey, Index, Integer, String, Text, text
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func
from sqlalchemy.types import UUID as SQLUUID

from nucleus.db.database import Base

WATCH_REASON_ACTION_REQUIRED = "action_required"
WATCH_REASON_CARRIED_FORWARD = "carried_forward"
WATCH_REASON_MANUAL = "manual"


class EProceedingsWatchlist(Base):
    """One client on the weekly e-Proceedings list, for one month or by hand."""

    __tablename__ = "e_proceedings_watchlist"

    id: Mapped[UUID] = mapped_column(
        SQLUUID(as_uuid=True), primary_key=True, default=uuid4
    )
    batch_id: Mapped[Optional[UUID]] = mapped_column(
        SQLUUID(as_uuid=True),
        ForeignKey("portal_automation_batches.id", ondelete="CASCADE"),
        nullable=True,
        index=True,
    )
    client_id: Mapped[UUID] = mapped_column(
        SQLUUID(as_uuid=True),
        ForeignKey("clients.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    reason: Mapped[str] = mapped_column(String(32), nullable=False)
    action_required_count: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    job_id: Mapped[Optional[UUID]] = mapped_column(
        SQLUUID(as_uuid=True),
        ForeignKey("portal_automation_jobs.id", ondelete="SET NULL"),
        nullable=True,
    )

    added_by_sub: Mapped[Optional[str]] = mapped_column(String(128), nullable=True)
    note: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    removed_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    __table_args__ = (
        Index(
            "uq_e_proceedings_watchlist_batch_client",
            "batch_id",
            "client_id",
            unique=True,
            postgresql_where=text("batch_id IS NOT NULL"),
        ),
        Index(
            "uq_e_proceedings_watchlist_manual_client",
            "client_id",
            unique=True,
            postgresql_where=text("batch_id IS NULL AND removed_at IS NULL"),
        ),
    )

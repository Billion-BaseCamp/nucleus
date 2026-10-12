"""Clients checked by the weekly e-Proceedings run.

One live list, at most one active row per client:

- A completed e-Proceedings check (any trigger) with a notice needing action
  adds the client (``action_required``).
- Only a completed monthly check with nothing pending removes an
  ``action_required`` row. Weekly and hand-run checks never remove.
- An advisor or admin can add a client (``manual``) or remove any row.
  ``manual`` rows are never removed by a check.

Removing sets ``removed_at``; the row stays as history.

Generate the table with Alembic autogenerate. Do not hand-write the migration.
"""

from __future__ import annotations

from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4

from sqlalchemy import DateTime, ForeignKey, Index, String, text
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func
from sqlalchemy.types import UUID as SQLUUID

from nucleus.db.database import Base

WATCH_REASON_ACTION_REQUIRED = "action_required"
WATCH_REASON_MANUAL = "manual"


class EProceedingsWatchlist(Base):
    """One client on the weekly e-Proceedings list."""

    __tablename__ = "e_proceedings_watchlist"

    id: Mapped[UUID] = mapped_column(
        SQLUUID(as_uuid=True), primary_key=True, default=uuid4
    )
    client_id: Mapped[UUID] = mapped_column(
        SQLUUID(as_uuid=True),
        ForeignKey("clients.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    reason: Mapped[str] = mapped_column(String(32), nullable=False)
    job_id: Mapped[Optional[UUID]] = mapped_column(
        SQLUUID(as_uuid=True),
        ForeignKey("portal_automation_jobs.id", ondelete="SET NULL"),
        nullable=True,
    )
    added_by_sub: Mapped[Optional[str]] = mapped_column(String(128), nullable=True)
    removed_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    __table_args__ = (
        Index(
            "uq_e_proceedings_watchlist_active_client",
            "client_id",
            unique=True,
            postgresql_where=text("removed_at IS NULL"),
        ),
    )

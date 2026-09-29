"""AA job queue — Postgres-as-a-queue, same shape as ``portal_automation_jobs``.

That pattern is already proven in this codebase: claim with
``FOR UPDATE SKIP LOCKED``, a partial unique index to stop duplicate in-flight
work, and attempt counters for bounded retries. Reusing it means no new
infrastructure and no second queue semantics to learn.

``FI_REQUEST`` is built unconditionally even when Auto-FI is enabled on the
channel. Auto-FI only covers the *first* fetch of a periodic consent; every
later refresh still calls /FIRequest, so the path is never dead code.
"""

from __future__ import annotations

from datetime import datetime
from typing import Any, Optional
from uuid import UUID, uuid4

from sqlalchemy import (
    DateTime,
    ForeignKey,
    Index,
    Integer,
    String,
    Text,
    text,
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func
from sqlalchemy.types import UUID as SQLUUID

from nucleus.db.database import Base
from nucleus.models.account_aggregator.constants import JOB_QUEUED


class AAJob(Base):
    """A unit of AA background work claimed by the worker."""

    __tablename__ = "aa_jobs"

    id: Mapped[UUID] = mapped_column(
        SQLUUID(as_uuid=True), primary_key=True, default=uuid4, index=True
    )
    job_type: Mapped[str] = mapped_column(String(32), nullable=False, index=True)

    aa_consent_id: Mapped[UUID] = mapped_column(
        SQLUUID(as_uuid=True),
        ForeignKey("aa_consents.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    aa_fi_session_id: Mapped[Optional[UUID]] = mapped_column(
        SQLUUID(as_uuid=True),
        ForeignKey("aa_fi_sessions.id", ondelete="CASCADE"),
        nullable=True,
        index=True,
    )

    status: Mapped[str] = mapped_column(
        String(16), nullable=False, default=JOB_QUEUED, index=True
    )
    attempt: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    max_attempts: Mapped[int] = mapped_column(Integer, nullable=False, default=5)
    worker_id: Mapped[Optional[str]] = mapped_column(String(128), nullable=True)

    # Backoff target. The claim query filters on ``scheduled_for <= now()`` so a
    # failed job becomes invisible until its retry is due.
    scheduled_for: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    started_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    finished_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    # Heartbeat for stale-job detection; the sweeper re-queues rows whose worker
    # died mid-run.
    heartbeat_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    error_code: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    error_message: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    # Never store credentials or tokens here.
    payload: Mapped[dict[str, Any]] = mapped_column(JSONB, nullable=False, default=dict)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), onupdate=func.now(), nullable=True
    )

    __table_args__ = (
        # One in-flight job per (consent, type). Without this, a retried webhook
        # or an impatient admin clicking "re-fetch" enqueues duplicate work that
        # races against itself at the FIP.
        Index(
            "uix_aa_jobs_active_per_consent_type",
            "aa_consent_id",
            "job_type",
            unique=True,
            postgresql_where=text("status IN ('queued', 'running')"),
        ),
        # Supports the claim query: queued rows whose backoff has elapsed.
        Index(
            "ix_aa_jobs_claimable",
            "scheduled_for",
            postgresql_where=text("status = 'queued'"),
        ),
    )

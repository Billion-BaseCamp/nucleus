"""Reusable portal-automation jobs.

Postgres is the queue of record. Workers claim ``queued`` rows with
``FOR UPDATE SKIP LOCKED``. Workflows (CHECK_ITR_VERIFICATION, later
DOWNLOAD_ITR, …) share this table — they only differ by ``workflow``.

Active statuses keep a partial unique index so the same client + year +
workflow cannot run twice at once.
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

PORTAL_AUTOMATION_ACTIVE_STATUSES = (
    "queued",
    "running",
    "waiting_for_password",
    "waiting_for_otp",
    "waiting_for_human",
)


class PortalAutomationJob(Base):
    """One workflow execution for one client + assessment year."""

    __tablename__ = "portal_automation_jobs"

    id: Mapped[UUID] = mapped_column(
        SQLUUID(as_uuid=True), primary_key=True, default=uuid4, index=True
    )
    workflow: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
    client_id: Mapped[UUID] = mapped_column(
        SQLUUID(as_uuid=True),
        ForeignKey("clients.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    itr_return_id: Mapped[Optional[UUID]] = mapped_column(
        SQLUUID(as_uuid=True),
        ForeignKey("itr_returns.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    assessment_year: Mapped[str] = mapped_column(String(16), nullable=False)
    financial_year_id: Mapped[Optional[UUID]] = mapped_column(
        SQLUUID(as_uuid=True), nullable=True
    )

    # queued | running | waiting_for_password | waiting_for_otp |
    # waiting_for_human | completed | failed | timed_out | cancelled
    status: Mapped[str] = mapped_column(
        String(32), nullable=False, default="queued", server_default="queued", index=True
    )
    current_step: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    attempt: Mapped[int] = mapped_column(
        Integer, nullable=False, default=0, server_default="0"
    )
    worker_id: Mapped[Optional[str]] = mapped_column(String(128), nullable=True)
    idempotency_key: Mapped[Optional[str]] = mapped_column(
        String(256), nullable=True, index=True
    )

    result: Mapped[Optional[dict[str, Any]]] = mapped_column(JSONB, nullable=True)
    error_code: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    error_message: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    requested_by_sub: Mapped[Optional[str]] = mapped_column(String(128), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    started_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    waiting_since: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    completed_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    updated_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), onupdate=func.now(), nullable=True
    )

    __table_args__ = (
        Index(
            "uq_portal_automation_active_workflow_client_ay",
            "workflow",
            "client_id",
            "assessment_year",
            unique=True,
            postgresql_where=text(
                "status IN ("
                "'queued', 'running', 'waiting_for_password', "
                "'waiting_for_otp', 'waiting_for_human')"
            ),
        ),
        Index("ix_portal_automation_jobs_status_created", "status", "created_at"),
    )

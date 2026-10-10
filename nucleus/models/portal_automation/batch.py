"""One Excel/API bulk enqueue, or one scheduled notice run.

Ingest rows (including failures) live in ``items`` so Results survive reload.
Jobs point back via ``batch_id``.

Scheduled runs set ``run_type`` and ``status``. Excel/API batches leave both
null. Only one scheduled batch per workflow may be ``running`` at a time.

A run that never finishes would block every later run of its workflow, so the
consumer must fail ``running`` batches past a deadline, counted from
``started_at`` (cronjob-scheduler: the notice batch finalizer,
``NOTICE_BATCH_DEADLINE_HOURS``).

``assessment_year`` is required, but a scheduled notice run covers every year
on the portal; it stores the financial year label of the run date
(``notice_assessment_year``).
"""

from __future__ import annotations

from datetime import datetime
from typing import Any, Optional
from uuid import UUID, uuid4

from sqlalchemy import DateTime, Index, String, Text, text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func
from sqlalchemy.types import UUID as SQLUUID

from nucleus.db.database import Base

RUN_TYPE_E_PROCEEDINGS_MONTHLY = "e_proceedings_monthly"
RUN_TYPE_E_PROCEEDINGS_WEEKLY = "e_proceedings_weekly"
RUN_TYPE_OUTSTANDING_DEMAND_MONTHLY = "outstanding_demand_monthly"

BATCH_STATUS_RUNNING = "running"
BATCH_STATUS_COMPLETED = "completed"
BATCH_STATUS_FAILED = "failed"


class PortalAutomationBatch(Base):
    """Bulk ingest, or one scheduled run of a notice workflow."""

    __tablename__ = "portal_automation_batches"

    id: Mapped[UUID] = mapped_column(
        SQLUUID(as_uuid=True), primary_key=True, default=uuid4, index=True
    )
    workflow: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
    assessment_year: Mapped[str] = mapped_column(String(16), nullable=False)
    requested_by_sub: Mapped[Optional[str]] = mapped_column(
        String(128), nullable=True, index=True
    )
    # PAN, ingest_status, error_*, client_id, job_id — never passwords.
    items: Mapped[list[dict[str, Any]]] = mapped_column(
        JSONB, nullable=False, default=list
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    run_type: Mapped[Optional[str]] = mapped_column(String(32), nullable=True)
    status: Mapped[Optional[str]] = mapped_column(String(16), nullable=True)
    started_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    completed_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    # Job counts and the reason a run failed. Never client data.
    summary: Mapped[Optional[dict[str, Any]]] = mapped_column(JSONB, nullable=True)
    error_message: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    __table_args__ = (
        Index(
            "uq_portal_automation_batches_running_scheduled",
            "workflow",
            unique=True,
            postgresql_where=text("status = 'running' AND run_type IS NOT NULL"),
        ),
        Index(
            "ix_portal_automation_batches_run_type_status",
            "run_type",
            "status",
            "completed_at",
        ),
    )

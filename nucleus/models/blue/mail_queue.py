"""Delta-mail pipeline: bookmark, job queue, Graph subscription, webhook doorbell log.

Generate the tables with Alembic autogenerate. Do not hand-write the migration.
`blue_app` can insert and update these tables and cannot delete them, so finished
jobs are archived (status ``archived``) rather than removed.
"""

from __future__ import annotations

from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4

from sqlalchemy import CheckConstraint, DateTime, Index, Integer, String, Text, UniqueConstraint
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func
from sqlalchemy.types import UUID as SQLUUID

from nucleus.db.database import Base
from nucleus.models.blue.constants import (
    BLUE_JOB_STATUSES,
    BLUE_JOB_TYPES,
    BLUE_SUBSCRIPTION_STATUSES,
    check_in,
)


class BlueMailboxSyncState(Base):
    """Microsoft's delta bookmark for one intake mailbox."""

    __tablename__ = "blue_mailbox_sync_state"

    mailbox: Mapped[str] = mapped_column(String(320), primary_key=True)
    delta_link: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    last_success_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    last_error: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    throttle_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0, server_default="0")
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )


class BlueJob(Base):
    """One unit of mail work. Claimed with FOR UPDATE SKIP LOCKED."""

    __tablename__ = "blue_jobs"
    __table_args__ = (
        UniqueConstraint("idempotency_key", name="uq_blue_jobs_idempotency_key"),
        CheckConstraint(check_in("job_type", BLUE_JOB_TYPES), name="ck_blue_jobs_job_type"),
        CheckConstraint(check_in("status", BLUE_JOB_STATUSES), name="ck_blue_jobs_status"),
        Index("ix_blue_jobs_status_run_after", "status", "run_after"),
    )

    id: Mapped[UUID] = mapped_column(SQLUUID(as_uuid=True), primary_key=True, default=uuid4)
    job_type: Mapped[str] = mapped_column(String(32), nullable=False)
    payload: Mapped[dict] = mapped_column(JSONB, nullable=False, default=dict)
    idempotency_key: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[str] = mapped_column(String(16), nullable=False, default="pending", server_default="pending")
    attempts: Mapped[int] = mapped_column(Integer, nullable=False, default=0, server_default="0")
    max_attempts: Mapped[int] = mapped_column(Integer, nullable=False, default=3, server_default="3")
    run_after: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    locked_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    locked_by: Mapped[Optional[str]] = mapped_column(String(128), nullable=True)
    last_error: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)


class BlueGraphSubscription(Base):
    """One Graph change-notification subscription for one mailbox. The clientState secret is stored as a hash."""

    __tablename__ = "blue_graph_subscriptions"
    __table_args__ = (
        UniqueConstraint("subscription_id", name="uq_blue_graph_subscriptions_subscription_id"),
        CheckConstraint(check_in("status", BLUE_SUBSCRIPTION_STATUSES), name="ck_blue_graph_subscriptions_status"),
    )

    mailbox: Mapped[str] = mapped_column(String(320), primary_key=True)
    subscription_id: Mapped[Optional[str]] = mapped_column(String(128), nullable=True)
    expires_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    client_state_hash: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    status: Mapped[str] = mapped_column(String(16), nullable=False, default="failed", server_default="failed")
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)


class BlueWebhookEvent(Base):
    """A doorbell ring from Microsoft. The endpoint stores this and enqueues a sync; it does not read mail."""

    __tablename__ = "blue_webhook_events"
    __table_args__ = (
        Index("ix_blue_webhook_events_mailbox_message", "mailbox", "graph_message_id"),
    )

    id: Mapped[UUID] = mapped_column(SQLUUID(as_uuid=True), primary_key=True, default=uuid4)
    mailbox: Mapped[str] = mapped_column(String(320), nullable=False)
    subscription_id: Mapped[Optional[str]] = mapped_column(String(128), nullable=True)
    graph_message_id: Mapped[str] = mapped_column(Text, nullable=False)
    change_type: Mapped[Optional[str]] = mapped_column(String(32), nullable=True)
    received_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)

"""Audit log and RM identity mapping."""

from __future__ import annotations

from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4

from sqlalchemy import BigInteger, DateTime, ForeignKey, Index, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func
from sqlalchemy.types import UUID as SQLUUID

from nucleus.db.database import Base


class BlueEvent(Base):
    """Append-only: everything BLUE did or was told to do. Answers "why is this X?"."""

    __tablename__ = "blue_events"
    __table_args__ = (
        Index("ix_blue_events_client_created", "client_id", "created_at"),
        Index("ix_blue_events_subject", "subject_type", "subject_id"),
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    # "blue" for the agent, "advisor" for an RM action, "system" for intake.
    actor_type: Mapped[str] = mapped_column(String(16), nullable=False)
    actor_advisor_id: Mapped[Optional[UUID]] = mapped_column(
        SQLUUID(as_uuid=True), ForeignKey("advisors.id", ondelete="SET NULL"), nullable=True
    )
    # e.g. message.received, document.matched, extraction.succeeded, email.sent, writeback.applied
    event: Mapped[str] = mapped_column(String(64), nullable=False)
    client_id: Mapped[Optional[UUID]] = mapped_column(
        SQLUUID(as_uuid=True), ForeignKey("clients.id", ondelete="SET NULL"), nullable=True
    )
    subject_type: Mapped[Optional[str]] = mapped_column(String(32), nullable=True)
    subject_id: Mapped[Optional[UUID]] = mapped_column(SQLUUID(as_uuid=True), nullable=True)
    approval_id: Mapped[Optional[UUID]] = mapped_column(
        SQLUUID(as_uuid=True), ForeignKey("blue_approvals.id", ondelete="SET NULL"), nullable=True
    )
    # before/after values, model run id, API response ids — whatever explains the event.
    detail: Mapped[dict] = mapped_column(JSONB, nullable=False, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)


class BlueRmIdentity(Base):
    """Teams user → advisor. BLUE scopes every RM conversation by this mapping."""

    __tablename__ = "blue_rm_identities"
    __table_args__ = (
        UniqueConstraint("teams_aad_object_id", name="uq_blue_rm_identities_aad"),
        UniqueConstraint("advisor_id", name="uq_blue_rm_identities_advisor"),
    )

    id: Mapped[UUID] = mapped_column(SQLUUID(as_uuid=True), primary_key=True, default=uuid4)
    advisor_id: Mapped[UUID] = mapped_column(
        SQLUUID(as_uuid=True), ForeignKey("advisors.id", ondelete="CASCADE"), nullable=False
    )
    teams_aad_object_id: Mapped[str] = mapped_column(String(64), nullable=False)
    teams_conversation_id: Mapped[Optional[str]] = mapped_column(String(512), nullable=True)
    enabled: Mapped[bool] = mapped_column(nullable=False, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), onupdate=func.now(), nullable=True)

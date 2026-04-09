"""
Audit and activity logging for ITR filing: authentication events, entity-level
actions, and a mutable per-field snapshot (latest change only per field).
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
    UniqueConstraint,
    UUID as SQLUUID,
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func

from nucleus.db.database import Base


class ITRAuthAuditEvent(Base):
    """Append-only log for login, logout, and related authentication events."""

    __tablename__ = "itr_auth_audit_events"

    id: Mapped[UUID] = mapped_column(SQLUUID(as_uuid=True), primary_key=True, default=uuid4)
    event_type: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
    login_id: Mapped[Optional[int]] = mapped_column(
        Integer,
        ForeignKey("logins.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    occurred_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        index=True,
    )
    ip_address: Mapped[Optional[str]] = mapped_column(String(45), nullable=True)
    user_agent: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    metadata_: Mapped[Optional[dict[str, Any]]] = mapped_column("metadata", JSONB, nullable=True)

    __table_args__ = (
        Index("ix_itr_auth_audit_login_occurred", "login_id", "occurred_at"),
    )


class ITRActivityLog(Base):
    """Append-only log for business actions (create, update, delete, submit, etc.)."""

    __tablename__ = "itr_activity_logs"

    id: Mapped[UUID] = mapped_column(SQLUUID(as_uuid=True), primary_key=True, default=uuid4)
    action: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
    entity_table: Mapped[str] = mapped_column(String(128), nullable=False, index=True)
    entity_id: Mapped[Optional[UUID]] = mapped_column(SQLUUID(as_uuid=True), nullable=True, index=True)
    itr_return_id: Mapped[Optional[UUID]] = mapped_column(
        SQLUUID(as_uuid=True),
        ForeignKey("itr_returns.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    client_id: Mapped[Optional[UUID]] = mapped_column(
        SQLUUID(as_uuid=True),
        ForeignKey("clients.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    actor_login_id: Mapped[Optional[int]] = mapped_column(
        Integer,
        ForeignKey("logins.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    occurred_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        index=True,
    )
    request_id: Mapped[Optional[str]] = mapped_column(String(64), nullable=True, index=True)
    summary: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    payload: Mapped[Optional[dict[str, Any]]] = mapped_column(JSONB, nullable=True)

    __table_args__ = (
        Index("ix_itr_activity_return_occurred", "itr_return_id", "occurred_at"),
        Index("ix_itr_activity_entity_occurred", "entity_table", "entity_id", "occurred_at"),
        Index("ix_itr_activity_actor_occurred", "actor_login_id", "occurred_at"),
    )


class ITRFieldChangeSnapshot(Base):
    """
    Latest change per (entity_table, entity_id, field_path); upsert on each update.
    """

    __tablename__ = "itr_field_change_snapshots"

    id: Mapped[UUID] = mapped_column(SQLUUID(as_uuid=True), primary_key=True, default=uuid4)
    entity_table: Mapped[str] = mapped_column(String(128), nullable=False)
    entity_id: Mapped[UUID] = mapped_column(SQLUUID(as_uuid=True), nullable=False, index=True)
    field_path: Mapped[str] = mapped_column(String(512), nullable=False)
    old_value: Mapped[Optional[Any]] = mapped_column(JSONB, nullable=True)
    new_value: Mapped[Optional[Any]] = mapped_column(JSONB, nullable=True)
    changed_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        index=True,
    )
    changed_by_login_id: Mapped[Optional[int]] = mapped_column(
        Integer,
        ForeignKey("logins.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    itr_return_id: Mapped[Optional[UUID]] = mapped_column(
        SQLUUID(as_uuid=True),
        ForeignKey("itr_returns.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    client_id: Mapped[Optional[UUID]] = mapped_column(
        SQLUUID(as_uuid=True),
        ForeignKey("clients.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )

    __table_args__ = (
        UniqueConstraint(
            "entity_table",
            "entity_id",
            "field_path",
            name="uq_itr_field_change_entity_field",
        ),
        Index("ix_itr_field_change_return_changed", "itr_return_id", "changed_at"),
    )

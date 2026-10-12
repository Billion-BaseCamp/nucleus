"""Latest notice harvest for one client and one portal source.

One row per (client, source). A successful e-Proceedings run replaces only the
``e_proceedings`` row; a successful outstanding-demand run replaces only
``outstanding_demand``. A failed run updates the last-attempt columns and
leaves ``notices`` as they were.

Generate the table with Alembic autogenerate. Do not hand-write the migration.
"""

from __future__ import annotations

from datetime import datetime
from typing import Any, Optional
from uuid import UUID, uuid4

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text, UniqueConstraint, text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func
from sqlalchemy.types import UUID as SQLUUID

from nucleus.db.database import Base

SOURCE_E_PROCEEDINGS = "e_proceedings"
SOURCE_OUTSTANDING_DEMAND = "outstanding_demand"


class ClientNotice(Base):
    """Latest successful harvest for one client + source. Notices live in JSON."""

    __tablename__ = "client_notices"
    __table_args__ = (
        UniqueConstraint("client_id", "source", name="uq_client_notices_client_source"),
    )

    id: Mapped[UUID] = mapped_column(
        SQLUUID(as_uuid=True), primary_key=True, default=uuid4
    )
    client_id: Mapped[UUID] = mapped_column(
        SQLUUID(as_uuid=True),
        ForeignKey("clients.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    source: Mapped[str] = mapped_column(String(32), nullable=False)

    notices: Mapped[list[dict[str, Any]]] = mapped_column(
        JSONB, nullable=False, default=list, server_default=text("'[]'::jsonb")
    )
    notice_count: Mapped[int] = mapped_column(
        Integer, nullable=False, default=0, server_default="0"
    )
    action_required_count: Mapped[int] = mapped_column(
        Integer, nullable=False, default=0, server_default="0"
    )
    fetched_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    job_id: Mapped[Optional[UUID]] = mapped_column(
        SQLUUID(as_uuid=True),
        ForeignKey("portal_automation_jobs.id", ondelete="SET NULL"),
        nullable=True,
    )

    last_attempt_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    last_error_code: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    last_error_message: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), onupdate=func.now(), nullable=True
    )

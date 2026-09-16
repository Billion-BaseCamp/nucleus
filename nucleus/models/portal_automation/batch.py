"""One Excel/API bulk enqueue. Ingest rows (including failures) live here
so Results survive reload. Jobs point back via ``batch_id``.
"""

from __future__ import annotations

from datetime import datetime
from typing import Any, Optional
from uuid import UUID, uuid4

from sqlalchemy import DateTime, String
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func
from sqlalchemy.types import UUID as SQLUUID

from nucleus.db.database import Base


class PortalAutomationBatch(Base):
    """Bulk CHECK_ITR_VERIFICATION (or later workflow) ingest."""

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

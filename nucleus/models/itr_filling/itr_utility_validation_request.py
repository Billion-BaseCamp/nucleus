"""ITR JSON validation via the CBDT offline *desktop utility* (UiPath VM worker).

Distinct from ``ITRFilingValidationJob`` (internal CBDT *schema* validation). This
tracks a request whose JSON is validated by the external offline utility driven by
a UiPath automation on a Windows VM:

  Validate button → generate JSON → upload to S3 → row ``queued``
  → UiPath pulls next job (``queued`` → ``processing``, presigned GET of the JSON)
  → utility runs → UiPath posts back error screenshots + utility JSON
  → we store them in S3 → row ``succeeded`` (``error_count`` may be > 0)

A periodic sweeper times out rows stuck in ``processing``/``queued`` past
``VALIDATION_TIMEOUT_MINUTES`` (default 5) so a dead VM never permanently blocks a
return. At most one active (``queued``/``processing``) request per return is allowed
(partial unique index); a request is only enqueued when the JSON SHA differs from the
last succeeded validation for that return.
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

# Terminal set is enforced in the service layer; kept here for reference.
UTILITY_VALIDATION_ACTIVE_STATUSES = ("queued", "processing")


class ITRUtilityValidationRequest(Base):
    """One offline-utility validation attempt for an ITR return's filing JSON."""

    __tablename__ = "itr_utility_validation_requests"

    id: Mapped[UUID] = mapped_column(
        SQLUUID(as_uuid=True), primary_key=True, default=uuid4, index=True
    )
    itr_return_id: Mapped[UUID] = mapped_column(
        SQLUUID(as_uuid=True),
        ForeignKey("itr_returns.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    client_id: Mapped[Optional[UUID]] = mapped_column(
        SQLUUID(as_uuid=True), nullable=True, index=True
    )
    financial_year_id: Mapped[Optional[UUID]] = mapped_column(
        SQLUUID(as_uuid=True), nullable=True
    )
    form: Mapped[str] = mapped_column(String(10), nullable=False, default="ITR-2")

    # queued | processing | succeeded | failed | timed_out | cancelled
    status: Mapped[str] = mapped_column(
        String(32), nullable=False, default="queued", server_default="queued", index=True
    )

    # Input JSON snapshot (the exact JSON validated).
    input_json_s3_key: Mapped[Optional[str]] = mapped_column(String(512), nullable=True)
    input_json_sha256: Mapped[Optional[str]] = mapped_column(
        String(64), nullable=True, index=True
    )

    # Utility outputs.
    result_json_s3_key: Mapped[Optional[str]] = mapped_column(String(512), nullable=True)
    screenshot_s3_keys: Mapped[Optional[list[Any]]] = mapped_column(JSONB, nullable=True)
    error_count: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    error_summary: Mapped[Optional[dict[str, Any]]] = mapped_column(JSONB, nullable=True)

    requested_by_sub: Mapped[Optional[str]] = mapped_column(String(128), nullable=True)
    attempts: Mapped[int] = mapped_column(
        Integer, nullable=False, default=0, server_default="0"
    )
    last_error: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    dispatched_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    completed_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    updated_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), onupdate=func.now(), nullable=True
    )

    __table_args__ = (
        # At most one active request per return (the in-flight lock).
        Index(
            "uq_itr_utility_validation_active_per_return",
            "itr_return_id",
            unique=True,
            postgresql_where=text("status IN ('queued', 'processing')"),
        ),
        Index("ix_itr_utility_validation_status_created", "status", "created_at"),
    )

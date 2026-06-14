"""Manual Form 16 processing runs (advisor-triggered SQS jobs)."""

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Any, Optional
from uuid import UUID, uuid4

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from sqlalchemy.types import UUID as SQLUUID

from nucleus.db.database import Base

if TYPE_CHECKING:
    from nucleus.models.itr_filling.itr_document import ITRDocument


class ITRDocumentProcessingRun(Base):
    """One advisor-triggered Form 16 extract + ingest attempt."""

    __tablename__ = "itr_document_processing_run"

    id: Mapped[UUID] = mapped_column(
        SQLUUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
        index=True,
    )
    document_id: Mapped[UUID] = mapped_column(
        SQLUUID(as_uuid=True),
        ForeignKey("itr_documents.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    correlation_id: Mapped[str] = mapped_column(
        String(64),
        nullable=False,
        index=True,
    )
    attempt: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    status: Mapped[str] = mapped_column(String(32), nullable=False, index=True)

    error_code: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    error_message_user: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    error_message_internal: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    requested_by: Mapped[Optional[str]] = mapped_column(String(32), nullable=True)
    requested_by_id: Mapped[Optional[UUID]] = mapped_column(
        SQLUUID(as_uuid=True),
        ForeignKey("advisors.id"),
        nullable=True,
    )

    started_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )
    finished_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    claude_input_tokens: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    claude_output_tokens: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    ingest_summary: Mapped[Optional[dict[str, Any]]] = mapped_column(
        JSONB,
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    document: Mapped["ITRDocument"] = relationship(
        "ITRDocument",
        back_populates="processing_runs",
    )

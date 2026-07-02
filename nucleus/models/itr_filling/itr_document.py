from datetime import datetime
from typing import Any, Optional
from uuid import UUID, uuid4

from sqlalchemy import UUID as SQLUUID
from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from nucleus.db.database import Base


class ITRDocument(Base):
    __tablename__ = "itr_documents"

    id: Mapped[UUID] = mapped_column(
        SQLUUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
        index=True,
    )
    slot_id: Mapped[UUID] = mapped_column(
        SQLUUID(as_uuid=True),
        ForeignKey("itr_document_slots.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    file_name: Mapped[str] = mapped_column(String, nullable=False)
    s3_key: Mapped[str] = mapped_column(String, nullable=False)
    bucket_name: Mapped[str] = mapped_column(String, nullable=False)

    is_password_protected: Mapped[bool] = mapped_column(
        Boolean, default=False, server_default="FALSE"
    )
    updated_by: Mapped[Optional[str]] = mapped_column(String, nullable=True,default="client",server_default="client")
    updated_by_advisor_id: Mapped[Optional[UUID]] = mapped_column(
        SQLUUID(as_uuid=True), 
        ForeignKey("advisors.id"),
         nullable=True
    )
    password: Mapped[str] = mapped_column(String, nullable=True)
    status: Mapped[str] = mapped_column(String, nullable=True)
    advisor_comment: Mapped[Optional[str]] = mapped_column(String, nullable=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), onupdate=func.now(), nullable=True
    )

    slot: Mapped["ITRDocumentSlot"] = relationship(
        "ITRDocumentSlot", back_populates="documents"
    )


class ITRDocumentReview(Base):
    """User review of a processed source document (approve ingest or upload correction)."""

    __tablename__ = "itr_document_review"

    document_id: Mapped[UUID] = mapped_column(
        SQLUUID(as_uuid=True),
        ForeignKey("itr_documents.id", ondelete="CASCADE"),
        primary_key=True,
    )
    itr_return_id: Mapped[UUID] = mapped_column(
        SQLUUID(as_uuid=True),
        ForeignKey("itr_returns.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    review_status: Mapped[str] = mapped_column(String(32), nullable=False)
    reviewed_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
    reviewed_by: Mapped[str] = mapped_column(String(32), nullable=False)
    reviewed_by_advisor_id: Mapped[Optional[UUID]] = mapped_column(
        SQLUUID(as_uuid=True),
        ForeignKey("advisors.id"),
        nullable=True,
    )


class ITRDocumentProcessingLog(Base):
    """One processing attempt for an uploaded ITR document."""

    __tablename__ = "itr_document_processing_logs"

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
    processing_source: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    attempt_number: Mapped[int] = mapped_column(Integer, nullable=False)
    status: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
    llm_model: Mapped[Optional[str]] = mapped_column(String(128), nullable=True)
    error_message: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    error_metadata: Mapped[Optional[dict[str, Any]]] = mapped_column(JSONB, nullable=True)
    processing_duration_ms: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    triggered_by: Mapped[Optional[str]] = mapped_column(String(32), nullable=True)
    triggered_by_advisor_id: Mapped[Optional[UUID]] = mapped_column(
        SQLUUID(as_uuid=True),
        ForeignKey("advisors.id"),
        nullable=True,
        index=True,
    )
    started_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )
    completed_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

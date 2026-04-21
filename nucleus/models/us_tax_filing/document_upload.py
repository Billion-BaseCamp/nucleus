"""Uploaded document linked to a questionnaire item and submission."""

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Optional
from uuid import UUID, uuid4

from sqlalchemy import UUID as SQLUUID
from sqlalchemy import DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from nucleus.db.database import Base

if TYPE_CHECKING:
    from .questionnaire_item import QuestionnaireItem
    from .submission import Submission


class DocumentUpload(Base):
    __tablename__ = "document_uploads"

    id: Mapped[UUID] = mapped_column(
        SQLUUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
    )
    questionnaire_item_id: Mapped[UUID] = mapped_column(
        SQLUUID(as_uuid=True),
        ForeignKey("questionnaire_items.id", ondelete="CASCADE"),
        nullable=False,
    )
    submission_id: Mapped[UUID] = mapped_column(
        SQLUUID(as_uuid=True),
        ForeignKey("submissions.id", ondelete="CASCADE"),
        nullable=False,
    )
    original_filename: Mapped[str] = mapped_column(String(512), nullable=False)
    s3_bucket: Mapped[str] = mapped_column(String(255), nullable=False)
    s3_key: Mapped[str] = mapped_column(String(1024), nullable=False)
    password_encrypted: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
    )
    comment: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    uploaded_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        server_default=func.now(),
    )
    file_size_bytes: Mapped[Optional[int]] = mapped_column(
        Integer,
        nullable=True,
    )
    mime_type: Mapped[Optional[str]] = mapped_column(
        String(128),
        nullable=True,
    )

    questionnaire_item: Mapped["QuestionnaireItem"] = relationship(
        "QuestionnaireItem",
        back_populates="documents",
    )
    submission: Mapped["Submission"] = relationship(
        "Submission",
        back_populates="document_uploads",
        foreign_keys=[submission_id],
    )

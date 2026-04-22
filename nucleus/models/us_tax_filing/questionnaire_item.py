"""Structured response for a single question in a submission."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Optional
from uuid import UUID, uuid4

from sqlalchemy import UUID as SQLUUID
from sqlalchemy import Boolean, ForeignKey, Integer, String, Text, text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from nucleus.db.database import Base

if TYPE_CHECKING:
    from .document_upload import DocumentUpload
    from .questionnaire_item_edit_audit import QuestionnaireItemEditAudit
    from .submission import Submission


class QuestionnaireItem(Base):
    __tablename__ = "questionnaire_items"

    id: Mapped[UUID] = mapped_column(
        SQLUUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
    )
    submission_id: Mapped[UUID] = mapped_column(
        SQLUUID(as_uuid=True),
        ForeignKey("submissions.id", ondelete="CASCADE"),
        nullable=False,
    )
    question_number: Mapped[int] = mapped_column(Integer, nullable=False)
    question_text: Mapped[str] = mapped_column(Text, nullable=False)
    question_type: Mapped[str] = mapped_column(
        String(32),
        nullable=False,
        default="text",
        server_default=text("'text'"),
    )
    has_document_upload: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )

    response_text: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    response_data: Mapped[Optional[dict[str, Any]]] = mapped_column(
        JSONB, nullable=True
    )
    not_applicable: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )
    remarks: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    submission: Mapped["Submission"] = relationship(
        "Submission",
        back_populates="items",
    )
    documents: Mapped[list["DocumentUpload"]] = relationship(
        "DocumentUpload",
        back_populates="questionnaire_item",
        cascade="all, delete-orphan",
    )
    edit_audits: Mapped[list["QuestionnaireItemEditAudit"]] = relationship(
        "QuestionnaireItemEditAudit",
        back_populates="questionnaire_item",
        cascade="all, delete-orphan",
    )

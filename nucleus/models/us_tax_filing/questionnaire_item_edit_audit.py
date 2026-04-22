"""Audit row: one field change on an item (non-draft submissions)."""

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Any, Optional
from uuid import UUID, uuid4

from sqlalchemy import UUID as SQLUUID
from sqlalchemy import DateTime, ForeignKey, Integer, String, func
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from nucleus.db.database import Base

if TYPE_CHECKING:
    from .questionnaire_item import QuestionnaireItem
    from .submission import Submission


class QuestionnaireItemEditAudit(Base):
    __tablename__ = "questionnaire_item_edit_audits"

    id: Mapped[UUID] = mapped_column(
        SQLUUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
    )
    submission_id: Mapped[UUID] = mapped_column(
        SQLUUID(as_uuid=True),
        ForeignKey("submissions.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    questionnaire_item_id: Mapped[UUID] = mapped_column(
        SQLUUID(as_uuid=True),
        ForeignKey("questionnaire_items.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    question_number: Mapped[int] = mapped_column(Integer, nullable=False)
    field_name: Mapped[str] = mapped_column(String(64), nullable=False)
    previous_value: Mapped[Optional[Any]] = mapped_column(JSONB, nullable=True)
    new_value: Mapped[Optional[Any]] = mapped_column(JSONB, nullable=True)
    changed_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        server_default=func.now(),
    )
    changed_by_user_id: Mapped[Optional[str]] = mapped_column(
        String(255),
        nullable=True,
    )
    changed_by_role: Mapped[Optional[str]] = mapped_column(
        String(32),
        nullable=True,
    )

    submission: Mapped["Submission"] = relationship(
        "Submission",
        back_populates="item_edit_audits",
    )
    questionnaire_item: Mapped["QuestionnaireItem"] = relationship(
        "QuestionnaireItem",
        back_populates="edit_audits",
    )

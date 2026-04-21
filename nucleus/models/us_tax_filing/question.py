"""Master question template for the tax questionnaire."""

from __future__ import annotations

from typing import Optional
from uuid import UUID, uuid4

from sqlalchemy import UUID as SQLUUID
from sqlalchemy import Boolean, Integer, String, Text, text
from sqlalchemy.orm import Mapped, mapped_column

from nucleus.db.database import Base


class Question(Base):
    __tablename__ = "questions"

    id: Mapped[UUID] = mapped_column(
        SQLUUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
    )
    question_number: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        unique=True,
    )
    question_text: Mapped[str] = mapped_column(Text, nullable=False)
    # form | file_upload | text | consent (validated in service layer)
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
    internal_notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )

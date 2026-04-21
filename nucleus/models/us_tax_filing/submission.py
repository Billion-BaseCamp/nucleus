"""Questionnaire submission (1040 return) for a client."""

# isort: skip_file

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Any, Optional
from uuid import UUID, uuid4

from sqlalchemy import (
    Boolean,
    DateTime,
    Integer,
    String,
    UniqueConstraint,
    UUID as SQLUUID,
    text,
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from nucleus.db.database import Base

PriorReturnPayload = Optional[dict[str, Any]]

if TYPE_CHECKING:
    from .document_upload import DocumentUpload
    from .questionnaire_item import QuestionnaireItem


class Submission(Base):
    __tablename__ = "submissions"
    __table_args__ = (
        UniqueConstraint(
            "client_email",
            "tax_year",
            name="uq_submission_client_email_tax_year",
        ),
    )

    id: Mapped[UUID] = mapped_column(
        SQLUUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
    )
    client_name: Mapped[str] = mapped_column(String(255), nullable=False)
    client_email: Mapped[str] = mapped_column(String(255), nullable=False)
    tax_year: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=2025,
        server_default=text("2025"),
    )
    # Validated in service layer (draft / submitted / under_review / completed)
    status: Mapped[str] = mapped_column(
        String(32),
        nullable=False,
        default="draft",
    )
    is_first_time_client: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )
    user_id: Mapped[Optional[str]] = mapped_column(
        String(255),
        nullable=True,
    )
    advisor_id: Mapped[Optional[str]] = mapped_column(
        String(255),
        nullable=True,
    )
    prior_return_extracted_data: Mapped[PriorReturnPayload] = mapped_column(
        JSONB,
        nullable=True,
    )
    is_data_extracted: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
        server_default=text("false"),
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        server_default=func.now(),
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )

    items: Mapped[list["QuestionnaireItem"]] = relationship(
        "QuestionnaireItem",
        back_populates="submission",
        cascade="all, delete-orphan",
    )
    document_uploads: Mapped[list["DocumentUpload"]] = relationship(
        "DocumentUpload",
        back_populates="submission",
        cascade="all, delete-orphan",
        foreign_keys="[DocumentUpload.submission_id]",
    )

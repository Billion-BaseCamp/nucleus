"""ITR-scoped TIS PDF file archives (S3-backed metadata)."""

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Optional
from uuid import UUID, uuid4

from sqlalchemy import DateTime, ForeignKey, Integer, String
from sqlalchemy import UUID as SQLUUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from nucleus.db.database import Base

if TYPE_CHECKING:
    from nucleus.models.itr_filling.itr_return import ITRReturn


class ITRTisPdfArchive(Base):
    """One stored TIS PDF export linked to an ITR return (raw file in S3).

    Retention is enforced in application code: at most two ``stored`` rows
    per ``itr_return_id`` (latest + previous for compare).
    """

    __tablename__ = "itr_tis_pdf_archives"

    id: Mapped[UUID] = mapped_column(
        SQLUUID(as_uuid=True), primary_key=True, default=uuid4
    )
    client_id: Mapped[UUID] = mapped_column(
        SQLUUID(as_uuid=True),
        ForeignKey("clients.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    itr_return_id: Mapped[Optional[UUID]] = mapped_column(
        SQLUUID(as_uuid=True),
        ForeignKey("itr_returns.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    # Canonical short FY label, e.g. "25-26" (metadata). Retention is max 2 per itr_return_id.
    financial_year: Mapped[Optional[str]] = mapped_column(
        String(16), nullable=True, index=True
    )

    s3_key: Mapped[str] = mapped_column(String(512), nullable=False)
    original_filename: Mapped[str] = mapped_column(String(255), nullable=False)
    file_size_bytes: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    status: Mapped[str] = mapped_column(
        String(32), nullable=False, server_default="pending_upload"
    )
    failure_reason: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), onupdate=func.now(), nullable=True
    )

    itr_return: Mapped[Optional["ITRReturn"]] = relationship(  # noqa: F821
        "ITRReturn",
        back_populates="tis_pdf_archives",
    )


__all__ = ["ITRTisPdfArchive"]

from __future__ import annotations

from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4

from sqlalchemy import DateTime, ForeignKey, String, Text, UniqueConstraint
from sqlalchemy import UUID as SQLUUID
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func

from nucleus.db.database import Base


class ITRClientCommentRead(Base):
    """Per-reader read state for aggregated client comments (virtual refs, no FK to sources)."""

    __tablename__ = "itr_client_comment_reads"

    id: Mapped[UUID] = mapped_column(
        SQLUUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
        index=True,
    )
    client_id: Mapped[UUID] = mapped_column(
        SQLUUID(as_uuid=True),
        ForeignKey("clients.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    financial_year_id: Mapped[UUID] = mapped_column(
        SQLUUID(as_uuid=True),
        ForeignKey("financial_years.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    reader_id: Mapped[UUID] = mapped_column(
        SQLUUID(as_uuid=True),
        nullable=False,
        index=True,
    )
    reader_role: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    source: Mapped[str] = mapped_column(String, nullable=False)
    source_id: Mapped[UUID] = mapped_column(SQLUUID(as_uuid=True), nullable=False)
    field: Mapped[str] = mapped_column(String, nullable=False)
    read_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
    source_updated_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )
    source_content_hash: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    rm_comment: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    __table_args__ = (
        UniqueConstraint(
            "reader_id",
            "source",
            "source_id",
            "field",
            name="uq_itr_client_comment_reads_reader_ref",
        ),
    )

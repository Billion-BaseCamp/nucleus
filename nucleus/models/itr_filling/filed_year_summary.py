"""Dashboard-only snapshot of a filed ITR year.

One header row per client per assessment year. Raw JSON lives in S3. Each
CBDT schedule is a child row so GET never parses S3 or hydrates live
``ITRReturn`` trees.

``financial_year_id`` is set only when ``financial_years`` already has that
client+FY; otherwise it stays NULL.

Schema changes are managed via Alembic autogenerate.
"""

from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from typing import List, Optional
from uuid import UUID, uuid4

from sqlalchemy import (
    DateTime,
    ForeignKey,
    Index,
    Integer,
    String,
    UniqueConstraint,
    UUID as SQLUUID,
    text,
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from sqlalchemy.types import Numeric

from nucleus.db.database import Base


class ITRFiledYearSummary(Base):
    """Header for one filed ITR snapshot (ITR-1 / ITR-2 / ITR-3)."""

    __tablename__ = "itr_filed_year_summaries"
    __table_args__ = (
        UniqueConstraint(
            "client_id",
            "assessment_year",
            name="uq_itr_filed_year_summaries_client_ay",
        ),
        Index(
            "ix_itr_filed_year_summaries_client_fy",
            "client_id",
            "financial_year",
        ),
    )

    id: Mapped[UUID] = mapped_column(
        SQLUUID(as_uuid=True), primary_key=True, default=uuid4
    )
    client_id: Mapped[UUID] = mapped_column(
        SQLUUID(as_uuid=True),
        ForeignKey("clients.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    # Set when ``financial_years`` already has this client+FY; otherwise NULL.
    financial_year_id: Mapped[Optional[UUID]] = mapped_column(
        SQLUUID(as_uuid=True),
        ForeignKey("financial_years.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )

    # CBDT Form_ITRx.AssessmentYear, normalized (e.g. 2023-24).
    assessment_year: Mapped[str] = mapped_column(String(10), nullable=False)
    # Dashboard / tax-engine income FY (e.g. 22-23 for AY 2023-24).
    financial_year: Mapped[str] = mapped_column(String(7), nullable=False)

    pan: Mapped[Optional[str]] = mapped_column(String(10), nullable=True)
    itr_type: Mapped[Optional[str]] = mapped_column(String(10), nullable=True)

    s3_key: Mapped[str] = mapped_column(String(512), nullable=False)
    original_filename: Mapped[str] = mapped_column(String(255), nullable=False)
    file_size_bytes: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    content_sha256: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    status: Mapped[str] = mapped_column(
        String(20), nullable=False, default="ready", server_default=text("'ready'")
    )

    total_income: Mapped[Optional[Decimal]] = mapped_column(
        Numeric(18, 2), nullable=True
    )
    tax_payable: Mapped[Optional[Decimal]] = mapped_column(
        Numeric(18, 2), nullable=True
    )
    refund_due: Mapped[Optional[Decimal]] = mapped_column(
        Numeric(18, 2), nullable=True
    )

    extractor_version: Mapped[str] = mapped_column(
        String(20), nullable=False, default="1", server_default=text("'1'")
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), onupdate=func.now(), nullable=True
    )

    schedules: Mapped[List["ITRFiledYearSchedule"]] = relationship(
        back_populates="filed_year_summary",
        cascade="all, delete-orphan",
    )


class ITRFiledYearSchedule(Base):
    """One CBDT schedule JSONB payload for a filed-year snapshot."""

    __tablename__ = "itr_filed_year_schedules"
    __table_args__ = (
        UniqueConstraint(
            "filed_year_summary_id",
            "schedule_code",
            name="uq_itr_filed_year_schedules_summary_code",
        ),
        Index(
            "ix_itr_filed_year_schedules_code",
            "schedule_code",
        ),
    )

    id: Mapped[UUID] = mapped_column(
        SQLUUID(as_uuid=True), primary_key=True, default=uuid4
    )
    filed_year_summary_id: Mapped[UUID] = mapped_column(
        SQLUUID(as_uuid=True),
        ForeignKey("itr_filed_year_summaries.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    # Extractor key, e.g. schedule_s / schedule_hp / part_b_ti.
    schedule_code: Mapped[str] = mapped_column(String(32), nullable=False)
    schedule_data: Mapped[dict] = mapped_column(
        JSONB, nullable=False, server_default=text("'{}'::jsonb")
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), onupdate=func.now(), nullable=True
    )

    filed_year_summary: Mapped["ITRFiledYearSummary"] = relationship(
        back_populates="schedules"
    )


__all__ = ["ITRFiledYearSummary", "ITRFiledYearSchedule"]

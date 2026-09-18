"""Dashboard-only snapshot of a filed ITR year (CBDT schedules as JSONB).

One row per client per assessment year. Raw JSON lives in S3; this table
stores per-schedule JSONB plus totals so the admin profile GET never
parses S3 or hydrates live ``ITRReturn`` trees.

Schema changes are managed via Alembic autogenerate.
"""

from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from typing import Optional
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
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func
from sqlalchemy.types import Numeric

from nucleus.db.database import Base

_EMPTY_JSONB = text("'{}'::jsonb")


def _schedule_jsonb() -> Mapped[dict]:
    return mapped_column(JSONB, nullable=False, server_default=_EMPTY_JSONB)


class ITRFiledYearSummary(Base):
    """Admin-dashboard snapshot of one filed ITR (ITR-1 / ITR-2 / ITR-3)."""

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

    schedule_s: Mapped[dict] = _schedule_jsonb()
    schedule_hp: Mapped[dict] = _schedule_jsonb()
    schedule_os: Mapped[dict] = _schedule_jsonb()
    schedule_cg: Mapped[dict] = _schedule_jsonb()
    schedule_112a: Mapped[dict] = _schedule_jsonb()
    schedule_115ad: Mapped[dict] = _schedule_jsonb()
    schedule_vda: Mapped[dict] = _schedule_jsonb()
    schedule_cfl: Mapped[dict] = _schedule_jsonb()
    schedule_cyla: Mapped[dict] = _schedule_jsonb()
    schedule_bfla: Mapped[dict] = _schedule_jsonb()
    schedule_via: Mapped[dict] = _schedule_jsonb()
    schedule_it: Mapped[dict] = _schedule_jsonb()
    schedule_tds1: Mapped[dict] = _schedule_jsonb()
    schedule_tds2: Mapped[dict] = _schedule_jsonb()
    schedule_tds3: Mapped[dict] = _schedule_jsonb()
    schedule_tcs: Mapped[dict] = _schedule_jsonb()
    schedule_si: Mapped[dict] = _schedule_jsonb()
    schedule_spi: Mapped[dict] = _schedule_jsonb()
    schedule_pti: Mapped[dict] = _schedule_jsonb()
    schedule_al: Mapped[dict] = _schedule_jsonb()
    schedule_fa: Mapped[dict] = _schedule_jsonb()
    schedule_fsi: Mapped[dict] = _schedule_jsonb()
    schedule_tr: Mapped[dict] = _schedule_jsonb()
    schedule_amt: Mapped[dict] = _schedule_jsonb()
    schedule_80g: Mapped[dict] = _schedule_jsonb()
    part_a_gen1: Mapped[dict] = _schedule_jsonb()
    part_b_ti: Mapped[dict] = _schedule_jsonb()
    part_b_tti: Mapped[dict] = _schedule_jsonb()

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), onupdate=func.now(), nullable=True
    )


__all__ = ["ITRFiledYearSummary"]

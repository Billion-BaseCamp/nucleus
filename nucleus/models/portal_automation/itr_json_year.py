"""Latest ITR JSON download for one client and one assessment year.

The JSON file lives in S3. This row is the portal result the screen reads:
which filing the file came from, and the newest card's type and date.
A later download of the same year replaces this row. A failed download does not.

Generate the table with Alembic autogenerate. Do not hand-write the migration.
"""

from __future__ import annotations

from datetime import date, datetime
from typing import Optional
from uuid import UUID, uuid4

from sqlalchemy import Date, DateTime, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func
from sqlalchemy.types import UUID as SQLUUID

from nucleus.db.database import Base


class ClientItrJsonYear(Base):
    """Current portal ITR JSON result for one client and assessment year."""

    __tablename__ = "client_itr_json_years"
    __table_args__ = (
        UniqueConstraint(
            "client_id",
            "assessment_year",
            name="uq_client_itr_json_years_client_ay",
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
    assessment_year: Mapped[str] = mapped_column(String(16), nullable=False)
    # downloaded | no_filing
    status: Mapped[str] = mapped_column(String(32), nullable=False)
    s3_key: Mapped[Optional[str]] = mapped_column(String(512), nullable=True)
    job_id: Mapped[Optional[UUID]] = mapped_column(
        SQLUUID(as_uuid=True),
        ForeignKey("portal_automation_jobs.id", ondelete="SET NULL"),
        nullable=True,
    )
    itr_form: Mapped[Optional[str]] = mapped_column(String(16), nullable=True)
    acknowledgement_no: Mapped[Optional[str]] = mapped_column(String(32), nullable=True)
    filing_section: Mapped[Optional[str]] = mapped_column(String(16), nullable=True)
    filing_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    e_verified_on: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    latest_filing_type: Mapped[Optional[str]] = mapped_column(String(32), nullable=True)
    latest_filing_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    filings_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    counts_by_filing_type: Mapped[dict] = mapped_column(
        JSONB, nullable=False, default=dict
    )
    fetched_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), onupdate=func.now(), nullable=True
    )

"""Latest foreign-assets PDF for one client and one calendar year.

A later download of the same year replaces this row and the S3 object.
The dashboard reads these rows. It does not scan portal job history.

Generate the table with Alembic autogenerate. Do not hand-write the migration.
"""

from __future__ import annotations

from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4

from sqlalchemy import DateTime, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func
from sqlalchemy.types import UUID as SQLUUID

from nucleus.db.database import Base


class ClientForeignAssetYear(Base):
    """Current portal result for one client + calendar year."""

    __tablename__ = "client_foreign_asset_years"
    __table_args__ = (
        UniqueConstraint(
            "client_id",
            "calendar_year",
            name="uq_client_foreign_asset_years_client_year",
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
    calendar_year: Mapped[int] = mapped_column(Integer, nullable=False)
    # downloaded | no_data | year_not_in_dropdown | dry_run
    status: Mapped[str] = mapped_column(String(32), nullable=False)
    s3_key: Mapped[Optional[str]] = mapped_column(String(512), nullable=True)
    pdf_password: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    job_id: Mapped[Optional[UUID]] = mapped_column(
        SQLUUID(as_uuid=True),
        ForeignKey("portal_automation_jobs.id", ondelete="SET NULL"),
        nullable=True,
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

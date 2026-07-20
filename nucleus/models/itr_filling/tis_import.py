"""TIS (Taxpayer Information Summary) page-1 category totals per ITR.

Each row belongs to a specific ``ITRTisPdfArchive``. When the oldest archive is
evicted (max 2 per return), ``ON DELETE CASCADE`` removes that archive's
summary rows. Applied Schedule OS / other filing data is never touched.
"""

from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from typing import TYPE_CHECKING, Optional
from uuid import UUID, uuid4

from sqlalchemy import DateTime, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy import UUID as SQLUUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from sqlalchemy.types import Numeric

from nucleus.db.database import Base

if TYPE_CHECKING:
    from nucleus.models.itr_filling.itr_return import ITRReturn
    from nucleus.models.itr_filling.tis_pdf_archive import ITRTisPdfArchive


class ITRTisSummaryCategory(Base):
    """One row from the TIS page-1 summary table (Accepted / Processed totals).

    Scoped to a PDF archive so latest + previous imports can coexist for
    compare. Unique per ``(tis_pdf_archive_id, sr_no)``.
    """

    __tablename__ = "itr_tis_summary_categories"
    __table_args__ = (
        UniqueConstraint(
            "tis_pdf_archive_id",
            "sr_no",
            name="uq_itr_tis_summary_categories_archive_sr",
        ),
    )

    id: Mapped[UUID] = mapped_column(
        SQLUUID(as_uuid=True), primary_key=True, default=uuid4
    )
    itr_return_id: Mapped[UUID] = mapped_column(
        SQLUUID(as_uuid=True),
        ForeignKey("itr_returns.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    tis_pdf_archive_id: Mapped[Optional[UUID]] = mapped_column(
        SQLUUID(as_uuid=True),
        ForeignKey("itr_tis_pdf_archives.id", ondelete="CASCADE"),
        nullable=True,
        index=True,
    )
    sr_no: Mapped[int] = mapped_column(Integer, nullable=False)
    category_name: Mapped[str] = mapped_column(String(200), nullable=False)
    processed_total: Mapped[Decimal] = mapped_column(
        Numeric(15, 2), nullable=False, default=0
    )
    accepted_total: Mapped[Decimal] = mapped_column(
        Numeric(15, 2), nullable=False, default=0
    )
    reconciliation_group: Mapped[str] = mapped_column(String(50), nullable=False)
    pan: Mapped[Optional[str]] = mapped_column(String(10), nullable=True)
    financial_year: Mapped[Optional[str]] = mapped_column(String(10), nullable=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), onupdate=func.now(), nullable=True
    )

    itr_return: Mapped["ITRReturn"] = relationship(  # noqa: F821
        "ITRReturn",
        back_populates="tis_summary_categories",
    )
    tis_pdf_archive: Mapped[Optional["ITRTisPdfArchive"]] = relationship(  # noqa: F821
        "ITRTisPdfArchive",
        back_populates="summary_categories",
    )


__all__ = ["ITRTisSummaryCategory"]

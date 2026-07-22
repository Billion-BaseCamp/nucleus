"""Client Summary PDF download log (S3-backed).

One append-only row per download, keyed by ``itr_return_id``.
``client_id`` / ``financial_year_id`` are derived from the ITR at write/read time
(not stored). PDF bytes live in S3; this table stores the key + tax snapshot.


```
"""

from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from typing import Optional
from uuid import UUID, uuid4

from sqlalchemy import (
    Boolean,
    DateTime,
    ForeignKey,
    Index,
    Integer,
    String,
    UUID as SQLUUID,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func, text
from sqlalchemy.types import Numeric

from nucleus.db.database import Base


class ITRClientSummaryDownloadLog(Base):
    """Append-only log of Client Summary PDF downloads for one ITR return."""

    __tablename__ = "itr_client_summary_download_logs"

    id: Mapped[UUID] = mapped_column(
        SQLUUID(as_uuid=True), primary_key=True, default=uuid4
    )
    itr_return_id: Mapped[UUID] = mapped_column(
        SQLUUID(as_uuid=True),
        ForeignKey("itr_returns.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    # JWT ``sub`` of the user who clicked Download + name snapshot.
    downloaded_by_user_id: Mapped[UUID] = mapped_column(
        SQLUUID(as_uuid=True), nullable=False, index=True
    )
    downloaded_by_name: Mapped[str] = mapped_column(String(255), nullable=False)

    downloaded_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )

    regime: Mapped[str] = mapped_column(String(5), nullable=False)
    share_status: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    include_cg_transactions: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=False, server_default=text("false")
    )

    total_income: Mapped[Decimal] = mapped_column(
        Numeric(18, 2), nullable=False, default=Decimal("0")
    )
    total_income_tax: Mapped[Decimal] = mapped_column(
        Numeric(18, 2), nullable=False, default=Decimal("0")
    )
    interest_234b: Mapped[Decimal] = mapped_column(
        Numeric(18, 2), nullable=False, default=Decimal("0")
    )
    interest_234c: Mapped[Decimal] = mapped_column(
        Numeric(18, 2), nullable=False, default=Decimal("0")
    )
    refund_due: Mapped[Decimal] = mapped_column(
        Numeric(18, 2), nullable=False, default=Decimal("0")
    )
    tax_payable: Mapped[Decimal] = mapped_column(
        Numeric(18, 2), nullable=False, default=Decimal("0")
    )

    bucket_name: Mapped[str] = mapped_column(String(255), nullable=False)
    s3_key: Mapped[str] = mapped_column(String(512), nullable=False)
    file_name: Mapped[str] = mapped_column(String(255), nullable=False)
    file_size_bytes: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    status: Mapped[str] = mapped_column(
        String(32), nullable=False, server_default="pending_upload"
    )

    itr_return: Mapped["ITRReturn"] = relationship(  # noqa: F821
        "ITRReturn",
        back_populates="client_summary_download_logs",
    )

    __table_args__ = (
        Index(
            "ix_cs_dl_itr_downloaded",
            "itr_return_id",
            "downloaded_at",
        ),
    )


__all__ = ["ITRClientSummaryDownloadLog"]

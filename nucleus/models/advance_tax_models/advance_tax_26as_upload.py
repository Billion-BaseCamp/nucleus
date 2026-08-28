from __future__ import annotations

from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4

from sqlalchemy import DateTime, ForeignKey, Integer, String, UniqueConstraint, UUID as SQLUUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from nucleus.db.database import Base


class AdvanceTax26asUpload(Base):
    __tablename__ = "advance_tax_26as_uploads"
    __table_args__ = (
        UniqueConstraint("quarter_id", name="uq_advance_tax_26as_uploads_quarter_id"),
    )

    id: Mapped[UUID] = mapped_column(
        SQLUUID(as_uuid=True), primary_key=True, default=uuid4, index=True
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
    quarter_id: Mapped[UUID] = mapped_column(
        SQLUUID(as_uuid=True),
        ForeignKey("quarters.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    s3_key: Mapped[str] = mapped_column(String(512), nullable=False)
    bucket_name: Mapped[str] = mapped_column(String(255), nullable=False)
    original_filename: Mapped[str] = mapped_column(String(255), nullable=False)
    file_size_bytes: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    pan: Mapped[Optional[str]] = mapped_column(String(10), nullable=True)
    # pending | parsing | parsed | failed
    parse_status: Mapped[str] = mapped_column(
        String(32), nullable=False, server_default="pending", default="pending", index=True
    )
    uploaded_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), onupdate=func.now(), nullable=True
    )

    client: Mapped["Client"] = relationship("Client")
    financial_year: Mapped["FinancialYear"] = relationship("FinancialYear")
    quarter: Mapped["Quarter"] = relationship(
        "Quarter",
        foreign_keys=[quarter_id],
    )

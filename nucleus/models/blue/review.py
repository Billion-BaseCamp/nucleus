"""Quarter review: what BLUE knows about one client's advance-tax quarter."""

from __future__ import annotations

from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4

from sqlalchemy import CheckConstraint, DateTime, ForeignKey, Integer, String, Text, UniqueConstraint
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func
from sqlalchemy.types import UUID as SQLUUID

from nucleus.db.database import Base
from nucleus.models.blue.constants import BLUE_REVIEW_READINESS, check_in


class BlueQuarterReview(Base):
    """Latest have / missing / mismatch picture for a client + FY + quarter.

    Rebuilt whenever a new document for the client is extracted; ``version``
    increments so a briefing can say what changed since the RM last looked.
    """

    __tablename__ = "blue_quarter_reviews"
    __table_args__ = (
        UniqueConstraint("client_id", "financial_year", "quarter_number", name="uq_blue_quarter_reviews_client_fy_q"),
        CheckConstraint("quarter_number BETWEEN 1 AND 4", name="ck_blue_quarter_reviews_quarter_number"),
        CheckConstraint(check_in("readiness", BLUE_REVIEW_READINESS), name="ck_blue_quarter_reviews_readiness"),
    )

    id: Mapped[UUID] = mapped_column(SQLUUID(as_uuid=True), primary_key=True, default=uuid4)
    client_id: Mapped[UUID] = mapped_column(
        SQLUUID(as_uuid=True), ForeignKey("clients.id", ondelete="CASCADE"), nullable=False, index=True
    )
    # Denormalised from clients.advisor_id at build time, for "my clients" queries.
    advisor_id: Mapped[Optional[UUID]] = mapped_column(
        SQLUUID(as_uuid=True), ForeignKey("advisors.id", ondelete="SET NULL"), nullable=True, index=True
    )
    financial_year: Mapped[str] = mapped_column(String(9), nullable=False)
    quarter_number: Mapped[int] = mapped_column(Integer, nullable=False)
    # Advance-tax quarter this review compares against / writes into, when it exists.
    quarter_id: Mapped[Optional[UUID]] = mapped_column(
        SQLUUID(as_uuid=True), ForeignKey("quarters.id", ondelete="SET NULL"), nullable=True
    )
    readiness: Mapped[str] = mapped_column(String(32), nullable=False, default="collecting")
    # {"salary": {"amount": "...", "sources": ["<field_id>", ...]}, ...}
    have: Mapped[dict] = mapped_column(JSONB, nullable=False, default=dict)
    # [{"item": "rent receipts Jul-Sep", "why": "rental income in Q1"}, ...]
    missing: Mapped[list] = mapped_column(JSONB, nullable=False, default=list)
    # [{"head": "interest", "previous": "...", "current": "...", "explanation": "..."}, ...]
    mismatches: Mapped[list] = mapped_column(JSONB, nullable=False, default=list)
    summary: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    version: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    last_briefed_version: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    built_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), onupdate=func.now(), nullable=True)

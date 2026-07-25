"""Advisor confirmations for Summary download verification.

One row per (ITR, rule code, subject). Once confirmed, Intelligence and the
download gate stop asking for that item. ``subject_key`` distinguishes
per-employer / per-transaction prompts; empty string = return-level item.
"""

from __future__ import annotations

from datetime import datetime
from typing import Any, Optional
from uuid import UUID, uuid4

from sqlalchemy import (
    DateTime,
    ForeignKey,
    String,
    Text,
    UniqueConstraint,
    UUID as SQLUUID,
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from nucleus.db.database import Base


class ITRSummaryVerification(Base):
    """Persisted advisor confirmation for a summary-download verification item."""

    __tablename__ = "itr_summary_verifications"

    id: Mapped[UUID] = mapped_column(
        SQLUUID(as_uuid=True), primary_key=True, default=uuid4
    )
    itr_return_id: Mapped[UUID] = mapped_column(
        SQLUUID(as_uuid=True),
        ForeignKey("itr_returns.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    # Rule id, e.g. ``sec_54_cost_paid``, ``ais_employer_not_considered``.
    code: Mapped[str] = mapped_column(String(64), nullable=False)
    # Empty for return-level items; TAN / txn id / etc. for per-entity items.
    subject_key: Mapped[str] = mapped_column(
        String(128), nullable=False, default="", server_default=""
    )

    # ``confirmed`` | ``not_applicable``
    status: Mapped[str] = mapped_column(String(20), nullable=False, default="confirmed")
    # Selected option payload, e.g. {"choice": "taxable_gift"} or {"reviewer": "..."}.
    response: Mapped[Optional[dict[str, Any]]] = mapped_column(JSONB, nullable=True)
    comment: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    confirmed_by_advisor_id: Mapped[Optional[UUID]] = mapped_column(
        SQLUUID(as_uuid=True), nullable=True, index=True
    )
    confirmed_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )

    # Optional hash of figures confirmed against (re-prompt on material change).
    data_signature: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), onupdate=func.now()
    )

    itr_return: Mapped["ITRReturn"] = relationship(  # noqa: F821
        "ITRReturn",
        back_populates="summary_verifications",
    )

    __table_args__ = (
        UniqueConstraint(
            "itr_return_id",
            "code",
            "subject_key",
            name="uq_itr_summary_verification_code_subject",
        ),
    )


__all__ = ["ITRSummaryVerification"]

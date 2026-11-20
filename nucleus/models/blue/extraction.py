"""Extraction: one row per model run on a document, one row per figure read."""

from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from typing import Optional
from uuid import UUID, uuid4

from sqlalchemy import CheckConstraint, DateTime, ForeignKey, Index, Integer, Numeric, String, Text, text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func
from sqlalchemy.types import UUID as SQLUUID

from nucleus.db.database import Base
from nucleus.models.blue.constants import BLUE_EXTRACTION_STATUSES, check_in


class BlueExtraction(Base):
    """A single extraction attempt. Re-runs add a row; the old one is marked superseded."""

    __tablename__ = "blue_extractions"
    __table_args__ = (
        CheckConstraint(check_in("status", BLUE_EXTRACTION_STATUSES), name="ck_blue_extractions_status"),
        Index("ix_blue_extractions_document_status", "document_id", "status"),
        # A re-run must mark the previous success "superseded" first: one current result per document.
        Index(
            "uq_blue_extractions_one_succeeded",
            "document_id",
            unique=True,
            postgresql_where=text("status = 'succeeded'"),
        ),
    )

    id: Mapped[UUID] = mapped_column(SQLUUID(as_uuid=True), primary_key=True, default=uuid4)
    document_id: Mapped[UUID] = mapped_column(
        SQLUUID(as_uuid=True), ForeignKey("blue_intake_documents.id", ondelete="CASCADE"), nullable=False
    )
    status: Mapped[str] = mapped_column(String(16), nullable=False, default="queued")
    # Which per-document-type schema the output was validated against, e.g. "form16@1".
    schema_version: Mapped[str] = mapped_column(String(64), nullable=False)
    model: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    input_tokens: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    output_tokens: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    cost_usd: Mapped[Optional[Decimal]] = mapped_column(Numeric(10, 4), nullable=True)
    # Validated structured output, kept whole for re-derivation and debugging.
    result: Mapped[Optional[dict]] = mapped_column(JSONB, nullable=True)
    # Failed arithmetic / consistency checks, e.g. Form 16 gross - exemptions != taxable.
    check_failures: Mapped[list] = mapped_column(JSONB, nullable=False, default=list)
    error: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    started_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    finished_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)


class BlueExtractedField(Base):
    """One figure read from a document, traceable to its page and source text."""

    __tablename__ = "blue_extracted_fields"
    __table_args__ = (
        CheckConstraint("confidence >= 0 AND confidence <= 1", name="ck_blue_extracted_fields_confidence"),
        Index("ix_blue_extracted_fields_extraction_field", "extraction_id", "field_path"),
    )

    id: Mapped[UUID] = mapped_column(SQLUUID(as_uuid=True), primary_key=True, default=uuid4)
    extraction_id: Mapped[UUID] = mapped_column(
        SQLUUID(as_uuid=True), ForeignKey("blue_extractions.id", ondelete="CASCADE"), nullable=False
    )
    # Dotted path within the document schema, e.g. "salary.gross_salary" or "tds[2].amount".
    field_path: Mapped[str] = mapped_column(String(255), nullable=False)
    # Advance-tax head this feeds, e.g. "salary", "interest", "capital_gains.stcg_111a".
    at_head: Mapped[Optional[str]] = mapped_column(String(64), nullable=True, index=True)
    value_text: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    value_amount: Mapped[Optional[Decimal]] = mapped_column(Numeric(18, 2), nullable=True)
    page: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    source_snippet: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    confidence: Mapped[Decimal] = mapped_column(Numeric(4, 3), nullable=False)
    # RM correction: original value stays in value_*; corrected value wins downstream.
    corrected_text: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    corrected_amount: Mapped[Optional[Decimal]] = mapped_column(Numeric(18, 2), nullable=True)
    corrected_by_advisor_id: Mapped[Optional[UUID]] = mapped_column(
        SQLUUID(as_uuid=True), ForeignKey("advisors.id", ondelete="SET NULL"), nullable=True
    )
    corrected_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    correction_reason: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)

"""Intake: one row per email received, one row per document in it."""

from __future__ import annotations

from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4

from sqlalchemy import (
    BigInteger,
    CheckConstraint,
    DateTime,
    ForeignKey,
    Index,
    Numeric,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func
from sqlalchemy.types import UUID as SQLUUID

from nucleus.db.database import Base
from nucleus.models.blue.constants import BLUE_DOCUMENT_TYPES, BLUE_MATCH_STATUSES, check_in


class BlueIntakeMessage(Base):
    """An email that arrived in the intake mailbox. Never deleted."""

    __tablename__ = "blue_intake_messages"
    __table_args__ = (
        UniqueConstraint("mailbox", "internet_message_id", name="uq_blue_intake_messages_mailbox_imid"),
    )

    id: Mapped[UUID] = mapped_column(SQLUUID(as_uuid=True), primary_key=True, default=uuid4)
    mailbox: Mapped[str] = mapped_column(String(320), nullable=False)
    # RFC 5322 Message-ID: stable across folders, the dedupe key.
    internet_message_id: Mapped[str] = mapped_column(String(998), nullable=False)
    graph_message_id: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    conversation_id: Mapped[Optional[str]] = mapped_column(String(512), nullable=True, index=True)
    from_address: Mapped[str] = mapped_column(String(320), nullable=False, index=True)
    from_name: Mapped[Optional[str]] = mapped_column(String(512), nullable=True)
    to_addresses: Mapped[list] = mapped_column(JSONB, nullable=False, default=list)
    cc_addresses: Mapped[list] = mapped_column(JSONB, nullable=False, default=list)
    subject: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    received_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, index=True)
    raw_s3_key: Mapped[Optional[str]] = mapped_column(String(1024), nullable=True)
    # auto_reply / bounce / no_documents / non_client — set when intake ignores the mail.
    ignored_reason: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    processed_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)


class BlueIntakeDocument(Base):
    """One attachment (or a data-bearing email body) and its client match."""

    __tablename__ = "blue_intake_documents"
    __table_args__ = (
        UniqueConstraint("message_id", "sha256", name="uq_blue_intake_documents_message_sha"),
        CheckConstraint(check_in("doc_type", BLUE_DOCUMENT_TYPES), name="ck_blue_intake_documents_doc_type"),
        CheckConstraint(check_in("match_status", BLUE_MATCH_STATUSES), name="ck_blue_intake_documents_match_status"),
        CheckConstraint(
            "match_confidence IS NULL OR (match_confidence >= 0 AND match_confidence <= 1)",
            name="ck_blue_intake_documents_match_confidence",
        ),
        Index("ix_blue_intake_documents_client_status", "client_id", "match_status"),
    )

    id: Mapped[UUID] = mapped_column(SQLUUID(as_uuid=True), primary_key=True, default=uuid4)
    message_id: Mapped[UUID] = mapped_column(
        SQLUUID(as_uuid=True), ForeignKey("blue_intake_messages.id", ondelete="CASCADE"), nullable=False, index=True
    )
    filename: Mapped[str] = mapped_column(String(512), nullable=False)
    content_type: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    size_bytes: Mapped[Optional[int]] = mapped_column(BigInteger, nullable=True)
    # Same file sent twice links to the first copy's extraction instead of re-reading it.
    sha256: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
    s3_key: Mapped[str] = mapped_column(String(1024), nullable=False)
    page_count: Mapped[Optional[int]] = mapped_column(BigInteger, nullable=True)
    is_encrypted: Mapped[Optional[bool]] = mapped_column(nullable=True)
    doc_type: Mapped[str] = mapped_column(String(32), nullable=False, default="unknown")

    client_id: Mapped[Optional[UUID]] = mapped_column(
        SQLUUID(as_uuid=True), ForeignKey("clients.id", ondelete="SET NULL"), nullable=True
    )
    match_status: Mapped[str] = mapped_column(String(32), nullable=False, default="pending")
    match_confidence: Mapped[Optional[float]] = mapped_column(Numeric(4, 3), nullable=True)
    # [{"signal": "pan_in_document", "value": "ABCDE1234F", "client_id": "...", "weight": 0.9}, ...]
    match_evidence: Mapped[list] = mapped_column(JSONB, nullable=False, default=list)
    # Financial year the document relates to, e.g. "2026-27", when the document states it.
    financial_year: Mapped[Optional[str]] = mapped_column(String(9), nullable=True)
    duplicate_of_id: Mapped[Optional[UUID]] = mapped_column(
        SQLUUID(as_uuid=True), ForeignKey("blue_intake_documents.id", ondelete="SET NULL"), nullable=True
    )
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), onupdate=func.now(), nullable=True)

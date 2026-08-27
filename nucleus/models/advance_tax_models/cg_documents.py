"""Advance-tax capital-gains document slots, files, and processing logs.

Replica of ITR ``itr_document_slots`` / ``itr_documents`` /
``itr_document_processing_logs``, keyed by ``quarter_id`` instead of
``financial_year_id``. Used when the request is
``request_portal=adv_tax`` with a compulsory ``quarter_id``.
"""

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Any, List, Optional
from uuid import UUID, uuid4

from sqlalchemy import UUID as SQLUUID
from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, Text, UniqueConstraint
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from nucleus.db.database import Base

if TYPE_CHECKING:
    from nucleus.models.advance_tax_models.brokerage_accounts import BrokerageAccounts
    from nucleus.models.advance_tax_models.quarter import Quarter
    from nucleus.models.common_models.client import Client


class ATCGDocumentSlot(Base):
    __tablename__ = "at_cg_document_slots"

    id: Mapped[UUID] = mapped_column(
        SQLUUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
        index=True,
    )
    quarter_id: Mapped[UUID] = mapped_column(
        SQLUUID(as_uuid=True),
        ForeignKey("quarters.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    client_id: Mapped[UUID] = mapped_column(
        SQLUUID(as_uuid=True),
        ForeignKey("clients.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    doc_type: Mapped[str] = mapped_column(String, nullable=False)
    sub_type: Mapped[str] = mapped_column(String, nullable=False)
    source: Mapped[str] = mapped_column(String, nullable=False)
    region: Mapped[str] = mapped_column(String, nullable=False, server_default="india")
    notes: Mapped[str] = mapped_column(String, nullable=True)
    noted_by: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    noted_by_id: Mapped[Optional[UUID]] = mapped_column(
        SQLUUID(as_uuid=True),
        ForeignKey("advisors.id"),
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), onupdate=func.now(), nullable=True
    )

    quarter: Mapped["Quarter"] = relationship("Quarter", back_populates="cg_document_slots")
    client: Mapped["Client"] = relationship("Client")
    documents: Mapped[List["ATCGDocument"]] = relationship(
        "ATCGDocument",
        back_populates="slot",
        cascade="all, delete-orphan",
    )

    __table_args__ = (
        UniqueConstraint(
            "quarter_id",
            "client_id",
            "doc_type",
            "sub_type",
            "source",
            "region",
            "notes",
            name="uq_at_cg_doc_slot",
            postgresql_nulls_not_distinct=True,
        ),
    )


class ATCGDocument(Base):
    __tablename__ = "at_cg_documents"

    id: Mapped[UUID] = mapped_column(
        SQLUUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
        index=True,
    )
    slot_id: Mapped[UUID] = mapped_column(
        SQLUUID(as_uuid=True),
        ForeignKey("at_cg_document_slots.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    file_name: Mapped[str] = mapped_column(String, nullable=False)
    s3_key: Mapped[str] = mapped_column(String, nullable=False)
    bucket_name: Mapped[str] = mapped_column(String, nullable=False)

    is_password_protected: Mapped[bool] = mapped_column(
        Boolean, default=False, server_default="FALSE"
    )
    updated_by: Mapped[Optional[str]] = mapped_column(
        String, nullable=True, default="client", server_default="client"
    )
    updated_by_advisor_id: Mapped[Optional[UUID]] = mapped_column(
        SQLUUID(as_uuid=True),
        ForeignKey("advisors.id"),
        nullable=True,
    )
    password: Mapped[str] = mapped_column(String, nullable=True)
    status: Mapped[str] = mapped_column(String, nullable=True)
    advisor_comment: Mapped[Optional[str]] = mapped_column(String, nullable=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), onupdate=func.now(), nullable=True
    )

    slot: Mapped["ATCGDocumentSlot"] = relationship(
        "ATCGDocumentSlot", back_populates="documents"
    )
    processing_logs: Mapped[List["ATCGDocumentProcessingLog"]] = relationship(
        "ATCGDocumentProcessingLog",
        back_populates="document",
        cascade="all, delete-orphan",
    )
    brokerage_accounts: Mapped[List["BrokerageAccounts"]] = relationship(
        "BrokerageAccounts",
        back_populates="source_document",
    )


class ATCGDocumentProcessingLog(Base):
    """One processing attempt for an uploaded advance-tax CG document."""

    __tablename__ = "at_cg_document_processing_logs"

    id: Mapped[UUID] = mapped_column(
        SQLUUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
        index=True,
    )
    document_id: Mapped[UUID] = mapped_column(
        SQLUUID(as_uuid=True),
        ForeignKey("at_cg_documents.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    processing_source: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    attempt_number: Mapped[int] = mapped_column(Integer, nullable=False)
    status: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
    llm_model: Mapped[Optional[str]] = mapped_column(String(128), nullable=True)
    error_message: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    error_metadata: Mapped[Optional[dict[str, Any]]] = mapped_column(JSONB, nullable=True)
    processing_duration_ms: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    triggered_by: Mapped[Optional[str]] = mapped_column(String(32), nullable=True)
    triggered_by_advisor_id: Mapped[Optional[UUID]] = mapped_column(
        SQLUUID(as_uuid=True),
        ForeignKey("advisors.id"),
        nullable=True,
        index=True,
    )
    started_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )
    completed_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    document: Mapped["ATCGDocument"] = relationship(
        "ATCGDocument", back_populates="processing_logs"
    )

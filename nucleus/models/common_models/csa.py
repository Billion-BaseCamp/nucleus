"""Slim Client Service Agreement tables.

Five tables. Clause flags are booleans on the agreement. Duplicate file names
stay as warning rows. The wide extraction that was loaded first lives in
``csa_raw.py`` (``*_raw`` tables).

Index and key names here are distinct from the names still attached to those
renamed tables.
"""

from __future__ import annotations

from datetime import date, datetime
from typing import List, Optional
from uuid import UUID, uuid4

from sqlalchemy import (
    Boolean,
    CheckConstraint,
    Date,
    DateTime,
    Enum,
    ForeignKey,
    Index,
    Integer,
    Numeric,
    PrimaryKeyConstraint,
    String,
    Text,
    text,
    UUID as SQLUUID,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from nucleus.core.constants import (
    CSAFeeType,
    CSAInclusion,
    CSALegalEntity,
    CSAMatchTier,
    CSAReviewStatus,
    CSAServiceCode,
)
from nucleus.db.database import Base


class CSADocument(Base):
    """One signed CSA PDF."""

    __tablename__ = "csa_documents"
    __table_args__ = (
        PrimaryKeyConstraint("id", name="pk_csa_documents"),
        Index("uq_csa_documents_sha256", "sha256", unique=True),
        Index(
            "uq_csa_documents_envelope",
            "docusign_envelope_id",
            unique=True,
            postgresql_where=text("docusign_envelope_id IS NOT NULL"),
        ),
        Index("ix_csa_documents_review_status", "review_status"),
    )

    id: Mapped[UUID] = mapped_column(SQLUUID(as_uuid=True), default=uuid4)

    file_name: Mapped[str] = mapped_column(String, nullable=False)
    sha256: Mapped[str] = mapped_column(String(64), nullable=False)
    page_count: Mapped[int] = mapped_column(Integer, nullable=False)
    docusign_envelope_id: Mapped[Optional[str]] = mapped_column(String, nullable=True)

    legal_entity: Mapped[Optional[CSALegalEntity]] = mapped_column(Enum(CSALegalEntity), nullable=True)

    retainer_start: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    retainer_end: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    signed_date_bbc: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    signed_date_client: Mapped[Optional[date]] = mapped_column(Date, nullable=True)

    refund_terms: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    aum_amount: Mapped[Optional[float]] = mapped_column(Numeric(20, 4), nullable=True)
    aum_currency: Mapped[Optional[str]] = mapped_column(String(3), nullable=True)

    is_service_agreement: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    not_csa_reason: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    review_status: Mapped[CSAReviewStatus] = mapped_column(
        Enum(CSAReviewStatus), default=CSAReviewStatus.PENDING, nullable=False
    )

    affiliate_transfer: Mapped[bool] = mapped_column(Boolean, nullable=False)
    ai_data_sharing: Mapped[bool] = mapped_column(Boolean, nullable=False)
    third_party_firm_sharing: Mapped[bool] = mapped_column(Boolean, nullable=False)
    confidentiality_survives: Mapped[bool] = mapped_column(Boolean, nullable=False)
    scrutiny_excluded: Mapped[bool] = mapped_column(Boolean, nullable=False)

    parties: Mapped[List["CSAParty"]] = relationship(
        "CSAParty", back_populates="document", cascade="all, delete-orphan"
    )
    fees: Mapped[List["CSAFee"]] = relationship(
        "CSAFee", back_populates="document", cascade="all, delete-orphan"
    )
    services: Mapped[List["CSAService"]] = relationship(
        "CSAService", back_populates="document", cascade="all, delete-orphan"
    )
    warnings: Mapped[List["CSAParseWarning"]] = relationship(
        "CSAParseWarning", back_populates="document", cascade="all, delete-orphan"
    )

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), onupdate=func.now(), nullable=True)


class CSAParty(Base):
    """One person named in a CSA."""

    __tablename__ = "csa_parties"
    __table_args__ = (
        PrimaryKeyConstraint("id", name="pk_csa_parties"),
        Index("ix_csa_parties_client_id", "client_id"),
        Index("ix_csa_parties_document", "csa_document_id"),
        Index(
            "ix_csa_parties_unmapped_doc",
            "csa_document_id",
            postgresql_where=text("client_id IS NULL"),
        ),
        CheckConstraint(
            "(client_id IS NULL) = (match_tier IS NULL)",
            name="ck_csa_parties_link_tier",
        ),
    )

    id: Mapped[UUID] = mapped_column(SQLUUID(as_uuid=True), default=uuid4)
    csa_document_id: Mapped[UUID] = mapped_column(
        SQLUUID(as_uuid=True),
        ForeignKey("csa_documents.id", ondelete="CASCADE", name="fk_csa_parties_document"),
        nullable=False,
    )
    client_id: Mapped[Optional[UUID]] = mapped_column(
        SQLUUID(as_uuid=True),
        ForeignKey("clients.id", ondelete="RESTRICT", name="fk_csa_parties_client"),
        nullable=True,
    )

    role: Mapped[str] = mapped_column(String, nullable=False)  # primary | family_member
    relation_in_document: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    name_in_document: Mapped[str] = mapped_column(String, nullable=False)
    email_in_document: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    mobile_in_document: Mapped[Optional[str]] = mapped_column(String, nullable=True)

    auth_receive_info: Mapped[Optional[bool]] = mapped_column(Boolean, nullable=True)
    auth_financial_decisions: Mapped[Optional[bool]] = mapped_column(Boolean, nullable=True)

    match_tier: Mapped[Optional[CSAMatchTier]] = mapped_column(Enum(CSAMatchTier), nullable=True)
    matched_by_advisor_id: Mapped[Optional[UUID]] = mapped_column(
        SQLUUID(as_uuid=True),
        ForeignKey("advisors.id", name="fk_csa_parties_matched_by"),
        nullable=True,
    )
    matched_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)

    document: Mapped["CSADocument"] = relationship("CSADocument", back_populates="parties")


class CSAFee(Base):
    """One charge. An amount, a rate, or an explicit unpriced row."""

    __tablename__ = "csa_fees"
    __table_args__ = (
        PrimaryKeyConstraint("id", name="pk_csa_fees"),
        CheckConstraint(
            "amount IS NOT NULL OR percentage_value IS NOT NULL OR is_unquantified",
            name="ck_csa_fees_has_value",
        ),
        CheckConstraint(
            "NOT (is_unquantified AND (amount IS NOT NULL OR percentage_value IS NOT NULL))",
            name="ck_csa_fees_unquantified_empty",
        ),
        CheckConstraint(
            "amount IS NULL OR currency IS NOT NULL",
            name="ck_csa_fees_amount_currency",
        ),
        Index("ix_csa_fees_csa_document_id", "csa_document_id"),
        Index(
            "ix_csa_fees_priced_rows",
            "csa_document_id",
            postgresql_where=text("NOT is_unquantified"),
        ),
    )

    id: Mapped[UUID] = mapped_column(SQLUUID(as_uuid=True), default=uuid4)
    csa_document_id: Mapped[UUID] = mapped_column(
        SQLUUID(as_uuid=True),
        ForeignKey("csa_documents.id", ondelete="CASCADE", name="fk_csa_fees_document"),
        nullable=False,
    )

    component_label: Mapped[str] = mapped_column(String, nullable=False)
    fee_type: Mapped[CSAFeeType] = mapped_column(Enum(CSAFeeType), nullable=False)

    amount: Mapped[Optional[float]] = mapped_column(Numeric(20, 4), nullable=True)
    currency: Mapped[Optional[str]] = mapped_column(String(3), nullable=True)
    is_unquantified: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    percentage_value: Mapped[Optional[float]] = mapped_column(Numeric(9, 4), nullable=True)
    percentage_basis: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    period_months: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)

    plan_name: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    hurdle_rate_pct: Mapped[Optional[float]] = mapped_column(Numeric(9, 4), nullable=True)
    high_water_mark: Mapped[Optional[bool]] = mapped_column(Boolean, nullable=True)

    gst_applicable: Mapped[Optional[bool]] = mapped_column(Boolean, nullable=True)
    verbatim: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    source_page: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)

    document: Mapped["CSADocument"] = relationship("CSADocument", back_populates="fees")


class CSAService(Base):
    """One service line."""

    __tablename__ = "csa_services"
    __table_args__ = (
        PrimaryKeyConstraint("id", name="pk_csa_services"),
        Index("ix_csa_services_canonical_code", "canonical_code"),
        Index("ix_csa_services_csa_document_id", "csa_document_id"),
        Index("ix_csa_services_code_and_inclusion", "canonical_code", "inclusion"),
    )

    id: Mapped[UUID] = mapped_column(SQLUUID(as_uuid=True), default=uuid4)
    csa_document_id: Mapped[UUID] = mapped_column(
        SQLUUID(as_uuid=True),
        ForeignKey("csa_documents.id", ondelete="CASCADE", name="fk_csa_services_document"),
        nullable=False,
    )

    fy: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    canonical_code: Mapped[CSAServiceCode] = mapped_column(Enum(CSAServiceCode), nullable=False)
    inclusion: Mapped[CSAInclusion] = mapped_column(Enum(CSAInclusion), nullable=False)
    verbatim_text: Mapped[str] = mapped_column(Text, nullable=False)
    unit_amount: Mapped[Optional[float]] = mapped_column(Numeric(20, 4), nullable=True)
    unit_currency: Mapped[Optional[str]] = mapped_column(String(3), nullable=True)
    source_page: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)

    document: Mapped["CSADocument"] = relationship("CSADocument", back_populates="services")


class CSAParseWarning(Base):
    """One review issue. Duplicate-file and same-envelope notes stay here."""

    __tablename__ = "csa_parse_warnings"
    __table_args__ = (
        PrimaryKeyConstraint("id", name="pk_csa_parse_warnings"),
        Index("ix_csa_parse_warnings_csa_document_id", "csa_document_id"),
        Index("ix_csa_parse_warnings_warning_code", "warning_code"),
    )

    id: Mapped[UUID] = mapped_column(SQLUUID(as_uuid=True), default=uuid4)
    csa_document_id: Mapped[UUID] = mapped_column(
        SQLUUID(as_uuid=True),
        ForeignKey("csa_documents.id", ondelete="CASCADE", name="fk_csa_parse_warnings_document"),
        nullable=False,
    )
    warning_code: Mapped[str] = mapped_column(String, nullable=False)
    severity: Mapped[str] = mapped_column(String, nullable=False)  # blocker | review | note
    message: Mapped[str] = mapped_column(Text, nullable=False)
    resolved: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    document: Mapped["CSADocument"] = relationship("CSADocument", back_populates="warnings")

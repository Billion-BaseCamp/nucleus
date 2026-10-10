"""Preserved wide CSA tables (``*_raw``).

The live agreements are the slim models in ``csa.py``.

Original notes:

Goal: map existing CSA documents onto clients we ALREADY have, and make the
agreements browsable. Nothing here creates, edits or promotes a client.

Design constraints agreed with Akash 2026-09-25:

* Every document in the corpus is a CSA. There is NO doc_type discriminator —
  percentage-fee investment-advisory deals are CSAs whose fee rows are rate rows.
* ``csa_parties_raw.client_id`` NULL = we could not map that name. Normal and
  permanent; the row is flagged unmapped and nothing else happens. Unmapped
  names are mostly family members who are not clients.
* Every extracted value is auditable back to the page it came from.
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
    String,
    Text,
    UniqueConstraint,
    UUID as SQLUUID,
    text,
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


class CSADocumentRaw(Base):
    """One signed CSA PDF.

    ``docusign_envelope_id`` is the true document identity — filenames lie. Two
    files with different bytes share an envelope (same agreement re-exported),
    and a ``_1`` suffix can be an unrelated engagement rather than a version.
    """

    __tablename__ = "csa_documents_raw"
    __table_args__ = (
        UniqueConstraint("sha256", name="uix_csa_documents_sha256"),
        # One row per envelope among non-superseded documents. Envelope is NULL
        # for the rare PDF with no DocuSign header, so the index is partial.
        Index(
            "uix_csa_documents_envelope",
            "docusign_envelope_id",
            unique=True,
            postgresql_where=text(
                "docusign_envelope_id IS NOT NULL AND superseded_by_id IS NULL"
            ),
        ),
        Index("ix_csa_documents_review", "review_status"),
    )

    id: Mapped[UUID] = mapped_column(SQLUUID(as_uuid=True), primary_key=True, default=uuid4, index=True)

    # --- source of truth -------------------------------------------------
    file_name: Mapped[str] = mapped_column(String, nullable=False)
    source_path: Mapped[str] = mapped_column(String, nullable=False)   # SharePoint server-relative URL
    sha256: Mapped[str] = mapped_column(String(64), nullable=False)
    page_count: Mapped[int] = mapped_column(Integer, nullable=False)
    docusign_envelope_id: Mapped[Optional[str]] = mapped_column(String, nullable=True, index=True)

    # --- agreement identity ----------------------------------------------
    legal_entity: Mapped[Optional[CSALegalEntity]] = mapped_column(
        Enum(CSALegalEntity, native_enum=False, length=10),
        nullable=True,
    )
    covers_family: Mapped[Optional[bool]] = mapped_column(Boolean, nullable=True)

    # --- term --------------------------------------------------------------
    retainer_start: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    retainer_end: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    signed_date_bbc: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    signed_date_client: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    place_bbc: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    place_client: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    notice_period_days: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    liability_cap_amount: Mapped[Optional[float]] = mapped_column(Numeric(20, 4), nullable=True)
    liability_cap_currency: Mapped[Optional[str]] = mapped_column(String(3), nullable=True)
    governing_law: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    jurisdiction: Mapped[Optional[str]] = mapped_column(String, nullable=True)

    # Refund is ASYMMETRIC in most of these agreements: nothing is refunded when
    # the CLIENT terminates, but a pro-rata refund is payable when BBC does. One
    # boolean cannot hold that, and ~12% of extractions put the whole sentence in
    # this field rather than lose the second half. So: the boolean answers only
    # "is a refund payable when the CLIENT terminates", and the full clause is
    # kept verbatim alongside it.
    refund_on_termination: Mapped[Optional[bool]] = mapped_column(Boolean, nullable=True)
    refund_terms: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # AUM is an investment amount, never a fee — it lives here, not in csa_fees_raw.
    aum_amount: Mapped[Optional[float]] = mapped_column(Numeric(20, 4), nullable=True)
    aum_currency: Mapped[Optional[str]] = mapped_column(String(3), nullable=True)

    # --- extraction provenance ---------------------------------------------
    extraction_method: Mapped[str] = mapped_column(String, nullable=False)  # text | mixed | ocr
    ocr_page_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    extraction_confidence: Mapped[Optional[float]] = mapped_column(Numeric(4, 3), nullable=True)
    extraction_run_id: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    raw_text: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # The folder is "ClientCSA" but not every PDF in it is a service agreement:
    # at least one is a Share Purchase Agreement where Klok is the SELLER and the
    # money flows FROM the client. Such rows must never be aggregated as service
    # revenue. False = it is not a CSA; the reason goes in `not_csa_reason`.
    is_service_agreement: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    not_csa_reason: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    review_status: Mapped[CSAReviewStatus] = mapped_column(
        Enum(CSAReviewStatus, native_enum=False, length=20),
        default=CSAReviewStatus.PENDING,
        nullable=False,
    )
    reviewed_by_advisor_id: Mapped[Optional[UUID]] = mapped_column(
        SQLUUID(as_uuid=True), ForeignKey("advisors.id"), nullable=True
    )
    reviewed_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)

    # A later CSA that replaces this one (renewal / re-execution).
    superseded_by_id: Mapped[Optional[UUID]] = mapped_column(
        SQLUUID(as_uuid=True), ForeignKey("csa_documents_raw.id", ondelete="SET NULL"), nullable=True
    )

    parties: Mapped[List["CSAPartyRaw"]] = relationship(
        "CSAPartyRaw", back_populates="document", cascade="all, delete-orphan"
    )
    fees: Mapped[List["CSAFeeRaw"]] = relationship(
        "CSAFeeRaw", back_populates="document", cascade="all, delete-orphan"
    )
    services: Mapped[List["CSAServiceRaw"]] = relationship(
        "CSAServiceRaw", back_populates="document", cascade="all, delete-orphan"
    )
    clause_flags: Mapped[List["CSAClauseFlagRaw"]] = relationship(
        "CSAClauseFlagRaw", back_populates="document", cascade="all, delete-orphan"
    )
    warnings: Mapped[List["CSAParseWarningRaw"]] = relationship(
        "CSAParseWarningRaw", back_populates="document", cascade="all, delete-orphan"
    )

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), onupdate=func.now(), nullable=True)


class CSAPartyRaw(Base):
    """A person named in a CSA, linked to an existing client where we can.

    The goal is mapping CSAs onto clients we already have. Nothing here creates
    or edits a client — this table never writes to ``clients``.

    ``client_id`` NULL means we could not map this name. That is a normal,
    permanent state: the row keeps the name, relation and contact details the
    PDF stated, stays visible on the document, and is simply flagged as
    unmapped. Most unmapped rows are family members (children, in-laws) who are
    not clients and were never meant to be.

    ``match_tier`` says how a link was made; ``EXACT`` and ``CROSSWALK`` are
    written by the pipeline, ``MANUAL`` by a human confirming a suggestion. A
    fuzzy suggestion is never auto-linked — it is recorded in
    ``match_candidates`` and left NULL for someone to confirm or ignore.
    """

    __tablename__ = "csa_parties_raw"
    __table_args__ = (
        Index("ix_csa_parties_client", "client_id"),
        # The flag: every party we could not map to a client.
        Index(
            "ix_csa_parties_unmapped",
            "csa_document_id",
            postgresql_where=text("client_id IS NULL"),
        ),
        CheckConstraint(
            "match_confidence IS NULL OR (match_confidence >= 0 AND match_confidence <= 1)",
            name="ck_csa_parties_confidence_range",
        ),
        # A link must say how it was made; an unlinked row must not claim one.
        CheckConstraint(
            "(client_id IS NULL) = (match_tier IS NULL)",
            name="ck_csa_parties_link_has_tier",
        ),
    )

    id: Mapped[UUID] = mapped_column(SQLUUID(as_uuid=True), primary_key=True, default=uuid4)
    csa_document_id: Mapped[UUID] = mapped_column(
        SQLUUID(as_uuid=True), ForeignKey("csa_documents_raw.id", ondelete="CASCADE"), nullable=False, index=True
    )

    # The link. NULL = not yet resolved to a client; the review queue works this.
    client_id: Mapped[Optional[UUID]] = mapped_column(
        SQLUUID(as_uuid=True), ForeignKey("clients.id", ondelete="RESTRICT"), nullable=True
    )

    role: Mapped[str] = mapped_column(String, nullable=False)            # primary | family_member
    relation_in_document: Mapped[Optional[str]] = mapped_column(String, nullable=True)  # Self/Spouse/Father...

    # --- what the PDF literally said (evidence, not master data) -----------
    name_in_document: Mapped[str] = mapped_column(String, nullable=False)
    email_in_document: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    mobile_in_document: Mapped[Optional[str]] = mapped_column(String, nullable=True)

    # --- authorization chart -----------------------------------------------
    auth_receive_info: Mapped[Optional[bool]] = mapped_column(Boolean, nullable=True)
    auth_financial_decisions: Mapped[Optional[bool]] = mapped_column(Boolean, nullable=True)

    # --- how the link was made ---------------------------------------------
    match_tier: Mapped[Optional[CSAMatchTier]] = mapped_column(
        Enum(CSAMatchTier, native_enum=False, length=20),
        nullable=True,
    )
    match_confidence: Mapped[Optional[float]] = mapped_column(Numeric(4, 3), nullable=True)
    # JSON: fuzzy candidates with scores, for a human to confirm or ignore.
    match_candidates: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    matched_by_advisor_id: Mapped[Optional[UUID]] = mapped_column(
        SQLUUID(as_uuid=True), ForeignKey("advisors.id"), nullable=True
    )
    matched_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)

    document: Mapped["CSADocumentRaw"] = relationship("CSADocumentRaw", back_populates="parties")

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), onupdate=func.now(), nullable=True)


class CSAFeeRaw(Base):
    """One charge in a CSA.

    A row is EITHER an absolute amount (``amount`` + ``currency``) OR a rate
    (``percentage_value`` + ``percentage_basis``) — never neither. Retainer rows
    and rate rows coexist in one agreement.

    ``hurdle_rate_pct`` is per ROW, not per document: the same agreement sets
    different hurdles per investment plan (8/6, 5/2.5, 4/2 all observed).
    """

    __tablename__ = "csa_fees_raw"
    __table_args__ = (
        # A row must say something: an amount, a rate, or an explicit statement
        # that the price is deliberately unquantified ("mutually agreed at
        # renewal"). The third case is a real contractual fact — dropping those
        # rows would lose the knowledge that a renewal/extra charge exists.
        CheckConstraint(
            "amount IS NOT NULL OR percentage_value IS NOT NULL OR is_unquantified",
            name="ck_csa_fees_amount_rate_or_unquantified",
        ),
        CheckConstraint(
            "NOT (is_unquantified AND (amount IS NOT NULL OR percentage_value IS NOT NULL))",
            name="ck_csa_fees_unquantified_has_no_value",
        ),
        CheckConstraint(
            "amount IS NULL OR currency IS NOT NULL",
            name="ck_csa_fees_amount_needs_currency",
        ),
        Index("ix_csa_fees_document", "csa_document_id"),
        # Revenue queries must be able to exclude unpriced rows cheaply.
        Index(
            "ix_csa_fees_priced",
            "csa_document_id",
            postgresql_where=text("NOT is_unquantified"),
        ),
    )

    id: Mapped[UUID] = mapped_column(SQLUUID(as_uuid=True), primary_key=True, default=uuid4)
    csa_document_id: Mapped[UUID] = mapped_column(
        SQLUUID(as_uuid=True), ForeignKey("csa_documents_raw.id", ondelete="CASCADE"), nullable=False
    )

    component_label: Mapped[str] = mapped_column(String, nullable=False)
    fee_type: Mapped[CSAFeeType] = mapped_column(
        Enum(CSAFeeType, native_enum=False, length=20),
        nullable=False,
    )

    amount: Mapped[Optional[float]] = mapped_column(Numeric(20, 4), nullable=True)
    currency: Mapped[Optional[str]] = mapped_column(String(3), nullable=True)

    # True when the document states a charge exists but deliberately does not
    # price it ("mutually agreed at the time of renewal", "separate mutually
    # agreed fees for items not covered"). Distinct from a failed extraction:
    # this is what the contract says, not something we could not read.
    # Always exclude these rows from revenue arithmetic.
    is_unquantified: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    percentage_value: Mapped[Optional[float]] = mapped_column(Numeric(9, 4), nullable=True)
    percentage_basis: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    hurdle_rate_pct: Mapped[Optional[float]] = mapped_column(Numeric(9, 4), nullable=True)
    high_water_mark: Mapped[Optional[bool]] = mapped_column(Boolean, nullable=True)
    period_months: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)

    # Groups rate rows belonging to one investment plan ("Indian Equity",
    # "Global debt & alternate investments"). Not a separate structure.
    plan_name: Mapped[Optional[str]] = mapped_column(String, nullable=True)

    gst_applicable: Mapped[Optional[bool]] = mapped_column(Boolean, nullable=True)
    payment_trigger: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    fy_applicable: Mapped[Optional[str]] = mapped_column(String, nullable=True)

    verbatim: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    source_page: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    source_method: Mapped[Optional[str]] = mapped_column(String, nullable=True)  # text | ocr
    confidence: Mapped[Optional[float]] = mapped_column(Numeric(4, 3), nullable=True)

    document: Mapped["CSADocumentRaw"] = relationship("CSADocumentRaw", back_populates="fees")


class CSAServiceRaw(Base):
    """One service line, normalised to a canonical code but keeping its wording.

    ``inclusion`` carries as much meaning as the code itself: ``excluded`` rows
    (e.g. "except scrutiny notices") are negative entitlements and must not be
    read as services provided.
    """

    __tablename__ = "csa_services_raw"
    __table_args__ = (
        Index("ix_csa_services_code", "canonical_code"),
        Index("ix_csa_services_document", "csa_document_id"),
        Index("ix_csa_services_code_inclusion", "canonical_code", "inclusion"),
    )

    id: Mapped[UUID] = mapped_column(SQLUUID(as_uuid=True), primary_key=True, default=uuid4)
    csa_document_id: Mapped[UUID] = mapped_column(
        SQLUUID(as_uuid=True), ForeignKey("csa_documents_raw.id", ondelete="CASCADE"), nullable=False
    )

    canonical_code: Mapped[CSAServiceCode] = mapped_column(
        Enum(CSAServiceCode, native_enum=False, length=30),
        nullable=False,
    )
    inclusion: Mapped[CSAInclusion] = mapped_column(
        Enum(CSAInclusion, native_enum=False, length=25),
        nullable=False,
    )

    verbatim_text: Mapped[str] = mapped_column(Text, nullable=False)
    fy: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    quantity: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)

    # Per-item price for a-la-carte service tables.
    unit_amount: Mapped[Optional[float]] = mapped_column(Numeric(20, 4), nullable=True)
    unit_currency: Mapped[Optional[str]] = mapped_column(String(3), nullable=True)

    source_page: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    source_method: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    confidence: Mapped[Optional[float]] = mapped_column(Numeric(4, 3), nullable=True)

    document: Mapped["CSADocumentRaw"] = relationship("CSADocumentRaw", back_populates="services")


class CSAClauseFlagRaw(Base):
    """Presence of a template clause. Tracks template drift across generations.

    ``ai_data_sharing`` gates whether a client's text may be sent to an external
    model — the newer KLOK template permits it, the older BFAPL one does not.
    """

    __tablename__ = "csa_clause_flags_raw"
    __table_args__ = (
        UniqueConstraint("csa_document_id", "clause_key", name="uix_csa_clause_flag"),
    )

    id: Mapped[UUID] = mapped_column(SQLUUID(as_uuid=True), primary_key=True, default=uuid4)
    csa_document_id: Mapped[UUID] = mapped_column(
        SQLUUID(as_uuid=True), ForeignKey("csa_documents_raw.id", ondelete="CASCADE"), nullable=False
    )
    clause_key: Mapped[str] = mapped_column(String, nullable=False)
    present: Mapped[bool] = mapped_column(Boolean, nullable=False)
    verbatim: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    source_page: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)

    document: Mapped["CSADocumentRaw"] = relationship("CSADocumentRaw", back_populates="clause_flags")


class CSAParseWarningRaw(Base):
    """Why a document is in the review queue. One row per issue, machine-generated."""

    __tablename__ = "csa_parse_warnings_raw"
    __table_args__ = (
        Index("ix_csa_parse_warnings_document", "csa_document_id"),
        Index("ix_csa_parse_warnings_code", "warning_code"),
    )

    id: Mapped[UUID] = mapped_column(SQLUUID(as_uuid=True), primary_key=True, default=uuid4)
    csa_document_id: Mapped[UUID] = mapped_column(
        SQLUUID(as_uuid=True), ForeignKey("csa_documents_raw.id", ondelete="CASCADE"), nullable=False
    )
    warning_code: Mapped[str] = mapped_column(String, nullable=False)   # e.g. CURRENCY_MISMATCH
    severity: Mapped[str] = mapped_column(String, nullable=False)       # blocker | review | note
    message: Mapped[str] = mapped_column(Text, nullable=False)
    field_path: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    resolved: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    resolved_by_advisor_id: Mapped[Optional[UUID]] = mapped_column(
        SQLUUID(as_uuid=True), ForeignKey("advisors.id"), nullable=True
    )
    resolved_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    resolution_note: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    document: Mapped["CSADocumentRaw"] = relationship("CSADocumentRaw", back_populates="warnings")

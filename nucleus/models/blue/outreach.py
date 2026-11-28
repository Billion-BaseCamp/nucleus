"""Outreach: client emails BLUE drafts, and every RM approval it waits on."""

from __future__ import annotations

from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4

from sqlalchemy import CheckConstraint, DateTime, ForeignKey, Index, String, Text, text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func
from sqlalchemy.types import UUID as SQLUUID

from nucleus.db.database import Base
from nucleus.models.blue.constants import (
    BLUE_APPROVAL_KINDS,
    BLUE_APPROVAL_STATUSES,
    BLUE_DRAFT_REQUEST_RESULTS,
    BLUE_EMAIL_STATUSES,
    check_in,
)


class BlueClientEmail(Base):
    """A client email. Nothing is sent unless an approved BlueApproval points at it."""

    __tablename__ = "blue_client_emails"
    __table_args__ = (
        CheckConstraint(check_in("status", BLUE_EMAIL_STATUSES), name="ck_blue_client_emails_status"),
        CheckConstraint(
            "status <> 'sent' OR (sent_at IS NOT NULL AND approval_id IS NOT NULL)",
            name="ck_blue_client_emails_sent_needs_approval",
        ),
        Index("ix_blue_client_emails_client_status", "client_id", "status"),
    )

    id: Mapped[UUID] = mapped_column(SQLUUID(as_uuid=True), primary_key=True, default=uuid4)
    client_id: Mapped[UUID] = mapped_column(
        SQLUUID(as_uuid=True), ForeignKey("clients.id", ondelete="CASCADE"), nullable=False
    )
    advisor_id: Mapped[UUID] = mapped_column(
        SQLUUID(as_uuid=True), ForeignKey("advisors.id", ondelete="CASCADE"), nullable=False, index=True
    )
    review_id: Mapped[Optional[UUID]] = mapped_column(
        SQLUUID(as_uuid=True), ForeignKey("blue_quarter_reviews.id", ondelete="SET NULL"), nullable=True
    )
    # Reply in the client's own thread so their answer comes back to intake.
    in_reply_to_message_id: Mapped[Optional[UUID]] = mapped_column(
        SQLUUID(as_uuid=True), ForeignKey("blue_intake_messages.id", ondelete="SET NULL"), nullable=True
    )
    purpose: Mapped[str] = mapped_column(String(64), nullable=False)
    to_addresses: Mapped[list] = mapped_column(JSONB, nullable=False)
    cc_addresses: Mapped[list] = mapped_column(JSONB, nullable=False, default=list)
    subject: Mapped[str] = mapped_column(Text, nullable=False)
    body_text: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[str] = mapped_column(String(32), nullable=False, default="draft")
    approval_id: Mapped[Optional[UUID]] = mapped_column(
        SQLUUID(as_uuid=True), ForeignKey("blue_approvals.id", ondelete="SET NULL"), nullable=True
    )
    graph_message_id: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    sent_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    error: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), onupdate=func.now(), nullable=True)


class BlueApproval(Base):
    """An RM decision BLUE asked for: client match, client email, write-back, correction."""

    __tablename__ = "blue_approvals"
    __table_args__ = (
        CheckConstraint(check_in("kind", BLUE_APPROVAL_KINDS), name="ck_blue_approvals_kind"),
        CheckConstraint(check_in("status", BLUE_APPROVAL_STATUSES), name="ck_blue_approvals_status"),
        CheckConstraint(
            "status = 'pending' OR (decided_at IS NOT NULL)",
            name="ck_blue_approvals_decided_at",
        ),
        Index("ix_blue_approvals_advisor_status", "advisor_id", "status"),
        # At most one open request per thing being approved, so an action can't be approved and run twice.
        Index(
            "uq_blue_approvals_pending_subject",
            "kind",
            "subject_id",
            unique=True,
            postgresql_where=text("status = 'pending'"),
        ),
    )

    id: Mapped[UUID] = mapped_column(SQLUUID(as_uuid=True), primary_key=True, default=uuid4)
    kind: Mapped[str] = mapped_column(String(32), nullable=False)
    status: Mapped[str] = mapped_column(String(16), nullable=False, default="pending")
    advisor_id: Mapped[UUID] = mapped_column(
        SQLUUID(as_uuid=True), ForeignKey("advisors.id", ondelete="CASCADE"), nullable=False
    )
    client_id: Mapped[Optional[UUID]] = mapped_column(
        SQLUUID(as_uuid=True), ForeignKey("clients.id", ondelete="CASCADE"), nullable=True, index=True
    )
    # What is being approved, by kind: document_id / email_id / review_id / field_id.
    subject_id: Mapped[UUID] = mapped_column(SQLUUID(as_uuid=True), nullable=False, index=True)
    # Exactly what the RM saw (e.g. the write-back diff), so the decision is auditable.
    proposal: Mapped[dict] = mapped_column(JSONB, nullable=False, default=dict)
    decided_by_advisor_id: Mapped[Optional[UUID]] = mapped_column(
        SQLUUID(as_uuid=True), ForeignKey("advisors.id", ondelete="SET NULL"), nullable=True
    )
    decided_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    decision_note: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    expires_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)


class BlueDraftRequest(Base):
    """One Draft email the dashboard asked for. The API inserts it and waits. The worker drafts it.

    Send now can stamp an approval because the draft already exists. A draft request does not, so it has its own row.
    Generate the table with Alembic autogenerate. Do not hand-write the migration.
    """

    __tablename__ = "blue_draft_requests"
    __table_args__ = (
        CheckConstraint(
            "result IS NULL OR " + check_in("result", BLUE_DRAFT_REQUEST_RESULTS),
            name="ck_blue_draft_requests_result",
        ),
        Index(
            "ix_blue_draft_requests_pending",
            "requested_at",
            postgresql_where=text("done_at IS NULL"),
        ),
    )

    id: Mapped[UUID] = mapped_column(SQLUUID(as_uuid=True), primary_key=True, default=uuid4)
    client_id: Mapped[UUID] = mapped_column(
        SQLUUID(as_uuid=True), ForeignKey("clients.id", ondelete="CASCADE"), nullable=False, index=True
    )
    advisor_id: Mapped[UUID] = mapped_column(
        SQLUUID(as_uuid=True), ForeignKey("advisors.id", ondelete="CASCADE"), nullable=False
    )
    kind: Mapped[str] = mapped_column(String(32), nullable=False)
    question: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    file_name: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    via: Mapped[str] = mapped_column(String(16), nullable=False, default="dashboard")
    # Filled by the worker. actual_kind can differ from kind (a request may come out as a reminder).
    result: Mapped[Optional[str]] = mapped_column(String(16), nullable=True)
    reason: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    actual_kind: Mapped[Optional[str]] = mapped_column(String(32), nullable=True)
    email_id: Mapped[Optional[UUID]] = mapped_column(SQLUUID(as_uuid=True), nullable=True)
    approval_id: Mapped[Optional[UUID]] = mapped_column(SQLUUID(as_uuid=True), nullable=True)
    subject: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    why: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    card_note: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    requested_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    claimed_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    done_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)

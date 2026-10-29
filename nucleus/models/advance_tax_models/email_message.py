from datetime import datetime
from uuid import UUID, uuid4

from sqlalchemy import DateTime, ForeignKey, Index, String, Text, UniqueConstraint
from sqlalchemy import UUID as SQLUUID
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func

from nucleus.db.database import Base


class EmailMessage(Base):
    """One composed Outlook message. Save updates this row; send marks it sent."""

    __tablename__ = "email_messages"
    __table_args__ = (
        UniqueConstraint("advisor_id", "compose_id", name="uq_email_messages_advisor_compose"),
        Index("ix_email_messages_advisor_client", "advisor_id", "client_id"),
    )

    id: Mapped[UUID] = mapped_column(SQLUUID(as_uuid=True), primary_key=True, default=uuid4)
    advisor_id: Mapped[UUID] = mapped_column(
        SQLUUID(as_uuid=True), ForeignKey("advisors.id"), nullable=False
    )
    client_id: Mapped[UUID | None] = mapped_column(
        SQLUUID(as_uuid=True),
        ForeignKey("clients.id", ondelete="SET NULL"),
        nullable=True,
    )
    compose_id: Mapped[UUID] = mapped_column(SQLUUID(as_uuid=True), nullable=False)
    to_addresses: Mapped[list[str]] = mapped_column(JSONB, nullable=False)
    subject: Mapped[str] = mapped_column(Text, nullable=False, default="")
    graph_message_id: Mapped[str | None] = mapped_column(Text, nullable=True)
    status: Mapped[str] = mapped_column(String(16), nullable=False, default="draft")
    sent_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

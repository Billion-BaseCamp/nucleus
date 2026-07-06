from datetime import datetime
from typing import List, Optional
from uuid import UUID, uuid4

from sqlalchemy import UUID as SQLUUID
from sqlalchemy import DateTime, ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from nucleus.db.database import Base


class ITRDocumentSlot(Base):
    __tablename__ = "itr_document_slots"

    id: Mapped[UUID] = mapped_column(
        SQLUUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
        index=True,
    )
    financial_year_id: Mapped[UUID] = mapped_column(
        SQLUUID(as_uuid=True),
        ForeignKey("financial_years.id", ondelete="CASCADE"),
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

    financial_year: Mapped["FinancialYear"] = relationship("FinancialYear")
    client: Mapped["Client"] = relationship("Client")
    documents: Mapped[List["ITRDocument"]] = relationship(
        "ITRDocument",
        back_populates="slot",
        cascade="all, delete-orphan",
    )

    __table_args__ = (
        # ``notes`` is part of the slot identity so a client can hold several
        # custom/"Other" broker slots under the same (doc_type, sub_type, source,
        # region) — one per distinct note. ``NULLS NOT DISTINCT`` keeps normal
        # slots (notes IS NULL) de-duplicated exactly as before. Requires
        # PostgreSQL 15+.
        UniqueConstraint(
            "financial_year_id",
            "client_id",
            "doc_type",
            "sub_type",
            "source",
            "region",
            "notes",
            name="uq_itr_doc_slot",
            postgresql_nulls_not_distinct=True,
        ),
    )

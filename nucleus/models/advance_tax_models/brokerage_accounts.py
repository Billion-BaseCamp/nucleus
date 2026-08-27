from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from typing import TYPE_CHECKING, Optional
from uuid import UUID, uuid4

from sqlalchemy import Boolean, DateTime, ForeignKey, String, UUID as SQLUUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from sqlalchemy.types import Numeric

from nucleus.db.database import Base

if TYPE_CHECKING:
    from nucleus.models.advance_tax_models.cg_documents import ATCGDocument


class BrokerageAccounts(Base):
    __tablename__ = "brokerage_accounts"
    id: Mapped[UUID] = mapped_column(SQLUUID(as_uuid=True), primary_key=True, default=uuid4, index=True)
    capital_gains_id: Mapped[UUID] = mapped_column(SQLUUID(as_uuid=True), ForeignKey("capital_gains.id", ondelete="CASCADE"), nullable=False)
    account_name: Mapped[str] = mapped_column(String, nullable=True)
    account_value: Mapped[Decimal] = mapped_column(Numeric[Decimal](18,2), nullable=True)
    processed_value: Mapped[Optional[Decimal]] = mapped_column(Numeric[Decimal](18, 2), nullable=True)
    tds_amount: Mapped[Decimal] = mapped_column(Numeric[Decimal](18,2), nullable=True)
    is_exempt: Mapped[bool] = mapped_column(Boolean, nullable=True)
    category: Mapped[str] = mapped_column(String, nullable=True)
    sub_category: Mapped[str] = mapped_column(String, nullable=True)
    source_document_id: Mapped[Optional[UUID]] = mapped_column(
        SQLUUID(as_uuid=True),
        ForeignKey("at_cg_documents.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), onupdate=func.now(), nullable=True)

    capital_gains: Mapped["CapitalGains"] = relationship("CapitalGains", back_populates="brokerage_accounts")
    source_document: Mapped[Optional["ATCGDocument"]] = relationship(
        "ATCGDocument",
        back_populates="brokerage_accounts",
    )

"""
Refund bank accounts for CBDT Refund.BankAccountDtls.

Domestic rows map to AddtnlBankDetails[]; foreign rows (ITR-2) to ForeignBankDetails[].
"""

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Optional
from uuid import UUID, uuid4

if TYPE_CHECKING:
    from nucleus.models.itr_filling.itr_return import ITRReturn

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, UUID as SQLUUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from nucleus.db.database import Base


class ITRRefundBankAccount(Base):
    """CBDT refund bank detail row — one or more per ITR return."""

    __tablename__ = "itr_refund_bank_accounts"

    id: Mapped[UUID] = mapped_column(
        SQLUUID(as_uuid=True), primary_key=True, default=uuid4
    )
    itr_return_id: Mapped[UUID] = mapped_column(
        SQLUUID(as_uuid=True),
        ForeignKey("itr_returns.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    display_order: Mapped[int] = mapped_column(Integer, nullable=False, default=1)

    is_foreign: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    ifsc_code: Mapped[Optional[str]] = mapped_column(String(11), nullable=True)
    bank_name: Mapped[Optional[str]] = mapped_column(String(125), nullable=True)
    bank_account_no: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    account_type: Mapped[Optional[str]] = mapped_column(String(5), nullable=True)
    use_for_refund: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    swift_code: Mapped[Optional[str]] = mapped_column(String(11), nullable=True)
    iban: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    country_code: Mapped[Optional[str]] = mapped_column(String(5), nullable=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), onupdate=func.now()
    )

    itr_return: Mapped["ITRReturn"] = relationship(
        "ITRReturn", back_populates="refund_bank_accounts"
    )

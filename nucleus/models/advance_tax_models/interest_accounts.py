from sqlalchemy import String, DateTime, ForeignKey, UUID as SQLUUID, Float
from nucleus.db.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from uuid import UUID, uuid4
from sqlalchemy.sql import func
from datetime import datetime


class InterestAccounts(Base):
    """Per-bank-account bifurcation for FD / Savings interest (mirrors brokerage_accounts for CG)."""

    __tablename__ = "interest_accounts"

    id: Mapped[UUID] = mapped_column(SQLUUID(as_uuid=True), primary_key=True, default=uuid4, index=True)
    interest_details_id: Mapped[UUID] = mapped_column(
        SQLUUID(as_uuid=True),
        ForeignKey("interest_details.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    account_name: Mapped[str] = mapped_column(String, nullable=True)
    account_value: Mapped[float] = mapped_column(Float, nullable=True)  # interest amount
    tds_amount: Mapped[float] = mapped_column(Float, nullable=True, default=0.0)
    # "FD" | "SAVINGS"
    sub_category: Mapped[str] = mapped_column(String, nullable=False)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), onupdate=func.now(), nullable=True)

    interest_details: Mapped["InterestDetails"] = relationship(
        "InterestDetails", back_populates="interest_accounts"
    )

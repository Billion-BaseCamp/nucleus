from sqlalchemy import String, DateTime, ForeignKey, UUID as SQLUUID, Float
from nucleus.db.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from uuid import UUID, uuid4
from sqlalchemy.sql import func
from datetime import datetime


class OtherIncomeAccounts(Base):
    """Per-account bifurcation for other income heads (mirrors interest_accounts)."""

    __tablename__ = "other_income_accounts"

    id: Mapped[UUID] = mapped_column(SQLUUID(as_uuid=True), primary_key=True, default=uuid4, index=True)
    other_income_id: Mapped[UUID] = mapped_column(
        SQLUUID(as_uuid=True),
        ForeignKey("other_income.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    account_name: Mapped[str] = mapped_column(String, nullable=True)
    account_value: Mapped[float] = mapped_column(Float, nullable=True)
    tds_amount: Mapped[float] = mapped_column(Float, nullable=True, default=0.0)
    # "44ADA" | "44AD" | "CONSULTANCY" | "ANY_OTHER"
    sub_category: Mapped[str] = mapped_column(String, nullable=False)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), onupdate=func.now(), nullable=True)

    other_income: Mapped["OtherIncome"] = relationship(
        "OtherIncome", back_populates="other_income_accounts"
    )

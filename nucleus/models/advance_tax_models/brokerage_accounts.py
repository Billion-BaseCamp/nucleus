from sqlalchemy import String, DateTime, ForeignKey, UUID as SQLUUID, Float, Boolean
from nucleus.db.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from uuid import UUID, uuid4
from sqlalchemy.sql import func
from datetime import datetime
from decimal import Decimal
from sqlalchemy.types import Numeric


class BrokerageAccounts(Base):
    __tablename__ = "brokerage_accounts"
    id: Mapped[UUID] = mapped_column(SQLUUID(as_uuid=True), primary_key=True, default=uuid4, index=True)
    capital_gains_id: Mapped[UUID] = mapped_column(SQLUUID(as_uuid=True), ForeignKey("capital_gains.id", ondelete="CASCADE"), nullable=False)
    account_name: Mapped[str] = mapped_column(String, nullable=True)
    account_value: Mapped[Decimal] = mapped_column(Numeric[Decimal](18,2), nullable=True)
    tds_amount: Mapped[Decimal] = mapped_column(Numeric[Decimal](18,2), nullable=True)
    is_exempt: Mapped[bool] = mapped_column(Boolean, nullable=True)
    category: Mapped[str] = mapped_column(String, nullable=True)
    sub_category: Mapped[str] = mapped_column(String, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), onupdate=func.now(), nullable=True)

    # Relationships
    capital_gains: Mapped["CapitalGains"] = relationship("CapitalGains", back_populates="brokerage_accounts")
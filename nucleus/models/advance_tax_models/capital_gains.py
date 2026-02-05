from sqlalchemy import String, DateTime, Float, ForeignKey, UUID as SQLUUID
from sqlalchemy.dialects.postgresql import JSONB
from typing import Dict, Any
from uuid import UUID, uuid4
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from datetime import datetime
from nucleus.db.database import Base
from nucleus.core.constants import CapitalGainsCategory
from typing import TypedDict

class LTCG_12_5(TypedDict):
    amount: float
    is_exempted: bool


class CapitalGains(Base):
    __tablename__ = "capital_gains"
    id: Mapped[UUID] = mapped_column(SQLUUID(as_uuid=True), primary_key=True, default=uuid4, index=True)
    
    # Foreign keys
    quarter_id: Mapped[UUID] = mapped_column(SQLUUID(as_uuid=True), ForeignKey("quarters.id", ondelete="CASCADE"), nullable=False)
    client_id: Mapped[UUID] = mapped_column(SQLUUID(as_uuid=True), ForeignKey("clients.id"), nullable=False)
    
    category: Mapped[CapitalGainsCategory] = mapped_column(String, nullable=False)
    ShortTermCG_15: Mapped[float] = mapped_column(Float, nullable=True)
    ShortTermCG_20: Mapped[Dict[str, float]] = mapped_column(JSONB, nullable=True)  # JSON: {"AngelBroking": 120000, "Zerodha": 20000}
    ShortTermCG_At_Marginal_Rate: Mapped[Dict[str, float]] = mapped_column(JSONB, nullable=True)  # JSON: {"label": value}
    LongTermCG_10: Mapped[float] = mapped_column(Float, nullable=True)
    LongTermCG_12_5: Mapped[Dict[str, LTCG_12_5]] = mapped_column(JSONB, nullable=True)  # JSON: {"label": value}
    LongTermCG_20: Mapped[Dict[str, float]] = mapped_column(JSONB, nullable=True)  # JSON: {"label": value}
    NetShortTermGain20: Mapped[float] = mapped_column(Float, nullable=True)
    NetLongTermGain12_5: Mapped[float] = mapped_column(Float, nullable=True)
    NetShortTermGainNormal: Mapped[float] = mapped_column(Float, nullable=True)
    NetLongTermGain20: Mapped[float] = mapped_column(Float, nullable=True)
    NetShortTermGain15: Mapped[float] = mapped_column(Float, nullable=True)
    NetLongTermGain10: Mapped[float] = mapped_column(Float, nullable=True)
    ShortTermLossBroughtForward: Mapped[float] = mapped_column(Float, nullable=True)
    LongTermLossBroughtForward: Mapped[float] = mapped_column(Float, nullable=True)
    TotalLossBroughtForward: Mapped[float] = mapped_column(Float, nullable=True)
    NetShortTermGain_15_AfterSetoff: Mapped[float] = mapped_column(Float, nullable=True)
    NetLongTermGain_10_AfterSetoff: Mapped[float] = mapped_column(Float, nullable=True)
    NetLongTermGain_20_AfterSetoff: Mapped[float] = mapped_column(Float, nullable=True)
    NetLongTermGain_12_5_AfterSetoff: Mapped[float] = mapped_column(Float, nullable=True)
    NetShortTermGain_20_AfterSetoff: Mapped[float] = mapped_column(Float, nullable=True)
    NetShortTermGain_Normal_AfterSetoff: Mapped[float] = mapped_column(Float, nullable=True)
    shortTermLossCarryForward: Mapped[float] = mapped_column(Float, nullable=True)
    longTermLossCarryForward: Mapped[float] = mapped_column(Float, nullable=True)
    cryptoCaptialGains: Mapped[float] = mapped_column(Float, nullable=True)

    # Relationships
    quarter: Mapped["Quarter"] = relationship("Quarter", back_populates="capital_gains")
    client: Mapped["Client"] = relationship("Client", back_populates="capital_gains")

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), onupdate=func.now(), nullable=True)
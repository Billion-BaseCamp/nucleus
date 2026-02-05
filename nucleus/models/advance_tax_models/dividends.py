from sqlalchemy import DateTime, Float, ForeignKey, UUID as SQLUUID
from uuid import UUID, uuid4
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from datetime import datetime
from nucleus.db.database import Base


class Dividends(Base):
    __tablename__ = "dividends"
    id: Mapped[UUID] = mapped_column(SQLUUID(as_uuid=True), primary_key=True, default=uuid4, index=True)
    
    # Foreign keys
    quarter_id: Mapped[UUID] = mapped_column(SQLUUID(as_uuid=True), ForeignKey("quarters.id", ondelete="CASCADE"), nullable=False)
    client_id: Mapped[UUID] = mapped_column(SQLUUID(as_uuid=True), ForeignKey("clients.id"), nullable=False)
    
    india_dividends: Mapped[float] = mapped_column(Float, nullable=True)
    foreign_dividends: Mapped[float] = mapped_column(Float, nullable=True)
    tds: Mapped[float] = mapped_column(Float, nullable=True)
    ftc: Mapped[float] = mapped_column(Float, nullable=True)
    india_dividends_reit: Mapped[float] = mapped_column(Float, nullable=True)
    # Relationships
    quarter: Mapped["Quarter"] = relationship("Quarter", back_populates="dividends")
    client: Mapped["Client"] = relationship("Client", back_populates="dividends")
    
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), onupdate=func.now(), nullable=True)
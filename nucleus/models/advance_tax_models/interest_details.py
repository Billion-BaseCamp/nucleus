from sqlalchemy import DateTime, Float, ForeignKey, UUID as SQLUUID
from uuid import UUID, uuid4
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from datetime import datetime
from nucleus.db.database import Base


class InterestDetails(Base):
    __tablename__ = "interest_details"
    id: Mapped[UUID] = mapped_column(SQLUUID(as_uuid=True), primary_key=True, default=uuid4, index=True)
    
    # Foreign keys
    quarter_id: Mapped[UUID] = mapped_column(SQLUUID(as_uuid=True), ForeignKey("quarters.id", ondelete="CASCADE"), nullable=False)
    client_id: Mapped[UUID] = mapped_column(SQLUUID(as_uuid=True), ForeignKey("clients.id"), nullable=False)
    
    fd_interest: Mapped[float] = mapped_column(Float, default=0.0)
    fd_tds: Mapped[float] = mapped_column(Float, default=0.0)
    savings_interest: Mapped[float] = mapped_column(Float, default=0.0)
    savings_tds: Mapped[float] = mapped_column(Float, default=0.0)
    other_interest: Mapped[float] = mapped_column(Float, default=0.0)
    other_tds: Mapped[float] = mapped_column(Float, default=0.0)
    pass_interest: Mapped[float] = mapped_column(Float, default=0.0)
    pass_tds: Mapped[float] = mapped_column(Float, default=0.0)
    epf_interest: Mapped[float] = mapped_column(Float, default=0.0)
    epf_tds: Mapped[float] = mapped_column(Float, default=0.0)
    it_refund_interest: Mapped[float] = mapped_column(Float, default=0.0)
    it_refund_tds: Mapped[float] = mapped_column(Float, default=0.0)
    foreign_interest: Mapped[float] = mapped_column(Float, default=0.0, nullable=True)
    foreign_interest_ftc: Mapped[float] = mapped_column(Float, default=0.0, nullable=True)
    total_interest: Mapped[float] = mapped_column(Float, default=0.0)
    total_tds: Mapped[float] = mapped_column(Float, default=0.0)

    
    
    # Relationships
    quarter: Mapped["Quarter"] = relationship("Quarter", back_populates="interest_details")
    client: Mapped["Client"] = relationship("Client", back_populates="interest_details")
    
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), onupdate=func.now(), nullable=True)
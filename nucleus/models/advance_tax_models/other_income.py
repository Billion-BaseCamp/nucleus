from sqlalchemy import DateTime, Float, ForeignKey, UUID as SQLUUID
from uuid import UUID, uuid4
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from datetime import datetime
from nucleus.db.database import Base


class OtherIncome(Base):
    __tablename__ = "other_income"
    id: Mapped[UUID] = mapped_column(SQLUUID(as_uuid=True), primary_key=True, default=uuid4, index=True)
    
    # Foreign keys
    quarter_id: Mapped[UUID] = mapped_column(SQLUUID(as_uuid=True), ForeignKey("quarters.id"), nullable=False)
    client_id: Mapped[UUID] = mapped_column(SQLUUID(as_uuid=True), ForeignKey("clients.id"), nullable=False)
    
    income_44ada: Mapped[float] = mapped_column(Float, default=0.0)
    property_sale_tds: Mapped[float] = mapped_column(Float, default=0.0)
    additional_foreign_tax_credits: Mapped[float] = mapped_column(Float, default=0.0)
    tcs_incurred: Mapped[float] = mapped_column(Float, default=0.0)
    tds_44ada: Mapped[float] = mapped_column(Float, default=0.0)
    salary_exemption: Mapped[float] = mapped_column(Float, default=0.0)
    any_other_income: Mapped[float] = mapped_column(Float, default=0.0)
    tcs_expected: Mapped[float] = mapped_column(Float, default=0.0)
    
    # Relationships
    quarter: Mapped["Quarter"] = relationship("Quarter", back_populates="other_income")
    client: Mapped["Client"] = relationship("Client", back_populates="other_income")
    
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), onupdate=func.now(), nullable=True)
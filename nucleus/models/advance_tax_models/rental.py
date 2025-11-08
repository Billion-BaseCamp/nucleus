from sqlalchemy import String, DateTime, Float, ForeignKey, UUID as SQLUUID
from uuid import UUID, uuid4
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func 
from datetime import datetime
from nucleus.db.database import Base
from nucleus.core.constants import Region
from sqlalchemy import Enum, Boolean

# Rental Model

class Rental(Base):
    __tablename__ = "rentals"
    id: Mapped[UUID] = mapped_column(SQLUUID(as_uuid=True), primary_key=True, default=uuid4, index=True)
    
    # Foreign keys
    quarter_id: Mapped[UUID] = mapped_column(SQLUUID(as_uuid=True), ForeignKey("quarters.id"), nullable=False)
    client_id: Mapped[UUID] = mapped_column(SQLUUID(as_uuid=True), ForeignKey("clients.id"), nullable=False)
    
    property_name: Mapped[str] = mapped_column(String, nullable=False)
    property_type: Mapped[str] = mapped_column(String, nullable=True)
    annual_rental_income: Mapped[float] = mapped_column(Float, nullable=False)
    property_tax: Mapped[float] = mapped_column(Float, nullable=True)
    ownership_percentage: Mapped[float] = mapped_column(Float, nullable=False)
    nav: Mapped[float] = mapped_column(Float, nullable=True)
    standard_deduction: Mapped[float] = mapped_column(Float, nullable=True)
    housing_loan_interest: Mapped[float] = mapped_column(Float, nullable=True)
    taxable_rental_income: Mapped[float] = mapped_column(Float, nullable=True)
    tds: Mapped[float] = mapped_column(Float, nullable=True)
    region: Mapped[Region] = mapped_column(Enum(Region, native_enum=False), nullable=True)
    acquired_this_year: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    transferred_this_year: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    
    # Relationships
    quarter: Mapped["Quarter"] = relationship("Quarter", back_populates="rentals")
    client: Mapped["Client"] = relationship("Client", back_populates="rentals")
    
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), onupdate=func.now(), nullable=True)
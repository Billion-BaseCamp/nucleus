from nucleus.db.database import Base
from sqlalchemy import BigInteger, String, ForeignKey, UUID as SQLUUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Optional
from datetime import datetime
from sqlalchemy.sql import func
from sqlalchemy import DateTime, Date
from datetime import date
from uuid import UUID, uuid4

class Employment(Base):
    __tablename__ = "employment"
    id: Mapped[UUID] = mapped_column(SQLUUID(as_uuid=True), primary_key=True, default=uuid4, index=True)
    client_profile_id: Mapped[UUID] = mapped_column(SQLUUID(as_uuid=True), ForeignKey("client_profiles.id", ondelete="CASCADE"), nullable=False)
    employer_name: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    designation: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    country_of_headquarter: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    start_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    end_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), onupdate=func.now(), nullable=True)

    client_profile: Mapped["ClientProfile"] = relationship(
        "ClientProfile",
        back_populates="employment_records"
    )
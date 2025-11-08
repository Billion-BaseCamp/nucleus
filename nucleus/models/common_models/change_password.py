from typing import TYPE_CHECKING
from sqlalchemy import String, DateTime, Integer, UUID as SQLUUID,ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func
from datetime import datetime
from nucleus.db.database import Base
from uuid import UUID, uuid4


class OtpVerification(Base):
    __tablename__ = "otp_verifications"
    id: Mapped[UUID] = mapped_column(SQLUUID(as_uuid=True), primary_key=True, default=uuid4, index=True)
    login_id: Mapped[int] = mapped_column(Integer, ForeignKey("logins.id"), nullable=False, index=True)
    otp_attempts: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    otp: Mapped[str] = mapped_column(String, nullable=False, unique=True, index=True)
    otp_expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    unique_id: Mapped[str] = mapped_column(String, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), onupdate=func.now(), nullable=True)

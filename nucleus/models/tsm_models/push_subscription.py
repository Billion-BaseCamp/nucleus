from uuid import UUID, uuid4
from datetime import datetime
from sqlalchemy import String, ForeignKey, DateTime, UUID as SQLUUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from nucleus.db.database import Base


class PushSubscription(Base):
    __tablename__ = "push_subscriptions"
    
    id: Mapped[UUID] = mapped_column(SQLUUID(as_uuid=True), primary_key=True, default=uuid4, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("logins.id", ondelete="CASCADE"), nullable=False, index=True)
    endpoint: Mapped[str] = mapped_column(String, nullable=False, unique=True, index=True)
    keys_p256dh: Mapped[str] = mapped_column(String, nullable=False)
    keys_auth: Mapped[str] = mapped_column(String, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=True)
    
    # Relationship
    login: Mapped["Login"] = relationship("Login", back_populates="push_subscriptions")

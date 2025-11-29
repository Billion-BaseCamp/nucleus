

from uuid import UUID, uuid4
from sqlalchemy import Integer, String, DateTime, Enum, ForeignKey, UUID as SQLUUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from datetime import datetime
from nucleus.db.database import Base
from nucleus.core.constants import UserRole


class Login(Base):
    __tablename__ = "logins"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    hashed_password: Mapped[str] = mapped_column(String, nullable=False)
    email: Mapped[str] = mapped_column(String, unique=True, nullable=True)
    username: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    mobile_number: Mapped[str] = mapped_column(String, unique=True, nullable=True)
    role: Mapped[UserRole] = mapped_column(Enum(UserRole), nullable=False)
    
    # Foreign key to client (if role is client)
    client_id: Mapped[UUID] = mapped_column(SQLUUID(as_uuid=True), ForeignKey("clients.id"), nullable=True)
    
    # Foreign key to advisor (if role is advisor)
    advisor_id: Mapped[UUID] = mapped_column(SQLUUID(as_uuid=True), ForeignKey("advisors.id"), nullable=True)
    
    # Relationships
    client: Mapped["Client"] = relationship("Client", back_populates="logins")
    advisor: Mapped["Advisor"] = relationship("Advisor", back_populates="logins")
    push_subscriptions: Mapped[list["PushSubscription"]] = relationship("PushSubscription", back_populates="login")
    
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), onupdate=func.now(), nullable=True)
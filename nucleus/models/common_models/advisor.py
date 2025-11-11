from sqlalchemy import String, DateTime,Date
import uuid
from uuid import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from datetime import date
from nucleus.db.database import Base
from typing import List, TYPE_CHECKING
from datetime import datetime

if TYPE_CHECKING:
    from nucleus.models.common_models.login import Login
    from nucleus.models.common_models.client import Client
    from nucleus.models.tsm_models.notification import Notification


class Advisor(Base):
    __tablename__ = "advisors"
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid.uuid4, index=True)
    first_name: Mapped[str] = mapped_column(String, nullable=False)
    last_name: Mapped[str] = mapped_column(String, nullable=False)
    date_of_birth: Mapped[date] = mapped_column(Date, nullable=False)
    gender: Mapped[str] = mapped_column(String, nullable=False)
    
    # Relationships
    logins: Mapped[List["Login"]] = relationship("Login", back_populates="advisor")
    clients: Mapped[List["Client"]] = relationship("Client", back_populates="advisor")
    notifications: Mapped[List["Notification"]] = relationship("Notification", back_populates="advisor")
    
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), onupdate=func.now(), nullable=True)
    notifications: Mapped[List["Notification"]] = relationship("Notification", back_populates="advisor")

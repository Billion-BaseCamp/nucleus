from datetime import datetime
from uuid import UUID, uuid4

from sqlalchemy import DateTime, ForeignKey, Integer, String, UUID as SQLUUID
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func

from nucleus.db.database import Base


class LoginEvent(Base):
    __tablename__ = "login_events"

    id: Mapped[UUID] = mapped_column(
        SQLUUID(as_uuid=True), primary_key=True, default=uuid4, index=True
    )
    user_id: Mapped[UUID] = mapped_column(SQLUUID(as_uuid=True), nullable=False, index=True)
    login_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("logins.id", ondelete="CASCADE"), nullable=False, index=True
    )
    service_id: Mapped[str | None] = mapped_column(String(64), nullable=True, index=True)
    logged_in_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now(), index=True
    )

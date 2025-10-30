import uuid
from datetime import datetime
from typing import TYPE_CHECKING
from sqlalchemy import String, Boolean, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from nucleus.db.database import Base
from nucleus.core.constants import IST_TIMEZONE

if TYPE_CHECKING:
    from nucleus.models.common_models.advisor import Advisor

class Notification(Base):
    __tablename__ = "notifications"

    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    assigner_user_id: Mapped[UUID]=mapped_column(UUID(as_uuid=True))
    assignee_user_id: Mapped[UUID] = mapped_column(ForeignKey("advisors.id", ondelete="CASCADE")) 
    message: Mapped[str] = mapped_column(String, nullable=False)
    is_read: Mapped[bool] = mapped_column(Boolean, default=False)
    title: Mapped[str] = mapped_column(String, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=False),
        default=lambda: datetime.now(IST_TIMEZONE).replace(tzinfo=None),
    )
    advisor: Mapped["Advisor"] = relationship(back_populates="notifications")
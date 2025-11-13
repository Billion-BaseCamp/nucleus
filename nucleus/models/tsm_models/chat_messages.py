import uuid
from datetime import datetime
from sqlalchemy import ARRAY, ForeignKey,Text, DateTime, UUID, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from nucleus.db.database import Base
from nucleus.core.constants import IST_TIMEZONE

class TaskChatMessage(Base):
    __tablename__ = "task_chat_messages"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)

    task_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("tasks.task_id", ondelete="CASCADE"), index=True
    )

    sender_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("advisors.id", ondelete="CASCADE"), index=True
    )

    message: Mapped[str] = mapped_column(Text, nullable=False)

    read_by: Mapped[list[uuid.UUID]] = mapped_column(ARRAY(UUID), nullable=True)

    file_urls: Mapped[list[str]] = mapped_column(ARRAY(String), nullable=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=False),
        default=lambda: datetime.now(IST_TIMEZONE).replace(tzinfo=None),
    )

    # Relationships
    sender: Mapped["Advisor"] = relationship("Advisor", back_populates="sent_messages")
    task: Mapped["Task"] = relationship("Task", back_populates="chat_messages")

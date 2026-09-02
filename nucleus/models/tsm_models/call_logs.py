from nucleus.db.database import Base
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
from typing import Optional
import uuid
from sqlalchemy import ForeignKey, String, DateTime, Float, Text



class CallLogs(Base):
    __tablename__ = "call_logs"
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    advisor_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("advisors.id", ondelete="CASCADE"), nullable=True)
    from_number: Mapped[str] = mapped_column(String, nullable=True)
    to_number: Mapped[str] = mapped_column(String, nullable=True)
    caller_name: Mapped[str] = mapped_column(String, nullable=True)
    call_type: Mapped[str] = mapped_column(String, nullable=True)
    client_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("clients.id", ondelete="CASCADE"), nullable=True)
    call_start_time: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    call_duration: Mapped[float] = mapped_column(Float, nullable=True)
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    task_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        ForeignKey("tasks.task_id", ondelete="SET NULL"),
        nullable=True,
        unique=True,
    )

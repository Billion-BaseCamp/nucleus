from nucleus.db.database import Base
from sqlalchemy import Mapped, mapped_column
from datetime import datetime
from nucleus.core.constants import IST_TIMEZONE
import uuid
from sqlalchemy import ForeignKey, String, Integer, DateTime
from sqlalchemy.orm import relationship



class CallLogs(Base):
    __tablename__ = "call_logs"
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    advisor_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("advisors.id", ondelete="CASCADE"), nullable=True)
    from_number: Mapped[str] = mapped_column(String, nullable=True)
    to_number: Mapped[str] = mapped_column(String, nullable=True)
    call_type: Mapped[str] = mapped_column(String, nullable=True)
    client_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("clients.id", ondelete="CASCADE"), nullable=True)
    call_start_time: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    call_duration: Mapped[int] = mapped_column(Integer, nullable=True)

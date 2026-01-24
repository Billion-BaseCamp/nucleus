from nucleus.db.database import Base
from uuid import UUID, uuid4
from sqlalchemy import String, ForeignKey, UUID as SQLUUID, Date, Boolean
from sqlalchemy.orm import Mapped, mapped_column
from datetime import date   
from sqlalchemy.types import DateTime
from sqlalchemy.sql import func
from datetime import datetime
from sqlalchemy.orm import relationship



class Citizenship(Base):
    __tablename__ = "citizenships"

    id: Mapped[UUID] = mapped_column(SQLUUID(as_uuid=True), primary_key=True, default=uuid4, index=True)

    client_id: Mapped[UUID] = mapped_column(SQLUUID(as_uuid=True), ForeignKey("clients.id", ondelete="CASCADE"), nullable=False)

    client: Mapped["Client"] = relationship("Client", back_populates="citizenships")

    citizenship :Mapped[str] = mapped_column(String(255), nullable=False)

    citizenship_start_date: Mapped[date] = mapped_column(Date, nullable=False)

    citizenship_end_date: Mapped[date] = mapped_column(Date, nullable=False)

    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True, server_default="TRUE")

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), onupdate=func.now(), nullable=True)

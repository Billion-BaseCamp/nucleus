from datetime import date
from nucleus.db.database import Base
from typing import Optional,Mapped
from uuid import UUID, uuid4
from sqlalchemy import String, Date, ForeignKey
from sqlalchemy.dialects.postgresql import UUID as SQLUUID
from sqlalchemy.orm import mapped_column
from sqlalchemy.sql import func
from sqlalchemy.types import DateTime
from datetime import datetime
from sqlalchemy.orm import relationship


class Residency(Base):

    __tablename__ = "residencies"

    id: Mapped[UUID] = mapped_column(SQLUUID(as_uuid=True), primary_key=True, default=uuid4, index=True)

    client_id: Mapped[UUID] = mapped_column(SQLUUID(as_uuid=True), ForeignKey("clients.id", ondelete="CASCADE"), nullable=False)

    current_citizenship: Mapped[Optional[date]] = mapped_column(Date, nullable=True)

    previous_citizenship: Mapped[Optional[str]] = mapped_column(String, nullable=True)

    previous_citizenship_end_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)

    residency_details: Mapped[Optional[str]] = mapped_column(String, nullable=True)

    residency_start_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)

    residency_end_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)

    client: Mapped["Client"] = relationship("Client", back_populates="residencies")

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), onupdate=func.now())
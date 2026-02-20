from __future__ import annotations

from datetime import datetime
from uuid import UUID, uuid4

from sqlalchemy import UUID as SQLUUID, DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func


from nucleus.db.database import Base


class Excemption(Base):
    __tablename__ = "excemptions"
    id: Mapped[UUID] = mapped_column(SQLUUID(as_uuid=True), primary_key=True, default=uuid4)

    quarter_id: Mapped[UUID] = mapped_column(SQLUUID(as_uuid=True), ForeignKey("quarters.id", ondelete="CASCADE"), nullable=False)
    client_id: Mapped[UUID] = mapped_column(SQLUUID(as_uuid=True), ForeignKey("clients.id", ondelete="CASCADE"), nullable=False)

    quarter: Mapped["Quarter"] = relationship("Quarter", back_populates="excemptions")
    client: Mapped["Client"] = relationship("Client", back_populates="excemptions")

    #category of excemption
    category_of_excemption: Mapped[str] = mapped_column(String, nullable=True)
    claim_id:Mapped[UUID] = mapped_column(SQLUUID(as_uuid=True), nullable=True)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), onupdate=func.now(), nullable=True)
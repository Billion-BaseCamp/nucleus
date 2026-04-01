from sqlalchemy import DateTime, Float, ForeignKey, UUID as SQLUUID
from uuid import UUID, uuid4
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func
from datetime import datetime
from nucleus.db.database import Base


class Deductions(Base):
    __tablename__ = "deductions"
    id: Mapped[UUID] = mapped_column(SQLUUID(as_uuid=True), primary_key=True, default=uuid4, index=True)

    # Foreign keys
    quarter_id: Mapped[UUID] = mapped_column(SQLUUID(as_uuid=True), ForeignKey("quarters.id"), nullable=False)
    client_id: Mapped[UUID] = mapped_column(SQLUUID(as_uuid=True), ForeignKey("clients.id"), nullable=False)

    # Chapter VI-A Deductions
    section_80c: Mapped[float] = mapped_column(Float, default=0.0)
    section_80ccd_1b: Mapped[float] = mapped_column(Float, default=0.0)
    section_80d_self: Mapped[float] = mapped_column(Float, default=0.0)
    section_80d_parents: Mapped[float] = mapped_column(Float, default=0.0)
    section_80e: Mapped[float] = mapped_column(Float, default=0.0)
    section_80g: Mapped[float] = mapped_column(Float, default=0.0)
    section_80tta: Mapped[float] = mapped_column(Float, default=0.0)
    section_80dd: Mapped[float] = mapped_column(Float, default=0.0)
    section_80u: Mapped[float] = mapped_column(Float, default=0.0)
    section_80gg: Mapped[float] = mapped_column(Float, default=0.0)
    section_80ddb: Mapped[float] = mapped_column(Float, default=0.0)
    section_80eea: Mapped[float] = mapped_column(Float, default=0.0)
    hra_exemption: Mapped[float] = mapped_column(Float, default=0.0)

    # Computed total
    total_deductions: Mapped[float] = mapped_column(Float, default=0.0)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), onupdate=func.now(), nullable=True)

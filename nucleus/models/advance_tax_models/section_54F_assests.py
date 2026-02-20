from __future__ import annotations

from datetime import datetime
from uuid import UUID, uuid4

from sqlalchemy import DateTime, ForeignKey, Numeric, String, UUID as SQLUUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from nucleus.db.database import Base



class Section54FAssets(Base):
    __tablename__ = "section_54f_assests"

    id: Mapped[UUID] = mapped_column(SQLUUID(as_uuid=True), primary_key=True, default=uuid4)

    name_of_asset: Mapped[str] = mapped_column(String, nullable=True)
    cost_of_asset: Mapped[float] = mapped_column(Numeric(18,2), default=0, nullable=True)
    sale_value_of_asset: Mapped[float] = mapped_column(Numeric(18,2), default=0, nullable=True)

    #capital gain on asset===> sale value of asset - cost of asset
    capital_gain_on_asset: Mapped[float] = mapped_column(Numeric(18,2), default=0, nullable=True)

    # Each Section54FAssets belongs to exactly one Section54FClaim (child holds FK)
    section_54f_claim_id: Mapped[UUID | None] = mapped_column(
        SQLUUID(as_uuid=True),
        ForeignKey("section_54f_claim.id", ondelete="CASCADE"),
        nullable=True,
    )
    section_54f_claim: Mapped["Section54FClaim | None"] = relationship(
        "Section54FClaim",
        back_populates="section_54f_assets",
    )

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), onupdate=func.now(), nullable=True)
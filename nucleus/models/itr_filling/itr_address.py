"""
ITR filing address for Part A (PersonalInfo.Address).

One row per ITR return — separate from client profiling ``addresses``.
"""

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Optional
from uuid import UUID, uuid4

if TYPE_CHECKING:
    from nucleus.models.itr_filling.itr_return import ITRReturn

from sqlalchemy import DateTime, ForeignKey, Integer, String, UUID as SQLUUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from nucleus.db.database import Base


class ITRAddress(Base):
    """CBDT Part A address persisted per ITR return (1:1)."""

    __tablename__ = "itr_address"

    id: Mapped[UUID] = mapped_column(
        SQLUUID(as_uuid=True), primary_key=True, default=uuid4
    )
    itr_return_id: Mapped[UUID] = mapped_column(
        SQLUUID(as_uuid=True),
        ForeignKey("itr_returns.id", ondelete="CASCADE"),
        nullable=False,
        unique=True,
        index=True,
    )

    residence_no: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    residence_name: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    road_or_street: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    locality_or_area: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    city_or_town_or_district: Mapped[Optional[str]] = mapped_column(
        String(50), nullable=True
    )
    state_code: Mapped[Optional[str]] = mapped_column(String(2), nullable=True)
    country_code: Mapped[Optional[str]] = mapped_column(String(10), nullable=True)
    pin_code: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    zip_code: Mapped[Optional[str]] = mapped_column(String(8), nullable=True)

    country_code_mobile: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    mobile_no: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    country_code_mobile_sec: Mapped[Optional[int]] = mapped_column(
        Integer, nullable=True
    )
    mobile_no_sec: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)

    email_address: Mapped[Optional[str]] = mapped_column(String(125), nullable=True)
    email_address_sec: Mapped[Optional[str]] = mapped_column(String(125), nullable=True)

    phone_std_code: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    phone_no: Mapped[Optional[str]] = mapped_column(String(10), nullable=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), onupdate=func.now()
    )

    itr_return: Mapped["ITRReturn"] = relationship(
        "ITRReturn", back_populates="address", uselist=False
    )

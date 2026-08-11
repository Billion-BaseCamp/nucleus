from __future__ import annotations

from datetime import datetime
from typing import List, Optional
from uuid import UUID, uuid4

from sqlalchemy import Boolean, DateTime, Enum, Float, ForeignKey, Integer, String, UUID as SQLUUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from nucleus.core.constants import Region
from nucleus.db.database import Base


class Rental(Base):
    __tablename__ = "rentals"
    id: Mapped[UUID] = mapped_column(SQLUUID(as_uuid=True), primary_key=True, default=uuid4, index=True)

    # Foreign keys
    quarter_id: Mapped[UUID] = mapped_column(
        SQLUUID(as_uuid=True), ForeignKey("quarters.id", ondelete="CASCADE"), nullable=False
    )
    client_id: Mapped[UUID] = mapped_column(SQLUUID(as_uuid=True), ForeignKey("clients.id"), nullable=False)

    # Links co-owner rental rows for the same property in a quarter
    property_group_id: Mapped[Optional[UUID]] = mapped_column(
        SQLUUID(as_uuid=True),
        nullable=True,
        index=True,
    )

    property_name: Mapped[str] = mapped_column(String, nullable=False)
    property_type: Mapped[str] = mapped_column(String, nullable=True)
    annual_rental_income: Mapped[float] = mapped_column(Float, nullable=False)
    property_tax: Mapped[float] = mapped_column(Float, nullable=True)
    ownership_percentage: Mapped[float] = mapped_column(Float, nullable=False)
    nav: Mapped[float] = mapped_column(Float, nullable=True)
    standard_deduction: Mapped[float] = mapped_column(Float, nullable=True)
    housing_loan_interest: Mapped[float] = mapped_column(Float, nullable=True)
    taxable_rental_income: Mapped[float] = mapped_column(Float, nullable=True)
    tds: Mapped[float] = mapped_column(Float, nullable=True)
    region: Mapped[Region] = mapped_column(Enum(Region, native_enum=False), nullable=True)
    acquired_this_year: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    transferred_this_year: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    # Relationships
    quarter: Mapped["Quarter"] = relationship("Quarter", back_populates="rentals")
    client: Mapped["Client"] = relationship("Client", back_populates="rentals")
    co_owners: Mapped[List["RentalCoOwner"]] = relationship(
        "RentalCoOwner",
        back_populates="rental",
        cascade="all, delete-orphan",
        foreign_keys="RentalCoOwner.rental_id",
        order_by="RentalCoOwner.display_order",
    )

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), onupdate=func.now(), nullable=True)


class RentalCoOwner(Base):
    """Co-owner share for a rental property group. Stored on the anchor rental row."""

    __tablename__ = "rental_co_owners"

    id: Mapped[UUID] = mapped_column(SQLUUID(as_uuid=True), primary_key=True, default=uuid4, index=True)
    rental_id: Mapped[UUID] = mapped_column(
        SQLUUID(as_uuid=True),
        ForeignKey("rentals.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    display_order: Mapped[int] = mapped_column(Integer, nullable=False, default=1)

    # Null when is_other is True
    co_owner_client_id: Mapped[Optional[UUID]] = mapped_column(
        SQLUUID(as_uuid=True),
        ForeignKey("clients.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    is_other: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    share_percent: Mapped[float] = mapped_column(Float, nullable=False)

    # Co-owner's rental row in the same quarter (null for Other)
    linked_rental_id: Mapped[Optional[UUID]] = mapped_column(
        SQLUUID(as_uuid=True),
        ForeignKey("rentals.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )

    rental: Mapped["Rental"] = relationship(
        "Rental",
        back_populates="co_owners",
        foreign_keys=[rental_id],
    )
    linked_rental: Mapped[Optional["Rental"]] = relationship(
        "Rental",
        foreign_keys=[linked_rental_id],
    )
    co_owner_client: Mapped[Optional["Client"]] = relationship("Client", foreign_keys=[co_owner_client_id])

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), onupdate=func.now(), nullable=True)

"""AA customer: the link between a Billion BaseCamp client and their AA handle.

One row per client that has ever started an Account Aggregator journey. The AA
handle (``mobile@finvu``) is the identity the AA network knows them by, and is
distinct from any mobile number we hold on the client record.
"""

from __future__ import annotations

from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4

from sqlalchemy import DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func
from sqlalchemy.types import UUID as SQLUUID

from nucleus.db.database import Base


class AACustomer(Base):
    """A client enrolled with the Account Aggregator network."""

    __tablename__ = "aa_customers"

    id: Mapped[UUID] = mapped_column(
        SQLUUID(as_uuid=True), primary_key=True, default=uuid4, index=True
    )
    client_id: Mapped[UUID] = mapped_column(
        SQLUUID(as_uuid=True),
        ForeignKey("clients.id", ondelete="CASCADE"),
        nullable=False,
        unique=True,
        index=True,
    )
    # ``9819894316@finvu`` — the custId every Finsense call carries.
    aa_handle: Mapped[str] = mapped_column(
        String(128), nullable=False, unique=True, index=True
    )
    # Stored separately: the client's mobile may change without the AA handle
    # following, and the handle is what the AA network keys on.
    mobile_number: Mapped[Optional[str]] = mapped_column(String(16), nullable=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), onupdate=func.now(), nullable=True
    )

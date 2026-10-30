"""Access grants: which employee may act on which primary client, and with which permissions.

Family members of the granted primary client are covered via clients.parent_id at
check/list time — they are not separate grant rows. No relationships to Advisor
or Client (project rule: do not change those models unless required).
"""

from datetime import datetime
from typing import List, Optional
from uuid import UUID, uuid4

from sqlalchemy import (
    DateTime,
    ForeignKey,
    Index,
    SmallInteger,
    String,
    Text,
    UUID as SQLUUID,
    text,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from nucleus.db.database import Base


class Permission(Base):
    """Developer-managed action the system can allow (e.g. client.read)."""

    __tablename__ = "permissions"

    id: Mapped[int] = mapped_column(SmallInteger, primary_key=True, autoincrement=True)
    key: Mapped[str] = mapped_column(String(80), unique=True, nullable=False)
    module: Mapped[str] = mapped_column(String(40), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    grant_links: Mapped[List["AccessGrantPermission"]] = relationship(
        "AccessGrantPermission",
        back_populates="permission",
    )


class AccessGrant(Base):
    """One employee granted access to one primary client (family included via parent_id)."""

    __tablename__ = "access_grants"
    __table_args__ = (
        Index(
            "uq_access_grants_active_employee_client",
            "employee_id",
            "client_id",
            unique=True,
            postgresql_where=text("revoked_at IS NULL"),
        ),
        Index(
            "ix_access_grants_active_client",
            "client_id",
            postgresql_where=text("revoked_at IS NULL"),
        ),
    )

    id: Mapped[UUID] = mapped_column(
        SQLUUID(as_uuid=True), primary_key=True, default=uuid4
    )
    employee_id: Mapped[UUID] = mapped_column(
        SQLUUID(as_uuid=True),
        ForeignKey("advisors.id"),
        nullable=False,
    )
    client_id: Mapped[UUID] = mapped_column(
        SQLUUID(as_uuid=True),
        ForeignKey("clients.id", ondelete="CASCADE"),
        nullable=False,
    )
    granted_by: Mapped[UUID] = mapped_column(
        SQLUUID(as_uuid=True),
        ForeignKey("advisors.id"),
        nullable=False,
    )
    granted_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
    expires_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    revoked_by: Mapped[Optional[UUID]] = mapped_column(
        SQLUUID(as_uuid=True),
        ForeignKey("advisors.id"),
        nullable=True,
    )
    revoked_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    note: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    permission_links: Mapped[List["AccessGrantPermission"]] = relationship(
        "AccessGrantPermission",
        back_populates="grant",
        cascade="all, delete-orphan",
    )


class AccessGrantPermission(Base):
    """Which permission keys are ticked on one access grant."""

    __tablename__ = "access_grant_permissions"

    grant_id: Mapped[UUID] = mapped_column(
        SQLUUID(as_uuid=True),
        ForeignKey("access_grants.id", ondelete="CASCADE"),
        primary_key=True,
    )
    permission_id: Mapped[int] = mapped_column(
        SmallInteger,
        ForeignKey("permissions.id"),
        primary_key=True,
        index=True,
    )

    grant: Mapped["AccessGrant"] = relationship(
        "AccessGrant",
        back_populates="permission_links",
    )
    permission: Mapped["Permission"] = relationship(
        "Permission",
        back_populates="grant_links",
    )

"""Login / staff roles (admin, advisor, client, intern, …).

``logins.role`` (enum) is kept for migration/backfill. New code should prefer
``logins.role_id`` → ``roles``. No role_permissions table — client actions stay
on access_grants / access_grant_permissions.
"""

from datetime import datetime
from typing import List

from sqlalchemy import DateTime, SmallInteger, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from nucleus.db.database import Base


class Role(Base):
    """Role assigned to a login (JWT role comes from ``key``)."""

    __tablename__ = "roles"

    id: Mapped[int] = mapped_column(SmallInteger, primary_key=True, autoincrement=True)
    key: Mapped[str] = mapped_column(String(40), unique=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    logins: Mapped[List["Login"]] = relationship(
        "Login",
        back_populates="role_row",
    )

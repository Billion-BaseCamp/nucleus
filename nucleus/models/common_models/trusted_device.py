from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4

from sqlalchemy import (
    Boolean,
    CheckConstraint,
    DateTime,
    ForeignKey,
    Index,
    Integer,
    LargeBinary,
    String,
    Text,
    UUID as SQLUUID,
    text,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from nucleus.core.constants import DeviceBindingStatus
from nucleus.db.database import Base


class TrustedDevice(Base):
    """A computer enrolled (or awaiting approval) for staff device binding.

    Private WebAuthn keys never leave the device. This row is the admin-facing
    record; the public key lives on WebAuthnCredential.
    """

    __tablename__ = "trusted_devices"
    __table_args__ = (
        CheckConstraint(
            "status IN ('pending', 'trusted', 'revoked')",
            name="ck_trusted_devices_status",
        ),
        Index(
            "uq_trusted_devices_one_trusted_per_login",
            "login_id",
            unique=True,
            postgresql_where=text("status = 'trusted'"),
        ),
        Index(
            "uq_trusted_devices_one_pending_per_login",
            "login_id",
            unique=True,
            postgresql_where=text("status = 'pending'"),
        ),
    )

    id: Mapped[UUID] = mapped_column(
        SQLUUID(as_uuid=True), primary_key=True, default=uuid4, index=True
    )
    login_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("logins.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    display_name: Mapped[str] = mapped_column(String(255), nullable=False)
    status: Mapped[str] = mapped_column(
        String(16),
        nullable=False,
        server_default=DeviceBindingStatus.PENDING.value,
        index=True,
    )
    user_agent: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    approved_by_login_id: Mapped[Optional[int]] = mapped_column(
        Integer,
        ForeignKey("logins.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    approved_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    last_used_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    revoked_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), onupdate=func.now(), nullable=True
    )

    login: Mapped["Login"] = relationship(
        "Login",
        back_populates="trusted_devices",
        foreign_keys=[login_id],
    )
    approved_by: Mapped[Optional["Login"]] = relationship(
        "Login",
        foreign_keys=[approved_by_login_id],
    )
    credential: Mapped[Optional["WebAuthnCredential"]] = relationship(
        "WebAuthnCredential",
        back_populates="device",
        uselist=False,
        cascade="all, delete-orphan",
    )


class WebAuthnCredential(Base):
    """Public WebAuthn material for one trusted device. Never store the private key."""

    __tablename__ = "webauthn_credentials"

    id: Mapped[UUID] = mapped_column(
        SQLUUID(as_uuid=True), primary_key=True, default=uuid4, index=True
    )
    device_id: Mapped[UUID] = mapped_column(
        SQLUUID(as_uuid=True),
        ForeignKey("trusted_devices.id", ondelete="CASCADE"),
        nullable=False,
        unique=True,
        index=True,
    )
    # Raw credential id from the authenticator (unique across all users).
    credential_id: Mapped[bytes] = mapped_column(LargeBinary, nullable=False, unique=True)
    public_key: Mapped[bytes] = mapped_column(LargeBinary, nullable=False)
    sign_count: Mapped[int] = mapped_column(Integer, nullable=False, server_default="0")
    aaguid: Mapped[Optional[str]] = mapped_column(String(36), nullable=True)
    transports: Mapped[Optional[str]] = mapped_column(String(128), nullable=True)
    backup_eligible: Mapped[bool] = mapped_column(
        Boolean, nullable=False, server_default="false"
    )
    backup_state: Mapped[bool] = mapped_column(
        Boolean, nullable=False, server_default="false"
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), onupdate=func.now(), nullable=True
    )

    device: Mapped["TrustedDevice"] = relationship(
        "TrustedDevice", back_populates="credential"
    )

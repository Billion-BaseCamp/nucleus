"""Add staff device binding tables and logins.device_binding_required.

Revision ID: d7e4a91c2b18
Revises: None
Create Date: 2026-09-02

Existing admins and all clients are grandfathered (device_binding_required =
false). Advisors and any future admin/advisor logins default to true.

If this database already has an Alembic head, set down_revision to that
revision before running upgrade.
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = "d7e4a91c2b18"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "logins",
        sa.Column(
            "device_binding_required",
            sa.Boolean(),
            server_default="true",
            nullable=False,
        ),
    )
    # Grandfather existing admins; clients never use WebAuthn. Advisors stay true.
    op.execute(
        """
        UPDATE logins
        SET device_binding_required = false
        WHERE lower(role::text) IN ('admin', 'client')
        """
    )

    op.create_table(
        "trusted_devices",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("login_id", sa.Integer(), nullable=False),
        sa.Column("display_name", sa.String(length=255), nullable=False),
        sa.Column(
            "status",
            sa.String(length=16),
            server_default="pending",
            nullable=False,
        ),
        sa.Column("user_agent", sa.Text(), nullable=True),
        sa.Column("approved_by_login_id", sa.Integer(), nullable=True),
        sa.Column("approved_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("last_used_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("revoked_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
        sa.CheckConstraint(
            "status IN ('pending', 'trusted', 'revoked')",
            name="ck_trusted_devices_status",
        ),
        sa.ForeignKeyConstraint(
            ["login_id"], ["logins.id"], ondelete="CASCADE"
        ),
        sa.ForeignKeyConstraint(
            ["approved_by_login_id"], ["logins.id"], ondelete="SET NULL"
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_trusted_devices_id"), "trusted_devices", ["id"], unique=False
    )
    op.create_index(
        op.f("ix_trusted_devices_login_id"),
        "trusted_devices",
        ["login_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_trusted_devices_status"),
        "trusted_devices",
        ["status"],
        unique=False,
    )
    op.create_index(
        op.f("ix_trusted_devices_approved_by_login_id"),
        "trusted_devices",
        ["approved_by_login_id"],
        unique=False,
    )
    op.create_index(
        "uq_trusted_devices_one_trusted_per_login",
        "trusted_devices",
        ["login_id"],
        unique=True,
        postgresql_where=sa.text("status = 'trusted'"),
    )
    op.create_index(
        "uq_trusted_devices_one_pending_per_login",
        "trusted_devices",
        ["login_id"],
        unique=True,
        postgresql_where=sa.text("status = 'pending'"),
    )

    op.create_table(
        "webauthn_credentials",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("device_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("credential_id", sa.LargeBinary(), nullable=False),
        sa.Column("public_key", sa.LargeBinary(), nullable=False),
        sa.Column("sign_count", sa.Integer(), server_default="0", nullable=False),
        sa.Column("aaguid", sa.String(length=36), nullable=True),
        sa.Column("transports", sa.String(length=128), nullable=True),
        sa.Column(
            "backup_eligible",
            sa.Boolean(),
            server_default="false",
            nullable=False,
        ),
        sa.Column(
            "backup_state",
            sa.Boolean(),
            server_default="false",
            nullable=False,
        ),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(
            ["device_id"], ["trusted_devices.id"], ondelete="CASCADE"
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("device_id"),
        sa.UniqueConstraint("credential_id"),
    )
    op.create_index(
        op.f("ix_webauthn_credentials_id"),
        "webauthn_credentials",
        ["id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_webauthn_credentials_device_id"),
        "webauthn_credentials",
        ["device_id"],
        unique=True,
    )


def downgrade() -> None:
    op.drop_index(
        op.f("ix_webauthn_credentials_device_id"),
        table_name="webauthn_credentials",
    )
    op.drop_index(
        op.f("ix_webauthn_credentials_id"), table_name="webauthn_credentials"
    )
    op.drop_table("webauthn_credentials")
    op.drop_index(
        "uq_trusted_devices_one_pending_per_login", table_name="trusted_devices"
    )
    op.drop_index(
        "uq_trusted_devices_one_trusted_per_login", table_name="trusted_devices"
    )
    op.drop_index(
        op.f("ix_trusted_devices_approved_by_login_id"),
        table_name="trusted_devices",
    )
    op.drop_index(op.f("ix_trusted_devices_status"), table_name="trusted_devices")
    op.drop_index(
        op.f("ix_trusted_devices_login_id"), table_name="trusted_devices"
    )
    op.drop_index(op.f("ix_trusted_devices_id"), table_name="trusted_devices")
    op.drop_table("trusted_devices")
    op.drop_column("logins", "device_binding_required")

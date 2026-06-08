"""Create login_events table for per-service login audit

Revision ID: a1b2c3d4e5f6
Revises: c8f2a1b3d4e5
Create Date: 2026-05-16 12:00:00.000000
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "a1b2c3d4e5f6"
down_revision: Union[str, Sequence[str], None] = "c8f2a1b3d4e5"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "login_events",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("user_id", sa.UUID(), nullable=False),
        sa.Column("login_id", sa.Integer(), nullable=False),
        sa.Column("service_id", sa.String(length=64), nullable=True),
        sa.Column(
            "logged_in_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(["login_id"], ["logins.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_login_events_id"), "login_events", ["id"], unique=False)
    op.create_index(op.f("ix_login_events_user_id"), "login_events", ["user_id"], unique=False)
    op.create_index(op.f("ix_login_events_login_id"), "login_events", ["login_id"], unique=False)
    op.create_index(
        op.f("ix_login_events_service_id"), "login_events", ["service_id"], unique=False
    )
    op.create_index(
        op.f("ix_login_events_logged_in_at"), "login_events", ["logged_in_at"], unique=False
    )


def downgrade() -> None:
    op.drop_index(op.f("ix_login_events_logged_in_at"), table_name="login_events")
    op.drop_index(op.f("ix_login_events_service_id"), table_name="login_events")
    op.drop_index(op.f("ix_login_events_login_id"), table_name="login_events")
    op.drop_index(op.f("ix_login_events_user_id"), table_name="login_events")
    op.drop_index(op.f("ix_login_events_id"), table_name="login_events")
    op.drop_table("login_events")

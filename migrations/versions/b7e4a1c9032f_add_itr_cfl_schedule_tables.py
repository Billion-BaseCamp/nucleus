"""add Schedule CFL (carry forward losses) tables

Revision ID: b7e4a1c9032f
Revises: a1f5c2e8d740
Create Date: 2026-04-21 12:00:00.000000

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "b7e4a1c9032f"
down_revision: Union[str, Sequence[str], None] = "a1f5c2e8d740"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "itr_cfl_schedule",
        sa.Column("id", sa.UUID(as_uuid=True), primary_key=True),
        sa.Column(
            "itr_return_id",
            sa.UUID(as_uuid=True),
            sa.ForeignKey("itr_returns.id", ondelete="CASCADE"),
            nullable=False,
            unique=True,
        ),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=True,
        ),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
    )

    op.create_table(
        "itr_cfl_year_entries",
        sa.Column("id", sa.UUID(as_uuid=True), primary_key=True),
        sa.Column(
            "cfl_schedule_id",
            sa.UUID(as_uuid=True),
            sa.ForeignKey("itr_cfl_schedule.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("years_back", sa.Integer(), nullable=False),
        sa.Column("original_assessment_year", sa.String(length=10), nullable=False),
        sa.Column("date_of_filing", sa.Date(), nullable=True),
        sa.Column(
            "hp_loss_cf",
            sa.Numeric(18, 2),
            nullable=False,
            server_default="0",
        ),
        sa.Column(
            "stcg_loss_cf",
            sa.Numeric(18, 2),
            nullable=False,
            server_default="0",
        ),
        sa.Column(
            "ltcg_loss_cf",
            sa.Numeric(18, 2),
            nullable=False,
            server_default="0",
        ),
        sa.Column(
            "os_race_horse_loss_cf",
            sa.Numeric(18, 2),
            nullable=False,
            server_default="0",
        ),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=True,
        ),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
        sa.UniqueConstraint(
            "cfl_schedule_id",
            "years_back",
            name="uq_cfl_year_entry_per_schedule",
        ),
    )
    op.create_index(
        "ix_itr_cfl_year_entries_cfl_schedule_id",
        "itr_cfl_year_entries",
        ["cfl_schedule_id"],
        unique=False,
    )

    op.create_table(
        "itr_cfl_summary",
        sa.Column("id", sa.UUID(as_uuid=True), primary_key=True),
        sa.Column(
            "cfl_schedule_id",
            sa.UUID(as_uuid=True),
            sa.ForeignKey("itr_cfl_schedule.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("summary_type", sa.String(length=30), nullable=False),
        sa.Column(
            "hp_loss_cf",
            sa.Numeric(18, 2),
            nullable=False,
            server_default="0",
        ),
        sa.Column(
            "stcg_loss_cf",
            sa.Numeric(18, 2),
            nullable=False,
            server_default="0",
        ),
        sa.Column(
            "ltcg_loss_cf",
            sa.Numeric(18, 2),
            nullable=False,
            server_default="0",
        ),
        sa.Column(
            "os_race_horse_loss_cf",
            sa.Numeric(18, 2),
            nullable=False,
            server_default="0",
        ),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=True,
        ),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
        sa.UniqueConstraint(
            "cfl_schedule_id",
            "summary_type",
            name="uq_cfl_summary_per_schedule",
        ),
    )
    op.create_index(
        "ix_itr_cfl_summary_cfl_schedule_id",
        "itr_cfl_summary",
        ["cfl_schedule_id"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index("ix_itr_cfl_summary_cfl_schedule_id", table_name="itr_cfl_summary")
    op.drop_table("itr_cfl_summary")
    op.drop_index(
        "ix_itr_cfl_year_entries_cfl_schedule_id", table_name="itr_cfl_year_entries"
    )
    op.drop_table("itr_cfl_year_entries")
    op.drop_table("itr_cfl_schedule")

"""Add reconciliation_status and tax-credit source/is_edited/remarks columns.

Revision ID: 8fe746b805a1
Revises: 260ae545150c
Create Date: 2026-06-08

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "8fe746b805a1"
down_revision: Union[str, None] = "260ae545150c"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def _add_is_edited(table_name: str) -> None:
    """Add NOT NULL is_edited with server default so existing rows backfill."""
    op.add_column(
        table_name,
        sa.Column(
            "is_edited",
            sa.Boolean(),
            nullable=False,
            server_default=sa.false(),
        ),
    )


def upgrade() -> None:
    op.add_column(
        "itr_unified_entries",
        sa.Column("reconciliation_status", sa.String(length=32), nullable=True),
    )
    op.create_index(
        op.f("ix_itr_unified_entries_reconciliation_status"),
        "itr_unified_entries",
        ["reconciliation_status"],
        unique=False,
    )

    for table in (
        "itr_tds_salary",
        "itr_tds_non_salary",
        "itr_tds_property",
        "itr_tcs",
    ):
        op.add_column(table, sa.Column("source", sa.String(length=20), nullable=True))
        _add_is_edited(table)
        op.add_column(table, sa.Column("remarks", sa.Text(), nullable=True))


def downgrade() -> None:
    for table in (
        "itr_tcs",
        "itr_tds_property",
        "itr_tds_non_salary",
        "itr_tds_salary",
    ):
        op.drop_column(table, "remarks")
        op.drop_column(table, "is_edited")
        op.drop_column(table, "source")

    op.drop_index(
        op.f("ix_itr_unified_entries_reconciliation_status"),
        table_name="itr_unified_entries",
    )
    op.drop_column("itr_unified_entries", "reconciliation_status")

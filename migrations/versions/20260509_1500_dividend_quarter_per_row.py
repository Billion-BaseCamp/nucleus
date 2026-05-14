"""dividend quarter per row + drop schedule-level dividend breakdown

Revision ID: 34041d2893d5
Revises: c365b727d497
Create Date: 2026-05-09 15:00:00.000000

Replaces the schedule-level ``dividend_quarterly_breakdown`` JSONB column
(added in c365b727d497) with a per-row ``quarter`` column on
``itr_os_dividend_details``. The advisor now picks a CBDT
``AccruOrRecOfCG.DateRange`` slot per dividend entry; the compute layer
aggregates per-row at compute time to drive the Sec 234C proviso.

``quarter`` is nullable — existing rows remain NULL until an advisor
fills them.
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


revision: str = "34041d2893d5"
down_revision: Union[str, Sequence[str], None] = "c365b727d497"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "itr_os_dividend_details",
        sa.Column("quarter", sa.String(length=20), nullable=True),
    )
    op.drop_column("itr_os_schedule", "dividend_quarterly_breakdown")


def downgrade() -> None:
    op.add_column(
        "itr_os_schedule",
        sa.Column(
            "dividend_quarterly_breakdown",
            postgresql.JSONB(astext_type=sa.Text()),
            nullable=True,
        ),
    )
    op.drop_column("itr_os_dividend_details", "quarter")

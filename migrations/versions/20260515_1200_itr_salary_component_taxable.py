"""Add taxable column to itr_salary_components

Revision ID: c8f2a1b3d4e5
Revises:
Create Date: 2026-05-15 12:00:00.000000

Persists Salary u/s 17(1) taxable amount (received - exempt when not overridden).
Backfill existing rows where taxable was implicitly received - exempt.
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "c8f2a1b3d4e5"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "itr_salary_components",
        sa.Column("taxable", sa.Numeric(precision=18, scale=2), nullable=False, server_default="0"),
    )
    op.execute(
        """
        UPDATE itr_salary_components
        SET taxable = GREATEST(received - exempt, 0)
        WHERE taxable = 0 AND received > 0
        """
    )
    op.alter_column("itr_salary_components", "taxable", server_default=None)


def downgrade() -> None:
    op.drop_column("itr_salary_components", "taxable")

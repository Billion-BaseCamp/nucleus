"""Restore flat salary schedule columns removed in 52e291d

Revision ID: d9e3f2a1b4c6
Revises: c8f2a1b3d4e5
Create Date: 2026-05-16 10:00:00.000000

The nucleus model commit 52e291d replaced total_exempt_us10 / net_salary /
total_deduction_us16 / total_net_taxable with new_regime_* / old_regime_*
variants but did not write a migration. Production DB was left without the
old columns while the installed backend (nucleus v0.22.3) still expects them.
This migration restores the four flat columns so the v0.22.3 ORM model works.
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "d9e3f2a1b4c6"
down_revision: Union[str, Sequence[str], None] = "c8f2a1b3d4e5"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "itr_salary_schedule",
        sa.Column("total_exempt_us10", sa.Numeric(precision=18, scale=2), nullable=True, server_default="0"),
    )
    op.add_column(
        "itr_salary_schedule",
        sa.Column("net_salary", sa.Numeric(precision=18, scale=2), nullable=True, server_default="0"),
    )
    op.add_column(
        "itr_salary_schedule",
        sa.Column("total_deduction_us16", sa.Numeric(precision=18, scale=2), nullable=True, server_default="0"),
    )
    op.add_column(
        "itr_salary_schedule",
        sa.Column("total_net_taxable", sa.Numeric(precision=18, scale=2), nullable=True, server_default="0"),
    )


def downgrade() -> None:
    op.drop_column("itr_salary_schedule", "total_net_taxable")
    op.drop_column("itr_salary_schedule", "total_deduction_us16")
    op.drop_column("itr_salary_schedule", "net_salary")
    op.drop_column("itr_salary_schedule", "total_exempt_us10")

"""Backfill NULL per-employer computed regime columns to zero.

Revision ID: f2a5b6c7d8e9
Revises: e1f4c3d5a6b7
Create Date: 2026-05-16 15:00:00.000000
"""

from typing import Sequence, Union

from alembic import op

revision: str = "f2a5b6c7d8e9"
down_revision: Union[str, Sequence[str], None] = "e1f4c3d5a6b7"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute(
        """
        UPDATE itr_salary_employers
        SET
            computed_gross_salary  = 0,
            old_regime_exempt_us10 = 0,
            old_regime_income      = 0,
            new_regime_exempt_us10 = 0,
            new_regime_income      = 0
        WHERE computed_gross_salary IS NULL
        """
    )


def downgrade() -> None:
    pass

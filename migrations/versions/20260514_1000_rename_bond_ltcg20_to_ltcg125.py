"""rename itr_cg_bond_entries.ltcg_20 → ltcg_125

Finance Act 2024 changed the LTCG rate on bonds/debentures from 20% to
12.5% (Sec 112, no indexation). The column is renamed to reflect the
correct statutory rate for AY 2025-26 onwards.

Revision ID: a3f8d2e1b047
Revises: 34041d2893d5
Create Date: 2026-05-14 10:00:00.000000
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "a3f8d2e1b047"
down_revision: Union[str, None] = "34041d2893d5"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column(
        "itr_cg_bond_entries",
        "ltcg_20",
        new_column_name="ltcg_125",
    )


def downgrade() -> None:
    op.alter_column(
        "itr_cg_bond_entries",
        "ltcg_125",
        new_column_name="ltcg_20",
    )

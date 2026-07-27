"""Add Schedule EI free-text Others columns on itr_tax_exempt_income.

Revision ID: c18ca367cb24
Revises: 743e974c55a6
Create Date: 2026-07-28

Existing rows need a server_default when adding NOT NULL exempt_others.
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "c18ca367cb24"
down_revision: Union[str, Sequence[str], None] = "743e974c55a6"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "itr_tax_exempt_income",
        sa.Column(
            "exempt_others",
            sa.Numeric(precision=15, scale=2),
            nullable=False,
            server_default="0",
        ),
    )
    op.add_column(
        "itr_tax_exempt_income",
        sa.Column(
            "exempt_others_description",
            sa.String(length=125),
            nullable=True,
        ),
    )
    # Keep DB default aligned with model default=0 for future inserts.
    # If you prefer app-only defaults, drop it:
    # op.alter_column("itr_tax_exempt_income", "exempt_others", server_default=None)


def downgrade() -> None:
    op.drop_column("itr_tax_exempt_income", "exempt_others_description")
    op.drop_column("itr_tax_exempt_income", "exempt_others")

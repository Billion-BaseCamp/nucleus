"""Add notes and noted_by JSONB columns on filed-year schedules.

Revision ID: 20260925_fy_notes
Revises: fa9610fce873
Create Date: 2026-09-25 11:40:00.000000

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision: str = "20260925_fy_notes"
down_revision: Union[str, Sequence[str], None] = "fa9610fce873"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "itr_filed_year_schedules",
        sa.Column(
            "notes",
            postgresql.JSONB(astext_type=sa.Text()),
            nullable=False,
            server_default=sa.text("'[]'::jsonb"),
        ),
    )
    op.add_column(
        "itr_filed_year_schedules",
        sa.Column(
            "noted_by",
            postgresql.JSONB(astext_type=sa.Text()),
            nullable=False,
            server_default=sa.text("'[]'::jsonb"),
        ),
    )


def downgrade() -> None:
    op.drop_column("itr_filed_year_schedules", "noted_by")
    op.drop_column("itr_filed_year_schedules", "notes")

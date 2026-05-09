"""dividend quarterly breakdown column

Revision ID: c365b727d497
Revises: b7e4a1c9032f
Create Date: 2026-05-09 12:00:00.000000

Adds ``dividend_quarterly_breakdown`` (JSONB, nullable) to
``itr_os_schedule``. Stores per-installment-window dividend amounts in the
CBDT ``AccruOrRecOfCG.DateRange`` shape so the 234C compute layer can apply
the Sec 234C proviso deferral to dividend income.

Nullable; no backfill required. Existing rows remain NULL until a user
enters a quarterly split or an importer populates it.
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


revision: str = "c365b727d497"
down_revision: Union[str, Sequence[str], None] = "b7e4a1c9032f"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "itr_os_schedule",
        sa.Column(
            "dividend_quarterly_breakdown",
            postgresql.JSONB(astext_type=sa.Text()),
            nullable=True,
        ),
    )


def downgrade() -> None:
    op.drop_column("itr_os_schedule", "dividend_quarterly_breakdown")

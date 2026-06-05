"""Add advisor_comment to itr_documents.

Revision ID: 20260605_advisor_comment
Revises:
Create Date: 2026-06-05
"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "20260605_advisor_comment"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "itr_documents",
        sa.Column("advisor_comment", sa.String(), nullable=True),
    )


def downgrade() -> None:
    op.drop_column("itr_documents", "advisor_comment")

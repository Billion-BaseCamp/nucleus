"""Merge all heads into one

Revision ID: 6a3129afc7aa
Revises: 20260128_addresstype, fix_residency_end_date_rule
Create Date: 2026-01-28 18:36:44.669160

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6a3129afc7aa'
down_revision: Union[str, Sequence[str], None] = ('20260128_addresstype', 'fix_residency_end_date_rule')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass

"""remove unique constraint on client_id and address_type from addresses

Revision ID: 76950d916f5a
Revises: 418b66d2ddf0
Create Date: 2026-01-28 18:57:27.551101

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '76950d916f5a'
down_revision: Union[str, Sequence[str], None] = '418b66d2ddf0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.drop_index(
        "ux_client_address_type",
        table_name="addresses",
    )

def downgrade():
    op.create_index(
        "ux_client_address_type",
        "addresses",
        ["client_id", "address_type"],
        unique=True,
    )


"""add unique index on client_id and address_type in addresses

Revision ID: 418b66d2ddf0
Revises: 6a3129afc7aa
Create Date: 2026-01-28 18:36:52.779890

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '418b66d2ddf0'
down_revision: Union[str, Sequence[str], None] = '6a3129afc7aa'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_index(
        "ux_client_address_type",
        "addresses",
        ["client_id", "address_type"],
        unique=True,
    )



def downgrade():
    op.drop_index(
        "ux_client_address_type",
        table_name="addresses",
    )


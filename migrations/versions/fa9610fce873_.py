"""auto migration

Revision ID: fa9610fce873
Revises: 72961275fc21
Create Date: 2026-09-23 00:00:00.000000

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "fa9610fce873"
down_revision: Union[str, Sequence[str], None] = "72961275fc21"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column(
        "itr_tax_credit_schedule",
        sa.Column(
            "total_relief_available",
            sa.Numeric(precision=20, scale=2),
            nullable=False,
            server_default="0",
        ),
    )
    op.add_column(
        "itr_tax_credit_schedule",
        sa.Column(
            "total_tds_on_property",
            sa.Numeric(precision=20, scale=2),
            nullable=False,
            server_default="0",
        ),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("itr_tax_credit_schedule", "total_tds_on_property")
    op.drop_column("itr_tax_credit_schedule", "total_relief_available")

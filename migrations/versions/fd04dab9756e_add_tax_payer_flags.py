from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'fd04dab9756e'
down_revision: Union[str, Sequence[str], None] = '02533cebd7c9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column(
        "tax_profile",
        sa.Column(
            "is_india_tax_payer",
            sa.Boolean(),
            nullable=False,
            server_default=sa.text("false"),
        ),
    )

    op.add_column(
        "tax_profile",
        sa.Column(
            "is_us_tax_payer",
            sa.Boolean(),
            nullable=False,
            server_default=sa.text("false"),
        ),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("tax_profile", "is_us_tax_payer")
    op.drop_column("tax_profile", "is_india_tax_payer")

from alembic import op
import sqlalchemy as sa

def upgrade():
    op.add_column(
        "addresses",
        sa.Column("citizenship_start_date", sa.Date(), nullable=True)
    )
    op.add_column(
        "addresses",
        sa.Column("citizenship_end_date", sa.Date(), nullable=True)
    )

def downgrade():
    op.drop_column("addresses", "citizenship_end_date")
    op.drop_column("addresses", "citizenship_start_date")

"""Advance Tax quarter-scoped Form 26AS S3 uploads.

Revision ID: 20260822_advance_tax_26as_uploads
Revises:
Create Date: 2026-08-22
"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "20260822_advance_tax_26as_uploads"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

_FORM_26AS_PART_TABLES = tuple(f"form_26as_part{i}" for i in range(1, 11))


def upgrade() -> None:
    op.create_table(
        "advance_tax_26as_uploads",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("client_id", sa.UUID(), nullable=False),
        sa.Column("financial_year_id", sa.UUID(), nullable=False),
        sa.Column("quarter_id", sa.UUID(), nullable=False),
        sa.Column("s3_key", sa.String(length=512), nullable=False),
        sa.Column("bucket_name", sa.String(length=255), nullable=False),
        sa.Column("original_filename", sa.String(length=255), nullable=False),
        sa.Column("file_size_bytes", sa.Integer(), nullable=True),
        sa.Column("pan", sa.String(length=10), nullable=True),
        sa.Column(
            "uploaded_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(["client_id"], ["clients.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(
            ["financial_year_id"], ["financial_years.id"], ondelete="CASCADE"
        ),
        sa.ForeignKeyConstraint(["quarter_id"], ["quarters.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("quarter_id", name="uq_advance_tax_26as_uploads_quarter_id"),
    )
    op.create_index(
        op.f("ix_advance_tax_26as_uploads_id"),
        "advance_tax_26as_uploads",
        ["id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_advance_tax_26as_uploads_client_id"),
        "advance_tax_26as_uploads",
        ["client_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_advance_tax_26as_uploads_financial_year_id"),
        "advance_tax_26as_uploads",
        ["financial_year_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_advance_tax_26as_uploads_quarter_id"),
        "advance_tax_26as_uploads",
        ["quarter_id"],
        unique=False,
    )

    op.add_column(
        "quarters",
        sa.Column("advance_tax_26as_upload_id", sa.UUID(), nullable=True),
    )
    op.create_index(
        op.f("ix_quarters_advance_tax_26as_upload_id"),
        "quarters",
        ["advance_tax_26as_upload_id"],
        unique=False,
    )
    op.create_foreign_key(
        "fk_quarters_advance_tax_26as_upload_id",
        "quarters",
        "advance_tax_26as_uploads",
        ["advance_tax_26as_upload_id"],
        ["id"],
        ondelete="SET NULL",
    )

    for table_name in _FORM_26AS_PART_TABLES:
        op.add_column(table_name, sa.Column("upload_id", sa.UUID(), nullable=True))
        op.create_index(
            op.f(f"ix_{table_name}_upload_id"),
            table_name,
            ["upload_id"],
            unique=False,
        )
        op.create_foreign_key(
            f"fk_{table_name}_upload_id",
            table_name,
            "advance_tax_26as_uploads",
            ["upload_id"],
            ["id"],
            ondelete="CASCADE",
        )


def downgrade() -> None:
    for table_name in reversed(_FORM_26AS_PART_TABLES):
        op.drop_constraint(f"fk_{table_name}_upload_id", table_name, type_="foreignkey")
        op.drop_index(op.f(f"ix_{table_name}_upload_id"), table_name=table_name)
        op.drop_column(table_name, "upload_id")

    op.drop_constraint(
        "fk_quarters_advance_tax_26as_upload_id", "quarters", type_="foreignkey"
    )
    op.drop_index(
        op.f("ix_quarters_advance_tax_26as_upload_id"), table_name="quarters"
    )
    op.drop_column("quarters", "advance_tax_26as_upload_id")

    op.drop_index(
        op.f("ix_advance_tax_26as_uploads_quarter_id"),
        table_name="advance_tax_26as_uploads",
    )
    op.drop_index(
        op.f("ix_advance_tax_26as_uploads_financial_year_id"),
        table_name="advance_tax_26as_uploads",
    )
    op.drop_index(
        op.f("ix_advance_tax_26as_uploads_client_id"),
        table_name="advance_tax_26as_uploads",
    )
    op.drop_index(
        op.f("ix_advance_tax_26as_uploads_id"), table_name="advance_tax_26as_uploads"
    )
    op.drop_table("advance_tax_26as_uploads")

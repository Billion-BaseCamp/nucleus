"""TIS PDF S3 archives per client.

Revision ID: 20260707_itr_tis_pdf_archives
Revises: 20260703_ais_json_archives_unique
Create Date: 2026-07-07

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "20260707_itr_tis_pdf_archives"
down_revision: Union[str, Sequence[str], None] = "20260703_ais_json_archives_unique"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "itr_tis_pdf_archives",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("client_id", sa.UUID(), nullable=False),
        sa.Column("itr_return_id", sa.UUID(), nullable=True),
        sa.Column("s3_key", sa.String(length=512), nullable=False),
        sa.Column("original_filename", sa.String(length=255), nullable=False),
        sa.Column("file_size_bytes", sa.Integer(), nullable=True),
        sa.Column(
            "status",
            sa.String(length=32),
            nullable=False,
            server_default="pending_upload",
        ),
        sa.Column("failure_reason", sa.String(length=64), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(["client_id"], ["clients.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["itr_return_id"], ["itr_returns.id"], ondelete="SET NULL"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_itr_tis_pdf_archives_client_id"),
        "itr_tis_pdf_archives",
        ["client_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_itr_tis_pdf_archives_itr_return_id"),
        "itr_tis_pdf_archives",
        ["itr_return_id"],
        unique=False,
    )
    op.create_index(
        "uq_itr_tis_pdf_archives_client_itr",
        "itr_tis_pdf_archives",
        ["client_id", "itr_return_id"],
        unique=True,
        postgresql_where=sa.text("itr_return_id IS NOT NULL"),
    )
    op.create_index(
        "uq_itr_tis_pdf_archives_client_unlinked",
        "itr_tis_pdf_archives",
        ["client_id"],
        unique=True,
        postgresql_where=sa.text("itr_return_id IS NULL"),
    )


def downgrade() -> None:
    op.drop_index(
        "uq_itr_tis_pdf_archives_client_unlinked",
        table_name="itr_tis_pdf_archives",
    )
    op.drop_index(
        "uq_itr_tis_pdf_archives_client_itr",
        table_name="itr_tis_pdf_archives",
    )
    op.drop_index(
        op.f("ix_itr_tis_pdf_archives_itr_return_id"),
        table_name="itr_tis_pdf_archives",
    )
    op.drop_index(
        op.f("ix_itr_tis_pdf_archives_client_id"),
        table_name="itr_tis_pdf_archives",
    )
    op.drop_table("itr_tis_pdf_archives")

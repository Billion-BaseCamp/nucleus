"""v0.20.0 capital gains ingestion columns

Revision ID: a1f5c2e8d740
Revises: be2b62f9ff0e
Create Date: 2026-04-20 15:00:00.000000

Phase 0 additive schema changes for tax-engine-backend V1 ITR-2 compute:
- isin, stt_paid, grandfathering_fmv on itr_cg_india_eq_and_debt_mf_transactions
- indexed_cost_of_acquisition on itr_cg_unlisted_transactions
- quarterly_breakdown (JSONB) on itr_cg_schedule
- source_document_id (UUID, indexed) on 7 CG child tables for broker-level
  idempotent re-ingestion.

All columns nullable; no backfill required.
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


revision: str = 'a1f5c2e8d740'
down_revision: Union[str, Sequence[str], None] = 'be2b62f9ff0e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


SOURCE_DOC_TABLES = [
    "itr_cg_india_eq_and_debt_mf_brokers_data",
    "itr_cg_us_brokers_data",
    "itr_cg_unlisted_transactions",
    "itr_cg_vda_transactions",
    "itr_cg_hp_entries",
    "itr_cg_exemptions_54",
    "itr_cg_exemptions_54f",
]


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column(
        "itr_cg_india_eq_and_debt_mf_transactions",
        sa.Column("isin", sa.String(length=12), nullable=True),
    )
    op.add_column(
        "itr_cg_india_eq_and_debt_mf_transactions",
        sa.Column("stt_paid", sa.Numeric(15, 2), nullable=True),
    )
    op.add_column(
        "itr_cg_india_eq_and_debt_mf_transactions",
        sa.Column("grandfathering_fmv", sa.Numeric(15, 4), nullable=True),
    )

    op.add_column(
        "itr_cg_unlisted_transactions",
        sa.Column("indexed_cost_of_acquisition", sa.Numeric(15, 2), nullable=True),
    )

    op.add_column(
        "itr_cg_schedule",
        sa.Column("quarterly_breakdown", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
    )

    for table in SOURCE_DOC_TABLES:
        op.add_column(
            table,
            sa.Column("source_document_id", postgresql.UUID(as_uuid=True), nullable=True),
        )
        op.create_index(
            f"ix_{table}_source_document_id",
            table,
            ["source_document_id"],
        )


def downgrade() -> None:
    """Downgrade schema."""
    for table in SOURCE_DOC_TABLES:
        op.drop_index(f"ix_{table}_source_document_id", table_name=table)
        op.drop_column(table, "source_document_id")

    op.drop_column("itr_cg_schedule", "quarterly_breakdown")

    op.drop_column("itr_cg_unlisted_transactions", "indexed_cost_of_acquisition")

    op.drop_column("itr_cg_india_eq_and_debt_mf_transactions", "grandfathering_fmv")
    op.drop_column("itr_cg_india_eq_and_debt_mf_transactions", "stt_paid")
    op.drop_column("itr_cg_india_eq_and_debt_mf_transactions", "isin")

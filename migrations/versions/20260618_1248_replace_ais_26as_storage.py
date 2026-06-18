"""Replace AIS/26AS staging storage.

Revision ID: 20260618_1248
Revises: None
Create Date: 2026-06-18 12:48:00

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = "20260618_1248"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute("DROP TABLE IF EXISTS itr_ais_sft_transactions CASCADE")
    op.execute("DROP TABLE IF EXISTS itr_unified_entries CASCADE")
    op.execute("DROP TABLE IF EXISTS itr_form26as_lines CASCADE")
    op.execute("DROP TABLE IF EXISTS itr_ais_lines CASCADE")

    op.create_table(
        "itr_ais_26as_uploads",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("itr_return_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("document_type", sa.String(length=8), nullable=False),
        sa.Column("original_filename", sa.String(length=255), nullable=False),
        sa.Column("pan", sa.String(length=10), nullable=True),
        sa.Column("financial_year", sa.String(length=9), nullable=True),
        sa.Column("assessment_year", sa.String(length=10), nullable=True),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("raw_json", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column("raw_text", sa.Text(), nullable=True),
        sa.Column("summary", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.CheckConstraint("document_type IN ('AIS', '26AS')", name="ck_itr_ais_26as_uploads_document_type"),
        sa.ForeignKeyConstraint(["itr_return_id"], ["itr_returns.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_itr_ais_26as_uploads_itr_return_id", "itr_ais_26as_uploads", ["itr_return_id"])
    op.create_index("ix_itr_ais_26as_uploads_pan", "itr_ais_26as_uploads", ["pan"])

    op.create_table(
        "itr_ais_entries",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("upload_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("itr_return_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("display_order", sa.Integer(), nullable=False),
        sa.Column("part", sa.String(length=64), nullable=False),
        sa.Column("entry_level", sa.String(length=32), nullable=True),
        sa.Column("info_code", sa.String(length=128), nullable=False),
        sa.Column("category_code", sa.String(length=32), nullable=False),
        sa.Column("description", sa.String(length=255), nullable=True),
        sa.Column("source_name", sa.String(length=125), nullable=True),
        sa.Column("source_tan_or_pan", sa.String(length=10), nullable=False),
        sa.Column("amount", sa.Numeric(20, 2), nullable=False),
        sa.Column("ais_tds_deducted", sa.Numeric(20, 2), nullable=False),
        sa.Column("ais_tds_deposited", sa.Numeric(20, 2), nullable=False),
        sa.Column("section_key", sa.String(length=64), nullable=False),
        sa.Column("section_code", sa.String(length=32), nullable=False),
        sa.Column("itr_schedule", sa.String(length=8), nullable=False),
        sa.Column("entry_type", sa.String(length=16), nullable=False),
        sa.Column("transaction_count", sa.Integer(), nullable=False),
        sa.Column("included_in_reconciliation", sa.Boolean(), nullable=False),
        sa.Column("skip_reason", sa.String(length=255), nullable=True),
        sa.Column("raw_payload", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["itr_return_id"], ["itr_returns.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["upload_id"], ["itr_ais_26as_uploads.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_itr_ais_entries_itr_return_id", "itr_ais_entries", ["itr_return_id"])
    op.create_index("ix_itr_ais_entries_upload_id", "itr_ais_entries", ["upload_id"])

    op.create_table(
        "itr_26as_entries",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("upload_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("itr_return_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("display_order", sa.Integer(), nullable=False),
        sa.Column("part", sa.String(length=16), nullable=False),
        sa.Column("deductor_or_collector_name", sa.String(length=125), nullable=False),
        sa.Column("tan_or_pan", sa.String(length=10), nullable=False),
        sa.Column("section", sa.String(length=16), nullable=False),
        sa.Column("amount_paid_or_transaction", sa.Numeric(20, 2), nullable=False),
        sa.Column("tax_deducted_or_collected", sa.Numeric(20, 2), nullable=False),
        sa.Column("tds_or_tcs_deposited", sa.Numeric(20, 2), nullable=False),
        sa.Column("transaction_count", sa.Integer(), nullable=False),
        sa.Column("notes", sa.String(length=255), nullable=True),
        sa.Column("raw_payload", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["itr_return_id"], ["itr_returns.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["upload_id"], ["itr_ais_26as_uploads.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_itr_26as_entries_itr_return_id", "itr_26as_entries", ["itr_return_id"])
    op.create_index("ix_itr_26as_entries_upload_id", "itr_26as_entries", ["upload_id"])

    op.create_table(
        "itr_ais_26as_reconciliations",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("itr_return_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("display_order", sa.Integer(), nullable=False),
        sa.Column("info_code", sa.String(length=128), nullable=False),
        sa.Column("category_code", sa.String(length=32), nullable=False),
        sa.Column("section_code", sa.String(length=32), nullable=False),
        sa.Column("itr_schedule", sa.String(length=8), nullable=False),
        sa.Column("entry_type", sa.String(length=16), nullable=False),
        sa.Column("source_name", sa.String(length=125), nullable=True),
        sa.Column("source_tan_or_pan", sa.String(length=10), nullable=False),
        sa.Column("ais_amount", sa.Numeric(20, 2), nullable=False),
        sa.Column("ais_tds_deducted", sa.Numeric(20, 2), nullable=False),
        sa.Column("form26as_amount", sa.Numeric(20, 2), nullable=False),
        sa.Column("form26as_tds_deposited", sa.Numeric(20, 2), nullable=False),
        sa.Column("income_amount", sa.Numeric(20, 2), nullable=False),
        sa.Column("tds_credit", sa.Numeric(20, 2), nullable=False),
        sa.Column("tcs_credit", sa.Numeric(20, 2), nullable=False),
        sa.Column("source_document", sa.String(length=8), nullable=False),
        sa.Column("flags", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column("reconciliation_status", sa.String(length=32), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["itr_return_id"], ["itr_returns.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "ix_itr_ais_26as_reconciliations_itr_return_id",
        "itr_ais_26as_reconciliations",
        ["itr_return_id"],
    )
    op.create_index(
        "ix_itr_ais_26as_reconciliations_reconciliation_status",
        "itr_ais_26as_reconciliations",
        ["reconciliation_status"],
    )

    op.create_table(
        "itr_ais_sft_transactions",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("upload_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("itr_return_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("display_order", sa.Integer(), nullable=False),
        sa.Column("transaction_kind", sa.String(length=16), nullable=False),
        sa.Column("tsn_id", sa.String(length=64), nullable=True),
        sa.Column("info_code", sa.String(length=128), nullable=False),
        sa.Column("category_code", sa.String(length=32), nullable=False),
        sa.Column("source_name", sa.String(length=125), nullable=True),
        sa.Column("source_id", sa.String(length=64), nullable=False),
        sa.Column("amount", sa.Numeric(20, 2), nullable=False),
        sa.Column("display_name", sa.String(length=255), nullable=True),
        sa.Column("asset_type", sa.String(length=32), nullable=True),
        sa.Column("transaction_date", sa.String(length=16), nullable=True),
        sa.Column("security_name", sa.String(length=255), nullable=True),
        sa.Column("nature_of_transfer", sa.String(length=128), nullable=True),
        sa.Column("holding_period", sa.String(length=64), nullable=True),
        sa.Column("quantity", sa.String(length=32), nullable=True),
        sa.Column("counterparty", sa.String(length=255), nullable=True),
        sa.Column("quarter", sa.String(length=32), nullable=True),
        sa.Column("client_id", sa.String(length=32), nullable=True),
        sa.Column("amc_name", sa.String(length=255), nullable=True),
        sa.Column("holder_flag", sa.String(length=16), nullable=True),
        sa.Column("sales_value", sa.Numeric(20, 2), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["itr_return_id"], ["itr_returns.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["upload_id"], ["itr_ais_26as_uploads.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_itr_ais_sft_transactions_itr_return_id", "itr_ais_sft_transactions", ["itr_return_id"])
    op.create_index("ix_itr_ais_sft_transactions_transaction_kind", "itr_ais_sft_transactions", ["transaction_kind"])
    op.create_index("ix_itr_ais_sft_transactions_tsn_id", "itr_ais_sft_transactions", ["tsn_id"])
    op.create_index("ix_itr_ais_sft_transactions_upload_id", "itr_ais_sft_transactions", ["upload_id"])


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("itr_ais_sft_transactions")
    op.drop_table("itr_ais_26as_reconciliations")
    op.drop_table("itr_26as_entries")
    op.drop_table("itr_ais_entries")
    op.drop_table("itr_ais_26as_uploads")

    op.create_table(
        "itr_ais_lines",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("itr_return_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("display_order", sa.Integer(), nullable=False),
        sa.Column("part", sa.String(length=64), nullable=False),
        sa.Column("info_code", sa.String(length=128), nullable=False),
        sa.Column("category_code", sa.String(length=32), nullable=False),
        sa.Column("description", sa.String(length=255), nullable=True),
        sa.Column("source_name", sa.String(length=125), nullable=True),
        sa.Column("source_tan_or_pan", sa.String(length=10), nullable=False),
        sa.Column("amount", sa.Numeric(20, 2), nullable=False),
        sa.Column("ais_tds_deducted", sa.Numeric(20, 2), nullable=False),
        sa.Column("ais_tds_deposited", sa.Numeric(20, 2), nullable=False),
        sa.Column("section_key", sa.String(length=64), nullable=False),
        sa.Column("section_code", sa.String(length=32), nullable=False),
        sa.Column("itr_schedule", sa.String(length=8), nullable=False),
        sa.Column("entry_type", sa.String(length=16), nullable=False),
        sa.Column("transaction_count", sa.Integer(), nullable=False),
        sa.Column("included_in_reconciliation", sa.Boolean(), nullable=False),
        sa.Column("skip_reason", sa.String(length=255), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["itr_return_id"], ["itr_returns.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_itr_ais_lines_itr_return_id", "itr_ais_lines", ["itr_return_id"])

    op.create_table(
        "itr_form26as_lines",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("itr_return_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("display_order", sa.Integer(), nullable=False),
        sa.Column("part", sa.String(length=16), nullable=False),
        sa.Column("deductor_or_collector_name", sa.String(length=125), nullable=False),
        sa.Column("tan_or_pan", sa.String(length=10), nullable=False),
        sa.Column("section", sa.String(length=16), nullable=False),
        sa.Column("amount_paid_or_transaction", sa.Numeric(20, 2), nullable=False),
        sa.Column("tax_deducted_or_collected", sa.Numeric(20, 2), nullable=False),
        sa.Column("tds_or_tcs_deposited", sa.Numeric(20, 2), nullable=False),
        sa.Column("transaction_count", sa.Integer(), nullable=False),
        sa.Column("notes", sa.String(length=255), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["itr_return_id"], ["itr_returns.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_itr_form26as_lines_itr_return_id", "itr_form26as_lines", ["itr_return_id"])

    op.create_table(
        "itr_unified_entries",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("itr_return_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("display_order", sa.Integer(), nullable=False),
        sa.Column("info_code", sa.String(length=128), nullable=False),
        sa.Column("category_code", sa.String(length=32), nullable=False),
        sa.Column("section_code", sa.String(length=32), nullable=False),
        sa.Column("itr_schedule", sa.String(length=8), nullable=False),
        sa.Column("entry_type", sa.String(length=16), nullable=False),
        sa.Column("source_name", sa.String(length=125), nullable=True),
        sa.Column("source_tan_or_pan", sa.String(length=10), nullable=False),
        sa.Column("ais_amount", sa.Numeric(20, 2), nullable=False),
        sa.Column("ais_tds_deducted", sa.Numeric(20, 2), nullable=False),
        sa.Column("form26as_amount", sa.Numeric(20, 2), nullable=False),
        sa.Column("form26as_tds_deposited", sa.Numeric(20, 2), nullable=False),
        sa.Column("income_amount", sa.Numeric(20, 2), nullable=False),
        sa.Column("tds_credit", sa.Numeric(20, 2), nullable=False),
        sa.Column("tcs_credit", sa.Numeric(20, 2), nullable=False),
        sa.Column("source_document", sa.String(length=8), nullable=False),
        sa.Column("flags", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column("reconciliation_status", sa.String(length=32), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["itr_return_id"], ["itr_returns.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_itr_unified_entries_itr_return_id", "itr_unified_entries", ["itr_return_id"])
    op.create_index("ix_itr_unified_entries_reconciliation_status", "itr_unified_entries", ["reconciliation_status"])

    op.create_table(
        "itr_ais_sft_transactions",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("itr_return_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("display_order", sa.Integer(), nullable=False),
        sa.Column("transaction_kind", sa.String(length=16), nullable=False),
        sa.Column("tsn_id", sa.String(length=64), nullable=True),
        sa.Column("info_code", sa.String(length=128), nullable=False),
        sa.Column("category_code", sa.String(length=32), nullable=False),
        sa.Column("source_name", sa.String(length=125), nullable=True),
        sa.Column("source_id", sa.String(length=64), nullable=False),
        sa.Column("amount", sa.Numeric(20, 2), nullable=False),
        sa.Column("display_name", sa.String(length=255), nullable=True),
        sa.Column("asset_type", sa.String(length=32), nullable=True),
        sa.Column("transaction_date", sa.String(length=16), nullable=True),
        sa.Column("security_name", sa.String(length=255), nullable=True),
        sa.Column("nature_of_transfer", sa.String(length=128), nullable=True),
        sa.Column("holding_period", sa.String(length=64), nullable=True),
        sa.Column("quantity", sa.String(length=32), nullable=True),
        sa.Column("counterparty", sa.String(length=255), nullable=True),
        sa.Column("quarter", sa.String(length=32), nullable=True),
        sa.Column("client_id", sa.String(length=32), nullable=True),
        sa.Column("amc_name", sa.String(length=255), nullable=True),
        sa.Column("holder_flag", sa.String(length=16), nullable=True),
        sa.Column("sales_value", sa.Numeric(20, 2), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["itr_return_id"], ["itr_returns.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_itr_ais_sft_transactions_itr_return_id", "itr_ais_sft_transactions", ["itr_return_id"])
    op.create_index("ix_itr_ais_sft_transactions_transaction_kind", "itr_ais_sft_transactions", ["transaction_kind"])
    op.create_index("ix_itr_ais_sft_transactions_tsn_id", "itr_ais_sft_transactions", ["tsn_id"])

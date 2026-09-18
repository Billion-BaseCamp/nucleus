"""Add itr_filed_year_summaries with nullable financial_year_id FK.

Revision ID: 20260918_filed_yr
Revises:
Create Date: 2026-09-18

Admin-dashboard snapshot of a filed ITR year. One row per client + assessment
year. ``financial_year_id`` is set only when ``financial_years`` already has
that client/FY; otherwise it stays NULL (historic years without a live FY row).

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
from sqlalchemy.engine.reflection import Inspector


# revision identifiers, used by Alembic.
# If `alembic current` already has a head, set down_revision to that revision
# before applying (this clone's versions/ folder was empty).
revision: str = "20260918_filed_yr"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

_TABLE = "itr_filed_year_summaries"
_FY_FK = "fk_itr_filed_year_summaries_financial_year_id"
_FY_IX = "ix_itr_filed_year_summaries_financial_year_id"

_JSONB_COLUMNS = (
    "schedule_s",
    "schedule_hp",
    "schedule_os",
    "schedule_cg",
    "schedule_112a",
    "schedule_115ad",
    "schedule_vda",
    "schedule_cfl",
    "schedule_cyla",
    "schedule_bfla",
    "schedule_via",
    "schedule_it",
    "schedule_tds1",
    "schedule_tds2",
    "schedule_tds3",
    "schedule_tcs",
    "schedule_si",
    "schedule_spi",
    "schedule_pti",
    "schedule_al",
    "schedule_fa",
    "schedule_fsi",
    "schedule_tr",
    "schedule_amt",
    "schedule_80g",
    "part_a_gen1",
    "part_b_ti",
    "part_b_tti",
)


def _inspector() -> Inspector:
    return sa.inspect(op.get_bind())


def _column_names(table: str) -> set[str]:
    return {col["name"] for col in _inspector().get_columns(table)}


def _fk_names(table: str) -> set[str]:
    return {fk["name"] for fk in _inspector().get_foreign_keys(table) if fk.get("name")}


def _index_names(table: str) -> set[str]:
    return {ix["name"] for ix in _inspector().get_indexes(table) if ix.get("name")}


def upgrade() -> None:
    """Upgrade schema."""
    inspector = _inspector()
    if _TABLE not in inspector.get_table_names():
        jsonb_cols = [
            sa.Column(
                name,
                postgresql.JSONB(astext_type=sa.Text()),
                nullable=False,
                server_default=sa.text("'{}'::jsonb"),
            )
            for name in _JSONB_COLUMNS
        ]
        op.create_table(
            _TABLE,
            sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
            sa.Column(
                "client_id",
                postgresql.UUID(as_uuid=True),
                sa.ForeignKey("clients.id", ondelete="CASCADE"),
                nullable=False,
            ),
            sa.Column(
                "financial_year_id",
                postgresql.UUID(as_uuid=True),
                sa.ForeignKey(
                    "financial_years.id",
                    ondelete="SET NULL",
                    name=_FY_FK,
                ),
                nullable=True,
            ),
            sa.Column("assessment_year", sa.String(length=10), nullable=False),
            sa.Column("financial_year", sa.String(length=7), nullable=False),
            sa.Column("pan", sa.String(length=10), nullable=True),
            sa.Column("itr_type", sa.String(length=10), nullable=True),
            sa.Column("s3_key", sa.String(length=512), nullable=False),
            sa.Column("original_filename", sa.String(length=255), nullable=False),
            sa.Column("file_size_bytes", sa.Integer(), nullable=True),
            sa.Column("content_sha256", sa.String(length=64), nullable=True),
            sa.Column(
                "status",
                sa.String(length=20),
                nullable=False,
                server_default=sa.text("'ready'"),
            ),
            sa.Column("total_income", sa.Numeric(18, 2), nullable=True),
            sa.Column("tax_payable", sa.Numeric(18, 2), nullable=True),
            sa.Column("refund_due", sa.Numeric(18, 2), nullable=True),
            sa.Column(
                "extractor_version",
                sa.String(length=20),
                nullable=False,
                server_default=sa.text("'1'"),
            ),
            *jsonb_cols,
            sa.Column(
                "created_at",
                sa.DateTime(timezone=True),
                server_default=sa.text("now()"),
                nullable=False,
            ),
            sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
            sa.UniqueConstraint(
                "client_id",
                "assessment_year",
                name="uq_itr_filed_year_summaries_client_ay",
            ),
        )
        op.create_index(
            "ix_itr_filed_year_summaries_client_id",
            _TABLE,
            ["client_id"],
        )
        op.create_index(_FY_IX, _TABLE, ["financial_year_id"])
        op.create_index(
            "ix_itr_filed_year_summaries_client_fy",
            _TABLE,
            ["client_id", "financial_year"],
        )
        return

    columns = _column_names(_TABLE)
    if "financial_year_id" not in columns:
        op.add_column(
            _TABLE,
            sa.Column(
                "financial_year_id",
                postgresql.UUID(as_uuid=True),
                nullable=True,
            ),
        )
    if _FY_FK not in _fk_names(_TABLE):
        op.create_foreign_key(
            _FY_FK,
            _TABLE,
            "financial_years",
            ["financial_year_id"],
            ["id"],
            ondelete="SET NULL",
        )
    if _FY_IX not in _index_names(_TABLE):
        op.create_index(_FY_IX, _TABLE, ["financial_year_id"])


def downgrade() -> None:
    """Downgrade schema."""
    inspector = _inspector()
    if _TABLE not in inspector.get_table_names():
        return
    if _FY_FK in _fk_names(_TABLE):
        op.drop_constraint(_FY_FK, _TABLE, type_="foreignkey")
    if _FY_IX in _index_names(_TABLE):
        op.drop_index(_FY_IX, table_name=_TABLE)
    if "financial_year_id" in _column_names(_TABLE):
        op.drop_column(_TABLE, "financial_year_id")

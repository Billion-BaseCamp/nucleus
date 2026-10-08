"""Rename CSA tables to *_raw, keeping every row.

Autogenerate treats a __tablename__ change as drop + create. These tables
already hold data, so this revision only renames them. Columns, indexes, and
foreign keys stay attached; PostgreSQL follows the table by identity.

Set down_revision to the current Alembic head before upgrading if this
environment already has other revisions. `alembic heads` prints that id.

Revision ID: 20261008_csa_raw
Revises: None
Create Date: 2026-10-08 11:40:00

"""
from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = "20261008_csa_raw"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

# Parent first, then the tables that reference it. Order does not matter for
# PostgreSQL rename; the pairs are listed this way so downgrade is the reverse.
_RENAMES = (
    ("csa_documents", "csa_documents_raw"),
    ("csa_parties", "csa_parties_raw"),
    ("csa_fees", "csa_fees_raw"),
    ("csa_services", "csa_services_raw"),
    ("csa_clause_flags", "csa_clause_flags_raw"),
    ("csa_parse_warnings", "csa_parse_warnings_raw"),
)


def upgrade() -> None:
    """Upgrade schema."""
    for old_name, new_name in _RENAMES:
        op.rename_table(old_name, new_name)


def downgrade() -> None:
    """Downgrade schema."""
    for old_name, new_name in reversed(_RENAMES):
        op.rename_table(new_name, old_name)

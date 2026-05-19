"""Add itr_salary_allowances.exempt_regime (old | new | both).

Revision ID: a3b4c5d6e7f8
Revises: f2a5b6c7d8e9
Create Date: 2026-05-19 10:00:00.000000
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "a3b4c5d6e7f8"
down_revision: Union[str, Sequence[str], None] = "f2a5b6c7d8e9"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

_NEW_SECTIONS = (
    "10(10)",
    "10(10A)",
    "10(10AA)",
    "10(10B)",
    "10(10C)",
    "10(10CC)",
)

_NEW_TYPES = (
    "Gratuity",
    "Commuted Pension",
    "Leave Encashment",
    "Retrenchment Compensation",
    "VRS Compensation",
    "Conveyance Allowance",
    "Transport Allowance",
    "Academic / Research Allowance",
    "Research Allowance",
    "Uniform Allowance",
)


def upgrade() -> None:
    op.add_column(
        "itr_salary_allowances",
        sa.Column(
            "exempt_regime",
            sa.String(length=10),
            nullable=False,
            server_default="old",
        ),
    )

    sections_sql = ", ".join(f"'{s}'" for s in _NEW_SECTIONS)
    types_sql = ", ".join(f"'{t}'" for t in _NEW_TYPES)
    op.execute(
        f"""
        UPDATE itr_salary_allowances
        SET exempt_regime = 'both'
        WHERE TRIM(COALESCE(exempt_section, '')) IN ({sections_sql})
           OR TRIM(allowance_type) IN ({types_sql})
        """
    )

    op.alter_column(
        "itr_salary_allowances",
        "exempt_regime",
        server_default="both",
    )


def downgrade() -> None:
    op.drop_column("itr_salary_allowances", "exempt_regime")

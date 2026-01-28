"""Fix residency active check constraint: is_active=true OR residency_end_date IS NOT NULL.
 
Revision ID: fix_residency_end_date_rule
Revises: fd04dab9756e
Create Date: 2026-01-28
 
"""
from typing import Sequence, Union
 
from alembic import op
import sqlalchemy as sa


revision: str = "fix_residency_end_date_rule"
down_revision: Union[str, Sequence[str], None] = "fd04dab9756e"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None
 
 
def upgrade() -> None:
    conn = op.get_bind()
    
    # Check if the residencies table exists
    inspector = sa.inspect(conn)
    tables = inspector.get_table_names()
    
    if "residencies" not in tables:
        # Table doesn't exist, skip this migration
        return
    
    # Check if the constraint exists before dropping
    constraints = [
        constraint["name"]
        for constraint in inspector.get_check_constraints("residencies")
    ]
    
    if "residencies_active_check" in constraints:
        # Drop the old incorrect constraint
        op.drop_constraint(
            "residencies_active_check",
            "residencies",
            type_="check",
        )
 
    # Add correct business rule
    op.create_check_constraint(
        "residencies_active_check",
        "residencies",
        "is_active = true OR residency_end_date IS NOT NULL",
    )
 
 
def downgrade() -> None:
    conn = op.get_bind()
    
    # Check if the residencies table exists
    inspector = sa.inspect(conn)
    tables = inspector.get_table_names()
    
    if "residencies" not in tables:
        # Table doesn't exist, skip this migration
        return
    
    # Check if the constraint exists before dropping
    constraints = [
        constraint["name"]
        for constraint in inspector.get_check_constraints("residencies")
    ]
    
    if "residencies_active_check" in constraints:
        op.drop_constraint(
            "residencies_active_check",
            "residencies",
            type_="check",
        )
 
        op.create_check_constraint(
            "residencies_active_check",
            "residencies",
            "is_active = false OR residency_end_date IS NOT NULL",
        )


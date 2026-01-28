"""Rename addresstype enum to PRIMARY/SECONDARY for nucleus compatibility.

Nucleus SQLAlchemy Enum(AddressType) looks up by enum .name on read, so PostgreSQL
must store 'PRIMARY' and 'SECONDARY'. This renames 'Primary'/'Secondary' if present.

Revision ID: 20260128_addresstype
Revises: 8fc2e418cf16
Create Date: 2026-01-28

"""
from typing import Sequence, Union

from alembic import op


revision: str = "20260128_addresstype"
down_revision: Union[str, Sequence[str], None] = "8fc2e418cf16"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Rename enum labels so nucleus Enum (lookup by .name) works on read.
    # Only runs if addresstype enum exists (e.g. after 02533cebd7c9 or similar).
    op.execute("""
        DO $$
        BEGIN
            IF EXISTS (SELECT 1 FROM pg_type WHERE typname = 'addresstype') THEN
                IF EXISTS (
                    SELECT 1 FROM pg_enum e
                    JOIN pg_type t ON e.enumtypid = t.oid
                    WHERE t.typname = 'addresstype' AND e.enumlabel = 'Primary'
                ) THEN
                    ALTER TYPE addresstype RENAME VALUE 'Primary' TO 'PRIMARY';
                END IF;
                IF EXISTS (
                    SELECT 1 FROM pg_enum e
                    JOIN pg_type t ON e.enumtypid = t.oid
                    WHERE t.typname = 'addresstype' AND e.enumlabel = 'Secondary'
                ) THEN
                    ALTER TYPE addresstype RENAME VALUE 'Secondary' TO 'SECONDARY';
                END IF;
            END IF;
        END $$;
    """)


def downgrade() -> None:
    op.execute("""
        DO $$
        BEGIN
            IF EXISTS (SELECT 1 FROM pg_type WHERE typname = 'addresstype') THEN
                IF EXISTS (
                    SELECT 1 FROM pg_enum e
                    JOIN pg_type t ON e.enumtypid = t.oid
                    WHERE t.typname = 'addresstype' AND e.enumlabel = 'PRIMARY'
                ) THEN
                    ALTER TYPE addresstype RENAME VALUE 'PRIMARY' TO 'Primary';
                END IF;
                IF EXISTS (
                    SELECT 1 FROM pg_enum e
                    JOIN pg_type t ON e.enumtypid = t.oid
                    WHERE t.typname = 'addresstype' AND e.enumlabel = 'SECONDARY'
                ) THEN
                    ALTER TYPE addresstype RENAME VALUE 'SECONDARY' TO 'Secondary';
                END IF;
            END IF;
        END $$;
    """)

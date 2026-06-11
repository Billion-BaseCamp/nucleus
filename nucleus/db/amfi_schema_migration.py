"""Idempotent schema for AMFI NAVAll master data (MF ISIN registry)."""

from __future__ import annotations

import logging

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncConnection

logger = logging.getLogger(__name__)

_AMFI_SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS amfi_master_meta (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    source VARCHAR(32) NOT NULL DEFAULT 'NAVAll',
    nav_date DATE,
    fetched_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    scheme_row_count INTEGER NOT NULL DEFAULT 0,
    isin_count INTEGER NOT NULL DEFAULT 0
);

CREATE TABLE IF NOT EXISTS amfi_mf_isin (
    isin CHAR(12) PRIMARY KEY,
    scheme_code INTEGER NOT NULL,
    scheme_name TEXT NOT NULL,
    amc_name VARCHAR(255),
    category VARCHAR(512),
    isin_role VARCHAR(32) NOT NULL,
    nav NUMERIC(18, 4),
    nav_date DATE NOT NULL,
    is_etf BOOLEAN NOT NULL DEFAULT FALSE,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS ix_amfi_mf_isin_scheme_code
    ON amfi_mf_isin(scheme_code);

CREATE INDEX IF NOT EXISTS ix_amfi_mf_isin_amc_name
    ON amfi_mf_isin(amc_name);

CREATE INDEX IF NOT EXISTS ix_amfi_mf_isin_is_etf
    ON amfi_mf_isin(is_etf);
"""


async def apply_amfi_schema_migrations(conn: AsyncConnection) -> None:
    """Create AMFI master tables if missing (safe to run repeatedly)."""
    for statement in _AMFI_SCHEMA_SQL.strip().split(";"):
        stmt = statement.strip()
        if stmt:
            await conn.execute(text(stmt))
    logger.info("AMFI schema migration applied (if needed)")

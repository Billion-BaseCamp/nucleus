"""AMFI NAVAll master data — MF scheme ISIN registry for broker dedup."""

from __future__ import annotations

from datetime import date, datetime
from decimal import Decimal
from typing import Optional
from uuid import UUID, uuid4

from sqlalchemy import Boolean, Date, DateTime, Integer, Numeric, String, Text
from sqlalchemy import UUID as SQLUUID
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func

from nucleus.db.database import Base


class AmfiMasterMeta(Base):
    """One row per NAVAll import (audit / freshness tracking)."""

    __tablename__ = "amfi_master_meta"

    id: Mapped[UUID] = mapped_column(
        SQLUUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
    )
    source: Mapped[str] = mapped_column(
        String(32),
        nullable=False,
        default="NAVAll",
        server_default="NAVAll",
    )
    nav_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    fetched_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )
    scheme_row_count: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0,
        server_default="0",
    )
    isin_count: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0,
        server_default="0",
    )


class AmfiMfIsin(Base):
    """Flattened ISIN lookup table — one row per AMFI-listed MF ISIN variant."""

    __tablename__ = "amfi_mf_isin"

    isin: Mapped[str] = mapped_column(String(12), primary_key=True)
    scheme_code: Mapped[int] = mapped_column(Integer, nullable=False, index=True)
    scheme_name: Mapped[str] = mapped_column(Text, nullable=False)
    amc_name: Mapped[Optional[str]] = mapped_column(String(255), nullable=True, index=True)
    category: Mapped[Optional[str]] = mapped_column(String(512), nullable=True)
    isin_role: Mapped[str] = mapped_column(String(32), nullable=False)
    nav: Mapped[Optional[Decimal]] = mapped_column(Numeric(18, 4), nullable=True)
    nav_date: Mapped[date] = mapped_column(Date, nullable=False)
    is_etf: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
        server_default="false",
        index=True,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )

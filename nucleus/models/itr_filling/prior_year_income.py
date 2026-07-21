"""Prior-year income heads for Client Summary YoY bar chart.

One row per current ``itr_returns`` row. Values are taken as filed from the
prior-year ITR-2 PartB-TI (whatever regime was used) and stored under the same
head names as ``ComputationDisplayBlock`` so the chart can compare
current-vs-prior apples-to-apples at the head level.

No Alembic migration ships with this model — create the table out-of-band.
"""

from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from typing import Optional
from uuid import UUID, uuid4

from sqlalchemy import (
    DateTime,
    ForeignKey,
    String,
    UUID as SQLUUID,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from sqlalchemy.types import Numeric

from nucleus.db.database import Base


class ITRPriorYearIncomeHeads(Base):
    """Snapshot of prior-year PartB-TI income heads for one current ITR return."""

    __tablename__ = "itr_prior_year_income_heads"

    id: Mapped[UUID] = mapped_column(
        SQLUUID(as_uuid=True), primary_key=True, default=uuid4
    )
    itr_return_id: Mapped[UUID] = mapped_column(
        SQLUUID(as_uuid=True),
        ForeignKey("itr_returns.id", ondelete="CASCADE"),
        nullable=False,
        unique=True,
        index=True,
    )

    # Assessment year label from the uploaded prior-year JSON (e.g. "2025-26").
    prior_assessment_year: Mapped[Optional[str]] = mapped_column(
        String(10), nullable=True
    )
    # PAN used to match the JSON to the client (uppercase).
    pan: Mapped[Optional[str]] = mapped_column(String(10), nullable=True, index=True)

    # Same semantics / names as Client Summary ComputationDisplayBlock heads.
    salary_income: Mapped[Decimal] = mapped_column(
        Numeric(18, 2), nullable=False, default=Decimal("0")
    )
    hp_income: Mapped[Decimal] = mapped_column(
        Numeric(18, 2), nullable=False, default=Decimal("0")
    )
    os_income: Mapped[Decimal] = mapped_column(
        Numeric(18, 2), nullable=False, default=Decimal("0")
    )
    net_cg_income: Mapped[Decimal] = mapped_column(
        Numeric(18, 2), nullable=False, default=Decimal("0")
    )
    dtaa_income: Mapped[Decimal] = mapped_column(
        Numeric(18, 2), nullable=False, default=Decimal("0")
    )

    source_filename: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), onupdate=func.now(), nullable=True
    )

    itr_return: Mapped["ITRReturn"] = relationship(
        "ITRReturn",
        back_populates="prior_year_income_heads",
    )

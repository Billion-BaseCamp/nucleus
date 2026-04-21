"""
ITR filing layer: Schedule CFL (Carry Forward of Losses).

itr_returns → itr_cfl_schedule (1:1) → year_entries (up to 8) + summary_entries (4)
"""

from __future__ import annotations

from datetime import date, datetime
from decimal import Decimal
from typing import TYPE_CHECKING, List, Optional
from uuid import UUID, uuid4

if TYPE_CHECKING:
    from nucleus.models.itr_filling.itr_return import ITRReturn

from sqlalchemy import UUID as SQLUUID
from sqlalchemy import (Date, DateTime, ForeignKey, Integer, String,
                        UniqueConstraint)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from sqlalchemy.types import Numeric

from nucleus.db.database import Base


class ITRCFLSchedule(Base):
    """Parent — 1:1 with ITRReturn. Holds up to 8 year-entries + 4 summaries."""

    __tablename__ = "itr_cfl_schedule"

    id: Mapped[UUID] = mapped_column(
        SQLUUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
    )
    itr_return_id: Mapped[UUID] = mapped_column(
        SQLUUID(as_uuid=True),
        ForeignKey("itr_returns.id", ondelete="CASCADE"),
        nullable=False,
        unique=True,
        index=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )
    updated_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        onupdate=func.now(),
    )

    year_entries: Mapped[List["ITRCFLYearEntry"]] = relationship(
        back_populates="cfl_schedule",
        cascade="all, delete-orphan",
        order_by="ITRCFLYearEntry.years_back",
    )
    summary_entries: Mapped[List["ITRCFLSummary"]] = relationship(
        back_populates="cfl_schedule",
        cascade="all, delete-orphan",
        order_by="ITRCFLSummary.summary_type",
    )

    itr_return: Mapped["ITRReturn"] = relationship(
        "ITRReturn",
        back_populates="cfl_schedule",
    )


class ITRCFLYearEntry(Base):
    """One per original AY — the `LossCFFromPrev{N}thYearFromAY` blocks."""

    __tablename__ = "itr_cfl_year_entries"

    id: Mapped[UUID] = mapped_column(
        SQLUUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
    )
    cfl_schedule_id: Mapped[UUID] = mapped_column(
        SQLUUID(as_uuid=True),
        ForeignKey("itr_cfl_schedule.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    # 1 = prev year (LossCFFromPrevYrToAY / LossCFFromPrev1stYearFromAY)
    # 2..8 = LossCFFromPrev{N}thYearFromAY
    years_back: Mapped[int] = mapped_column(Integer, nullable=False)

    original_assessment_year: Mapped[str] = mapped_column(String(10), nullable=False)

    date_of_filing: Mapped[Optional[date]] = mapped_column(Date, nullable=True)

    hp_loss_cf: Mapped[Decimal] = mapped_column(
        Numeric(18, 2),
        nullable=False,
        default=0,
    )
    stcg_loss_cf: Mapped[Decimal] = mapped_column(
        Numeric(18, 2),
        nullable=False,
        default=0,
    )
    ltcg_loss_cf: Mapped[Decimal] = mapped_column(
        Numeric(18, 2),
        nullable=False,
        default=0,
    )
    os_race_horse_loss_cf: Mapped[Decimal] = mapped_column(
        Numeric(18, 2),
        nullable=False,
        default=0,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )
    updated_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        onupdate=func.now(),
    )

    cfl_schedule: Mapped["ITRCFLSchedule"] = relationship(back_populates="year_entries")

    __table_args__ = (
        UniqueConstraint(
            "cfl_schedule_id",
            "years_back",
            name="uq_cfl_year_entry_per_schedule",
        ),
    )


class ITRCFLSummary(Base):
    """One of the four named summary blocks on Schedule CFL."""

    __tablename__ = "itr_cfl_summary"

    id: Mapped[UUID] = mapped_column(
        SQLUUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
    )
    cfl_schedule_id: Mapped[UUID] = mapped_column(
        SQLUUID(as_uuid=True),
        ForeignKey("itr_cfl_schedule.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    summary_type: Mapped[str] = mapped_column(String(30), nullable=False)

    hp_loss_cf: Mapped[Decimal] = mapped_column(
        Numeric(18, 2),
        nullable=False,
        default=0,
    )
    stcg_loss_cf: Mapped[Decimal] = mapped_column(
        Numeric(18, 2),
        nullable=False,
        default=0,
    )
    ltcg_loss_cf: Mapped[Decimal] = mapped_column(
        Numeric(18, 2),
        nullable=False,
        default=0,
    )
    os_race_horse_loss_cf: Mapped[Decimal] = mapped_column(
        Numeric(18, 2),
        nullable=False,
        default=0,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )
    updated_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        onupdate=func.now(),
    )

    cfl_schedule: Mapped["ITRCFLSchedule"] = relationship(
        back_populates="summary_entries"
    )

    __table_args__ = (
        UniqueConstraint(
            "cfl_schedule_id",
            "summary_type",
            name="uq_cfl_summary_per_schedule",
        ),
    )

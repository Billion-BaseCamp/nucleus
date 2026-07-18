from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from typing import TYPE_CHECKING, Optional
from uuid import UUID, uuid4

from sqlalchemy import UUID as SQLUUID
from sqlalchemy import Boolean, DateTime, ForeignKey, String, UniqueConstraint
from sqlalchemy.types import Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from nucleus.db.database import Base

if TYPE_CHECKING:
    from nucleus.models.advance_tax_models.financial_year import FinancialYear
    from nucleus.models.common_models.client import Client


class DocumentCollectorInfo(Base):
    __tablename__ = "document_collector_info"
    __table_args__ = (
        UniqueConstraint(
            "client_id",
            "financial_year_id",
            name="uq_document_collector_info_client_fy",
        ),
    )

    id: Mapped[UUID] = mapped_column(
        SQLUUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
        index=True,
    )
    client_id: Mapped[UUID] = mapped_column(
        SQLUUID(as_uuid=True),
        ForeignKey("clients.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    financial_year_id: Mapped[UUID] = mapped_column(
        SQLUUID(as_uuid=True),
        ForeignKey("financial_years.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    is_cg_applicable: Mapped[Optional[bool]] = mapped_column(
        Boolean,
        nullable=True,
    )
    cg_status: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    is_fa_applicable: Mapped[Optional[bool]] = mapped_column(
        Boolean,
        nullable=True,
    )
    fa_status: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    fi_status: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    is_fcg_applicable: Mapped[Optional[bool]] = mapped_column(
        Boolean,
        nullable=True,
    )
    is_return_filing_applicable: Mapped[Optional[bool]] = mapped_column(
        Boolean,
        nullable=True,
    )
    is_foreign_income_applicable: Mapped[Optional[bool]] = mapped_column(
        Boolean,
        nullable=True,
    )
    is_foreign_salary_applicable:Mapped[Optional[bool]] = mapped_column(
        Boolean,
         nullable=True,
    )
    is_foreign_dividend_applicable:Mapped[Optional[bool]] = mapped_column(
        Boolean,
        nullable=True,
    )
    is_foreign_rental_applicable:Mapped[Optional[bool]] = mapped_column(
        Boolean,
        nullable=True,
    )
    is_foreign_interest_applicable:Mapped[Optional[bool]] = mapped_column(
        Boolean,
        nullable=True,
    )
    is_foreign_consultancy_applicable:Mapped[Optional[bool]] = mapped_column(
        Boolean,
        nullable=True,
    )
    is_salary_applicable: Mapped[Optional[bool]] = mapped_column(
        Boolean,
        nullable=True,
    )
    salary_status: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    job_change_during_year: Mapped[Optional[str]] = mapped_column(
        String, nullable=True
    )
    is_ais_imported: Mapped[Optional[bool]] = mapped_column(
        Boolean,
        nullable=True,
        default=False,
        server_default="FALSE",
    )
    is_json_imported: Mapped[Optional[bool]] = mapped_column(
        Boolean,
        nullable=True,
        default=False,
        server_default="FALSE",
    )
    is_ais_reconcile_imported: Mapped[Optional[bool]] = mapped_column(
        Boolean,
        nullable=True,
        default=False,
        server_default="FALSE",
    )
    is_26as_imported: Mapped[Optional[bool]] = mapped_column(
        Boolean,
        nullable=True,
        default=False,
        server_default="FALSE",
    )
    is_tis_imported: Mapped[Optional[bool]] = mapped_column(
        Boolean,
        nullable=True,
        default=False,
        server_default="FALSE",
    )
    has_employment_gap: Mapped[bool] = mapped_column(
        Boolean,
        nullable=True,
        default=False,
        server_default="FALSE",
    )
    ll_pan: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    annual_rent: Mapped[Optional[Decimal]] = mapped_column(
        Numeric(18, 2),
        nullable=True,
    )
    balance_tax: Mapped[Optional[Decimal]] = mapped_column(
        Numeric(15, 2),
        nullable=True,
    )
    is_other_info_applicable: Mapped[Optional[bool]] = mapped_column(
        Boolean,
        nullable=True,
    )
    other_info_status: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    is_80c_applicable: Mapped[Optional[bool]] = mapped_column(
        Boolean,
        nullable=True,
    )
    salary_old_regime_detected: Mapped[Optional[bool]] = mapped_column(
        Boolean,
        nullable=True,
    )

    client: Mapped["Client"] = relationship("Client")
    financial_year: Mapped["FinancialYear"] = relationship("FinancialYear")

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), onupdate=func.now(), nullable=True
    )


class SubTypeComments(Base):
    __tablename__ = "sub_type_comments"

    id: Mapped[UUID] = mapped_column(
        SQLUUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
        index=True,
    )
    client_id: Mapped[UUID] = mapped_column(
        SQLUUID(as_uuid=True),
        ForeignKey("clients.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    financial_year_id: Mapped[UUID] = mapped_column(
        SQLUUID(as_uuid=True),
        ForeignKey("financial_years.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    sub_type: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    region: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    comment: Mapped[Optional[str]] = mapped_column(String, nullable=True)

    client: Mapped["Client"] = relationship("Client")
    financial_year: Mapped["FinancialYear"] = relationship("FinancialYear")

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), onupdate=func.now(), nullable=True
    )

from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4

from sqlalchemy import (
    DateTime,
    Float,
    ForeignKey,
    String,
    UniqueConstraint,
    UUID as SQLUUID,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from nucleus.db.database import Base


class PriorItrSnapshot(Base):
    """Frozen last-year filed ITR amounts for Advance Tax YoY compare.

    One row per client per current financial year. Written on ITR JSON import
    (and overwritten on reimport) so later quarter edits do not lose the filed
    prior-year figures.
    """

    __tablename__ = "advance_tax_prior_itr_snapshots"
    __table_args__ = (
        UniqueConstraint(
            "client_id",
            "financial_year_id",
            name="uq_at_prior_itr_snapshot_client_fy",
        ),
    )

    id: Mapped[UUID] = mapped_column(
        SQLUUID(as_uuid=True), primary_key=True, default=uuid4, index=True
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
    imported_quarter_id: Mapped[Optional[UUID]] = mapped_column(
        SQLUUID(as_uuid=True),
        ForeignKey("quarters.id", ondelete="SET NULL"),
        nullable=True,
    )

    assessment_year: Mapped[str] = mapped_column(String, nullable=False)
    itr_type: Mapped[str] = mapped_column(String, nullable=False)
    pan: Mapped[Optional[str]] = mapped_column(String, nullable=True)

    total_taxable_income: Mapped[float] = mapped_column(Float, default=0.0)
    interest_total: Mapped[float] = mapped_column(Float, default=0.0)
    fd_interest: Mapped[float] = mapped_column(Float, default=0.0)
    savings_interest: Mapped[float] = mapped_column(Float, default=0.0)
    other_interest: Mapped[float] = mapped_column(Float, default=0.0)
    pass_interest: Mapped[float] = mapped_column(Float, default=0.0)
    epf_interest: Mapped[float] = mapped_column(Float, default=0.0)
    it_refund_interest: Mapped[float] = mapped_column(Float, default=0.0)
    foreign_interest: Mapped[float] = mapped_column(Float, default=0.0)
    dividends_total: Mapped[float] = mapped_column(Float, default=0.0)
    india_dividends: Mapped[float] = mapped_column(Float, default=0.0)
    foreign_dividends: Mapped[float] = mapped_column(Float, default=0.0)
    taxable_rental: Mapped[float] = mapped_column(Float, default=0.0)
    business_income: Mapped[float] = mapped_column(Float, default=0.0)
    income_44ada: Mapped[float] = mapped_column(Float, default=0.0)
    income_44ad: Mapped[float] = mapped_column(Float, default=0.0)
    consultancy_income: Mapped[float] = mapped_column(Float, default=0.0)
    other_income: Mapped[float] = mapped_column(Float, default=0.0)
    any_other_income: Mapped[float] = mapped_column(Float, default=0.0)
    capital_gains: Mapped[float] = mapped_column(Float, default=0.0)
    stcg_20: Mapped[float] = mapped_column(Float, default=0.0)
    ltcg_125: Mapped[float] = mapped_column(Float, default=0.0)
    stcg_marginal: Mapped[float] = mapped_column(Float, default=0.0)
    ltcg_20: Mapped[float] = mapped_column(Float, default=0.0)
    crypto_gains: Mapped[float] = mapped_column(Float, default=0.0)
    gross_salary: Mapped[float] = mapped_column(Float, default=0.0)
    net_salary: Mapped[float] = mapped_column(Float, default=0.0)
    total_normal_income: Mapped[float] = mapped_column(Float, default=0.0)
    total_income_other_than_cg: Mapped[float] = mapped_column(Float, default=0.0)
    tax_on_normal_income: Mapped[float] = mapped_column(Float, default=0.0)
    tax_on_stcg_20: Mapped[float] = mapped_column(Float, default=0.0)
    tax_on_stcg_normal: Mapped[float] = mapped_column(Float, default=0.0)
    tax_on_ltcg_125: Mapped[float] = mapped_column(Float, default=0.0)
    tax_on_ltcg_20: Mapped[float] = mapped_column(Float, default=0.0)
    tax_on_crypto: Mapped[float] = mapped_column(Float, default=0.0)
    total_tax_on_capital_gains: Mapped[float] = mapped_column(Float, default=0.0)
    total_base_tax: Mapped[float] = mapped_column(Float, default=0.0)
    rebate_87a: Mapped[float] = mapped_column(Float, default=0.0)
    surcharge: Mapped[float] = mapped_column(Float, default=0.0)
    marginal_relief: Mapped[float] = mapped_column(Float, default=0.0)
    health_and_education_cess: Mapped[float] = mapped_column(Float, default=0.0)
    total_tax: Mapped[float] = mapped_column(Float, default=0.0)
    tds: Mapped[float] = mapped_column(Float, default=0.0)
    tcs: Mapped[float] = mapped_column(Float, default=0.0)
    foreign_tax_credit: Mapped[float] = mapped_column(Float, default=0.0)
    other_tax_credit: Mapped[float] = mapped_column(Float, default=0.0)
    total_tax_credits: Mapped[float] = mapped_column(Float, default=0.0)
    balance_tax: Mapped[float] = mapped_column(Float, default=0.0)
    due_amount: Mapped[float] = mapped_column(Float, default=0.0)
    advance_tax_q1: Mapped[float] = mapped_column(Float, default=0.0)
    advance_tax_q2: Mapped[float] = mapped_column(Float, default=0.0)
    advance_tax_q3: Mapped[float] = mapped_column(Float, default=0.0)
    advance_tax_q4: Mapped[float] = mapped_column(Float, default=0.0)
    advance_tax_till_date: Mapped[float] = mapped_column(Float, default=0.0)
    due_this_quarter: Mapped[float] = mapped_column(Float, default=0.0)

    financial_year: Mapped["FinancialYear"] = relationship(
        "FinancialYear",
        back_populates="prior_itr_snapshot",
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), onupdate=func.now(), nullable=True
    )

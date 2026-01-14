from nucleus.db.database import Base
from sqlalchemy import (
    BigInteger,
    DateTime,
    ForeignKey,
    DECIMAL,
    func,
    UUID as SQLUUID,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from uuid import UUID, uuid4


class CashFlowOffice(Base):
    __tablename__ = "cash_flow_office"

    id: Mapped[UUID] = mapped_column(
        SQLUUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
        index=True,
    )

    financial_year_id: Mapped[UUID] = mapped_column(
        SQLUUID(as_uuid=True),
        ForeignKey("financial_years.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    financial_year: Mapped["FinancialYear"] = relationship("FinancialYear")

    home_loan_principal_balance: Mapped[float] = mapped_column(
        DECIMAL(15, 2),
        nullable=True,
    )

    emergency_fund_requirement: Mapped[float] = mapped_column(
        DECIMAL(15, 2),
        nullable=True,
    )

    annual_fixed_expense: Mapped[float] = mapped_column(
        DECIMAL(15, 2),
        nullable=True,
    )

    annual_variable_expense: Mapped[float] = mapped_column(
        DECIMAL(15, 2),
        nullable=True,
    )

    annual_lifestyle_expense: Mapped[float] = mapped_column(
        DECIMAL(15, 2),
        nullable=True,
    )

    arbitrage_fund_balance: Mapped[float] = mapped_column(
        DECIMAL(15, 2),
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        server_default=func.now(),
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )

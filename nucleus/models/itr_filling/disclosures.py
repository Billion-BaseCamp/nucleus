"""
ITR filing layer: Disclosures (Schedule AL, Part A Gen, Schedule FA).

itr_returns → itr_disclosures_schedule (1:1) → child tables
"""

from __future__ import annotations

from datetime import date, datetime
from decimal import Decimal
from typing import List, Optional
from uuid import UUID, uuid4

from sqlalchemy import (
    Boolean,
    Date,
    DateTime,
    ForeignKey,
    Integer,
    String,
    UUID as SQLUUID,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from sqlalchemy.types import Numeric

from nucleus.db.database import Base


class ITRDisclosuresSchedule(Base):
    """Schedule AL + Part A disclosures + Schedule FA root (1:1 with itr_returns)."""

    __tablename__ = "itr_disclosures_schedule"

    id: Mapped[UUID] = mapped_column(SQLUUID(as_uuid=True), primary_key=True, default=uuid4)
    itr_return_id: Mapped[UUID] = mapped_column(
        SQLUUID(as_uuid=True),
        ForeignKey("itr_returns.id", ondelete="CASCADE"),
        nullable=False,
        unique=True,
        index=True,
    )

    net_movable_assets: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False, default=0)
    investment:Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False, default=0)
    immovable:Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False, default=0)

    is_directorship: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    is_unlisted_shares: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    is_foreign_assets: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)


    itr_return: Mapped["ITRReturn"] = relationship("ITRReturn", back_populates="disclosures")

    movable_assets: Mapped[List["ITRALMovableAsset"]] = relationship(
        back_populates="disclosures_schedule",
        cascade="all, delete-orphan"
    )
    investments: Mapped[List["ITRALInvestment"]] = relationship(
        back_populates="disclosures_schedule",
        cascade="all, delete-orphan",
    )

    immovable_properties: Mapped[List["ITRALImmovableProperty"]] = relationship(
        back_populates="disclosures_schedule",
        cascade="all, delete-orphan",
        order_by="ITRALImmovableProperty.display_order",
    )

    directorship: Mapped[List["ITRDiscDirectorship"]] = relationship(
        back_populates="disclosures_schedule",
        cascade="all, delete-orphan",
        order_by="ITRDiscDirectorship.display_order",
    )
    unlisted_shares: Mapped[List["ITRDiscUnlistedShare"]] = relationship(
        back_populates="disclosures_schedule",
        cascade="all, delete-orphan",
        order_by="ITRDiscUnlistedShare.display_order",
    )

    fa_bank_accounts: Mapped[List["ITRFABankAccount"]] = relationship(
        back_populates="disclosures_schedule",
        cascade="all, delete-orphan",
        order_by="ITRFABankAccount.display_order",
    )
    fa_equity_debt: Mapped[List["ITRFAEquityDebt"]] = relationship(
        back_populates="disclosures_schedule",
        cascade="all, delete-orphan",
        order_by="ITRFAEquityDebt.display_order",
    )
    fa_cash_value_insurance: Mapped[List["ITRFACashValueInsurance"]] = relationship(
        back_populates="disclosures_schedule",
        cascade="all, delete-orphan",
        order_by="ITRFACashValueInsurance.display_order",
    )
    fa_immovable_properties: Mapped[List["ITRFAImmovableProperty"]] = relationship(
        back_populates="disclosures_schedule",
        cascade="all, delete-orphan",
        order_by="ITRFAImmovableProperty.display_order",
    )
    fa_financial_interests: Mapped[List["ITRFAFinancialInterest"]] = relationship(
        back_populates="disclosures_schedule",
        cascade="all, delete-orphan",
        order_by="ITRFAFinancialInterest.display_order",
    )
    fa_signing_authorities: Mapped[List["ITRFASigningAuthority"]] = relationship(
        back_populates="disclosures_schedule",
        cascade="all, delete-orphan",
        order_by="ITRFASigningAuthority.display_order",
    )
    fa_other_assets: Mapped[List["ITRFAOtherAsset"]] = relationship(
        back_populates="disclosures_schedule",
        cascade="all, delete-orphan",
        order_by="ITRFAOtherAsset.display_order",
    )
    fa_foreign_trusts: Mapped[List["ITRFAForeignTrust"]] = relationship(
        back_populates="disclosures_schedule",
        cascade="all, delete-orphan",
        order_by="ITRFAForeignTrust.display_order",
    )
    fa_other_foreign_income: Mapped[List["ITRFAOtherForeignIncome"]] = relationship(
        back_populates="disclosures_schedule",
        cascade="all, delete-orphan",
        order_by="ITRFAOtherForeignIncome.display_order",
    )

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), onupdate=func.now())

class ITRALMovableAsset(Base):
    __tablename__ = "itr_al_movable_assets"
    id: Mapped[UUID] = mapped_column(SQLUUID(as_uuid=True), primary_key=True, default=uuid4)
    disclosures_schedule_id: Mapped[UUID] = mapped_column(SQLUUID(as_uuid=True), ForeignKey("itr_disclosures_schedule.id", ondelete="CASCADE"), nullable=False)
    asset_type: Mapped[str] = mapped_column(String(20), nullable=False)
    fy_amount: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False, default=0)
    previous_year_amount: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False, default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), onupdate=func.now())
    disclosures_schedule: Mapped["ITRDisclosuresSchedule"] = relationship("ITRDisclosuresSchedule", back_populates="movable_assets")

class ITRALInvestment(Base):
    __tablename__ = "itr_al_investments"
    id: Mapped[UUID] = mapped_column(SQLUUID(as_uuid=True), primary_key=True, default=uuid4)
    disclosures_schedule_id: Mapped[UUID] = mapped_column(SQLUUID(as_uuid=True), ForeignKey("itr_disclosures_schedule.id", ondelete="CASCADE"), nullable=False)
    investment_type: Mapped[str] = mapped_column(String(20), nullable=False)
    balance:Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False, default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), onupdate=func.now())
    disclosures_schedule: Mapped["ITRDisclosuresSchedule"] = relationship("ITRDisclosuresSchedule", back_populates="investments")

class ITRALImmovableProperty(Base):
    """Schedule AL immovable details (India)."""

    __tablename__ = "itr_al_immovable_properties"

    id: Mapped[UUID] = mapped_column(SQLUUID(as_uuid=True), primary_key=True, default=uuid4)
    disclosures_schedule_id: Mapped[UUID] = mapped_column(
        SQLUUID(as_uuid=True),
        ForeignKey("itr_disclosures_schedule.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    display_order: Mapped[int] = mapped_column(Integer, nullable=False, default=1)

    description: Mapped[str] = mapped_column(String(25), nullable=False)
    flat_door_block_no: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    premise_building: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    road_street_po: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    area_locality: Mapped[str] = mapped_column(String(50), nullable=False)
    town_city_district: Mapped[str] = mapped_column(String(50), nullable=False)
    state_code: Mapped[str] = mapped_column(String(5), nullable=False)
    country_code: Mapped[str] = mapped_column(String(5), nullable=False, default="91")
    pin_code: Mapped[Optional[str]] = mapped_column(String(6), nullable=True)
    zip_code: Mapped[Optional[str]] = mapped_column(String(8), nullable=True)

    cost_of_property: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False, default=0)

    disclosures_schedule: Mapped["ITRDisclosuresSchedule"] = relationship(back_populates="immovable_properties")

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), onupdate=func.now())


class ITRDiscDirectorship(Base):
    """Part A — directorships."""

    __tablename__ = "itr_disc_directorships"

    id: Mapped[UUID] = mapped_column(SQLUUID(as_uuid=True), primary_key=True, default=uuid4)
    disclosures_schedule_id: Mapped[UUID] = mapped_column(
        SQLUUID(as_uuid=True),
        ForeignKey("itr_disclosures_schedule.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    display_order: Mapped[int] = mapped_column(Integer, nullable=False, default=1)

    company_name: Mapped[str] = mapped_column(String(125), nullable=False)
    company_type: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    company_pan: Mapped[Optional[str]] = mapped_column(String(10), nullable=True)
    listed_unlisted: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    din: Mapped[Optional[str]] = mapped_column(String(8), nullable=True)
    shares_held: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)

    disclosures_schedule: Mapped["ITRDisclosuresSchedule"] = relationship(back_populates="directorship")

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), onupdate=func.now())


class ITRDiscUnlistedShare(Base):
    """Part A — unlisted shares."""

    __tablename__ = "itr_disc_unlisted_shares"

    id: Mapped[UUID] = mapped_column(SQLUUID(as_uuid=True), primary_key=True, default=uuid4)
    disclosures_schedule_id: Mapped[UUID] = mapped_column(
        SQLUUID(as_uuid=True),
        ForeignKey("itr_disclosures_schedule.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    display_order: Mapped[int] = mapped_column(Integer, nullable=False, default=1)

    company_name: Mapped[str] = mapped_column(String(125), nullable=False)
    company_type: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    company_pan: Mapped[Optional[str]] = mapped_column(String(10), nullable=True)

    opening_qty: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    opening_cost: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False, default=0)

    acquired_qty: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    acquired_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    face_value_per_share: Mapped[Decimal] = mapped_column(Numeric(15, 4), nullable=False, default=0)
    price_paid_fresh_issue: Mapped[Decimal] = mapped_column(Numeric(15, 4), nullable=False, default=0)
    price_paid_existing_sh: Mapped[Decimal] = mapped_column(Numeric(15, 4), nullable=False, default=0)

    transferred_qty: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    sale_consideration: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False, default=0)

    closing_qty: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    closing_cost: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False, default=0)

    disclosures_schedule: Mapped["ITRDisclosuresSchedule"] = relationship(back_populates="unlisted_shares")

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), onupdate=func.now())


class ITRFABankAccount(Base):
    """Schedule FA A1 (Depository) + A2 (Custodial)."""

    __tablename__ = "itr_fa_bank_accounts"

    id: Mapped[UUID] = mapped_column(SQLUUID(as_uuid=True), primary_key=True, default=uuid4)
    disclosures_schedule_id: Mapped[UUID] = mapped_column(
        SQLUUID(as_uuid=True),
        ForeignKey("itr_disclosures_schedule.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    display_order: Mapped[int] = mapped_column(Integer, nullable=False, default=1)

    account_type: Mapped[str] = mapped_column(String(20), nullable=False)

    country_code: Mapped[str] = mapped_column(String(5), nullable=False)
    country_name: Mapped[Optional[str]] = mapped_column(String(55), nullable=True)
    zip_code: Mapped[Optional[str]] = mapped_column(String(8), nullable=True)

    institution_name: Mapped[str] = mapped_column(String(125), nullable=False)
    institution_address: Mapped[Optional[str]] = mapped_column(String(200), nullable=True)

    account_number: Mapped[Optional[str]] = mapped_column(String(34), nullable=True)
    owner_status: Mapped[Optional[str]] = mapped_column(String(30), nullable=True)
    date_of_opening: Mapped[Optional[date]] = mapped_column(Date, nullable=True)

    peak_balance: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False, default=0)
    closing_balance: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False, default=0)

    gross_interest_credited: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False, default=0)
    gross_dividend_credited: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False, default=0)
    gross_other_income: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False, default=0)

    scheduling_head: Mapped[Optional[str]] = mapped_column(String(10), nullable=True)

    disclosures_schedule: Mapped["ITRDisclosuresSchedule"] = relationship(back_populates="fa_bank_accounts")

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), onupdate=func.now())


class ITRFAEquityDebt(Base):
    """Schedule FA A3 — equity/debt interests."""

    __tablename__ = "itr_fa_equity_debt"

    id: Mapped[UUID] = mapped_column(SQLUUID(as_uuid=True), primary_key=True, default=uuid4)
    disclosures_schedule_id: Mapped[UUID] = mapped_column(
        SQLUUID(as_uuid=True),
        ForeignKey("itr_disclosures_schedule.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    display_order: Mapped[int] = mapped_column(Integer, nullable=False, default=1)

    country_code: Mapped[str] = mapped_column(String(5), nullable=False)
    country_name: Mapped[Optional[str]] = mapped_column(String(55), nullable=True)
    zip_code: Mapped[Optional[str]] = mapped_column(String(8), nullable=True)

    entity_name: Mapped[str] = mapped_column(String(125), nullable=False)
    entity_address: Mapped[Optional[str]] = mapped_column(String(200), nullable=True)
    nature_of_entity: Mapped[Optional[str]] = mapped_column(String(34), nullable=True)

    date_acquired: Mapped[Optional[date]] = mapped_column(Date, nullable=True)

    initial_value: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False, default=0)
    peak_value: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False, default=0)
    closing_value: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False, default=0)
    total_investment: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False, default=0)
    total_gross_proceeds: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False, default=0)

    income_derived: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False, default=0)
    nature_of_income: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    scheduling_head: Mapped[Optional[str]] = mapped_column(String(10), nullable=True)

    disclosures_schedule: Mapped["ITRDisclosuresSchedule"] = relationship(back_populates="fa_equity_debt")

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), onupdate=func.now())


class ITRFACashValueInsurance(Base):
    """Schedule FA A4."""

    __tablename__ = "itr_fa_cash_value_insurance"

    id: Mapped[UUID] = mapped_column(SQLUUID(as_uuid=True), primary_key=True, default=uuid4)
    disclosures_schedule_id: Mapped[UUID] = mapped_column(
        SQLUUID(as_uuid=True),
        ForeignKey("itr_disclosures_schedule.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    display_order: Mapped[int] = mapped_column(Integer, nullable=False, default=1)

    country_code: Mapped[str] = mapped_column(String(5), nullable=False)
    country_name: Mapped[Optional[str]] = mapped_column(String(55), nullable=True)
    zip_code: Mapped[Optional[str]] = mapped_column(String(8), nullable=True)

    institution_name: Mapped[str] = mapped_column(String(125), nullable=False)
    institution_address: Mapped[Optional[str]] = mapped_column(String(200), nullable=True)

    date_of_contract: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    cash_value_surrender_val: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False, default=0)
    total_gross_premium_paid: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False, default=0)

    disclosures_schedule: Mapped["ITRDisclosuresSchedule"] = relationship(back_populates="fa_cash_value_insurance")

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), onupdate=func.now())


class ITRFAImmovableProperty(Base):
    """Schedule FA B1 — foreign immovable property."""

    __tablename__ = "itr_fa_immovable_properties"

    id: Mapped[UUID] = mapped_column(SQLUUID(as_uuid=True), primary_key=True, default=uuid4)
    disclosures_schedule_id: Mapped[UUID] = mapped_column(
        SQLUUID(as_uuid=True),
        ForeignKey("itr_disclosures_schedule.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    display_order: Mapped[int] = mapped_column(Integer, nullable=False, default=1)

    country_code: Mapped[str] = mapped_column(String(5), nullable=False)
    country_name: Mapped[Optional[str]] = mapped_column(String(55), nullable=True)
    zip_code: Mapped[Optional[str]] = mapped_column(String(8), nullable=True)

    property_address: Mapped[Optional[str]] = mapped_column(String(200), nullable=True)
    ownership: Mapped[Optional[str]] = mapped_column(String(30), nullable=True)
    date_acquired: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    total_investment: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False, default=0)

    income_from_property: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False, default=0)
    nature_of_income: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)

    income_taxable_amount: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False, default=0)
    schedule_offered: Mapped[Optional[str]] = mapped_column(String(5), nullable=True)
    schedule_item_number: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)

    disclosures_schedule: Mapped["ITRDisclosuresSchedule"] = relationship(back_populates="fa_immovable_properties")

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), onupdate=func.now())


class ITRFAFinancialInterest(Base):
    """Schedule FA B2 — financial interest in foreign entity."""

    __tablename__ = "itr_fa_financial_interests"

    id: Mapped[UUID] = mapped_column(SQLUUID(as_uuid=True), primary_key=True, default=uuid4)
    disclosures_schedule_id: Mapped[UUID] = mapped_column(
        SQLUUID(as_uuid=True),
        ForeignKey("itr_disclosures_schedule.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    display_order: Mapped[int] = mapped_column(Integer, nullable=False, default=1)

    country_code: Mapped[str] = mapped_column(String(5), nullable=False)
    country_name: Mapped[Optional[str]] = mapped_column(String(55), nullable=True)
    zip_code: Mapped[Optional[str]] = mapped_column(String(8), nullable=True)

    entity_name: Mapped[str] = mapped_column(String(125), nullable=False)
    entity_address: Mapped[Optional[str]] = mapped_column(String(200), nullable=True)
    nature_of_entity: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    nature_of_interest: Mapped[Optional[str]] = mapped_column(String(30), nullable=True)

    date_acquired: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    total_investment: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False, default=0)

    income_derived: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False, default=0)
    nature_of_income: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)

    income_taxable_amount: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False, default=0)
    schedule_offered: Mapped[Optional[str]] = mapped_column(String(5), nullable=True)
    schedule_item_number: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    scheduling_head: Mapped[Optional[str]] = mapped_column(String(10), nullable=True)

    disclosures_schedule: Mapped["ITRDisclosuresSchedule"] = relationship(back_populates="fa_financial_interests")

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), onupdate=func.now())


class ITRFASigningAuthority(Base):
    """Schedule FA C — signing authority."""

    __tablename__ = "itr_fa_signing_authorities"

    id: Mapped[UUID] = mapped_column(SQLUUID(as_uuid=True), primary_key=True, default=uuid4)
    disclosures_schedule_id: Mapped[UUID] = mapped_column(
        SQLUUID(as_uuid=True),
        ForeignKey("itr_disclosures_schedule.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    display_order: Mapped[int] = mapped_column(Integer, nullable=False, default=1)

    country_code: Mapped[str] = mapped_column(String(5), nullable=False)
    country_name: Mapped[Optional[str]] = mapped_column(String(55), nullable=True)
    zip_code: Mapped[Optional[str]] = mapped_column(String(8), nullable=True)

    institution_name: Mapped[str] = mapped_column(String(125), nullable=False)
    institution_address: Mapped[Optional[str]] = mapped_column(String(200), nullable=True)

    account_holder_name: Mapped[Optional[str]] = mapped_column(String(125), nullable=True)
    institution_account_number: Mapped[Optional[str]] = mapped_column(String(34), nullable=True)

    peak_balance: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False, default=0)

    income_accrued_taxable_flag: Mapped[Optional[str]] = mapped_column(String(1), nullable=True)
    income_accrued_in_account: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False, default=0)
    income_offered_amount: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False, default=0)
    income_offered_schedule: Mapped[Optional[str]] = mapped_column(String(5), nullable=True)
    income_offered_schedule_no: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)

    disclosures_schedule: Mapped["ITRDisclosuresSchedule"] = relationship(back_populates="fa_signing_authorities")

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), onupdate=func.now())


class ITRFAOtherAsset(Base):
    """Schedule FA D — other capital assets."""

    __tablename__ = "itr_fa_other_assets"

    id: Mapped[UUID] = mapped_column(SQLUUID(as_uuid=True), primary_key=True, default=uuid4)
    disclosures_schedule_id: Mapped[UUID] = mapped_column(
        SQLUUID(as_uuid=True),
        ForeignKey("itr_disclosures_schedule.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    display_order: Mapped[int] = mapped_column(Integer, nullable=False, default=1)

    country_code: Mapped[str] = mapped_column(String(5), nullable=False)
    country_name: Mapped[Optional[str]] = mapped_column(String(55), nullable=True)
    zip_code: Mapped[Optional[str]] = mapped_column(String(8), nullable=True)

    nature_of_asset: Mapped[str] = mapped_column(String(100), nullable=False)
    ownership: Mapped[Optional[str]] = mapped_column(String(30), nullable=True)
    date_acquired: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    total_investment: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False, default=0)

    income_derived: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False, default=0)
    nature_of_income: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)

    income_taxable_amount: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False, default=0)
    schedule_offered: Mapped[Optional[str]] = mapped_column(String(5), nullable=True)
    schedule_item_number: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    scheduling_head: Mapped[Optional[str]] = mapped_column(String(10), nullable=True)

    disclosures_schedule: Mapped["ITRDisclosuresSchedule"] = relationship(back_populates="fa_other_assets")

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), onupdate=func.now())


class ITRFAForeignTrust(Base):
    """Schedule FA E — foreign trust."""

    __tablename__ = "itr_fa_foreign_trusts"

    id: Mapped[UUID] = mapped_column(SQLUUID(as_uuid=True), primary_key=True, default=uuid4)
    disclosures_schedule_id: Mapped[UUID] = mapped_column(
        SQLUUID(as_uuid=True),
        ForeignKey("itr_disclosures_schedule.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    display_order: Mapped[int] = mapped_column(Integer, nullable=False, default=1)

    country_code: Mapped[str] = mapped_column(String(5), nullable=False)
    country_name: Mapped[Optional[str]] = mapped_column(String(55), nullable=True)
    zip_code: Mapped[Optional[str]] = mapped_column(String(8), nullable=True)

    trust_name: Mapped[str] = mapped_column(String(125), nullable=False)
    trust_address: Mapped[Optional[str]] = mapped_column(String(200), nullable=True)

    relationship_nature: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    name_of_other_trustees: Mapped[Optional[str]] = mapped_column(String(125), nullable=True)
    address_of_other_trustees: Mapped[Optional[str]] = mapped_column(String(200), nullable=True)
    name_of_settlor: Mapped[Optional[str]] = mapped_column(String(125), nullable=True)
    address_of_settlor: Mapped[Optional[str]] = mapped_column(String(200), nullable=True)
    name_of_beneficiaries: Mapped[Optional[str]] = mapped_column(String(125), nullable=True)
    address_of_beneficiaries: Mapped[Optional[str]] = mapped_column(String(200), nullable=True)

    date_established: Mapped[Optional[date]] = mapped_column(Date, nullable=True)

    income_taxable_flag: Mapped[Optional[str]] = mapped_column(String(1), nullable=True)
    income_derived: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False, default=0)
    nature_of_income: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    income_offered_amount: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False, default=0)
    income_offered_schedule: Mapped[Optional[str]] = mapped_column(String(5), nullable=True)
    income_offered_sch_no: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    scheduling_head: Mapped[Optional[str]] = mapped_column(String(10), nullable=True)

    disclosures_schedule: Mapped["ITRDisclosuresSchedule"] = relationship(back_populates="fa_foreign_trusts")

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), onupdate=func.now())


class ITRFAOtherForeignIncome(Base):
    """Schedule FA F — other sources of income outside India."""

    __tablename__ = "itr_fa_other_foreign_income"

    id: Mapped[UUID] = mapped_column(SQLUUID(as_uuid=True), primary_key=True, default=uuid4)
    disclosures_schedule_id: Mapped[UUID] = mapped_column(
        SQLUUID(as_uuid=True),
        ForeignKey("itr_disclosures_schedule.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    display_order: Mapped[int] = mapped_column(Integer, nullable=False, default=1)

    country_code: Mapped[str] = mapped_column(String(5), nullable=False)
    country_name: Mapped[Optional[str]] = mapped_column(String(55), nullable=True)
    zip_code: Mapped[Optional[str]] = mapped_column(String(8), nullable=True)

    name_of_person: Mapped[str] = mapped_column(String(125), nullable=False)
    address_of_person: Mapped[Optional[str]] = mapped_column(String(200), nullable=True)

    income_derived: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False, default=0)
    nature_of_income: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)

    income_taxable_flag: Mapped[Optional[str]] = mapped_column(String(1), nullable=True)
    income_offered_amount: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False, default=0)
    income_offered_schedule: Mapped[Optional[str]] = mapped_column(String(5), nullable=True)
    income_offered_sch_no: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)

    disclosures_schedule: Mapped["ITRDisclosuresSchedule"] = relationship(back_populates="fa_other_foreign_income")

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), onupdate=func.now())

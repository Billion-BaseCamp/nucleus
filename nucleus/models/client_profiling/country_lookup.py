from nucleus.db.database import Base
from sqlalchemy import BigInteger, String, UUID as SQLUUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List
from uuid import UUID, uuid4


class CountryLookup(Base):
    __tablename__ = "country_lookup"
    id: Mapped[UUID] = mapped_column(SQLUUID(as_uuid=True), primary_key=True, default=uuid4, index=True)
    country_name: Mapped[str] = mapped_column(String, nullable=True,index=True)
    country_code: Mapped[str] = mapped_column(String, nullable=True,index=True)
    
    # Relationship to foreign depository accounts
    foreign_depository_accounts: Mapped[List["ForeignDepositoryAccounts"]] = relationship("ForeignDepositoryAccounts", back_populates="country")

    # Relationship to foreign custodial accounts
    foreign_custodial_accounts: Mapped[List["ForeignCustodialAccounts"]] = relationship("ForeignCustodialAccounts", back_populates="country")

    # Relationship to foreign insurance contracts
    foreign_insurance_contracts: Mapped[List["ForeignInsuranceContracts"]] = relationship("ForeignInsuranceContracts", back_populates="country")

    # Relationship to foreign immovable properties
    foreign_immovable_properties: Mapped[List["ForeignImmovableProperties"]] = relationship("ForeignImmovableProperties", back_populates="country")

    # Relationship to foreign other incomes
    foreign_other_incomes: Mapped[List["ForeignOtherIncomes"]] = relationship("ForeignOtherIncomes", back_populates="country")

    # Relationship to foreign other capital assets
    foreign_other_capital_assets: Mapped[List["ForeignOtherCapitalAssets"]] = relationship("ForeignOtherCapitalAssets", back_populates="country")

    # Relationship to foreign financial interests
    foreign_financial_interests: Mapped[List["ForeignFinancialInterests"]] = relationship("ForeignFinancialInterests", back_populates="country")

    # Relationship to foreign equity debt interests
    foreign_equity_debt_interests: Mapped[List["ForeignEquityDebtInterests"]] = relationship("ForeignEquityDebtInterests", back_populates="country")

    # Relationship to foreign signing authority accounts
    foreign_signing_authority_accounts: Mapped[List["ForeignSigningAuthorityAccounts"]] = relationship("ForeignSigningAuthorityAccounts", back_populates="country")
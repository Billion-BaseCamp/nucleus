# Import all models here for Alembic autogenerate to detect them

# Common Models
from nucleus.models.common_models.advisor import Advisor
from nucleus.models.common_models.client import Client, ClientPhoneMapping
from nucleus.models.common_models.login import Login
from nucleus.models.common_models.change_password import OtpVerification

# Advance Tax Models (import order in advance_tax_models/__init__.py for relationship resolution)
from nucleus.models.advance_tax_models import (
    BrokerageAccounts,
    CapitalGains,
    Comments,
    Dividends,
    DocumentsUpload,
    Excemption,
    FinancialYear,
    Employer,
    InterestDetails,
    OtherIncome,
    Quarter,
    Rental,
    Section54Claim,
    Section54FAssets,
    Section54FClaim,
    TaxProfile,
)

# TSM Models
from nucleus.models.tsm_models.call_logs import CallLogs
from nucleus.models.tsm_models.chat_messages import TaskChatMessage
from nucleus.models.tsm_models.files import File
from nucleus.models.tsm_models.notification import Notification
from nucleus.models.tsm_models.push_subscription import PushSubscription
from nucleus.models.tsm_models.task import Task, TaskAssignee, Session

# Client Profiling Models
from nucleus.models.client_profiling.address import Address
from nucleus.models.client_profiling.personal_info import PersonalInformation
from nucleus.models.client_profiling.country_lookup import CountryLookup
from nucleus.models.client_profiling.assets_disclosure_documents import AssetsDisclosureDocuments
from nucleus.models.client_profiling.employment import Employment
from nucleus.models.client_profiling.foreign_custodial_accounts import ForeignCustodialAccounts
from nucleus.models.client_profiling.foreign_deposit_custodial_accounts import ForeignDepositCustodialAccounts
from nucleus.models.client_profiling.foreign_depository_accounts import ForeignDepositoryAccounts
from nucleus.models.client_profiling.foreign_equity_debt_interests import ForeignEquityDebtInterests
from nucleus.models.client_profiling.foreign_financial_interests import ForeignFinancialInterests
from nucleus.models.client_profiling.foreign_immovable_properties import ForeignImmovableProperties
from nucleus.models.client_profiling.foreign_insurance_contracts import ForeignInsuranceContracts
from nucleus.models.client_profiling.foreign_other_capital_assets import ForeignOtherCapitalAssets
from nucleus.models.client_profiling.foreign_signing_authority_accounts import ForeignSigningAuthorityAccounts
from nucleus.models.client_profiling.foreign_other_incomes import ForeignOtherIncomes
from nucleus.models.client_profiling.insurance import Insurance
from nucleus.models.client_profiling.loan_records import LoanRecord
from nucleus.models.client_profiling.real_estate import RealEstate
from nucleus.models.client_profiling.jointly_owned_accounts import JointlyOwnedAccounts
from nucleus.models.client_profiling.separately_owned_accounts import SeparatelyOwnedAccounts
from nucleus.models.client_profiling.residency import Residency
from nucleus.models.client_profiling.citizenship import Citizenship
from nucleus.models.client_profiling.address import AddressType
from nucleus.models.advance_tax_models.form_26as_models import Form26ASPart1, Form26ASPart2, Form26ASPart3, Form26ASPart4, Form26ASPart5, Form26ASPart6, Form26ASPart7, Form26ASPart8, Form26ASPart9, Form26ASPart10
from nucleus.models.advance_tax_models.rule_validations import RuleValidations


__all__ = [
    # Common Models
    "Advisor",
    "Client",
    "ClientPhoneMapping",
    "Login",
    "OtpVerification",
    # Advance Tax Models
    "BrokerageAccounts",
    "CapitalGains",
    "Comments",
    "Dividends",
    "DocumentsUpload",
    "FinancialYear",
    "InterestDetails",
    "OtherIncome",
    "Excemption",
    "Quarter",
    "Rental",
    "Section54Claim",
    "Section54FAssets",
    "Section54FClaim",
    "TaxProfile",
    # TSM Models
    "CallLogs",
    "File",
    "Notification",
    "PushSubscription",
    "Session",
    "Task",
    "TaskAssignee",
    "TaskChatMessage",
    # Client Profiling Models
    "Address",
    "PersonalInformation",
    "CountryLookup",
    "AssetsDisclosureDocuments",
    "Employment",
    "ForeignCustodialAccounts",
    "ForeignDepositCustodialAccounts",
    "JointlyOwnedAccounts",
    "SeparatelyOwnedAccounts",
    "ForeignDepositoryAccounts",
    "ForeignEquityDebtInterests",
    "ForeignFinancialInterests",
    "ForeignImmovableProperties",
    "ForeignInsuranceContracts",
    "ForeignOtherCapitalAssets",
    "ForeignOtherIncomes",
    "ForeignSigningAuthorityAccounts",
    "Insurance",
    "LoanRecord",
    "RealEstate",
    "Residency",
    "Citizenship",
    "Employer",
    "AddressType",
    "Form26ASPart1",
    "Form26ASPart2",
    "Form26ASPart3",
    "Form26ASPart4",
    "Form26ASPart5",
    "Form26ASPart6",
    "Form26ASPart7",
    "Form26ASPart8",
    "Form26ASPart9",
    "Form26ASPart10",
    "RuleValidations",
]

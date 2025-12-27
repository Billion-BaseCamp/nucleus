# Import all models here for Alembic autogenerate to detect them

# Common Models
from nucleus.models.common_models.advisor import Advisor
from nucleus.models.common_models.client import Client, ClientPhoneMapping
from nucleus.models.common_models.login import Login
from nucleus.models.common_models.change_password import OtpVerification

# Advance Tax Models
from nucleus.models.advance_tax_models.capital_gains import CapitalGains
from nucleus.models.advance_tax_models.comments import Comments
from nucleus.models.advance_tax_models.dividends import Dividends
from nucleus.models.advance_tax_models.documents_upload import DocumentsUpload
from nucleus.models.advance_tax_models.financial_year import FinancialYear
from nucleus.models.advance_tax_models.interest_details import InterestDetails
from nucleus.models.advance_tax_models.other_income import OtherIncome
from nucleus.models.advance_tax_models.quarter import Quarter
from nucleus.models.advance_tax_models.rental import Rental
from nucleus.models.advance_tax_models.tax_profile import TaxProfile

# TSM Models
from nucleus.models.tsm_models.call_logs import CallLogs
from nucleus.models.tsm_models.chat_messages import TaskChatMessage
from nucleus.models.tsm_models.files import File
from nucleus.models.tsm_models.notification import Notification
from nucleus.models.tsm_models.push_subscription import PushSubscription
from nucleus.models.tsm_models.task import Task, TaskAssignee, Session

# Client Profiling Models
from nucleus.models.client_profiling.address import Address
from nucleus.models.client_profiling.assets_with_maturity import AssetWithMaturity
from nucleus.models.client_profiling.cash_flow_office import CashFlowOffice
from nucleus.models.client_profiling.cash_flows import CashFlow
from nucleus.models.client_profiling.children_info import ChildInfo
from nucleus.models.client_profiling.client_profiling import ClientProfile
from nucleus.models.client_profiling.country_lookup import CountryLookup
from nucleus.models.client_profiling.cp_advisors import CPAdvisor
from nucleus.models.client_profiling.employment import Employment
from nucleus.models.client_profiling.foreign_custodial_accounts import ForeignCustodialAccounts
from nucleus.models.client_profiling.foreign_depository_accounts import ForeignDepositoryAccounts
from nucleus.models.client_profiling.foreign_equity_debt_interests import ForeignEquityDebtInterests
from nucleus.models.client_profiling.foreign_financial_interests import ForeignFinancialInterests
from nucleus.models.client_profiling.foreign_immovable_properties import ForeignImmovableProperties
from nucleus.models.client_profiling.foreign_insurance_contracts import ForeignInsuranceContracts
from nucleus.models.client_profiling.foreign_other_capital_assets import ForeignOtherCapitalAssets
from nucleus.models.client_profiling.foreign_signing_authority_accounts import ForeignSigningAuthorityAccounts
from nucleus.models.client_profiling.foreign_other_incomes import ForeignOtherIncomes
from nucleus.models.client_profiling.goals import Goal
from nucleus.models.client_profiling.income import income
from nucleus.models.client_profiling.insurance import Insurance
from nucleus.models.client_profiling.loan_records import LoanRecord
from nucleus.models.client_profiling.other_assets import OtherAsset
from nucleus.models.client_profiling.other_loans import OtherLoan
from nucleus.models.client_profiling.parent_assets import ParentAsset
from nucleus.models.client_profiling.real_estate import RealEstate
from nucleus.models.client_profiling.real_estate_plans import RealEstatePlan
from nucleus.models.client_profiling.rsu_vesting import RSUVesting
from nucleus.models.client_profiling.soa_master import SOAMaster
from nucleus.models.client_profiling.tax_records import TaxRecords


__all__ = [
    # Common Models
    "Advisor",
    "Client",
    "ClientPhoneMapping",
    "Login",
    "OtpVerification",
    # Advance Tax Models
    "CapitalGains",
    "Comments",
    "Dividends",
    "DocumentsUpload",
    "FinancialYear",
    "InterestDetails",
    "OtherIncome",
    "Quarter",
    "Rental",
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
    "AssetWithMaturity",
    "CashFlow",
    "CashFlowOffice",
    "ChildInfo",
    "ClientProfile",
    "CountryLookup",
    "CPAdvisor",
    "Employment",
    "ForeignCustodialAccounts",
    "ForeignDepositoryAccounts",
    "ForeignEquityDebtInterests",
    "ForeignFinancialInterests",
    "ForeignImmovableProperties",
    "ForeignInsuranceContracts",
    "ForeignOtherCapitalAssets",
    "ForeignOtherIncomes",
    "ForeignSigningAuthorityAccounts",
    "Goal",
    "income",
    "Insurance",
    "LoanRecord",
    "OtherAsset",
    "OtherLoan",
    "ParentAsset",
    "RealEstate",
    "RealEstatePlan",
    "RSUVesting",
    "SOAMaster",
    "TaxRecords",
]

# Import all models here for Alembic autogenerate to detect them
from nucleus.models.common_models.advisor import Advisor
from nucleus.models.advance_tax_models.capital_gains import CapitalGains
from nucleus.models.common_models.client import Client
from nucleus.models.advance_tax_models.comments import Comments
from nucleus.models.advance_tax_models.dividends import Dividends
from nucleus.models.advance_tax_models.documents_upload import DocumentsUpload
from nucleus.models.advance_tax_models.financial_year import FinancialYear
from nucleus.models.advance_tax_models.interest_details import InterestDetails
from nucleus.models.common_models.login import Login
from nucleus.models.advance_tax_models.other_income import OtherIncome
from nucleus.models.advance_tax_models.quarter import Quarter
from nucleus.models.advance_tax_models.rental import Rental
from nucleus.models.advance_tax_models.tax_profile import TaxProfile
from nucleus.models.tsm_models.notification import Notification
from nucleus.models.tsm_models.chat_messages import TaskChatMessage
from nucleus.models.tsm_models.task import Task, TaskAssignee
from nucleus.models.common_models.change_password import OtpVerification
from nucleus.models.tsm_models.files import File
from nucleus.models.tsm_models.push_subscription import PushSubscription
from nucleus.models.tsm_models.call_logs import CallLogs

__all__ = [
    "Advisor",
    "CapitalGains",
    "Client",
    "Comments",
    "Dividends",
    "DocumentsUpload",
    "FinancialYear",
    "InterestDetails",
    "Login",
    "Notification",
    "OtherIncome",
    "Quarter",
    "Rental",
    "Task",
    "TaskAssignee",
    "TaskChatMessage",
    "TaxProfile",
    "OtpVerification",
    "File",
    "PushSubscription",
    "CallLogs"
]

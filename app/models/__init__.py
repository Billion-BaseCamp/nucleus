# Import all models here for Alembic autogenerate to detect them
from app.models.common_models.advisor import Advisor
from app.models.advance_tax_models.capital_gains import CapitalGains
from app.models.common_models.client import Client
from app.models.advance_tax_models.comments import Comments
from app.models.advance_tax_models.dividends import Dividends
from app.models.advance_tax_models.documents_upload import DocumentsUpload
from app.models.advance_tax_models.financial_year import FinancialYear
from app.models.advance_tax_models.interest_details import InterestDetails
from app.models.common_models.login import Login
from app.models.advance_tax_models.other_income import OtherIncome
from app.models.advance_tax_models.quarter import Quarter
from app.models.advance_tax_models.rental import Rental
from app.models.advance_tax_models.tax_profile import TaxProfile
from app.models.tsm_models.notification import Notification
from app.models.tsm_models.task import Task

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
    "OtherIncome",
    "Quarter",
    "Rental",
    "TaxProfile",
]

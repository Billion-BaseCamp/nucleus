# Advance Tax Models
# Import order matters for SQLAlchemy string-based relationship resolution:
# 1. FinancialYear first (no dependency on other advance_tax_models)
# 2. Employer second (relationship "FinancialYear" must be in registry)
# 3. TaxProfile and others (no Employer dependency)

from nucleus.models.advance_tax_models.capital_gains import CapitalGains
from nucleus.models.advance_tax_models.brokerage_accounts import BrokerageAccounts
from nucleus.models.advance_tax_models.comments import Comments
from nucleus.models.advance_tax_models.dividends import Dividends
from nucleus.models.advance_tax_models.documents_upload import DocumentsUpload
from nucleus.models.advance_tax_models.excemption import Excemption
from nucleus.models.advance_tax_models.financial_year import FinancialYear
from nucleus.models.advance_tax_models.employer import Employer
from nucleus.models.advance_tax_models.interest_details import InterestDetails
from nucleus.models.advance_tax_models.other_income import OtherIncome
from nucleus.models.advance_tax_models.quarter import Quarter
from nucleus.models.advance_tax_models.rental import Rental
from nucleus.models.advance_tax_models.section_54_claim import Section54Claim
from nucleus.models.advance_tax_models.section_54F_claim import Section54FClaim
from nucleus.models.advance_tax_models.section_54F_assests import Section54FAssets
from nucleus.models.advance_tax_models.tax_profile import TaxProfile

__all__ = [
    "BrokerageAccounts",
    "CapitalGains",
    "Comments",
    "Dividends",
    "DocumentsUpload",
    "Excemption",
    "FinancialYear",
    "Employer",
    "InterestDetails",
    "OtherIncome",
    "Quarter",
    "Rental",
    "Section54Claim",
    "Section54FAssets",
    "Section54FClaim",
    "TaxProfile",
]

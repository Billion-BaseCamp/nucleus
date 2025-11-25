from enum import Enum

import pytz

IST_TIMEZONE = pytz.timezone('Asia/Kolkata')

# User roles
class UserRole(Enum):
    ADMIN = "admin"
    CLIENT = "client"
    ADVISOR = "advisor"

class CapitalGainsCategory(Enum):
    INTRA_DAY = "INTRA_DAY"
    INTER_DAY = "INTER_DAY"
    LBF = "LBF"
    NET_GAINS_AFSTOFF = "NET_GAINS_AFSTOFF"
    CAPITAL_GAINS="CAPITAL_GAINS"

class ResidenceType(Enum):
    RES="RES"
    NRI="NRI"
    NRO="NRO"

# Other income field names
OTHER_INCOME_FIELDS = [
    "income_44ada",
    "property_sale_tds", 
    "additional_foreign_tax_credits",
    "tcs_incurred",
    "tds_44ada",
    "salary_exemption",
    "any_other_income",
    "tcs_expected"
]
class CommentsCategory(Enum):
    CAPITAL_GAINS = "capital_gains"
    INTEREST_DETAILS = "interest_details"
    DIVIDENDS = "dividends"
    RENTAL = "rental"
    OTHER_INCOME = "other_income"
    SUMMARY = "summary"


class Region(str,Enum):
    DOMESTIC = "DOMESTIC"
    FOREIGN = "FOREIGN"


class TASK_STATUSES(Enum):
    PENDING = "Pending"
    IN_PROGRESS = "In Progress"
    COMPLETED = "Completed"
    Pending_ON_CLIENT = "Pending on Client"


class ACCEPTANCE_STATUS(Enum):
    PENDING = "Pending"
    ACCEPTED = "Accepted"
    REJECTED = "Rejected"
    TRANSFERRED = "Transferred"

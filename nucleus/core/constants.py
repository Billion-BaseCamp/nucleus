from enum import Enum

import pytz

IST_TIMEZONE = pytz.timezone('Asia/Kolkata')

# User roles
class UserRole(Enum):
    ADMIN = "admin"
    CLIENT = "client"
    ADVISOR = "advisor"
    ANALYST = "analyst"

class CapitalGainsCategory(Enum):
    INTRA_DAY = "INTRA_DAY"
    INTER_DAY = "INTER_DAY"
    LBF = "LBF"
    NET_GAINS_AFSTOFF = "NET_GAINS_AFSTOFF"
    CAPITAL_GAINS="CAPITAL_GAINS"
    LCF="LCF"

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
    PDF_COMMENT = "pdf_comment"


class Region(str,Enum):
    DOMESTIC = "DOMESTIC"
    FOREIGN = "FOREIGN"


class TASK_STATUSES(Enum):
    PENDING = "Pending"
    IN_PROGRESS = "In Progress"
    COMPLETED = "Completed"


class ACCEPTANCE_STATUS(Enum):
    PENDING = "Pending"
    ACCEPTED = "Accepted"
    REJECTED = "Rejected"
    TRANSFERRED = "Transferred"


# Marital status enum
class MaritalStatus(Enum):
    SINGLE = "Single"
    MARRIED = "Married"
    DIVORCED = "Divorced"
    WIDOWED = "Widowed"

# Yes/No/NA enum
class YesNoNA(Enum):
    YES = "Yes"
    NO = "No"
    NA = "NA"

class InsuranceCategory(Enum):
    LIFE_INSURANCE = "Life Insurance"
    HEALTH_INSURANCE = "Health Insurance"
    CAR_INSURANCE = "Car Insurance"
    HOME_INSURANCE = "Home Insurance"
    TRAVEL_INSURANCE = "Travel Insurance"
    OTHER_INSURANCE = "Other Insurance"


class LoanType(Enum):
    HOME_LOAN = "Home Loan"
    CAR_LOAN = "Car Loan"
    PERSONAL_LOAN = "Personal Loan"
    EDUCATION_LOAN = "Education Loan"
    BUSINESS_LOAN = "Business Loan"
    GOLD_LOAN = "Gold Loan"
    OVERDRAFT_LOAN = "Overdraft Loan"
    CREDIT_CARD_LOAN = "Credit Card Loan"
    STUDENT_LOAN = "Student Loan"
    OTHER_LOAN = "Other Loan"


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


class EmployerSource(str, Enum):
    JSON = "JSON"
    MANUAL = "MANUAL"




# ---------------------------------------------------------------------------
# Client Service Agreement (CSA) repository
# ---------------------------------------------------------------------------


class CSALegalEntity(str, Enum):
    """Contracting Billion BaseCamp entity named in the agreement."""

    KLOK = "KLOK"      # Klok Global Family Office LLP (ACD-6756)
    BFAPL = "BFAPL"    # Billion Financial Advisors Private Limited (U67190PN2020PTC190207)
    OTHER = "OTHER"


class CSAMatchTier(str, Enum):
    """How a csa_parties row was linked to a client. NULL = unmapped.

    Fuzzy matches are never auto-linked, so there is deliberately no FUZZY tier:
    a fuzzy suggestion lives in ``match_candidates`` until a human accepts it,
    at which point the tier becomes MANUAL.
    """

    EXACT = "EXACT"          # normalized sorted-token key matched a client
    CROSSWALK = "CROSSWALK"  # matched via ClientNameMapping.xlsx
    MANUAL = "MANUAL"        # a human confirmed the link


class CSAReviewStatus(str, Enum):
    """Extraction-quality state of a document — about the PDF, not the client link."""

    PENDING = "PENDING"    # extracted, not yet checked
    FLAGGED = "FLAGGED"    # auto-flagged: unreadable table, empty section, contradiction
    VERIFIED = "VERIFIED"  # a human confirmed the extraction
    FAILED = "FAILED"      # could not be extracted at all


class CSAFeeType(str, Enum):
    ANNUAL_RETAINER = "ANNUAL_RETAINER"
    ONE_TIME = "ONE_TIME"
    MILESTONE = "MILESTONE"
    RENEWAL = "RENEWAL"
    UPFRONT = "UPFRONT"          # 0.50% initial one-time fixed fee
    PERFORMANCE = "PERFORMANCE"  # 20% over a hurdle
    EARLY_EXIT = "EARLY_EXIT"    # 0.50% on withdrawal before minimum period
    PERCENTAGE = "PERCENTAGE"    # other rate-based charge (e.g. 7% of tax refund)
    OTHER = "OTHER"


class CSAInclusion(str, Enum):
    """Whether a service line is covered, extra, or explicitly carved out.

    EXCLUDED is a negative entitlement ("except scrutiny notices") and must not
    be read as a service provided.
    """

    INCLUDED_IN_RETAINER = "INCLUDED_IN_RETAINER"
    CHARGED_SEPARATELY = "CHARGED_SEPARATELY"
    EXCLUDED = "EXCLUDED"
    UNSPECIFIED = "UNSPECIFIED"


class CSAServiceCode(str, Enum):
    """Canonical service catalogue.

    v2 (2026-09-25). Extended after a full-corpus UNMAPPED clustering pass;
    see csa-repository-pipeline skill for the method.
    """

    # --- India tax ---
    IN_ITR_FILING = "IN_ITR_FILING"
    IN_ADVANCE_TAX = "IN_ADVANCE_TAX"
    IN_TAX_PLANNING = "IN_TAX_PLANNING"
    IN_PRIOR_YEAR_REVIEW = "IN_PRIOR_YEAR_REVIEW"
    IN_NOTICE_SUPPORT = "IN_NOTICE_SUPPORT"
    IN_SCRUTINY = "IN_SCRUTINY"
    IN_APPEALS = "IN_APPEALS"
    IN_HUF = "IN_HUF"
    IN_TDS = "IN_TDS"
    IN_CA_CERTIFICATE = "IN_CA_CERTIFICATE"  # 15CA/15CB remittance certificate
    IN_GST = "IN_GST"

    # --- UK tax ---
    # The corpus is not India/US only: a small UK cohort exists, with fees
    # billed in GBP (Hemant Arora, Gunjan Soni, Nikunj Jhunjhunwala) and
    # UK-specific deliverables. Do not fold these into IN_*/US_* codes.
    UK_TAX_FILING = "UK_TAX_FILING"
    UK_TAX_PLANNING = "UK_TAX_PLANNING"
    UK_RESIDENCY_CERT = "UK_RESIDENCY_CERT"
    UK_INHERITANCE_TAX = "UK_INHERITANCE_TAX"

    # --- cross-border & equity comp ---
    CAP_GAINS_ADVISORY = "CAP_GAINS_ADVISORY"
    RSU_ESOP = "RSU_ESOP"
    CROSS_BORDER = "CROSS_BORDER"
    FOREX_ADVISORY = "FOREX_ADVISORY"
    FOREX_NEGOTIATION = "FOREX_NEGOTIATION"

    # --- US tax ---
    US_1040 = "US_1040"
    US_STATE = "US_STATE"
    US_TAX_PLANNING = "US_TAX_PLANNING"
    US_PRIOR_YEAR_REVIEW = "US_PRIOR_YEAR_REVIEW"
    US_FBAR = "US_FBAR"
    US_FATCA = "US_FATCA"
    US_PFIC = "US_PFIC"
    US_STREAMLINED = "US_STREAMLINED"
    US_ESTIMATED_TAX = "US_ESTIMATED_TAX"
    US_IRS_NOTICE = "US_IRS_NOTICE"
    US_GIFT_ESTATE = "US_GIFT_ESTATE"
    US_K1 = "US_K1"
    US_FORM_3520 = "US_FORM_3520"
    US_FORM_5471 = "US_FORM_5471"
    US_FORM_5472 = "US_FORM_5472"
    US_FORM_8833 = "US_FORM_8833"
    US_1040X = "US_1040X"
    US_FTC_FEIE = "US_FTC_FEIE"      # Form 1116 / 2555
    US_EXTENSION = "US_EXTENSION"
    US_SCHED_A = "US_SCHED_A"
    US_SCHED_C = "US_SCHED_C"
    US_SCHED_E = "US_SCHED_E"
    US_CREDIT_CARRYOVER = "US_CREDIT_CARRYOVER"
    US_TAX_ADV_SAVINGS = "US_TAX_ADV_SAVINGS"
    US_401K = "US_401K"

    # --- wealth / structuring ---
    ESTATE_PLANNING = "ESTATE_PLANNING"
    TRUST_SPV = "TRUST_SPV"
    RISK_MANAGEMENT = "RISK_MANAGEMENT"
    SALARY_RESTRUCTURING = "SALARY_RESTRUCTURING"
    BOOKKEEPING = "BOOKKEEPING"
    FIN_PLANNING = "FIN_PLANNING"
    WEALTH_ADVISORY = "WEALTH_ADVISORY"

    # --- investment advisory ---
    ADVISORY_INVESTMENT = "ADVISORY_INVESTMENT"
    ADVISORY_ACCOUNT_OPENING = "ADVISORY_ACCOUNT_OPENING"
    ADVISORY_REPORTING = "ADVISORY_REPORTING"
    ADVISORY_PLAN_EXECUTION = "ADVISORY_PLAN_EXECUTION"

    UNMAPPED = "UNMAPPED"

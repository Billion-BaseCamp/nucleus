# ITR filing persistence (separate from advance-tax coarse models).
# Import order: ITRReturn first (parent), then schedule + children.

from nucleus.models.itr_filling.itr_return import ITRReturn

from nucleus.models.itr_filling.salary import (
    ITRForeignSalary,
    ITROtherSalary,
    ITRSalaryAllowance,
    ITRSalaryComponent,
    ITRSalaryEmployer,
    ITRSalaryPerquisite,
    ITRSalarySchedule,
)

from nucleus.models.itr_filling.house_property import (
    ITRHPCoOwner,
    ITRHPLoan,
    ITRHPProperty,
    ITRHPSchedule,
    ITRHPTenant,
)

from nucleus.models.itr_filling.deductions import (
    ITRDedSchedule,
    ITRDed80C,
    ITRDed_80C_80CCD,
    ITR80DDetail,
    ITR80DMeta,
    ITR80DPolicy,
)

from nucleus.models.itr_filling.disclosures import (
    ITRALImmovableProperty,
    ITRDiscDirectorship,
    ITRDiscUnlistedShare,
    ITRDisclosuresSchedule,
    ITRFABankAccount,
    ITRFACashValueInsurance,
    ITRFAEquityDebt,
    ITRFAFinancialInterest,
    ITRFAForeignTrust,
    ITRFAImmovableProperty,
    ITRFAOtherAsset,
    ITRFAOtherForeignIncome,
    ITRFASigningAuthority,
)

from nucleus.models.itr_filling.tax_credits import (
    ITRAdvanceTaxPayment,
    ITRForm67Entry,
    ITRForm67Refund,
    ITRFSIEntry,
    ITRTCSEntry,
    ITRTDSSalary,
    ITRTDSNonSalary,
    ITRTDSProperty,
)

from nucleus.models.itr_filling.other_sources import (
    ITROSBuybackShare,
    ITROSClubbingEntry,
    ITROSDividendDetail,
    ITROSIncomeLine,
    ITROSInterestDetail,
    ITROSOtherIncome,
    ITROSPTIEntity,
    ITROSSchedule,
)

from nucleus.models.itr_filling.capital_gains import (
    ITRCGBFLYear,
    ITRCGBrokerSummary,
    ITRCGData,
    ITRCGDebtMFEntry,
    ITRCGExemption54EC,
    ITRCGExemption54F,
    ITRCGHPAcquisitionDetail,
    ITRCGHPBuyer,
    ITRCGHPEntry,
    ITRCGHPImprovement,
    ITRCGHPTransferExpense,
    ITRCGIndiaEQEntry,
    ITRCGUnlistedEntry,
    ITRCGUSEntry,
    ITRCGVDAEntry,
)

from nucleus.models.itr_filling.audit_logging import (
    ITRActivityLog,
    ITRAuthAuditEvent,
    ITRFieldChangeSnapshot,
)

from nucleus.models.itr_filling.itr_document_slot import ITRDocumentSlot
from nucleus.models.itr_filling.itr_document import ITRDocument

__all__ = [
    "ITRReturn",
    # Salary (Schedule S)
    "ITRForeignSalary",
    "ITROtherSalary",
    "ITRSalaryAllowance",
    "ITRSalaryComponent",
    "ITRSalaryEmployer",
    "ITRSalaryPerquisite",
    "ITRSalarySchedule",
    # House Property (Schedule HP)
    "ITRHPCoOwner",
    "ITRHPLoan",
    "ITRHPProperty",
    "ITRHPSchedule",
    "ITRHPTenant",
    # Other Sources (Schedule OS)
    "ITROSBuybackShare",
    "ITROSClubbingEntry",
    "ITROSDividendDetail",
    "ITROSIncomeLine",
    "ITROSInterestDetail",
    "ITROSOtherIncome",
    "ITROSPTIEntity",
    "ITROSSchedule",
    # Deductions (Chapter VI-A)
    "ITRDedSchedule",
    "ITRDed80C",
    "ITRDed_80C_80CCD",
    "ITR80DDetail",
    "ITR80DMeta",
    "ITR80DPolicy",
    # Tax credits
    "ITRAdvanceTaxPayment",
    "ITRForm67Entry",
    "ITRForm67Refund",
    "ITRFSIEntry",
    "ITRTCSEntry",
    "ITRTDSSalary",
    "ITRTDSNonSalary",
    "ITRTDSProperty",
    # Disclosures (AL / Part A / FA)
    "ITRALImmovableProperty",
    "ITRDiscDirectorship",
    "ITRDiscUnlistedShare",
    "ITRDisclosuresSchedule",
    "ITRFABankAccount",
    "ITRFACashValueInsurance",
    "ITRFAEquityDebt",
    "ITRFAFinancialInterest",
    "ITRFAForeignTrust",
    "ITRFAImmovableProperty",
    "ITRFAOtherAsset",
    "ITRFAOtherForeignIncome",
    "ITRFASigningAuthority",
    # Capital gains (Schedule CG)
    "ITRCGData",
    "ITRCGIndiaEQEntry",
    "ITRCGDebtMFEntry",
    "ITRCGUSEntry",
    "ITRCGUnlistedEntry",
    "ITRCGHPEntry",
    "ITRCGHPAcquisitionDetail",
    "ITRCGHPImprovement",
    "ITRCGHPTransferExpense",
    "ITRCGHPBuyer",
    "ITRCGVDAEntry",
    "ITRCGExemption54F",
    "ITRCGExemption54EC",
    "ITRCGBFLYear",
    "ITRCGBrokerSummary",
    # Audit / activity logging
    "ITRAuthAuditEvent",
    "ITRActivityLog",
    "ITRFieldChangeSnapshot",
    # Document upload slots
    "ITRDocumentSlot",
    "ITRDocument",
]

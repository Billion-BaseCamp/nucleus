# Advance Tax and ITR data models

Source of truth: `nucleus/models/` in this repository. Advance Tax and Tax Engine share **one Postgres**. They are two products on the same schema, not two databases.

This document is for an AI agent or a new developer. It covers:

- Which models exist, and what they are for
- Important fields, types, and nullability where it matters
- Foreign keys, parent-child trees, and soft (non-FK) pointers
- Uniqueness that encodes a business rule vs uniqueness that only exists in application code

Conventions used throughout:

- Primary key is UUID `id` unless noted (`Login.id` is integer).
- Most tables have `created_at` / `updated_at` (`DateTime(timezone=True)`). They are omitted below unless a table breaks the pattern.
- Default SQLAlchemy `ondelete` when omitted is PostgreSQL `NO ACTION`.
- Amounts: Advance Tax income heads often use `Float`. Salary / CG / s.54 claims and almost all ITR amounts use `Numeric(15,2)` or `Numeric(18,2)`.

---

## 1. How the two products scope data

**Advance Tax** is quarter-based projection:

```
Client
  └── FinancialYear          (Apr–Mar, label like "25-26")
        ├── TaxProfile       (FY-level settings)
        ├── Form 26AS parts  (FY-level parsed TDS/TCS)
        ├── CarryForwardLosses
        ├── PriorItrSnapshot (frozen last-year ITR)
        └── Quarter          (Q1 Apr–Jun … Q4 Jan–Mar)
              ├── Employer, InterestDetails, Dividends, Rental,
              │   OtherIncome, CapitalGains, Deductions, Excemption
              ├── ATCGSchedule (1:1 unique quarter_id)
              ├── ATCGDocumentSlot
              └── AdvanceTax26asUpload (1:1 unique quarter_id)
```

**Tax Engine / ITR** is return-based filing:

```
Client
  └── ITRReturn              (assessment year / FY / version)
        ├── 1:1 schedules    (salary, HP, BP, OS, deductions, disclosures, CFL;
        │                    CG + tax credits intended 1:1 in ORM)
        │     └── 1:N child rows
        ├── 1:N address / refund bank / AIS imports / jobs
        └── optional archives (AIS JSON, TIS PDF, 26AS) — client-owned, ITR-linked
```

`FinancialYear` is the **shared year spine**. Advance Tax owns the table. Tax Engine stores the same UUID on `ITRReturn.financial_year_id` **without a declared `ForeignKey`**. Deleting an FY does **not** cascade to ITR rows.

Document slots and the Step 2 wizard are **Client + FY trees**, not children of `ITRReturn`.

---

## 2. Cross-product bridges

| Bridge | From | To | How it actually links |
|---|---|---|---|
| Year spine | `FinancialYear` | `ITRReturn` | Same UUID in `itr_returns.financial_year_id`. No FK either way. |
| Salary employer | `employers` | `itr_salary_employers` | `source_employer_id` → `employers.id` `ON DELETE SET NULL`. |
| Prior ITR for AT YoY | Filed JSON import | `PriorItrSnapshot` | Denormalized floats on the **current** AT FY. Not an FK to `ITRReturn`. Unique `(client_id, financial_year_id)`. |
| CG documents | `at_cg_document_slots` | `itr_document_slots` | Parallel replicas, not a shared table. AT keyed by **quarter**; ITR keyed by **FY**. |
| Generic files | `DocumentsUpload` | both products | Polymorphic `link_id` + `category`. No `client_id` column. |
| FA collector → filing | `foreign_*` (FY-scoped) | `itr_fa_*` | Tax Engine copies collector FA into Schedule FA. Advance Tax does not read FA tables. |
| 26AS | `advance_tax_26as_uploads` + parts | `itr_form_26as_archives` + `itr_26as_entries` | Three families, not one shared file table. |
| AMFI ISIN | `amfi_mf_isin` | ITR CG ingest | Global MF ISIN registry. Tax Engine only. |

---

## 3. Shared identity

### `Client` — `clients`

Master tax-client record. Both products hang year-scoped work off this id.

| Column | Type | Null | Meaning |
|---|---|---|---|
| `first_name`, `last_name` | String | NO | Display name |
| `middle_name`, `father_name` | String | YES | |
| `pan_number` | String | YES | Unique among **active** clients (partial unique on `upper(btrim(pan_number))`) |
| `adhar_number` | String | YES | Aadhaar (spelling as stored) |
| `date_of_birth` | Date | YES | Used to derive AIS/TIS passwords (`PAN lowercase + DOB ddmmyyyy`) |
| `gender` | String | YES | |
| `is_family_member` | Boolean | default False | |
| `parent_id` | UUID | YES | Household grouping. **Not an FK** |
| `family_relationship` | String | YES | |
| `is_advance_tax_payer` | Boolean | default True | |
| `residence_type` | Enum `RES` / `NRI` / `NRO` | YES | |
| `is_active` | Boolean | YES, default True | Soft-deleted rows keep PAN so it can be reused |
| `deactivated_at` | DateTime(tz) | YES | |
| `it_portal_username`, `it_portal_pass` | String | YES | IT-portal credentials |
| `advisor_id` | UUID FK `advisors.id` | YES | No `ondelete` |

### `Advisor` — `advisors`

Staff who own clients, approve devices, and review filings. `first_name` / `last_name` required. `is_active` default true.

### `Login` — `logins`

Sign-in identity. **Integer PK**. Exactly one of `client_id` (CASCADE) or `advisor_id` (check `ck_logins_exactly_one_owner`). Role: `admin` / `client` / `advisor` / `analyst`. `email` is indexed, **not unique**. `device_binding_required` — clients typically stay false.

Related: `LoginEvent` (`login_events`), `TrustedDevice` (one pending device per login), `WebAuthnCredential` (1:1 with device; private key never stored), `OtpVerification` (HMAC hex digest, never plaintext).

### Contact mappings

- `ClientPhoneMapping` — `client_phone_mappings`. Unique `(client_id, phone_number)`. TSM resolves inbound calls through this.
- `ClientEmailMapping` — `client_email_mappings`. Unique `(client_id, email)` plus case-insensitive `lower(email)`. Sign-in identity stays on `logins.email`.

### CSA (engagement)

`CSADocument` maps a signed PDF onto an **existing** client (never creates one). Unique `sha256`; unique `docusign_envelope_id` where not null. Children: `CSAParty` (`client_id` RESTRICT, nullable), `CSAFee`, `CSAService` (`canonical_code` includes `IN_ITR_FILING` and `IN_ADVANCE_TAX`), `CSAParseWarning`. Raw OCR tables (`csa_*_raw`) preserve extraction; live tables are what tax products see.

### Collector flags (Tax Engine writes)

`DocumentCollectorInfo` — `document_collector_info`. Unique `(client_id, financial_year_id)`. FY-level flags: CG / FA / salary / AIS / 26AS / TIS / JSON imported, applicability booleans, `balance_tax`. Advance Tax backend does **not** import this class.

`SubTypeComments` — collector comments by `sub_type` + `region`. No unique (app upserts).

---

## 4. Client profiling

Two shapes:

1. **Client-scoped** (`clients.id` FK): `PersonalInformation`, `Address`, `Employment`, `Residency`, `Citizenship`, `Insurance`, `LoanRecord`, `RealEstate`.
2. **FY-scoped** (only `financial_years.id` FK, **no `client_id`**): all `Foreign*` FA tables, jointly/separately owned, `AssetsDisclosureDocuments`. Client is implied via `FinancialYear.client_id`.

### Used today

| Class | Table | Notes |
|---|---|---|
| `PersonalInformation` | `personal_information` | 1:1 with client. HUF / karta for ITR Part A. Tax Engine writes. |
| `Address` | `addresses` | Legacy mailing address. ITR Part A now prefers `ITRAddress`. No unique on `(client_id, address_type)`. |
| `ForeignDepositoryAccounts` | `foreign_depository_accounts` | FA A1 → `ITRFABankAccount` |
| `ForeignCustodialAccounts` | `foreign_custodial_accounts` | FA A2 → `ITRFABankAccount` |
| `ForeignEquityDebtInterests` | `foreign_equity_debt_interests` | FA A3 → `ITRFAEquityDebt` |
| `ForeignInsuranceContracts` | `foreign_insurance_contracts` | FA A4 → `ITRFACashValueInsurance` |
| `ForeignImmovableProperties` | `foreign_immovable_properties` | FA B1 → `ITRFAImmovableProperty` |
| `ForeignFinancialInterests` | `foreign_financial_interests` | FA B2 → `ITRFAFinancialInterest` |
| `ForeignSigningAuthorityAccounts` | `foreign_signing_authority_accounts` | FA C → `ITRFASigningAuthority` |
| `ForeignOtherCapitalAssets` | `foreign_other_capital_assets` | FA D → `ITRFAOtherAsset` |
| `ForeignOtherIncomes` | `foreign_other_incomes` | FA F → `ITRFAOtherForeignIncome` |
| `AssetsDisclosureDocuments` | `assets_disclosure_documents` | FA source files in S3. Unique `(sha256_hash, financial_year_id)`. Keyed by `client_email`, not `client_id`. Password flag + value if protected. |
| `CountryLookup` | `country_lookup` | Country master for FA `country_id`. No unique on code/name. |

Advance Tax does **not** read or write the FA collector tables.

### Present, unused by current AT/TE services

`Employment`, `Residency`, `Citizenship`, `Insurance`, `LoanRecord`, `RealEstate` — ITR uses Step 2 + schedules instead.

FBAR-shaped, unused: `ForeignDepositCustodialAccounts`, `JointlyOwnedAccounts`, `SeparatelyOwnedAccounts`.

---

## 5. Shared year spine

### `FinancialYear` — `financial_years`

Indian FY (Apr–Mar) for one client. Advance Tax owns the table; Tax Engine reuses the same rows.

| Column | Type | Null | Meaning |
|---|---|---|---|
| `client_id` | UUID FK CASCADE | NO | Owner |
| `financial_year` | String | NO | Label, e.g. `"25-26"` |
| `start_date` / `end_date` | Date | NO | Typically 1 Apr – 31 Mar |
| `return_date` | Date | NO | ITR due date (typically 31 Jul of next calendar year) |
| `status` | String | NO | `"active"` current FY, `"completed"` prior |
| `is_fbar_imported` / `is_fatca_imported` | Boolean | NO | Default false. Neither backend currently references these flags |

**No UniqueConstraint** on `(client_id, financial_year)` — one-FY-per-client is application-only.

Declared relationships: `quarters`, Form 26AS parts 1–10, `carry_forward_losses`, `prior_itr_snapshot` (1:1). **No relationship to `ITRReturn` or `TaxProfile`.**

---

## 6. Advance Tax models

Package: `nucleus/models/advance_tax_models/`.

Registration creates 3 FYs × 4 quarters. Q1 = Apr–Jun, Q2 = Jul–Sep, Q3 = Oct–Dec, Q4 = Jan–Mar. Future quarters start `is_locked=True`.

### 6.1 Period

#### `Quarter` — `quarters`

Working period for income heads, CG docs/schedule, employers, 26AS upload, comments, and rule overrides.

| Column | Type | Null | Meaning |
|---|---|---|---|
| `financial_year_id` | UUID FK CASCADE | NO | Parent FY |
| `quarter_number` | Integer | NO | 1–4 |
| `start_date` / `end_date` | Date | NO | Quarter window |
| `is_locked` | Boolean | YES, default False | Future quarters start locked |
| `status` | String | NO | `active` / `completed` / `inactive` |
| `is_liability` | Boolean | YES | **Legacy**; use `liability_status` |
| `liability_status` | String | YES | `liability_confirmed` / `no_liability_confirmed` / `paid` / NULL |
| `is_json_imported` | Boolean | YES, default False | ITR JSON imported into this quarter |

**No UniqueConstraint** on `(financial_year_id, quarter_number)`.

No reverse relationship to Comments, Deductions, or `AdvanceTax26asUpload` (upload owns the link to avoid a cycle).

#### `TaxProfile` — `tax_profile`

FY-level Advance Tax settings. **Advance Tax writes.** Tax Engine does not import this class. No ORM `relationship()` declared.

| Column | Type | Null | Meaning |
|---|---|---|---|
| `financial_year_id` | UUID FK CASCADE | NO | |
| `client_id` | UUID FK CASCADE | NO | Denormalized; also reachable via FY |
| `expected_current_year_income` | Float | NO | Projected total income |
| `tax_rate` | Float | NO | Slab / effective rate |
| `advance_tax_paid_Q1`…`Q4` | Float | YES | Challan amounts already paid |
| `is_26as_imported` | Boolean | NO | Default false |
| `net_salary`, `gross_salary`, `tds`, `income_under_the_head_salary`, `basic_salary`, `employer_contribution_to_pf`, `employer_contribution_to_nps` | JSONB `Dict[str,float]` | YES | Aggregated salary maps |
| `tax_regime` | String | NO | `"NEW"` (default) or `"OLD"` |

**No UniqueConstraint.** App upserts by `(client_id, financial_year_id)`.

### 6.2 Income heads

Application code treats Interest / Dividends / OtherIncome / Deductions as **one row per client+quarter**. That is not a DB unique.

#### `Employer` — `employers`

Per-quarter salary / Form 16 line.

| Column | Type | Null | Meaning |
|---|---|---|---|
| `quarter_id` | UUID FK CASCADE | **YES** | Orphan employers possible |
| `employer_name` | String | NO | |
| `tan` | String(20) | YES | Indexed; unique with quarter when not null |
| `source` | Enum `JSON` / `MANUAL` | NO | Default MANUAL |
| `gross_salary`, `income_under_the_head_salary`, `basic_salary`, PF/NPS, `standard_deduction`, `professional_tax`, `gratuity`, `leave_encashment`, `hra`, `other_allowances`, `tds` | Numeric(18,2) | YES | Components |

Partial unique index `uq_employers_quarter_id_tan` on `(quarter_id, tan)` **WHERE `tan IS NOT NULL`**.

Inbound FK from ITR: `ITRSalaryEmployer.source_employer_id` → `employers.id` `SET NULL`.

#### `InterestDetails` / `InterestAccounts`

Quarter roll-up of FD / savings / other / pass-through / EPF / IT-refund / foreign interest + TDS + rates (`Float`, defaults 0). Accounts split by `sub_category`: `FD` | `SAVINGS` | `PASS` | `OTHER` | `FOREIGN`.

`client_id` has **no ondelete**.

#### `Dividends` / `DividendAccounts`

Indian + foreign dividends, TDS, FTC. Account `sub_category`: `"Foreign Dividends"` or `"Indian Dividends"`. Indian rows use `tds_amount` / `tds_rate`; foreign rows use `ftc_amount` / `ftc_rate`.

#### `Rental` / `RentalCoOwner`

One house-property row per property (multiple per quarter allowed). `property_name` and `annual_rental_income` / `ownership_percentage` required. `property_group_id` groups co-owner rows of the same property — **UUID, not an FK**.

`RentalCoOwner`: `rental_id` CASCADE; `co_owner_client_id` SET NULL; `linked_rental_id` SET NULL; `is_other` for non-client co-owners.

#### `OtherIncome` / `OtherIncomeAccounts`

44AD / 44ADA, consultancy, insurance/PF proceeds, TCS/TDS credits, AIF / other expenses. Account `sub_category`: `44AD` | `44ADA` | `CONSULTANCY` | `ANY_OTHER`.

#### `Deductions` — `deductions`

Coarse Chapter VI-A totals (`section_80c` … `section_80eea`, `hra_exemption`, `total_deductions`). **No ORM relationship.** `quarter_id` has **no ondelete** (unlike almost every other quarter FK).

### 6.3 Capital gains

Two parallel stores:

1. **Legacy JSON store:** `CapitalGains` + `BrokerageAccounts` (rate-bucket totals as JSONB / Numeric).
2. **ITR-replica trade store:** `ATCGSchedule` + broker/txn tables. HP / bonds / other assets / DTAA / 54 / 54F are **not** replicated here.

#### `CapitalGains` — `capital_gains`

Category stored as String, not a DB enum: `INTRA_DAY`, `INTER_DAY`, `LBF`, `NET_GAINS_AFSTOFF`, `CAPITAL_GAINS`, `LCF`. Mix of Float nets and JSONB `{broker: amount}` maps. `cryptoCaptialGains` spelling as stored. Multiple rows per quarter (one per category) are expected.

#### `BrokerageAccounts` — `brokerage_accounts`

Per-broker amount. `source_document_id` → `at_cg_documents.id` `SET NULL`.

#### `ATCGSchedule` — `at_cg_schedule`

**One CG schedule per quarter** (`quarter_id` unique). `computation_status` default `NOT_STARTED`. Numeric(15,2) STCG/LTCG buckets; F&O business-opt flags.

Children (all CASCADE, ordered by `display_order`):

| Class | Table | Notes |
|---|---|---|
| `ATCGIndiaEQAndDebtMFBroker` | `at_cg_india_eq_and_debt_mf_brokers_data` | Broker roll-up. `source_document_id` is indexed UUID, **not an FK** |
| `ATCGIndiaEQAndDebtMFTransaction` | `at_cg_india_eq_and_debt_mf_transactions` | Per-scrip. Qty Numeric(15,4); ISIN; STT; grandfathering FMV. `source_document_id` CASCADE (deleting the PDF deletes trades) |
| `ATCGUSBroker` / `ATCGUSTransaction` | `at_cg_us_brokers_data`, `at_cg_us_transactions` | USD + `exchange_rate` Numeric(10,4) + INR |
| `ATCGUnlistedTransaction` | `at_cg_unlisted_transactions` | Schedule-level, no broker parent. Per-share values, FMV, indexed COA |
| `ATCGVDATransaction` | `at_cg_vda_transactions` | Crypto u/s 115BBH. `income` = consideration − COA |

#### CG documents

`ATCGDocumentSlot` — unique `uq_at_cg_doc_slot` on `(quarter_id, client_id, doc_type, sub_type, source, region, notes)` with `NULLS NOT DISTINCT`. Replica of ITR slots, keyed by quarter.

`ATCGDocument` — S3 object + `is_password_protected` + stored `password`. Original stays encrypted. View is a presigned URL of the still-locked file; UI may show the saved password.

`ATCGDocumentProcessingLog` — one LLM/parser attempt. No unique on `(document_id, attempt_number)`. No `updated_at`.

### 6.4 Form 26AS

Two layers:

- **Parsed 26AS (current):** one upload per quarter + 10 part tables on the FY.
- **Legacy log:** `upload_batches` + `file_metadata` — PAN/batch scoped, **unused** by current backends.

#### `AdvanceTax26asUpload` — `advance_tax_26as_uploads`

`.txt` from TRACES. **No password.** Unique `quarter_id`. `parse_status`: `pending` → `parsing` → `parsed` | `failed`.

S3 key + bucket + original filename required. `pan` optional. Quarter has **no reverse relationship** (avoids a cycle).

#### Parts 1–10 — `form_26as_part1` … `form_26as_part10`

Shared: `financial_year_id` CASCADE; optional `upload_id` CASCADE; `sr_no`; amounts `Numeric(15,2)` default 0. **No unique constraints.** No `relationship()` from the upload to the parts.

| Part | Meaning |
|---|---|
| 1 | TDS on salary / dividend / interest, aggregated per deductor (TAN) |
| 2 | TDS with 15G/15H declarations (same shape as Part 1) |
| 3 | TDS u/s 194B / 194R / 194S / 194BA |
| 4 | TDS u/s 194IA / 194IB / 194M / 194S **for the seller** (PAN of deductor, not TAN) |
| 5 | 194S via Form 26QE **for the VDA seller** |
| 6 | TCS aggregated per collector |
| 7 | Tax refunds aggregated per assessment year |
| 8 | 194IA / 194IB / 194M / 194S **for the buyer/tenant** |
| 9 | 194S via 26QE **for the VDA buyer** |
| 10 | TDS/TCS defaults (short payment, 234E, 220(2)) |

View in the product is parsed tables from `GET /get26AS/...`, not the raw `.txt`.

### 6.5 Exemptions (s.54 / s.54F)

Linkage is **soft**: `Excemption.claim_id` is a UUID pointing at `section_54_claim.id` or `section_54f_claim.id` with **no DB FK**. Category strings: `"SECTION_54"` / `"SECTION_54F"`.

`Section54Claim` and `Section54FClaim` have **no client / FY / quarter columns**. Reached only via `Excemption.claim_id` and `DocumentsUpload.link_id`.

`Section54FAssets` (`section_54f_assests` — table name misspelled) FK `section_54f_claim_id` CASCADE (nullable parent).

### 6.6 Documents, comments, supporting

#### `DocumentsUpload` — `documents_upload`

Polymorphic S3 file table. **No FKs.** Both products write.

| Column | Type | Null | Meaning |
|---|---|---|---|
| `category` / `subCategory` | String | NO | e.g. `employer`, `SECTION_54`, `SECTION_54F`, `CAPITAL_GAINS`, `brokerage_account`, `26AS` |
| `link_id` | UUID | NO | **Soft FK** — employer / claim / asset / brokerage-account / client id depending on category |
| `file_key` / `bucket_name` / `file_name` | String | NO | S3 |
| `is_password_protected` | Boolean | default False | |
| `password` | String | YES | Stored when protected |
| `field_name` / `status` | String | YES | |

No `updated_at`.

#### `Comments` — `comments`

Quarter-scoped notes. Native PG enum category: `capital_gains` / `interest_details` / `dividends` / `rental` / `other_income` / `summary` / `pdf_comment`. `created_by` is UUID, **not an FK**.

#### `PriorItrSnapshot` — `advance_tax_prior_itr_snapshots`

Frozen last-year filed ITR amounts for YoY compare. One row per client per **current** FY (`uq_at_prior_itr_snapshot_client_fy`). Written on ITR JSON import into Advance Tax (overwritten on reimport). **Not an FK to `ITRReturn`.** `imported_quarter_id` SET NULL. ~50 Float income/tax/credit/Q1–Q4 columns default 0.

#### `CarryForwardLosses` — `carry_forward_losses`

FY-level B/F ST / LT / housing / OS losses. Multiple loss-year rows per FY allowed. No timestamps.

#### `RuleValidations` — `rule_validations`

Advisor override of `rule_id` for a quarter. `advisor_id` is UUID, **not an FK**. No unique on `(quarter_id, rule_id)`.

#### `cost_inflation_index` — `cost_inflation_indexes`

Global CII (`year` → `cii`). **Not client-scoped.** Orphaned from package `__init__.py`; unused in backends today. No unique on `year`.

---

## 7. Tax Engine / ITR models

Package: `nucleus/models/itr_filling/`. ~132 classes. Every schedule hangs off `ITRReturn` unless noted.

### 7.1 Parent — `ITRReturn` — `itr_returns`

One client / FY / version. Unique `uq_itr_return_client_fy_version` (`client_id`, `financial_year_id`, `version_number`).

| Column | Type | Null | Meaning |
|---|---|---|---|
| `client_id` | UUID, indexed | NO | **No FK** |
| `financial_year_id` | UUID, indexed | NO | **No FK** — same UUID as `financial_years.id` |
| `version_number` | Integer | NO | Default 1 |
| `parent_itr_return_id` | UUID FK SET NULL | YES | Prior version |
| `assessment_year` | String(10) | NO | CBDT AY, e.g. `2025-26` |
| `itr_form_type` | String(10) | YES | Default `ITR-2` |
| `regime` | String(5) | NO | `new` / `old` |
| `filing_status` | String(50) | YES | `not_started` … `filed` |
| `filed_at` | DateTime(tz) | YES | |
| `residential_status` | String(10) | YES | ROR / RNOR / NR |
| `form67_enabled` / `form67_filed` | Boolean | NO | Form 67 / Schedule TR1 |
| `outside_filed` | Boolean | NO | Filed outside the product |
| `outside_filing_comment` | Text | YES | |
| `verifier_name` / `preparer_name` / `reviewer_name` | String(125) | YES | Sign-off |
| `review_not_required` | Boolean | NO | |
| `total_income` / `tax_payable` / `refund_due` | Numeric(18,2) | YES | Computed totals |
| `is_huf` | Boolean | YES | Default False |

1:1 relationships (cascade delete-orphan, `uselist=False`): salary, house_property, bp_schedule, other_sources, deductions, disclosures, cg_schedule, tax_credit_schedule, cfl_schedule, prior_year_income_heads.

Filing jobs, document reviews, activity logs, and Step 2 tables **FK to the return (or to Client+FY) but are not declared as relationships on `ITRReturn`**.

### 7.2 Salary — Schedule S

`ITRSalarySchedule` — unique `itr_return_id`. Totals: gross, exempt u/s 10, deduction u/s 16, net taxable, TDS.

`ITRSalaryEmployer` — Form 16 employer. FKs: schedule CASCADE; `source_employer_id` → `employers.id` SET NULL; `source_document_id` → `itr_documents.id` SET NULL. Identity: name, TAN, address, nature of employment. AIS TAN/TDS. `breakup_reconciliation` JSONB.

Children of employer (CASCADE; source doc SET NULL): `ITRSalaryComponent` (u/s 17(1)), `ITRSalaryAllowance` (`calc_inputs` JSONB, `exempt_regime` old/new/both), `ITRSalaryPerquisite` (u/s 17(2)). `source_type` default `USER`; `is_modified`.

Under the schedule (not per employer): `ITRForeignSalary`, `ITROtherSalary`. No unique on TAN.

### 7.3 House property — Schedule HP

`ITRHPSchedule` — unique `itr_return_id`. Totals: HP income, B/F loss, income under head HP.

`ITRHPProperty` — nature/type of property; `ownership_percent` default 100; ALV, rent, vacancy, taxes, interest, 25A arrears, pre-construction interest + `fy_of_completion`; computed GAV / NAV / 30%.

Children: `ITRHPCoOwner` (PAN uniqueness is **app-layer 409**), `ITRHPLoan` (24(b)), `ITRHPTenant`.

### 7.4 Business / profession — Schedule BP (presumptive)

`ITRBPSchedule` — unique `itr_return_id`. Income % digital (6–100) / other (8–100) / ADA (50–100). 44AD / 44ADA / 44AE turnover and presumptive income with check constraints. Small balance-sheet block.

Children unique on `(bp_schedule_id, line_no)`:

- `ITRBPNatOfBus44AD` / `44ADA` / `44AE` (AE codes checked)
- `ITRBPGoods44AE` — tonnage 0–100, holding 1–12, presumptive ≥ 7500; `OWN` / `LEASE` / `HIRED`
- `ITRBPGstinTurnover` — GSTIN regex, non-negative turnover

### 7.5 Other sources — Schedule OS

`ITROSSchedule` — unique `itr_return_id`. Most children carry `source` = `AIS` | `TIS` | `MANUAL` plus index `(os_schedule_id, source)` so TIS apply can replace auto-imported rows.

| Class | Role |
|---|---|
| `ITROSIncomeLine` + `ITROSIncomeLineDetail` | Fixed OS grid |
| `ITROSInterestDetail` | Bank SB / FD |
| `ITROSItRefundInterest` | Sec 244A |
| `ITROSDividendDetail` | Indian / foreign; FTC; USD trail |
| `ITROSPTIEntity` | Pass-through trust |
| `ITROSBuybackShare` | Buyback lots |
| `ITROSClubbingEntry` | Schedule SPI |
| `ITROSSpecialRate` | NRI special-rate OS (not yet wired to export) |
| `ITROSDtaaIncome` | NR DTAA OS; `is_trc_obtained` default true |
| `ITROSOtherIncome` | `income_type` discriminator |
| `ITRDeemedIncome` | 56(2)(x) / machinery rent. Intended 1:1, **not unique** |
| `ITROSDeductionUs57` | **Unique** — one u/s 57 block per OS schedule |
| `ITRTaxExemptIncome` | Schedule EI. Intended 1:1, **not unique** |

### 7.6 Deductions — Chapter VI-A

`ITRDedSchedule` — unique `itr_return_id`. Capped section totals including `sec_80cch_total` (Agniveer, both regimes).

| Class | Cardinality |
|---|---|
| `ITRDed80C` | 1:N lines |
| `ITRDed_80C_80CCD` | Intended 1:1, **no unique** (80CCC, 80CCD(1)/(1B)/(2), PRAN) |
| `ITRDed80DDetail` | 1:N SELF_FAMILY / PARENTS × SENIOR / OTHERS |
| `ITRDed80DMeta` | **Unique** schedule FK — senior flags, lump-sum premium |
| `ITRDed80DPolicy` | 1:N policies |
| `ITRDed80GDonation` | 1:N; donee, PAN, cash flag, ARN |
| `ITRDed80DD` / `ITRDed80U` | **Unique** — one dependent / self disability per return (Form 10IA, UDID) |
| `ITRDed80DDB` | Unique `(ded_schedule_id, type)` Senior Citizens / Others |
| `ITRDedLoan` / `ITRDed80ELoan` / `ITRDed80EEALoan` / `ITRDed80EEBLoan` | 1:N housing / education / affordable housing / EV |
| `ITRDedOtherLine` | Unique `(schedule, section)` — seeded 80GG / 80QQB / 80RRB / 80TTA / 80TTB |
| `ITRDed80GGAEntry` / `ITRDed80GGCEntry` | Research / political donations |

### 7.7 Tax credits — Schedules IT / TDS1–3 / TCS / TR1 / FSI

`ITRTaxCreditSchedule` — **filing source of truth**. ORM `uselist=False` but **no unique on `itr_return_id`**. Snapshots: `ais_json_snapshot` JSONB, `form_26as_text`.

| Class | Schedule | Notes |
|---|---|---|
| `ITRAdvanceTaxPayment` | IT | BSR (7), challan (5), date, amount, `source` |
| `ITRTDSSalary` | TDS1 | Optional `salary_employer_id` SET NULL. Deducted vs claimed; `is_edited` |
| `ITRTDSNonSalary` | TDS2 | TAN / section / head of income; 26AS vs offered; balance CF |
| `ITRTDSProperty` | TDS3 194IA | PAN not TAN. `is_property_purchase`: buyer 194IA is **informational only** |
| `ITRTCSEntry` | TCS | Collected vs claimed; `balance_tcs_cf` |
| `ITRForm67Entry` | TR1 FTC | Country, DTAA article; USD trail. Soft `source_type` / `source_row_id`: `OS_FOREIGN_DIVIDEND` \| `CG_US_BROKER` \| `HP_PROPERTY` |
| `ITRForm67Refund` | | Prior-year tax refunded |
| `ReliefClaimed` | | Relief already claimed in earlier AYs |
| `ITRFSIEntry` | FSI | `source` default `FORM67` (auto-sync) vs `MANUAL` (survives Form 67 replace) |

TAN/section matching is in services, not DB uniques.

### 7.8 Capital gains — Schedule CG

`ITRCGSchedule` — indexed `itr_return_id`, **not unique**. STCG/LTCG buckets; HP / exempt / BF / VDA totals; `quarterly_breakdown` JSONB (234C); F&O flags.

Trade trees match the AT replica, plus bonds / other assets / DTAA CG that AT does not replicate.

**Document FK difference:** CG trade `source_document_id` is `ON DELETE CASCADE` (deleting the PDF deletes the trade). Salary / HP source docs use `SET NULL`. Broker-level `source_document_id` is indexed UUID, **not an FK**.

HP CG subtree: `ITRCGHPEntry` (optional `hp_schedule_property_id` SET NULL) → acquisition details, improvements, transfer expenses, buyers.

Exemptions: `ITRCGExemption54` / `ITRCGExemption54F` hang off the CG schedule (structured, unlike AT’s soft-linked claims). 54F `claim_group_id` and `india_eq_transaction_id` are soft UUIDs; `india_eq_txn_snapshot` JSONB.

### 7.9 Disclosures — AL / Part A / FA

`ITRDisclosuresSchedule` — unique `itr_return_id`. Flags: `is_directorship`, `is_unlisted_shares`, `is_foreign_assets`.

This is the **filing copy**. Collector `foreign_*` tables are the **source**; Tax Engine copies via `cp_fa_to_itr`.

| Class | Purpose |
|---|---|
| `ITRALMovableAsset` / `ITRALInvestment` / `ITRALImmovableProperty` | Schedule AL |
| `ITRDiscDirectorship` / `ITRDiscUnlistedShare` | Part A (`disclosures_schedule_id` nullable on unlisted) |
| `ITRFABankAccount` | FA A1/A2 |
| `ITRFAEquityDebt` | FA A3 |
| `ITRFACashValueInsurance` | FA A4 |
| `ITRFAImmovableProperty` | FA B1 |
| `ITRFAFinancialInterest` | FA B2 |
| `ITRFASigningAuthority` | FA C |
| `ITRFAOtherAsset` | FA D |
| `ITRFAForeignTrust` | FA E |
| `ITRFAOtherForeignIncome` | FA F |

No unique on FA account numbers.

### 7.10 CFL

`ITRCFLSchedule` — unique `itr_return_id`.

- `ITRCFLYearEntry` — unique `(cfl_schedule_id, years_back)` for lookback 1–8. Heads: HP, STCG, LTCG, OS race-horse.
- `ITRCFLSummary` — unique `(cfl_schedule_id, summary_type)`: `total_bf_earlier`, `adj_bfla`, `current_ay`, `total_cf`.

### 7.11 AIS / TIS / 26AS — three layers

These are **not interchangeable**.

| Layer | Models | Owned by | Role |
|---|---|---|---|
| Archive (raw file) | `ITRAisJsonArchive`, `ITRTisPdfArchive`, `ITRForm26asArchive` | Client; optional ITR `ON DELETE SET NULL` | S3 metadata. Encrypted originals stay as uploaded. Decrypt on import and on view with `PAN(lowercase) + DOB(ddmmyyyy)`. Not filing JSON. App keeps max 2 TIS/26AS archives per return. |
| Imported working copy | `ITRAis26asUpload` → `ITRAisEntry` / `ITR26asEntry` / `ITRAisSftTransaction`; `ITRAis26asReconciliation`; `ITRTisSummaryCategory` | ITRReturn CASCADE (TIS category ↔ PDF archive is SET NULL) | Parsed rows used to prefill and reconcile. OS children tagged `AIS` \| `TIS` \| `MANUAL`. |
| Filing source of truth | `ITRTaxCreditSchedule` + TDS/TCS/advance-tax/Form 67/FSI | ITRReturn (ORM 1:1) | What goes into Schedules IT, TDS1/2/3, TCS, TR1, FSI. Rows may keep `source` + `is_edited`. |

Flow: upload archive → parse into import tables → reconcile AIS vs 26AS vs claimed credit → copy/claim into **tax credit schedule** (and OS/salary income lines). Archives survive return unlink; import rows die with the return.

`ITRForm26asArchive.financial_year` is a **String(16) label** (`"25-26"`), not an FK.

`ITRTisSummaryCategory` unique `(tis_pdf_archive_id, sr_no)`: `processed_total` vs `accepted_total`.

Advance Tax 26AS is a **different store**: `.txt` only, one upload per quarter, parsed into FY-level parts. No AIS or TIS models in Advance Tax.

### 7.12 Documents

`ITRDocumentSlot` — Client+FY inbox. Unique `uq_itr_doc_slot` (`financial_year_id`, `client_id`, `doc_type`, `sub_type`, `source`, `region`, `notes`) `NULLS NOT DISTINCT`. Custom broker slots distinguished by `notes`. `noted_by_id` → `advisors.id` (no ondelete).

`ITRDocument` — S3 + password flag/value + `status` + `advisor_comment`. `updated_by` default `client`.

`ITRDocumentReview` — PK = `document_id`. Also `itr_return_id` CASCADE. One review row per document.

`ITRDocumentProcessingLog` — LLM/parse attempts. Defined in models; not in package `__all__`.

### 7.13 Address and refund bank

`ITRAddress` — CBDT Part A address (separate from profiling `addresses`). Unique `(itr_return_id, address_type)` — at most one Primary and one Secondary.

`ITRRefundBankAccount` — `use_for_refund`; foreign: SWIFT / IBAN / `country_code`. No unique (multiple accounts; one should be refund).

### 7.14 Step 2 wizard (Client + FY, not `ITRReturn`)

Intake Q&A. All parent rows FK `client_id` CASCADE and `financial_year_id` CASCADE.

| Class | Unique rule |
|---|---|
| `ITRStep2Salary` | None (multiple employers). Form 16 checklist flags |
| `ITRStep2SalaryTrigger` | `(client_id, financial_year_id, trigger_id)`. Optional `slot_id` SET NULL |
| `ITRStep2SalaryDeductionDetail` | `(client_id, financial_year_id, deduction_id)` |
| `ITRStep2SalaryDeductions` | Booleans: health, donations, education, NPS, other 80C. No unique |
| `ITRStep2OtherInfo` | `(client, FY, section, qcode)`. Child `ITRStep2OtherInfoData` JSONB |
| `ITRStep2Residency` | **One per client+FY.** `computed_status` ROR/RNOR/NR + `override_status` |
| `ITRStep2Citizenship` | **One per client+FY.** Citizenships JSON; `us_visa_primary_client_id` SET NULL |

### 7.15 Filed-year snapshot, prior-year heads, summary

`ITRPriorYearIncomeHeads` — unique on `itr_return_id`. YoY chart + F&O / CF flags for the **current** return.

`ITRFiledYearSummary` — admin dashboard snapshot of a **previously filed** JSON (not live `ITRReturn`). Unique `(client_id, assessment year)`. `financial_year_id` SET NULL. Child `ITRFiledYearSchedule` unique `(summary_id, schedule_code)` with JSONB payload.

`ITRSummaryVerification` — unique `(itr_return_id, code, subject_key)`. Advisor confirmation that unblocks Client Summary download. `confirmed_by_advisor_id` has **no FK**.

`ITRClientCommentRead` — unique `(reader_id, source, source_id, field)`. Virtual refs; no FK to comment sources.

`ITRClientSummaryDownloadLog` — append-only PDF downloads. Downloader UUID/name **no FK**.

### 7.16 Audit and filing jobs

`ITRAuthAuditEvent` — append-only auth events. `login_id` SET NULL. Not ITR-scoped.

`ITRActivityLog` — append-only business actions. Optional `itr_return_id` / `client_id` / `actor_login_id` SET NULL.

`ITRFieldChangeSnapshot` — unique `(entity_table, entity_id, field_path)` — one current snapshot per field.

Jobs (FK `itr_return_id` CASCADE; **no ORM relationship on `ITRReturn`**):

- `ITRFilingValidationJob` — internal CBDT schema validation (SQS)
- `ITRFilingExportJob` — async filing JSON export
- `ITRUtilityValidationRequest` — CBDT desktop utility via UiPath. Partial unique: at most one in-flight (`queued` / `processing`) per return. `client_id` / `financial_year_id` UUIDs **with no FK**

### 7.17 Reference — AMFI

`AmfiMasterMeta` / `AmfiMfIsin` — NAVAll master. `isin` is the PK of `amfi_mf_isin`. Tax Engine CG ingest uses this to classify equity / ETF / MF. Not per-client. Advance Tax does not import AMFI.

---

## 8. Cardinality cheatsheet

### Advance Tax — intended one-row rules

| Rule | Enforced |
|---|---|
| One FY per `(client_id, financial_year)` | App only |
| Four quarters, unique `(financial_year_id, quarter_number)` | App only |
| One TaxProfile per client+FY | App upsert |
| One Interest / Dividend / OtherIncome / Deductions per client+quarter | App get-or-create |
| One ATCGSchedule per quarter | **DB** unique `quarter_id` |
| One 26AS upload per quarter | **DB** unique |
| One PriorItrSnapshot per client+FY | **DB** unique |
| One CG document slot per identity | **DB** unique `NULLS NOT DISTINCT` |
| One TAN per quarter (when TAN present) | **DB** partial unique |

Multiple `CapitalGains` rows per quarter (by `category`) and multiple `Rental` rows (by property) are by design.

### Tax Engine — intended one-row rules

| Rule | Enforced |
|---|---|
| One ITR version per client+FY+version | **DB** unique |
| One salary / HP / BP / OS / deductions / disclosures / CFL / prior-year-heads | **DB** unique `itr_return_id` |
| One CG schedule / tax-credit schedule | **ORM only** — no unique |
| One Primary + one Secondary address | **DB** unique `(return, type)` |
| One 80DD / 80U / 80D meta / u/s 57 | **DB** unique |
| One 80DDB row per Senior/Others | **DB** unique |
| One Step 2 residency + citizenship per client+FY | **DB** unique |
| One in-flight utility validation | **DB** partial unique |
| One document slot per identity | **DB** unique `NULLS NOT DISTINCT` |
| One filed-year snapshot per client per AY | **DB** unique |

**Not uniquely constrained vs ORM intent:** `itr_cg_schedule.itr_return_id`, `itr_tax_credit_schedule.itr_return_id`, `itr_deemed_income.os_schedule_id`, `itr_tax_exempt_income.os_schedule_id`, `itr_ded_80c_80ccd.ded_schedule_id`.

---

## 9. Soft / missing FKs

| Column | Intended target | Notes |
|---|---|---|
| `ITRReturn.client_id` / `financial_year_id` | `clients.id` / `financial_years.id` | Application-level only |
| `Excemption.claim_id` | `section_54_claim.id` or `section_54f_claim.id` | UUID only |
| `DocumentsUpload.link_id` | Polymorphic | UUID only |
| `Client.parent_id` | Another client | Household grouping, not an FK |
| `Comments.created_by` | login / advisor | UUID only |
| `RuleValidations.advisor_id` | `advisors.id` | UUID only |
| `Rental.property_group_id` | Grouping key | UUID, not a table |
| Broker-level CG `source_document_id` (AT and ITR) | document id | Indexed UUID, **no ForeignKey** (txn-level `source_document_id` **is** an FK) |
| `ITRCGExemption54F.claim_group_id` / `india_eq_transaction_id` | grouping / txn | Soft UUIDs |
| `ITRForm67Entry.source_row_id` | OS / CG / HP row | Soft pointer + `source_type` |
| `ITRSummaryVerification.confirmed_by_advisor_id` | advisor | No FK |
| `ITRUtilityValidationRequest.client_id` / `financial_year_id` | client / FY | UUIDs, no FK |

---

## 10. Integrity gaps

1. **`ITRReturn.client_id` / `financial_year_id` are not FKs** — orphan ITR rows possible; FY delete does not cascade to ITR.
2. **No unique on `financial_years (client_id, financial_year)` or `tax_profile (client_id, financial_year_id)`** — duplicates prevented in services, not in the schema.
3. **FY-scoped FA tables have no `client_id` and no uniqueness** — client is only via FY; duplicate FA rows are allowed.
4. **CG / tax-credit schedules lack unique(`itr_return_id`)** — ORM `uselist=False` assumes 1:1; a second row would break that.
5. **`logins.email` is not unique.**
6. **Mixed amount types** — AT income heads often `Float`; salary/CG/54 and ITR use `Numeric`.
7. **`DocumentsUpload` and 54/54F claims are not constrained to a parent table** — `category` / `claim_id` decide the target.

---

## 11. Write vs read cheat-sheet

| Table group | Advance Tax | Tax Engine |
|---|---|---|
| `clients`, `logins`, mappings, OTP, trusted devices | read (auth) | write + read (identity) |
| `personal_information`, `addresses` | unused | write + read (HUF/karta; primary address upsert). Filing prefers `itr_addresses` for Part A |
| `employment`, `residencies`, `citizenships`, `insurances`, `loans`, `real_estate` | unused | unused (ITR has Step 2 / schedules) |
| Foreign\* FA (except 3 FBAR tables) | unused | write collector; read → copy into ITR Schedule FA |
| jointly/separately owned, `foreign_deposit_custodial_accounts` | unused | unused |
| `financial_years` | write + read | read (and lookup/create as needed) |
| `tax_profile` | write + read | unused |
| `itr_returns` and schedules | unused | write + read |
| `advance_tax_prior_itr_snapshots` | write + read (ITR JSON import) | unused |
| `document_collector_info`, `sub_type_comments` | unused | write + read |
| `documents_upload` | write + read | write + read (FA attachments) |
| ITR vs AT CG document slots | AT CG replica | ITR replica |
| `form26_as_log_models` | unused | unused |
| `amfi_mf_isin` | unused | write (ingest) + read (CG ISIN classify) |

---

## 12. Out of this catalog

These live in the same nucleus package but are **not** part of the Advance Tax or ITR filing graphs:

- TSM — tasks, chat, timers, notifications
- Portal automation — notice watchlist, batches, jobs
- Account aggregator — Finvu/Finsense consents, holdings, transactions
- US tax filing — questionnaire, submissions, `ClientPriorReturn` (email + tax year, no `client_id` FK)

Alembic autogenerate only sees models imported from `nucleus/models/__init__.py` (directly or via subpackage `__init__.py`). New tables must be registered there. See `PROJECT_CONTEXT.md`.

---

## 13. Class index

### Shared / bridge

| Class | Table |
|---|---|
| Client | clients |
| ClientPhoneMapping | client_phone_mappings |
| ClientEmailMapping | client_email_mappings |
| Advisor | advisors |
| Login | logins |
| LoginEvent | login_events |
| TrustedDevice | trusted_devices |
| WebAuthnCredential | webauthn_credentials |
| OtpVerification | otp_verifications |
| CSADocument / CSAParty / CSAFee / CSAService / CSAParseWarning | csa_* |
| DocumentCollectorInfo | document_collector_info |
| SubTypeComments | sub_type_comments |
| FinancialYear | financial_years |
| PersonalInformation | personal_information |
| Address | addresses |
| DocumentsUpload | documents_upload |
| CountryLookup | country_lookup |
| AmfiMasterMeta / AmfiMfIsin | amfi_master_meta / amfi_mf_isin |

### Advance Tax

| Class | Table |
|---|---|
| Quarter | quarters |
| TaxProfile | tax_profile |
| Employer | employers |
| InterestDetails / InterestAccounts | interest_details / interest_accounts |
| Dividends / DividendAccounts | dividends / dividend_accounts |
| Rental / RentalCoOwner | rentals / rental_co_owners |
| OtherIncome / OtherIncomeAccounts | other_income / other_income_accounts |
| Deductions | deductions |
| CapitalGains / BrokerageAccounts | capital_gains / brokerage_accounts |
| ATCGSchedule + brokers/txns | at_cg_* |
| ATCGDocumentSlot / ATCGDocument / ATCGDocumentProcessingLog | at_cg_document_* |
| AdvanceTax26asUpload | advance_tax_26as_uploads |
| Form26ASPart1–10 | form_26as_part1 … part10 |
| Excemption / Section54Claim / Section54FClaim / Section54FAssets | excemptions / section_54_claim / section_54f_claim / section_54f_assests |
| Comments | comments |
| PriorItrSnapshot | advance_tax_prior_itr_snapshots |
| CarryForwardLosses | carry_forward_losses |
| RuleValidations | rule_validations |

### Tax Engine

Headers: `ITRReturn`, `ITRSalarySchedule`, `ITRHPSchedule`, `ITRBPSchedule`, `ITROSSchedule`, `ITRDedSchedule`, `ITRTaxCreditSchedule`, `ITRCGSchedule`, `ITRDisclosuresSchedule`, `ITRCFLSchedule`.

Archives / import: `ITRAisJsonArchive`, `ITRTisPdfArchive`, `ITRForm26asArchive`, `ITRAis26asUpload`, `ITRAisEntry`, `ITR26asEntry`, `ITRAisSftTransaction`, `ITRAis26asReconciliation`, `ITRTisSummaryCategory`.

Documents / ops: `ITRDocumentSlot`, `ITRDocument`, `ITRDocumentReview`, `ITRAddress`, `ITRRefundBankAccount`, `ITRStep2*`, `ITRFiledYearSummary`, filing jobs, activity logs.

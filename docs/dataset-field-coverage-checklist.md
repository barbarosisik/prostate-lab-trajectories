# Dataset Field-Coverage Checklist

**Current use, 2026-09-06:** retain this field-level checklist as the test specification. The completed DREAM audit supersedes historical unknowns. D-024 permits visit-anchored analyses; actual pre-dose timing remains unavailable. Candidate 0-7-day pre-dose windows below apply only to a source with verified administration dates, not an assumed DREAM schedule. A0R is complete. Stage 01 is explicitly authorized; later preparation and modeling remain scoped separately.

## Purpose

This is the column-level audit specification for the fixed research question. It translates the literature evidence into fields that must be found, typed, joined and quality-checked before a cleaning specification or analysis pipeline is written.

This checklist is deliberately broader than the 13 laboratory tests used in earlier DREAM baseline models. Every source column and every distinct laboratory test will be inventoried before repeated-measure eligibility is decided.

## Evidence and status codes

| Code | Meaning |
|---|---|
| `REQ` | Required by the fixed research question or project protocol. |
| `PUB` | Confirmed in public official PDS/Synapse documentation, but not yet checked in the gated dictionary/source file. |
| `LIT` | Supported by the curated literature catalog. |
| `SRC` | Must be confirmed from the actual data dictionary and source files. |

The PDS-specific public evidence is recorded in [`pds-dream-access-audit.md`](source-coverage-matrix.md). A field is not considered source-verified until its actual column name, type, values, missingness and join behavior have been inspected.

## A. Source provenance, identifiers and joins

| ID | Required field or property | Expected grain | Audit checks | Evidence |
|---|---|---|---|---|
| ID-01 | Deidentified patient identifier | Patient | Exact column name; type; uniqueness within trial; stability across all tables; no direct identifiers | REQ, SRC |
| ID-02 | Trial/study identifier | Patient and event | Exact codes and labels; map `ASCENT2`, `CELGENE`/MAINSAIL, `EFC6546`/VENICE and `AZ`/ENTHUSE-33 without losing original values | REQ, PUB, SRC |
| ID-03 | Data-provider identifier | Patient and event | Determine whether provider is separate from study; preserve original value | REQ, LIT-005, SRC |
| ID-04 | Site/country identifier | Patient or site | Availability, deidentification, cross-trial comparability, sparse-category risk | REQ, SRC |
| ID-05 | Event/row identifier | Event | Determine whether supplied or must be generated; test uniqueness and exact duplicates | REQ, LIT-008, SRC |
| ID-06 | Source table and source filename | Event | Attach during ingestion; retain release, version and checksum | REQ |
| ID-07 | Source row number | Event | Generate on read so every transformation is traceable to the immutable source row | REQ |
| ID-08 | Join key from every event table to patient | Event | Candidate `STUDYID` plus patient ID must be verified; measure unmatched and many-to-many joins | REQ, PUB, SRC |
| ID-09 | Join key from laboratory event to treatment cycle | Lab event | Direct key, administration ID, date-time rule or visit label; quantify ambiguous and unmatched events | REQ, SRC |
| ID-10 | Reference-date definition | Patient/trial/table | First dose, randomization, consent or screening; document exceptions and table-specific definitions | PUB, SRC |
| ID-11 | Data-cut/release version | Source | File modification date, version, dictionary version, PDS/Synapse IDs and acquisition date | REQ |

## B. Discovery-population eligibility and baseline context

| ID | Required field or property | Expected grain | Audit checks | Evidence |
|---|---|---|---|---|
| POP-01 | Prostate-cancer diagnosis | Patient | Diagnosis coding and histology where available | REQ, SRC |
| POP-02 | Metastatic status | Patient/time | Confirm stage IV/metastatic disease at chemotherapy start | REQ, LIT-001 to LIT-007, SRC |
| POP-03 | Castration-resistant state | Patient/time | Confirm mCRPC at first docetaxel; preserve source definition | REQ, PUB, SRC |
| POP-04 | Chemotherapy-naive status | Patient | Confirm no prior cytotoxic chemotherapy before trial treatment | REQ, LIT-005, LIT-006, SRC |
| POP-05 | Age at baseline | Patient | Numeric age, grouping, top-coding and implausible values | REQ, LIT-005 to LIT-007, SRC |
| POP-06 | Performance status | Patient/time | ECOG value and date; baseline rule; retain scale and unknown | REQ, LIT-002, LIT-005 to LIT-007, SRC |
| POP-07 | Metastatic sites | Patient/time | Bone, liver, lung, lymph node, other visceral and number of sites; source-specific coding | REQ, LIT-007, LIT-010, SRC |
| POP-08 | Disease burden | Patient/time | Target/non-target lesions, lesion count and measurements; do not substitute a summary for event data silently | REQ, LIT-005, LIT-007, SRC |
| POP-09 | Gleason score and stage | Patient | Diagnosis and baseline values; missing-by-trial pattern | LIT-008, PUB, SRC |
| POP-10 | Pain and opioid/analgesic use | Patient/time | Original medication evidence, summary flags and baseline timing | LIT-007, LIT-010, LIT-018, SRC |
| POP-11 | Relevant comorbidities | Patient | Original and standardized terms; body-system hierarchy; baseline-only status | REQ, PUB, SRC |
| POP-12 | Prior cancer treatments | Patient/event | Drug, surgery, radiotherapy, dates and intent; distinguish cancer treatment from other medication | REQ, LIT-002, LIT-003, SRC |
| POP-13 | Concurrent cancer/supportive treatments | Patient/event | Prednisone, growth factors, transfusion and other agents; start/end timing | REQ, LIT-019 to LIT-022, SRC |
| POP-14 | Trial arm and randomized treatment | Patient | Comparator/experimental arm, placebo and co-agent; retain source arm exactly | REQ, LIT-020 to LIT-022, SRC |

## C. Chemotherapy administration and cycle timing

These fields decide whether a laboratory event can be aligned to the **next actual chemotherapy administration**. A nominal schedule or visit label is not an adequate substitute when delays, missed cycles or dose changes are outcomes.

| ID | Required field or property | Expected grain | Audit checks | Evidence |
|---|---|---|---|---|
| CHEMO-01 | Chemotherapy administration identifier | Administration | Unique within patient; joins to regimen and cycle | REQ, SRC |
| CHEMO-02 | Actual administration date/time | Administration | Exact date or study day; time zone/time precision; repeated same-day administrations | REQ, SRC |
| CHEMO-03 | Planned administration date | Administration | Needed to define delays and missed cycles; distinguish rescheduling from missing data | REQ, SRC |
| CHEMO-04 | Cycle number | Administration | Original cycle/visit value; numeric standardized cycle; weekly versus three-weekly schedule | REQ, LIT-020 to LIT-022, SRC |
| CHEMO-05 | Day within cycle | Administration | Day number, visit label and unscheduled status | REQ, SRC |
| CHEMO-06 | Regimen and agent | Administration | Docetaxel and co-agents; original and standardized drug names | REQ, PUB, SRC |
| CHEMO-07 | Actual dose and unit | Administration | Total dose, dose per square metre, infusion status and unit | REQ, SRC |
| CHEMO-08 | Planned dose | Administration | Supports relative dose intensity and reduction detection | REQ, SRC |
| CHEMO-09 | Dose reduction flag/reason | Administration | Date/cycle of first reduction; toxicity versus other reason | REQ, SRC |
| CHEMO-10 | Dose held/missed flag/reason | Administration | Distinguish true omission, delay and absent record | REQ, SRC |
| CHEMO-11 | Cycle delay duration/reason | Administration | Planned-to-actual difference; source reason coding | REQ, SRC |
| CHEMO-12 | Treatment start/end day | Patient/treatment | Actual first dose and last dose; verify PDS `ENTRT_PC` semantics | PUB, LIT-006, SRC |
| CHEMO-13 | Discontinuation date and reason | Patient/treatment | Adverse event, possible adverse event, progression, death, withdrawal and other categories | REQ, PUB, LIT-006, SRC |
| CHEMO-14 | Relative dose intensity/cumulative exposure inputs | Patient/cycle | Derive only when planned and actual dose/timing are both available | REQ, SRC |

## D. Laboratory event fields

Every distinct laboratory name is in scope. The named tests below are literature precedents and audit anchors, not an inclusion whitelist.

| ID | Required field or property | Expected grain | Audit checks | Evidence |
|---|---|---|---|---|
| LAB-01 | Original laboratory test name | Lab event | Preserve verbatim text; enumerate every distinct value by trial | REQ, LIT-008, SRC |
| LAB-02 | Standardized laboratory test name/code | Lab event | Preserve supplied code; build mapping only after value/unit review | REQ, SRC |
| LAB-03 | Laboratory category/panel | Lab event | Hematology, chemistry, urinary or other; do not exclude a category before counts | REQ, PUB, SRC |
| LAB-04 | Specimen type | Lab event | Serum/plasma/whole blood/urine and unknown; prevent invalid pooling | REQ, SRC |
| LAB-05 | Collection date/time or relative study day | Lab event | Exact source field and precision; verify PDS `LBDT_PC`; compare with visit and baseline flag | REQ, PUB, SRC |
| LAB-06 | Visit/cycle label | Lab event | Original label; scheduled versus unscheduled; consistency with collection day | REQ, PUB, SRC |
| LAB-07 | Baseline flag | Lab event | Verify PDS `LBBLFL`; independently test against date and first dose; retain contradictions | PUB, SRC |
| LAB-08 | Original result | Lab event | Preserve character representation including qualifiers and detection-limit strings | REQ, PUB, LIT-008, SRC |
| LAB-09 | Original unit | Lab event | Enumerate by test/trial/site; never infer silently | REQ, SRC |
| LAB-10 | Standardized character result | Lab event | Verify PDS `LBSTRESC`; preserve nonnumeric text and qualifiers | PUB, LIT-008, SRC |
| LAB-11 | Standardized numeric result | Lab event | Exact column, parsing rule and mismatch with character result | REQ, SRC |
| LAB-12 | Standardized unit | Lab event | Verify supplied conversions before cross-trial use | REQ, SRC |
| LAB-13 | Completion/status field | Lab event | Verify PDS `LBSTAT`; retain `NOT DONE` as missing-test information, never zero | REQ, LIT-008, SRC |
| LAB-14 | Lower reference limit | Lab event | Numeric value, unit and availability by trial/site/date | REQ, LIT-008, SRC |
| LAB-15 | Upper reference limit | Lab event | Numeric value, unit and availability by trial/site/date | REQ, LIT-008, SRC |
| LAB-16 | Reference-range indicator | Lab event | Verify PDS `LBNRIND`; compare with limits/result and record disagreements | PUB, SRC |
| LAB-17 | Result qualifier | Lab event | `<`, `>`, below/above detection, trace, negative, not calculable and other strings | REQ, SRC |
| LAB-18 | Result status/finality | Lab event | Preliminary, corrected, final or unknown | REQ, SRC |
| LAB-19 | Same-day sequence/time | Lab event | Needed to resolve multiple eligible results without averaging blindly | REQ, SRC |
| LAB-20 | Duplicate signature | Lab event | Count exact and near duplicates using patient/test/day/value/unit/status/visit | REQ, LIT-008, SRC |
| LAB-21 | Days before next actual dose | Derived lab-cycle | Compute only after actual administration linkage; initial eligibility 0–7 days | REQ |
| LAB-22 | Eligible pre-cycle flag/window | Derived lab-cycle | Primary 0–7 days; sensitivities 0–3 and 0–14; no post-dose leakage | REQ |
| LAB-23 | Chosen pre-cycle result rank | Derived lab-cycle | Closest eligible pre-dose result with documented tie-break | REQ |

### Laboratory audit anchors from prior work

The source inventory must include these expected tests and aliases while still enumerating **all** others:

- PSA, alkaline phosphatase, hemoglobin, LDH, albumin, AST and ALT.
- White blood cells, neutrophils, lymphocytes, red blood cells and platelets.
- Calcium, creatinine/creatinine clearance, magnesium, phosphorus, total protein, total bilirubin and testosterone.
- Any additional chemistry, hematology or urinary tests present in `LabValue`.
- Derived NLR and platelet-to-lymphocyte ratio only when the component tests are compatible and temporally aligned.

The 13 previously selected DREAM tests, ALT, AST, ALP, LDH, magnesium, phosphorus, albumin, total protein, PSA, hemoglobin, WBC, neutrophils and lymphocytes, are comparison anchors from LIT-008, not the project feature set.

## E. Laboratory repetition and timing feasibility

For every original test name × trial combination, calculate the following before exclusion:

| ID | Required count or diagnostic | Unit of report | Decision supported |
|---|---|---|---|
| REP-01 | Total source rows | Test × trial | Raw prevalence |
| REP-02 | Distinct patients tested | Test × trial | Coverage |
| REP-03 | Rows per patient: min, median, quartiles, max | Test × trial | Repetition depth |
| REP-04 | Patients with at least 2, 3 and 4 observations | Test × trial | Slope/curvature feasibility |
| REP-05 | Distinct collection days per patient | Test × trial | Detect same-day repeats |
| REP-06 | Baseline, post-baseline and unknown-timing rows | Test × trial | Temporal usability |
| REP-07 | Observations by cycle/visit | Test × trial × cycle | Landmark coverage |
| REP-08 | Eligible observations in 0–3, 0–7 and 0–14 day pre-dose windows | Test × trial × cycle | Pre-cycle snapshot feasibility |
| REP-09 | Patients with eligible results before cycles 1–4 | Test × trial × cycle | Early landmark cohort size |
| REP-10 | Missing scheduled tests by cycle | Test × trial × cycle | Informative missingness |
| REP-11 | Unit distribution and cross-unit overlaps | Test × trial | Harmonization feasibility |
| REP-12 | Reference-range availability and contradictions | Test × trial | Normalized-position feasibility |
| REP-13 | Exact and near duplicates | Test × trial | De-duplication rules |
| REP-14 | `NOT DONE`, nonnumeric and detection-limit strings | Test × trial | Parsing and missingness rules |
| REP-15 | Time from collection to next actual dose | Test × trial × cycle | Critical alignment feasibility |

Minimum observations are feature-specific: two for a slope; three for acceleration/curvature or useful volatility. Minimum patient counts for inferential modeling remain unset until these distributions are visible.

## F. Survival outcomes

| ID | Required field or property | Expected grain | Audit checks | Evidence |
|---|---|---|---|---|
| OS-01 | Death indicator | Patient | Source values and missing meaning; verify PDS `DEATH` | REQ, PUB, LIT-005, SRC |
| OS-02 | Death date or relative death day | Patient | Exact day/date where released; privacy transformation; event ordering | REQ, SRC |
| OS-03 | Last-known-alive/censoring day | Patient | Verify PDS `LKADT_P`; source reference date and administrative censoring | REQ, PUB, LIT-005, SRC |
| OS-04 | Survival duration | Patient | Independently reproduce from dates where possible | REQ, SRC |
| OS-05 | Censoring reason | Patient | Administrative, lost follow-up, withdrawal or unknown | REQ, SRC |
| OS-06 | Outcome visibility by release/trial | Trial/release | Training versus leaderboard/final-scoring withholding, especially ENTHUSE-33 | REQ, PUB, LIT-005, SRC |

## G. Progression and response outcomes

These outcome families must remain separate. A generic PFS field is not accepted without its event definition.

| ID | Required field or property | Expected grain | Audit checks | Evidence |
|---|---|---|---|---|
| PROG-01 | Radiographic assessment date/day | Assessment | Reference date, imaging modality and scheduled/unscheduled status | REQ, LIT-002, LIT-003, SRC |
| PROG-02 | Radiographic progression flag/date | Patient/assessment | Source criteria, confirmation and censoring | REQ, LIT-002, LIT-003, SRC |
| PROG-03 | Clinical progression flag/date | Patient/event | Reason components and relation to treatment stop | REQ, LIT-001 to LIT-003, SRC |
| PROG-04 | PSA progression flag/date | Patient/lab | Source rule, confirmation, nadir and early-rise handling | REQ, LIT-001 to LIT-003, SRC |
| PROG-05 | Composite progression/PFS | Patient | Decompose components before any cross-source use | REQ, SRC |
| RESP-01 | PSA response flag and assessment window | Patient/landmark | Continuous percentage change and published thresholds around 3 months | REQ, LIT-011, SRC |
| RESP-02 | Imaging response category | Assessment | CR/PR/SD/PD/NE and criteria version | REQ, LIT-002, LIT-003, SRC |
| RESP-03 | Target-lesion measurement | Lesion event | Original/standard result and unit; verify PDS lesion fields | PUB, SRC |
| RESP-04 | Non-target/new-lesion status | Lesion event | Source coding and assessment day | REQ, PUB, SRC |
| RESP-05 | Response confirmation date | Assessment | Confirmation requirement and interval | REQ, LIT-002, LIT-003, SRC |

## H. Treatment-tolerance outcomes

The DREAM early-discontinuation flag is retained as one outcome. It does not replace the other tolerance definitions.

| ID | Required field or property | Expected grain | Audit checks | Evidence |
|---|---|---|---|---|
| TOL-01 | AE-related early-discontinuation flag | Patient | Verify PDS `DISCONT`; exact cutoff recorded as source-defined | REQ, PUB, LIT-006, SRC |
| TOL-02 | Treatment end day | Patient | Verify PDS `ENTRT_PC`; distinguish end from last administration | PUB, LIT-006, SRC |
| TOL-03 | Broad discontinuation-reason category | Patient | Verify PDS `ENDTRS_C`; preserve original reason if available | PUB, LIT-006, SRC |
| TOL-04 | Adverse-event identifier | AE event | Patient join, event date, onset/end, seriousness and relatedness | REQ, SRC |
| TOL-05 | AE term and standardized code | AE event | Verbatim, coded term, system-organ class and dictionary version | REQ, SRC |
| TOL-06 | AE severity/grade | AE event | CTCAE version, maximum grade and missing meaning | REQ, SRC |
| TOL-07 | Severe-toxicity outcome | Patient/cycle | Prespecified grade threshold and competing events | REQ, SRC |
| TOL-08 | Dose-reduction outcome | Patient/cycle | First cycle/date, amount and reason | REQ, SRC |
| TOL-09 | Delayed-cycle outcome | Patient/cycle | Planned-versus-actual delay and reason | REQ, SRC |
| TOL-10 | Missed-cycle outcome | Patient/cycle | Expected cycle definition and censoring by progression/death | REQ, SRC |
| TOL-11 | Inability-to-continue outcome | Patient/cycle | Operational rule separating toxicity, progression, choice and death | REQ, SRC |
| TOL-12 | Supportive intervention | Event | Growth factor, transfusion, hospitalization or other rescue care where available | REQ, LIT-019, SRC |

## I. Derived trajectory-feature feasibility

Each feature is calculated separately for every sufficiently repeated laboratory test and only from observations available before the prediction landmark.

| Feature family | Minimum source fields | Minimum observations | Required safeguards |
|---|---|---:|---|
| Baseline/current level | Test, numeric result, unit, date, dose/cycle | 1 | Unit compatibility and landmark cutoff |
| Reference-normalized position | Result, lower and upper limits or validated external ranges | 1 | Do not mix incompatible ranges; record source of range |
| Change from baseline/prior cycle | Two aligned results | 2 | Same standardized test/unit; explicit baseline/tie rule |
| Percentage change | Two aligned results | 2 | Define zero/near-zero denominator handling |
| Slope per day/week/cycle | Values and dates/cycles | 2 | Use actual intervals; do not assume equal spacing |
| Acceleration/curvature | Values and dates/cycles | 3 | Require temporal order and adequate spacing |
| Volatility/irregular jumps | Repeated values and dates | 3 preferred | Separate measurement noise, unit changes and true jumps |
| Time outside reference interval | Repeated value/range/date | 2 | Explicit interpolation assumptions; sensitivity analysis |
| Threshold crossing/recovery | Repeated value/range/date | 2+ | Threshold provenance; interval-censor crossing time |
| Missing-test pattern | Expected schedule and observed labs | Per cycle | Requires an expected-test denominator |
| Delayed-cycle pattern | Planned and actual administrations | 2 cycles | Cannot infer from missing lab alone |
| Interactions/joint movement | Compatible aligned features | Varies | Prevent asynchronous or future measurements from being combined |

## J. Dataset acceptance gates

A source or trial can support the discovery analysis only if all critical gates below are answered with source evidence:

1. Patient joins work across the required tables with quantified unmatched rows.
2. Laboratory events have usable timing and retain original result, unit and status.
3. Every laboratory test has a complete repetition/missingness inventory before inclusion decisions.
4. The next **actual** chemotherapy administration can be identified, or the source is explicitly limited to calendar-time/visit-based sensitivity analyses.
5. Overall-survival event and censoring definitions are reconstructable.
6. Progression, response and tolerance outcomes are kept source-specific when definitions differ.
7. No patient-level or restricted data are committed.
8. Cleaning rules are written only after the actual dictionary and columns are verified.

## Literature-to-field traceability

| Evidence group | Checklist impact |
|---|---|
| LIT-001 to LIT-003 | Separate progression/response families; assessment dates; no future leakage; cycle-level biomarker context |
| LIT-005, LIT-007, LIT-010, LIT-018 | Trial identifiers, survival/censoring, ECOG, disease sites, pain/opioids and baseline adjustment context |
| LIT-006, LIT-009 | AE-related early discontinuation, end timing/reason and separate tolerance outcomes |
| LIT-008 | Event-level `LabValue`, dates, ranges, status, duplicates, `NOT DONE`, original/standard results and the 13 comparison anchors |
| LIT-011 to LIT-014 | PSA, ALP, hemoglobin and inflammatory-cell trajectories; 4-week, 8-week and 90-day benchmarks |
| LIT-015 to LIT-017 | Landmark timing, sparse/irregular measurements and strict landmark-only information use |
| LIT-019 | Distinguish pre-cycle blood-count trajectories from post-dose nadirs and exposure signals |
| LIT-020 to LIT-022 | Trial-specific regimen and schedule differences, especially ASCENT2 weekly versus three-weekly treatment |

# Research Log

Living record for decisions, plans, progress, blockers and changes in the **Prostate Lab Trajectories** project.

This file should be updated whenever we:

- Make or revise a research decision.
- Learn something material about a dataset.
- Change inclusion criteria, outcomes, features or modeling choices.
- Complete a task or encounter a blocker.
- Start or finish an analysis phase.

## Current snapshot

**Last updated:** 2026-09-06

**Verified:** A5 audit complete and preparation Stage 01 explicitly authorized and completed under D-034. All 1,600 training patients retained, zero duplicate core keys and zero unmatched joins across 412,575 event rows. All 18 source CSVs verified against the original archive; the roster passed exact read-back. Twenty-one tests passed after fixing byte-encoding and missing-marker assumptions.

**Pending:** Stage 02 cycle-label harmonization, followed by the remaining preparation checks and integrity checkpoint before features. Stage 01 approval does not authorize modeling. Preserve D-003 and the two-track direction: DREAM methods cohort plus PDS-first search for a hormone-sensitive docetaxel source; no dbGaP application now.

**Verified patient-data handling:** the user-supplied latest panel was transcribed into a private four-page PDF and structured data outside Git. All 58 current-result rows passed PDF text read-back checks and the rendered pages were inspected. The original latest PDF is unavailable. Cycle numbering is inferred only and a missing unit remains unresolved. The index patient is the application case, not independent model validation.

**Verified documentation policy:** six essential docs remain after five tracked duplicates were consolidated and removed locally. No new research documentation files were created. Changes and new code/tests remain uncommitted; no publication authorization was supplied. See the data register for current preservation and cleanup evidence.

## Fixed research question

> Among patients with stage-IV metastatic prostate cancer receiving chemotherapy, how are serial pre-chemotherapy blood-test trajectories, individually and in combination, associated with survival, disease progression, treatment response and treatment tolerance, and how early can favorable or unfavorable patterns be detected?

## Decision register

| ID | Date | Decision | Reason | Status |
|---|---|---|---|---|
| D-001 | 2026-08-24 | Repository name is `prostate-lab-trajectories` and visibility is private. | Selected by the project owner. | Active |
| D-002 | 2026-08-24 | Analyze every sufficiently repeated blood-test value, not only PSA. | The central goal is a complete view of patient laboratory trajectories. | Active |
| D-003 | 2026-08-24 | Keep the research question exactly as written above. | It captures individual and combined trends, four outcome families and early detection. | Active |
| D-004 | 2026-08-24 | Do not restrict the project to a country or ethnicity. | Geographic and demographic fields may be described or adjusted for, but are not the main research question. | Active |
| D-005 | 2026-08-24 | Start with a narrow, coherent discovery population before broadening. | Reduces treatment/disease heterogeneity and makes the first patterns easier to interpret. | Active |
| D-006 | 2026-08-24 | Use three stages: discover, broaden and externally validate. | Separates pattern discovery from generalization and confirmation. | Active |
| D-007 | 2026-08-24 | Use PDS DREAM as the preferred discovery source. | It is the strongest identified source for harmonized event-level laboratory and outcome data in docetaxel-treated mCRPC. | Pending data audit |
| D-008 | 2026-08-24 | Use CHAARTED/E3805 mainly to broaden longitudinal PSA and treatment-exposure findings. | Its linked submissions explicitly include longitudinal PSA, treatment and outcome components, but not necessarily all laboratory values. | Pending access |
| D-009 | 2026-08-24 | Use Vivli trials or Flatiron only after confirming exact variable availability. | Access and advertised scope do not guarantee every required CBC/CMP, timing or outcome field. | Pending enquiry |
| D-010 | 2026-08-24 | Never commit patient-level or restricted data to GitHub. | Privacy, licensing and data-use agreements take priority. | Active |
| D-011 | 2026-08-24 | Maintain a curated literature catalog, BibTeX file and download manifest in the repository. | Each study must map to a concrete variable, outcome, method or data decision. | Active |
| D-012 | 2026-08-24 | Keep downloaded papers and extracted full text local and excluded from Git. | Avoid redistributing publisher files while preserving a searchable working library. | Active |
| D-013 | 2026-08-25 | Treat linkage to the next actual chemotherapy administration as a dataset acceptance gate; nominal calendar/visit landmarks are a separate fallback analysis, not equivalent evidence. | Delays, missed cycles and dose changes cannot be reconstructed safely from the nominal three-week schedule alone. | Active |
| D-014 | 2026-08-25 | Do not select ENTHUSE-33 as an independent validation set until the current PDS final-scoring package is audited for longitudinal data and outcome visibility. | The original challenge withheld non-baseline longitudinal data and dependent outcomes from participants. | Active |
| D-015 | 2026-08-25 | Use public DREAM analysis code only as documentary schema evidence, not as a replacement for the official dictionary or source files. | The repository exposes useful column names but intentionally contains no raw patient data. | Active |
| D-016 | 2026-08-25 | Run an aggregate-only, read-only inventory before writing any cleaning transformations. | This proves what was received and prevents premature assumptions while keeping patient identifiers and laboratory values out of the report. | Active |
| D-017 | 2026-08-25 | Acquire the complete PDS bundle first, preserve it unchanged and verify checksum and ZIP safety before extraction. | The full bundle provides one traceable acquisition artifact while safe verification protects source integrity and the local filesystem. | Acquisition complete; protected extraction follows approved execution plan |
| D-018 | 2026-08-25 | Maintain `PROJECT_CONTINUITY_LOG.md` as the operational memory and reminder queue, with methodological decisions also recorded in this research log. | The user needs durable cross-agent continuity, reminders and an exact account of developments while working away from home. | Active |
| D-019 | 2026-08-27 | Keep the permanent unchanged restricted package in the PDS-approved private Google Cloud bucket with public access prevention and uniform bucket access. | This keeps the source outside GitHub and ordinary file-sharing services while preserving controlled access. | Active; temporary local processing clarified by D-024 |
| D-020 | 2026-08-27 | Remove local restricted copies only after remote existence, size, checksum and access controls are verified and the user gives fresh action-time confirmation. | A verified cloud source must exist before local restricted data is removed. | Completed for the two Downloads copies |
| D-021 | 2026-08-27 | Perform the real-file audit only inside an approved protected environment and keep patient-level data out of chat, GitHub and ordinary logs. | Earlier interpretation was protected cloud compute without local download. | Cloud-compute interpretation superseded by D-024; privacy rule retained |
| D-022 | 2026-08-31 | Treat an onboarding or next-agent handoff request as a trigger to publish approved permitted work and clean up temporary local project folders after remote verification and fresh exact-target confirmation. Honor every backup condition attached to deletion approval. | The user wants GitHub as the permanent permitted project record and does not want local working copies retained after handoff. Restricted data remains in its approved private cloud storage, never GitHub. | Active; current all-files-backup condition unresolved |
| D-023 | 2026-08-31 | Record private Google Cloud use and moving forward to protected compute and audit as approved. Ask for approval of concrete execution plans and later research stages, not repeated generic cloud permission. | Earlier documentation interpreted this as cloud computation. | Cloud-compute interpretation superseded by D-024; concrete approval gates retained |
| D-024 | 2026-08-31 | Use cloud storage only as the permanent restricted-data home; perform computations, tests, audits, cleaning and analysis locally in a recorded protected temporary run folder. Upload new versioned outputs, verify them, then obtain fresh confirmation and delete local copies after each stage. | The user explicitly corrected the compute location and wants future agents to resume from verified cloud versions without forgotten local data. | Active; next-agent approval-first sequence clarified by D-026 |
| D-025 | 2026-08-31 | Execute the first local read-only audit under `LOCAL-AUDIT-2026-08-31-01`, track each step and evidence in the continuity log, and publish the approved corrected data-free instructions. | The user explicitly approved the concrete plan and requested a persistent completion tracker. | Historical approval/publication complete; next execution checkpoint now follows D-026; no real-file audit occurred |
| D-026 | 2026-08-31 | The next agent must first explain the local data-processing plan and ask one approval question before data work. Withdraw the previous agent's added mandatory drive-encryption detour; retain source integrity, folder privacy, disclosure checks, verified uploads and exact-target cleanup confirmation. | The user explicitly rejected the detour and requested an approval-first handoff, with the plan explained in chat before GitHub onboarding changes. | Active; next-agent approval pending; corrected handoff publication now explicitly authorized |

### Decisions added 2026-09-04 after the real-data audit

| ID | Date | Decision | Reason | Status |
|---|---|---|---|---|
| D-021 | 2026-09-04 | Treat the 1,600-patient training partition as the only analysable cohort and do not attempt supervised use of the leaderboard or final scoring partitions. | Their `DEATH` and `LKADT_P` fields are entirely blank because they were the blinded DREAM challenge test sets, so no outcome label exists. | Active |
| D-022 | 2026-09-04 | Do not claim treatment tolerance in terms of dose reduction, dose delay or cycle-level administration on this package. | `PriorMed` is baseline-only with `CMPRE=YES` on all 147,770 rows and zero on-treatment records, so no administration, cycle or dose data exists. Tolerance can only be operationalized through discontinuation, its recorded reason, and laboratory toxicity grades. | Active |
| D-023 | 2026-09-04 | Do not treat radiographic progression or RECIST response as primary outcomes on this package. | `LesionMeasure` covers only 70.2% of patients, omits ASCENT2 entirely, has a median of 2 assessment days and is largely qualitative. | Active |
| D-024 | 2026-09-04 | Interpret pre-chemotherapy as measured around each chemotherapy cycle, not only before docetaxel starts, and anchor all trajectory features to harmonized `VISIT` cycle labels. | The user confirmed the intended design is trend analysis across cycles. The `VISIT` field names cycles explicitly in three trial-specific vocabularies, and 1,179 patients have all of cycles 1 to 4 measured. The before-treatment-only reading gives a median of 2 laboratory days and is not feasible. | Active |
| D-025 | 2026-09-04 | Use cycles 1 to 4 as the primary analysis window on the 1,179 complete-case patients, with cycle 5 and the 1,292 three-cycle patients as sensitivity analyses. | Patient coverage is 90.6%, 93.3%, 89.6% and 82.9% at cycles 1 to 4, falls to 48.1% at cycle 5 and is negligible beyond. | Active |
| D-026 | 2026-09-04 | Set primary endpoints as overall survival and treatment discontinuation, with PSA response as an explicitly labelled secondary. | 663 death events with complete follow-up time, and `ENDTRS_C` complete for all 1,600. No RECIST response field exists, so PSA response must not be presented as radiographic response. | Active |
| D-032 | 2026-09-04 | Before starting any dbGaP application, search the Project Data Sphere catalogue for a hormone-sensitive metastatic prostate cancer trial with docetaxel, because PDS access is already granted and working. | NCTN and NCORP clinical data moved to dbGaP in the third quarter of 2025, and dbGaP controlled access requires an eRA Commons account plus approval from an institutional Signing Official followed by Data Access Committee review. Without a university or research-institution affiliation that route may be unavailable, whereas the PDS account already produced the DREAM package. Checking PDS costs days rather than months. | Active |
| D-033 | 2026-09-04 | Do not expect CHAARTED to validate the full twelve-test panel. Plan for it to confirm the prostate-specific antigen findings only. | The project's own public field audit established that submission D8 is longitudinal prostate-specific antigen only, with D12 adding testosterone, and no CHAARTED submission publicly provides repeated full blood panels. The multi-test trajectory result will therefore remain DREAM-derived and castration-resistant unless a hormone-sensitive source with complete panels is found. | Active |
| D-030 | 2026-09-04 | Run method development on DREAM and the CHAARTED access request in parallel rather than sequentially, and never report a DREAM-derived survival estimate as the index patient's prognosis. | Agreed with the user. CHAARTED is controlled access through dbGaP and will take weeks to months, while DREAM is already downloaded and verified, so waiting would idle the project. The stage mismatch makes DREAM valid for identifying which trends matter but invalid for quantifying this patient's outcome. | Active |
| D-031 | 2026-09-04 | Validate internally by leave-one-trial-out cross-validation across EFC6546, CELGENE and ASCENT2, and freeze the pipeline before the final run. | The leaderboard and final scoring partitions carry no outcome labels, so no external validation set exists. Holding out an entire trial is the strongest honest generalization test available and directly probes cross-trial transportability. | Active |
| D-029 | 2026-09-04 | Do not seek a separate prostate-specific-antigen dataset. | The DREAM package already contains 9,310 prostate-specific antigen measurements covering 99.9% of its 1,600 patients, so it is one of the twelve near-universal tests. The reason to obtain CHAARTED is disease-stage matching, not antigen coverage. | Active |
| D-027 | 2026-09-04 | Judge every candidate dataset against the index patient's actually measured panel and timing, not against a generic ideal. | The project's purpose is to interpret one real patient's blood-test trends. Coverage of a test the index patient never had is near worthless; a test he has serially is high value even at partial dataset coverage. | Active |
| D-028 | 2026-09-04 | Treat the DREAM package as the METHODS development cohort rather than the primary clinical reference. Confirmed by Q-010: the index patient is hormone-sensitive, so CHAARTED is the stage-matched reference and must be requested, while all method development proceeds on DREAM immediately rather than waiting. | DREAM is entirely castration-resistant: 90.1% had prior anti-androgens and 87.9% prior gonadotropin therapy, so all had progressed through androgen deprivation. The index patient's prostate-specific antigen is falling steeply while testosterone is at castrate level, which is the hormone-SENSITIVE response pattern. If confirmed, CHAARTED becomes the correct primary reference population and DREAM the secondary. | Pending clinical confirmation |

### Decision added 2026-09-06

| ID | Date | Decision | Reason | Status |
|---|---|---|---|---|
| D-034 | 2026-09-06 | Execute preparation Stage 01 locally: freeze all 1,600 training patients and check source integrity and composite-key joins without test/cycle filtering or outcome recoding. Later stages remain scoped separately. | The user explicitly requested starting Stage 1, correct tests and disclosure of error points after each step. | Verified complete; 21 tests passed |

### Continued preparation authorization, 2026-09-06

| ID | Date | Decision | Reason | Status |
|---|---|---|---|---|
| D-035 | 2026-09-06 | Continue preparation stages 02 to 07 sequentially toward cleaned data after publishing the current permitted work. Retain raw fields, explicit uncertainty, per-stage tests and the integrity checkpoint before features. | The user explicitly requested continuing cleaning one step at a time and function-level documentation. | Authorized; execution pending |

## Master plan

### Phase 0 - Repository and protocol setup

**Goal:** Create a stable project home and freeze the first analysis definitions.

- [x] Select project name and private visibility.
- [x] Create research blueprint.
- [x] Create living research log.
- [x] Build the initial literature evidence map and bibliography.
- [x] Add the dataset field-coverage checklist.
- [ ] Draft the statistical analysis plan.
- [ ] Define outcome hierarchy and pre-cycle timing windows.

**Exit condition:** The project structure, inclusion criteria, endpoints and validation policy are documented before data modeling begins.

### Phase 1 - Data access and dataset audit

**Goal:** Prove which requested analyses are actually supported by the available fields.

- [x] Complete PDS authorization and access requirements.
- [x] Obtain and verify the PDS DREAM package in approved private cloud storage.
- [ ] Inspect every PDS dictionary sheet and supplied table inside approved protected cloud compute.
- [ ] Inventory tables, columns, join keys and date variables.
- [ ] Count patients and repeated observations per laboratory test and trial.
- [ ] Audit survival, progression, response and tolerance endpoints.
- [ ] Request CHAARTED D5, D7, D8, D9 and D11.
- [x] Audit the public CHAARTED submission descriptions and available dictionary fields.
- [x] Prepare and test an aggregate-only raw-data inventory tool using invented records.
- [ ] Enquire about FIRSTANA, PROSELICA and TROPIC through Vivli.
- [ ] Request a Flatiron variable list and commercial-access details.

**Exit condition:** A source-by-source coverage matrix identifies which dataset supports which value, feature and outcome.

### Phase 2 - Cleaning and harmonization

**Goal:** Produce reproducible analysis-ready longitudinal tables without leakage.

- [ ] Standardize patient and trial identifiers.
- [ ] Map laboratory names and specimens.
- [ ] Normalize units while preserving originals.
- [ ] Clean duplicates, `NOT DONE`, detection-limit and nonnumeric results.
- [ ] Align each blood test to the next chemotherapy cycle.
- [ ] Harmonize outcome definitions and censoring.
- [ ] Create missingness and data-quality reports.
- [ ] Freeze transformation rules and tests.

**Exit condition:** Long-format test data, cycle snapshots and patient outcomes can be rebuilt from source data by one documented pipeline.

### Phase 3 - Discovery analysis

**Goal:** Evaluate all usable laboratory trajectories in the PDS discovery data.

- [ ] Generate per-patient and population trajectory plots for every usable value.
- [ ] Calculate baseline, current level, changes, slopes, acceleration, volatility and threshold history.
- [ ] Test individual features against survival, progression, response and tolerance.
- [ ] Fit interpretable multivariable models.
- [ ] Explore nonlinear interactions and trajectory clusters where supported.
- [ ] Compare prediction landmarks after cycles 1, 2, 3 and 4.
- [ ] Report null, contradictory and unstable patterns.

**Exit condition:** Candidate findings are ranked with effect sizes, uncertainty, earliest detection time and internal cross-trial validation.

### Phase 4 - Controlled broadening

**Goal:** Test available findings in CHAARTED/E3805.

- [ ] Join linked CHAARTED submissions using common deidentified IDs.
- [ ] Rebuild longitudinal PSA features.
- [ ] Link PSA to dose, progression and survival.
- [ ] Apply frozen discovery definitions where compatible.
- [ ] Explain non-comparable fields instead of forcing a merge.

**Exit condition:** Findings are labeled portable, disease-setting-specific, unsupported or failed.

### Phase 5 - External validation and reporting

**Goal:** Test frozen findings in independent patients and publish a reproducible result package.

- [ ] Select Vivli or Flatiron based on the completed coverage matrix.
- [ ] Freeze preprocessing, models and thresholds before outcome access.
- [ ] Run independent validation once without retuning.
- [ ] Report calibration, discrimination, effect sizes and coverage.
- [ ] Produce the final value-by-value atlas and combined-pattern report.
- [ ] Release only permitted, aggregated and disclosure-checked outputs.

**Exit condition:** The final report separates reproduced, failed, dataset-specific and unresolved patterns.

## Active task board

| Priority | Task | Status | Completion evidence |
|---|---|---|---|
| 1 | Create the private GitHub repository with `README.md` and this log. | Completed | Private repository created; initial commit `d38740c` |
| 2 | Build the initial curated literature library. | Completed | 22-study catalog, BibTeX file, manifest and 10 validated local PDFs |
| 3 | Convert the literature map into a field-coverage checklist. | Completed | `docs/dataset-field-coverage-checklist.md` |
| 4 | Secure and verify the PDS DREAM package. | Completed | Private cloud object exists with verified size, checksums and access controls; local restricted ZIP copies were removed after confirmation |
| 4A | Inspect the PDS dictionary and real tables in protected cloud compute. | Proceeding approved; execution-plan approval next | Every dictionary sheet, schema, join key, repeated-lab count and outcome field audited without patient-level output |
| 5 | Define exact primary and secondary outcomes. | Planned | Statistical analysis plan section approved |
| 6 | Define pre-cycle timing and repeated-measure eligibility rules. | Planned | Frozen configuration and sensitivity windows |
| 7 | Prepare CHAARTED and external-validation access requests. | Planned | Submitted requests or documented access route |
| 8 | Produce the first source-coverage matrix. | Completed with documented unknowns | `docs/source-coverage-matrix.md`; source-column cells remain pending gated-file audit |
| 9 | Audit public CHAARTED fields and DREAM code clues. | Completed | `docs/chaarted-public-field-audit.md` and `docs/dream-public-code-audit.md` |
| 10 | Prepare a safe first-pass source inspector. | Completed | `src/audit/inventory_raw_data.py`; three synthetic-data tests pass |
| 11 | Create durable operational continuity and next-agent onboarding. | Completed | `PROJECT_CONTINUITY_LOG.md` and `NEXT_AGENT_ONBOARDING_PROMPT.md` |

| 14 | Reconcile the new macOS working copy with remote main and preserve the unpushed 2026-08-26 state. | Completed | Fast-forward to `7392d50`; preservation branch `backup/local-2026-08-26-session` at `a85919f` |
| 15 | Register and verify a macOS restricted-work run root outside all synchronized locations. | Completed | `/Users/barbarosisik/PDS-Restricted-Work/.../runs/2026-09-04-audit-001`; seven containment and permission checks recorded in `docs/data-location-register.md` |
| 16 | Install and verify the macOS toolchain for the local audit. | Completed | Python 3.12.8, Google Cloud CLI 583.0.0, `~/tools/venv-pds-audit` with pinned `openpyxl==3.1.5`; all 3 synthetic tests pass |
| 17 | Download and verify the real PDS source package on the Mac. | Completed | 6,227,480 bytes; SHA-256 matches the 2026-08-27 record; MD5 matches live cloud metadata; archive scanned safe without extracting |
| 18 | Audit the real DREAM files at aggregate level against the four outcome families. | Completed | 1,600 analysable patients; survival strong; tolerance partial; progression and response weak; no chemotherapy administration records |
## Open questions

| ID | Question | Needed for |
|---|---|---|
| Q-001 | Which PDS laboratory values have at least two eligible pre-cycle measurements in enough patients? | Final analysis feature set |
| Q-002 | Does the released ENTHUSE-33 package include the outcome fields needed for independent validation? | Discovery/validation split |
| Q-003 | Which treatment-tolerance variables are consistently dated across PDS trials? | Tolerance endpoint definition |
| Q-004 | Can progression be separated into radiographic, clinical and PSA progression in every source? | Outcome hierarchy |
| Q-008 | Should the leaderboard and final scoring partitions be held out entirely, or pooled with training after the coverage audit? | RESOLVED by audit: their outcome labels were never released, so they are unusable for supervised work and the effective sample is 1,600 |
| Q-010 | Is the index patient castration-resistant or still hormone-sensitive at the start of docetaxel? | High-confidence hormone-sensitive inference recorded 2026-09-04 from the private care-pathway and laboratory records. Pathology, imaging and baseline-treatment documentation remain incomplete. Patient details and values remain in the restricted patient folders. |
| Q-009 | Does pre-chemotherapy in the fixed research question mean before docetaxel starts, or before each docetaxel cycle? | RESOLVED 2026-09-04 by the user: tests are taken around every chemotherapy cycle so that trends across cycles can be related to survival and recovery. The per-cycle reading is confirmed and the design is feasible |
| Q-005 | Which Vivli trials expose serial standard laboratory panels and chemotherapy-cycle dates? | External validation choice |
| Q-006 | Does Flatiron provide all standard blood values and reliable chemotherapy-cycle linkage, not only PSA? | Purchase/access decision |
| Q-011 | Why do 112,167 training rows disagree numerically between `LBSTRESN` and `LBSTRESC`, and which column is authoritative? | RESOLVED 2026-09-06 by Stage 05: `LBSTRESN` is a whole-number rounding of `LBSTRESC`. Use `LBSTRESC` only. |
| Q-012 | Given that ASCENT2 cycle-labelled rows contain only PSA, should ASCENT2 be restricted to PSA trajectories or excluded from multi-test per-cycle work? | Final trial composition |
| Q-013 | When `LBBLFL` equal to `Y` sits on a row that also carries a `CYCLE` visit label, which record defines baseline? | RESOLVED 2026-09-06 by Stage 07: the flag defines it. A cycle 1 day 1 draw at day 0 is a legitimate baseline and most CELGENE baselines are exactly that. |
| Q-014 | Should EFC6546 cycle 1 be treated as missing for panel tests, given a median of 4 test codes per patient there against 26 at later cycles? | Cycle window for the per-cycle feature set |
| Q-015 | When one visit label spans more than one recorded collection day, which draw represents that cycle? 1,495 of 8,512 patient-visit groups are affected. | Stage 06 repeat-measurement rule |
| Q-016 | How should the laboratory clock (first treatment) be reconciled with the outcome clock (consent for ASCENT2 and CELGENE, randomization for EFC6546) when no per-patient offset is recoverable? | Any landmark or time-to-event analysis |
| Q-017 | Should the discontinuation endpoint be restricted to the 1,489 patients with a non-missing `DISCONT`, and how are the 95 patients without a treatment stop day handled? | Second endpoint definition |
| Q-018 | How are the 815 bounded results and the 543 rows whose bound was lost upstream to be handled in a trajectory? | Stage 06 value rule |
| Q-019 | Should LDH be kept in the panel at 463 patients at cycle 2, roughly half the coverage of every other test, given its recognized prognostic value? | Final feature set |
| Q-020 | Does EFC6546 number its first treatment day as 1 rather than 0? All 2,221 positive-day baselines are exactly day 1 and all come from that trial. | Confirming baselines precede treatment |

## Risk register

| Risk | Impact | Planned response |
|---|---|---|
| Sparse repeated tests | Some values cannot support slopes or complex trajectories. | Set minimum patient/observation thresholds and report sparse values descriptively. |
| Different units and test names | False trends or failed pooling. | Use an explicit harmonization dictionary and preserve original fields. |
| Informative missingness | Missing tests may reflect worsening health or treatment decisions. | Model and report missingness patterns; avoid naive filling. |
| Outcome-definition mismatch | Biased comparisons between trials. | Keep source-specific endpoints and harmonize only defensible definitions. |
| Treatment/disease heterogeneity | Associations may reflect setting rather than the laboratory trajectory. | Discover narrowly, stratify by trial and broaden in a separate stage. |
| Future leakage | Artificially strong early prediction. | Enforce time-aware feature generation and trial-level validation. |
| Multiple testing | False discoveries across many values/features/outcomes. | Use hierarchical screening, multiplicity control and external validation. |
| Restricted data | Privacy or contractual breach. | Keep patient-level data outside Git and follow every data-use agreement. |

## Dated activity log

### 2026-08-24 - Project initialized

**Completed**

- Fixed the research question.
- Confirmed that the project will analyze all usable repeated blood values.
- Selected a narrow-to-broad-to-validation strategy.
- Selected PDS DREAM, CHAARTED and Vivli/Flatiron as the initial dataset path.
- Selected repository name `prostate-lab-trajectories` and private visibility.
- Created the initial README and living research log.
- Created the private GitHub repository and committed `README.md`, `RESEARCH_LOG.md` and `.gitignore`.

**Next**

- Obtain the PDS DREAM data dictionary.
- Convert the dataset requirements into a field-coverage checklist.

### 2026-08-24 - Literature foundation added

**Completed**

- Curated 22 core, direct, supporting, methodological and source-trial studies.
- Created a study-to-analysis evidence map and a reusable BibTeX bibliography.
- Downloaded and validated 10 legitimate full-text PDFs locally and extracted searchable text.
- Added an access manifest for downloaded and link-only studies.
- Excluded the local paper library from Git while keeping its catalog and metadata tracked.

**Decisions**

- D-011: Every retained paper must change or justify a concrete analysis decision.
- D-012: PDFs and extracted full text remain local; the catalog, bibliography and manifest are versioned.

**Evidence / files**

- `literature/README.md`
- `literature/STUDY_CATALOG.md`
- `literature/references.bib`
- `literature/download_manifest.csv`

**Next**

- Turn the evidence map into a dataset field-coverage checklist.
- Obtain and audit the PDS DREAM data dictionary and source files.
- Draft the first cleaning and restructuring specification only after the available columns are verified.

### 2026-08-25 - PDS public release and access audit

**Completed**

- Re-read the project and literature handoff files in the required order and preserved the fixed research question and strategy.
- Confirmed the canonical private GitHub `main` branch remains at handoff commit `1bb2656d61adeae32f4009962dbfaa6351b6ba48` with nine commits.
- Rechecked GitHub access: the connector still returns 404, GitHub CLI is unavailable and non-interactive HTTPS Git has no usable credentials. The signed-in in-app browser can read the canonical repository.
- Located the official PDS contribution `Prostat_na_2006_149`, DOI `10.34949/e6c8-v326`, dictionary `Challenge_data_dictionary v2.xlsx` and the training, leaderboard and final-scoring ZIP listings.
- Located the official Synapse project `syn2813558`, dictionary `syn3348062`, challenge-data folder `syn3325825`, training folder `syn3348064`, combined training ZIP `syn3350917` and all six training CSV IDs.
- Confirmed from official public Synapse documentation that training `LabValue` is event-level and includes screening through day 84, with `LBDT_PC`, `LBBLFL`, original/standardized results, `LBSTAT`, `LBNRIND` and visit information relevant to the audit.
- Converted the literature evidence into a detailed field-coverage checklist.
- Created a PDS access/release audit and an initial source-by-source coverage matrix with unknown cells kept explicit.

**Decisions**

- D-013: Actual-administration linkage is a feasibility gate; nominal calendar or visit landmarks are not silently treated as actual cycles.
- D-014: ENTHUSE-33 remains a validation candidate only after current outcome and longitudinal-field visibility is confirmed.
- The cleaning and restructuring specification remains intentionally unwritten until the gated dictionary and source columns are verified.

**Evidence / files**

- `docs/dataset-field-coverage-checklist.md`
- `docs/pds-dream-access-audit.md`
- `docs/source-coverage-matrix.md`
- Official PDS contribution: `0abbd47a-dcfb-42c2-a036-af1898ea3c1c`
- Official Synapse project: `syn2813558`

**Problems or blockers**

- The PDS contribution page is not signed in and exposes no download controls.
- Synapse reports `canDownload=false` for dictionary `syn3348062` with unmet access requirement `3325885` and certification required.
- No source file has been downloaded, so actual columns, joins, laboratory counts and cycle alignment have not been reported as verified.
- The six-table release inventory contains no chemotherapy-administration event table, dose/cycle table, AE event table or progression event table. These fields may be absent; the dictionary audit must decide.

**Next**

- Complete PDS/Synapse sign-in and required terms/access acceptance.
- Download the official dictionary and training package into ignored `data/raw/pds_dream/` storage.
- Inventory every table/column, then count every laboratory test by patient, trial and cycle/visit.
- Test whether laboratory events can be aligned to actual administrations before writing the cleaning specification or pipeline.

### 2026-08-25 - PDS application submitted

**Completed**

- Submitted the Project Data Sphere registration and data-access application.
- PDS confirmed successful submission and stated that review usually takes less than seven days.
- Identified public work that can continue during review: official Synapse table documentation, public DREAM winning-solution code and public CHAARTED/E3805 data dictionaries.
- Confirmed that the public DREAM winning-solution repository does not redistribute raw patient data, but it does expose code and selected baseline feature names that can inform the pending schema audit.
- Confirmed from the current NCI page that NCTN/NCORP patient-level access is now routed through dbGaP, while public CHAARTED dataset descriptions and dictionaries remain useful for a compatibility audit.

**Problems or blockers**

- The PDS dictionary and patient-level files remain unavailable until the application is approved.
- Public code and dictionaries can refine the field inventory, but they cannot replace the source-row, repetition and actual-cycle checks required for discovery.

**Next**

- Wait for the PDS decision email and resume acquisition immediately after approval.
- Audit the public CHAARTED D5, D7, D8, D9 and D11 dictionaries while PDS is reviewing the application.
- Use public DREAM code only as documentary evidence and never as a substitute for the gated source files.

### 2026-08-25 - Waiting-period preparation completed

**Completed**

- Audited the public CHAARTED D5, D7, D8, D9, D11 and D12 descriptions and the exact D5/D12 fields exposed by official dictionaries.
- Confirmed that linked CHAARTED submissions share `group_uid`, D8 contains longitudinal PSA, D9 contains chemotherapy total dose and D5 contains survival and several progression outcomes.
- Confirmed that public CHAARTED evidence still does not prove an exact administration date for each chemotherapy cycle.
- Inspected the public DREAM winning-solution processing and paper code for core patient, trial, baseline laboratory, death, discontinuation and treatment-ending fields.
- Built a read-only CSV inventory tool that reports tables, columns, missingness, field coverage and repeated-laboratory counts without writing patient identifiers or laboratory values.
- Tested the tool with invented CoreTable and LabValue records. All three tests passed.

**Decisions**

- D-015: Public code is a column-name clue only; the official dictionary and received files remain authoritative.
- D-016: The aggregate inventory runs before any cleaning or restructuring code is written.

**Evidence / files**

- `docs/chaarted-public-field-audit.md`
- `docs/dream-public-code-audit.md`
- `docs/raw-data-inventory-tool.md`
- `src/audit/inventory_raw_data.py`
- `tests/test_inventory_raw_data.py`
- `tests/fixtures/synthetic_pds/`

**Problems or blockers**

- PDS review is still pending, so no real dictionary or patient file has been inspected.
- CHAARTED is promising for repeated PSA, survival and progression, but current public evidence does not establish complete blood panels or exact per-cycle administration dates.

**Next**

- Watch for the PDS decision email and answer any request for additional information.
- After approval, download only to ignored restricted storage and run the aggregate inventory immediately.
- Use the report to decide which blood values repeat enough, which outcomes exist and whether exact pre-treatment linkage is possible.
- Write cleaning rules only after those answers are verified.

### 2026-08-25 - PDS access approved and continuity handoff created

**Completed**

- Confirmed that PDS accepted the user's registration and access request.
- Opened the PDS login page and allowed the user to enter credentials privately.
- Confirmed successful sign-in and opened Access Data.
- Located approved contribution `Prostat_na_2006_149` and verified it is marked Available for Download.
- Verified the contribution reports 2,070 patients.
- Verified the page lists `AllProvidedFiles_149.zip`, the official Excel dictionary, training ZIP, leaderboard ZIP, final-scoring ZIP and CRF location document.
- Verified the training package lists CoreTable, LabValue, LesionMeasure, MedHistory, PriorMed and VitalSign CSV files.
- Attempted the PDS Download controls through semantic, visible-DOM and physical browser interactions.
- Confirmed that no browser download event occurred and no new file appeared in the Windows Downloads folder.
- Recorded that the user is away from home and must postpone the large download or use suitable protected storage.
- Created an extensive operational continuity log and reusable GPT-5.6 Sol onboarding prompt.

**Decisions**

- D-017: Preserve and verify the complete bundle before extraction.
- D-018: Maintain a separate operational continuity log and reminder queue alongside this formal research log.

**Evidence / files**

- `PROJECT_CONTINUITY_LOG.md`
- `NEXT_AGENT_ONBOARDING_PROMPT.md`
- Official PDS contribution `0abbd47a-dcfb-42c2-a036-af1898ea3c1c`

**Problems or blockers**

- No protected PDS file has been downloaded yet.
- Automated browser interaction did not start the site download.
- The user cannot complete the large download until returning home or arranging suitable protected storage.

**Next**

- Remind the user at home to manually download `AllProvidedFiles_149.zip`.
- Verify the completed file path, size and SHA-256 checksum.
- Inspect ZIP members for unsafe paths before extraction.
- Inspect the dictionary and run the aggregate inventory before any cleaning specification.

### 2026-08-27 - PDS package secured and local restricted copies removed

**Completed**

- Recorded the user's confirmation that Craig at PDS permitted private Google Cloud storage.
- Verified the unchanged source package at `gs://pds-dream-secure-storage-eu-20260827/prostate-lab-trajectories/data/raw/pds_dream/source/AllProvidedFiles_149 (1).zip`.
- Verified remote size 6,227,480 bytes, SHA-256 `AB3ECA19C5D0CC4106C96AC04E665DD1A5C9DF58F66328ECD24E8E1067932391`, matching MD5 and Google Cloud CRC32C metadata.
- Verified a Netherlands regional bucket, enforced public-access prevention, uniform bucket-level access, Google-managed encryption and no public principals.
- Permanently removed the two exact verified Downloads copies after fresh user confirmation and found no matching copies or partial downloads in the targeted rescan.
- Cloned and verified the private GitHub repository on `main` at `d02eed8359229d19008efb60ba60a4cb3c08e903`.
- Re-ran all three invented-data inventory tests successfully.

**Decisions**

- D-019: Use only the approved private Google Cloud bucket for the unchanged restricted source package.
- D-020: Local restricted files can be removed only after complete remote verification and fresh deletion confirmation.
- D-021: Use protected cloud compute for the dictionary and real-file audit so the restricted source is not downloaded back to this computer.

**Evidence / files**

- Project and bucket metadata recorded in `PROJECT_CONTINUITY_LOG.md`.
- Local restricted-data rescan found zero matching files in Windows Downloads.
- Test command: `python -m unittest discover -s tests -v`, three tests passed.

**Problems or blockers**

- No private cloud computing resource has been selected or created.
- Exact source columns, joins, repeated laboratory counts and actual chemotherapy timing remain unaudited.

**Next**

- Explain protected Google Cloud computing options, costs, access controls and shutdown requirements.
- Obtain explicit approval before creating paid computing resources or beginning the real-file audit.
- Stop again for approval after the audit before writing cleaning and restructuring transformations.

### 2026-08-31 - Session-closeout and local-working-copy policy

- Added D-022 and documented its safe execution order in the onboarding prompt and `AGENTS.md`.
- Verified the existing GitHub backup and identified local-only full-text literature before proposing deletion.
- No research question, source priority, field definition or analysis method changed.
- No restricted patient data was opened or transferred in this session.
- The user explicitly approved publication of the new policy. Approval to delete both exact folders is conditional on every local project file being backed up in GitHub first.
- Full-text papers, extracted text, temporary downloads and generated caches remain excluded from GitHub. No folder deletion is permitted while that condition is unmet. Obtain approval for an alternative backup or explicit exception; do not silently relax the condition.
- Do not record local cleanup as completed before a fresh filesystem check.

### 2026-08-31 - Cloud-work approval and plan-level checkpoints clarified

- User confirmed that Google Cloud use is approved and requested an actionable handoff for the next agent.
- Added D-023 and updated current status documents to separate settled cloud permission from approval of the exact resource-and-audit execution plan.
- The next agent should propose concrete resources, access controls, current costs, audit outputs and shutdown arrangements, then execute the approved plan. A later cleaning plan and analysis plan follow the actual-field audit.
- No source field, outcome definition, inclusion rule or model was changed. This was a documentation update only, explicitly authorized for publication to `main`.
- Local-folder cleanup retains the separate all-files-backup condition and remains unperformed.

### 2026-08-31 - Concrete protected-audit plan prepared

Historical unapproved proposal, superseded by the later same-day local-processing correction. No VM was created.

- Verified current local and remote `main` at `fb059b91df2fd38740ab305fb17058204e7d9096`, read all required records and re-ran the three invented-data tests successfully.
- Refreshed cloud storage/access metadata without reading patient content. Compute Engine is not enabled in the console; the asset inventory displayed no compute resources and the service-account list was empty. No setup or audit was executed.
- Prepared an uncommitted small-VM proposal. The user subsequently corrected execution to local processing; that file was withdrawn and replaced by `docs/local-processing-and-cloud-storage-plan.md`.
- The proposed audit separates source-observed repetitions from dictionary-supported numeric-valid repetitions; it does not silently treat every nonempty result as valid or every nonpositive study day as baseline. It adds aggregate join checks and checks every dictionary-defined field rather than relying only on fixed aliases.
- Proposed export safeguards include verified metadata labels, no patient IDs or lab result values, suppression of nonzero patient groups below 10 and complementary disclosure checks. These are proposed project safeguards, not an assertion of a PDS-prescribed disclosure threshold.
- Exact administration linkage remains the critical scientific gate, including trial/table reference dates and ambiguity when only same-day dates are available. Survival, progression, response and tolerance remain separate. ENTHUSE-33 is assessed for availability only, not used for model fitting.
- No source-defined outcome, cleaning rule, final measurement eligibility rule, timing window, discovery population or model was approved or changed. Audit code extensions, later cleaning and later analysis are not implemented.
- New records remain uncommitted. Next action is approval of the specific setup-and-audit plan, followed by the separately approved cleaning and analysis stages.

### 2026-08-31 - Local processing and cloud-storage continuity clarified

- Added D-024 after the user explicitly rejected cloud computation. All tests and data processes are to run locally; private cloud storage preserves immutable source files and new versioned outputs, including later cleaned datasets.
- Proposed one registered local audit folder, local encryption/access checks, local-only dictionary/CSV inspection, read-only audit extensions and privacy-reviewed outputs. No download is allowed before the local security gates and specific plan approval.
- Added a data-location register and per-run manifests to connect source hashes, exact code versions, cloud generations and local cleanup. Verified upload is required before local removal, with fresh exact-target deletion confirmation.
- Existing audit limitations, actual-administration timing gate, all sufficiently repeated tests and all four separate outcome families remain unchanged. This workflow correction does not authorize cleaning transformations or modeling.
- Encryption status could not be read through the available Windows command context and remains unverified. No data was exposed or processed to work around that check.
- New documentation is local and uncommitted. No real-file audit, cleaned dataset, output upload, commit/push or local deletion has occurred. The exact local audit plan is next; cleaning and scientific analysis each require later approval.

### 2026-08-31 - Specific local audit approved; tracked execution started

- Recorded D-025 and the user's approval of the concrete local audit/upload plan plus corrected data-free GitHub publication. Added the detailed A0-A10 execution tracker to the continuity log.
- Published the corrected ten data-free documents at `9843e5b86a89c4f5ca583a60f1906c69032ee9c8`, independently verified remote main at that SHA and confirmed all required document paths in the matching commit. All three invented-data tests passed again; no source/test code or scientific definitions changed.
- Local encryption remains unverified after the permitted command retry returned access denied. No patient data was downloaded to work around this prerequisite, and no Windows security setting was changed.
- The approved audit remains read-only and covers every repeated lab, full joins, exact administration timing, four separate outcome families and ENTHUSE-33 availability. No source-derived cleaning definition, treatment window or model has been established.
- Continue routine approved audit steps once local security passes. Prepare the cleaning specification from verified fields afterward, then obtain separate approval before transformations. Scientific analysis remains a later approval gate.

### 2026-08-31 - Approval-first handoff and removal of the added encryption detour

- Added D-026 following the user's latest instruction. The earlier approval is not erased, but the next agent now has an explicit explanation-and-approval checkpoint before data work.
- The mandatory BitLocker check was an agent-added precaution, not a newly verified PDS requirement. The user rejected that detour. It is withdrawn from current instructions; disk status remains unknown, and no Windows setting or scientific definition changed.
- Preserved the full local audit scope, immutable source, all sufficiently repeated labs, four distinct outcome families, actual-administration timing gate and later separate cleaning/modeling approvals.
- Completed a read-only inventory of both known project folders for the handoff cleanup workflow. Unbacked local-only papers/text/temp files and older working-copy changes remain in the retired folder; no backup exception or deletion was authorized.
- New handoff/current-state changes remain local and uncommitted pending publication authorization. No restricted data was downloaded, extracted, audited, cleaned, modeled, uploaded or deleted.

## Update template

### 2026-08-31 - Corrected handoff publication authorized; cleanup pending

- The user explicitly authorized publication, followed by local project cleanup after preservation. The approval-first research handoff remains unchanged: A0R must be answered before data execution, with separate later cleaning and modeling approvals.
- All 19 permitted retired working-file contents were matched to canonical Git history, allowing newline normalization. The 27 ignored local-only papers, extracted text, temporary PDFs and caches are not backed up in GitHub. Their backup exception or permitted alternative and fresh exact-target confirmation remain unresolved.
- This closeout changes documentation only. No patient data was downloaded, inspected, transformed or uploaded, and no new scientific result or timing assumption was made. Publication evidence belongs in the continuity log; deletion must not be reported without a fresh filesystem check.

### 2026-09-05 - Onboarding verification and snapshot reconciliation

- **Verified:** Completed mandatory reading and local state checks. Source size and SHA-256 match the registered package; restricted directories remain outside the repository. No patient contents were opened.
- **Verified:** Replaced stale snapshot instructions that reopened Q-009 and A0R. Preserved the current two-track direction and separate A9/A10 gates. Highest existing identifier is D-033; no methodological decision or new identifier was added.
- **Blocked:** Fresh remote branch verification failed because `github.com` could not be resolved. Cached references are not a fresh publication receipt.
- **Pending:** Implement stages 01 to 07 only after explicit approval; show integrity results before features. User reminders remain PDS dataset name/ID, institutional affiliation and duplicate-record housekeeping. No scientific analysis or data transformation was performed.

### 2026-09-06: Reasons for preparation and proposed reuse of excluded records

- **Verified user preference:** Explain the reason for each proposed step, including what it enables or which error it prevents. Keep replies short and numbered.
- **Verified discussion scope:** The user asked whether excluded records could be compressed into 5 to 10 weighted, column-average observations and returned to the analysis. This is a methodological question, not approval to transform data or revise D-025.
- **Inferred methodological assessment:** Such averages may describe excluded groups, but treating them as additional observed patients would lose individual cycle patterns and their links to outcomes. Arbitrary weights do not restore those links or supply independent observations. Preserve source records and distinguish row-level exclusions from whole-patient exclusions.
- **Pending alternatives:** Assess usable portions of incomplete records and, where assumptions are defensible, multiple imputation or missingness weighting as separately specified sensitivity analyses. Multiple imputation creates plausible versions of missing entries and combines estimates with uncertainty; it does not append invented average patients. Preserve the approved primary cohort. Any learned preprocessing for prediction must respect trial splits and prediction-time availability.
- **Verified sources consulted:** [Sterne et al., BMJ 2009](https://www.bmj.com/content/338/bmj.b2393) on imputation assumptions and uncertainty; [scikit-learn common pitfalls](https://scikit-learn.org/stable/common_pitfalls.html) on preprocessing leakage.
- **Verified execution boundary:** Documentation only. No restricted record was opened, excluded, transformed or deleted in this discussion; no new decision identifier or implementation approval was recorded.

### 2026-09-06: Educational walkthrough requested before local preparation

- **Verified user request:** Explain the proposed cleaning process step by step with invented before-and-after tables and a reason for each action, before starting implementation on this Mac. This request does not approve execution yet.
- **Verified code state:** The existing `src/audit/inventory_raw_data.py` is an inventory tool, not the A9 preparation pipeline. Its baseline heuristic must not silently become the cleaning definition.
- **Pending preparation sequence:** 01 freeze the training roster and verify joins; 02 harmonize visit labels while retaining within-cycle day; 03 check visit/day consistency using dictionary-defined trial time origins; 04 specify off-schedule and discontinuation visit handling; 05 harmonize test identities and verify units; 06 preserve missingness and bounded-result information, and distinguish exact duplicates from conflicting repeats; 07 define baseline using `LBBLFL` with timing and uniqueness checks. These are proposed operational details, not executed transformations or newly approved numerical thresholds.
- **Pending integrity checkpoint:** Reconcile source rows with retained/excluded/review categories; report patient/test/cycle coverage, unit conflicts, timing discrepancies, baseline ambiguity and missingness. The recorded 1,179 patients with visits in cycles 1 to 4 must not be described as proven complete numeric coverage for all twelve tests. The 663 deaths refer to all 1,600 training patients, not the final landmark-eligible subset.
- **Pending later work:** Select cycle snapshots under explicit duplicate/timing rules, build features and endpoint-specific landmark eligibility, then evaluate against baseline predictors with leave-one-trial-out validation. Early-cycle analyses must not require future visit completion; future measurements and held-out trial data cannot inform learned preprocessing. A10 approval remains separate.
- **Verified boundaries:** Only documentation and existing invented fixtures were read. No restricted patient contents were opened and no preparation code, derived data, feature, model, upload or deletion was produced. All teaching examples in the reply are invented; clinical meaning is not inferred from them. No new decision identifier was added.

### 2026-09-06 - Stage 01 executed, private transcription verified and documentation consolidated

- **Verified authorization:** user requested local Stage 01 execution, correct tests, progress/error reports, durable patient locations, fewer documents and a private PDF from supplied report text. Added D-034 for the scoped stage. No authorization was inferred for later modeling or Git publication.
- **Verified implementation:** new roster code and invented failure tests; 21 tests passed. All 18 source CSVs matched the original nested archives. Roster: 1,600 patients, zero duplicate keys; five event tables: 412,575 rows, zero unmatched keys. All patients retained regardless of laboratory completeness. Output read-back and mode 600 verified.
- **Verified errors and recovery:** initial UTF-8 decoding failure and then the evaluation literal-dot missing marker each stopped output safely. Fixed with reversible byte parsing/ASCII-key enforcement and explicit missing-marker handling, with regression tests. Free-text semantics and endpoint coding remain pending.
- **Verified private patient work:** read eight prior PDFs for dates and explicit cycle labels; created a labelled four-page transcription and structured data from the latest user text, outside Git. All 58 current rows and historical comparison columns survived text extraction. Rendered all four pages and inspected their layout. Original-PDF verification and confirmed latest cycle number remain pending; no patient values or identifiers were copied into project documentation.
- **Verified consolidation:** reduced docs from eleven to six. Retained useful provenance and limitations in the existing source matrix, dataset audit and execution plan. Removed only five tracked, unmodified duplicate/obsolete documents, recoverable at local HEAD 4b3dae8. Refreshed onboarding and agent instructions so patient paths and current scope persist across sessions.
- **Pending:** cycle/day/unit/baseline checks, source PDF for the latest transcription, private-output preservation/cleanup completion as recorded in the register, and any Git commit/push. No index-patient file is included in the DREAM preservation bundle. No restricted file was deleted.

**Stage 01 final verification receipt, 2026-09-06:** independently rechecked 1,600 unique roster keys, laboratory-row accounting, all 18 input hashes, executed code hash and roster hash. Five retired docs are absent; six remain. Markdown links, whitespace and patient-identifier checks passed. Only the new preparation code and invented tests are untracked. No commit or push occurred.

**Blocked preservation receipt:** stopped the stalled read-only cloud metadata request; a noninteractive retry timed out after 30 seconds and was terminated. No upload was attempted and no restricted file was deleted. The local Stage 01 bundle and private patient artifacts remain at their registered locations. This is a connectivity/access-check failure, not a new storage-permission question.

### 2026-09-06: Publication, documented functions and continued cleaning authorized

- **Verified user authorization:** first commit and push the permitted developments; then continue toward cleaned data stage by stage. Treat this as approval for preparation stages 02 to 07, retaining the integrity checkpoint before features and the separate A10 modeling gate. The user also authorized testing private cloud reads and a new write or edit; the original source remains immutable.
- **Verified publication preparation:** live GitHub main is 7392d50 and dataset-audit is 4b3dae8, matching the local branch references. Added function-level documentation to the existing Stage 01 implementation without changing its behavior. Its original executed code remains preserved in the restricted bundle with its original hash; the docstring revision has a different source hash.
- **Standing preference:** explain every production function, report reasons and error points after each stage, and keep user-facing updates TLDR. No new documentation files.
- **Pending:** commit/push verification, current cloud reachability and subsequent cleaning execution. Do not call authorization or a planned write a completed operation.

### 2026-09-06: Publication verified and pre-Stage-02 source measurements

- **Verified publication:** `dataset-audit` is published at `721d84a` and confirmed against the GitHub remote with a fresh `git ls-remote`. The working tree is clean and no restricted file entered Git.
- **Verified, aggregate only, training partition:** the unrecognized laboratory code `.` is `SODIUM`, `CHEMISTRY`, `MMOL/L` in all 6,151 of its rows and can be recovered rather than dropped. No test code carries more than one non-missing `LBSTRESU` across trials. Result formats are 194,714 numeric, 12,295 non-numeric text, 2,618 missing and 815 bounded originals, of which 540 lose their `<` or `>` bound in the standard character column. 112,167 rows disagree numerically between `LBSTRESN` and `LBSTRESC` and must be explained before values are used.
- **Verified coverage limitation:** rows carrying a `CYCLE` visit label include only `PSA` from ASCENT2 (1,882 rows); the wider panels come from CELGENE and EFC6546 alone. A multi-test per-cycle model is therefore a two-trial design, and ASCENT2 can only contribute PSA trajectories.
- **Verified baseline ambiguity:** `LBBLFL` equal to `Y` appears on 22,129 CELGENE, 16,101 EFC6546 and 6,143 ASCENT2 rows, and 15,639, 4,141 and 322 of those also carry a `CYCLE` visit label, so the supplied flag and the cycle labels overlap and cannot both define baseline without an explicit rule.
- **Blocked:** private Google Cloud is unreachable from this machine, so the authorized read and write connectivity test did not run.
- **No new decision identifier added.** Highest existing remains D-034.

### 2026-09-06: Stage 02 visit standardization and its consequence for trial composition

- **Verified method:** visit labels are translated by an exhaustive lookup table of the 29 observed (trial, label) pairs. An unenumerated, differently cased or differently spaced label is refused rather than parsed, so the source cannot change meaning without stopping the stage. Original text is retained and no laboratory value is read.
- **Verified result:** all 210,442 training laboratory rows received exactly one disposition, zero were dropped, and per-label counts matched the audited source exactly.
- **Verified design consequence:** a multi-test per-cycle analysis is supported by CELGENE at cycles 1 to 5 and by EFC6546 at cycles 2 to 5 only. EFC6546 cycle 1 holds a median of 4 test codes per patient against 26 later, and ASCENT2 cycle visits hold PSA alone. ASCENT2 therefore contributes PSA trajectories and a 13-code pre-enrolment baseline, not a per-cycle panel.
- **Verified open assumption:** only CELGENE states a day within the cycle. 58,839 EFC6546 and 1,882 ASCENT2 cycle-start rows carry an assumed rather than a stated day, which Stage 03 must test against `LBDT_PC`.
- **Added Q-014.** No new decision identifier; highest existing remains D-034.

### 2026-09-06: Stage 03 timing verification and the realistic per-cycle sample

- **Verified method:** the schedule used for checking was derived from the source rather than assumed. Cycle-start median days are 0, 21, 42, 63 and 84 in all three trials independently, giving an observed 21 day cycle, applied only as a check with a stated 10 day tolerance. A second check, that a patient's later cycle is never recorded on or before an earlier one, uses no schedule assumption at all.
- **Verified result:** zero cycle order violations across 1,600 patients, and a median deviation of 0 days in every trial and cycle bar one. The Stage 02 labels and the recorded dates agree. Q-014's sibling concern, that 60,721 cycle-start rows carried an assumed rather than a stated day, is resolved in favour of the labels.
- **Verified usable sample for a per-cycle panel study:** 922 patients, 403 CELGENE and 519 EFC6546, hold timing-verified cycle starts at cycles 2, 3 and 4. 726 hold cycles 1 to 4. This is the honest denominator for the planned design, against 1,600 in the roster and 1,124 in those two trials.
- **Verified hard boundary:** the largest recorded day anywhere is 84, so the laboratory record ends at twelve weeks. Cycles 1 to 4 are complete, cycle 5 is a truncated boundary case, and no per-cycle feature may assume observation beyond day 84.
- **Added Q-015.** No new decision identifier; highest existing remains D-034.

### 2026-09-06: Stage 04 research roles and a direct inspection of the outcome fields

- **Verified method:** one ordered rule set assigns every row a single purpose. A row that cannot be placed in time is excluded before its visit role is considered, because a measurement with no usable date cannot support a trajectory whatever its label says. Exclusion is recorded with a fixed reason and the row is retained, so a later question may still use it on stated grounds.
- **Verified result:** 136,681 cycle measurements, 44,155 baseline candidates, 15,341 mid-cycle measurements, 7,135 context only and 7,130 excluded, from 210,442 rows with none deleted.
- **Verified outcome structure:** `DEATH` blank means censored, not missing. `DISCONT` is absent for 111 patients and `ENTRT_PC` for 95, so the discontinuation endpoint has a smaller usable sample than the survival endpoint.
- **Verified confounding risk:** death rates are 72.4, 29.0 and 17.5 per cent in EFC6546, ASCENT2 and CELGENE, tracking median follow-up of 642, 357 and 279 days. Trial must enter any pooled survival model as a stratum.
- **Verified clock mismatch, now the leading methodological risk:** laboratory days run from first treatment while outcome days run from consent (ASCENT2, CELGENE) or randomization (EFC6546). No same-patient offset is measurable for the consent-referenced trials in the released data. EFC6546's offset is measurable at a median of 2 days.
- **Added Q-016 and Q-017.** No new decision identifier; highest existing remains D-034.

### 2026-09-06: Stage 05 settles the value column and closes the unit question

- **Verified and decisive:** `LBSTRESN` is a whole-number rounding of `LBSTRESC` throughout this source. All 194,814 of its parsable values are integers and 99.8 per cent of the 112,167 disagreements are reproduced exactly by rounding to the nearest integer. Q-011 is therefore RESOLVED: `LBSTRESC` is authoritative and `LBSTRESN` must never be used, because rounding to whole numbers destroys creatinine, bilirubin, potassium, calcium and neutrophil counts, whose entire clinical ranges span only a few units.
- **Verified:** 103 test codes, each with exactly one name and exactly one standardized unit across all three trials. No unit conversion is required or performed. The 42 codes with several original units were already harmonized by the sponsors into `LBSTRESU`.
- **Verified:** the code `.` is SODIUM and is recovered from its test name alone, never from the size of its result.
- **Verified caution:** 543 rows lost a `<` or `>` bound between the original and standardized columns and must not be read as exact values. A further 815 rows retain their bound and need an explicit rule at Stage 06.
- **Added Q-018.** No new decision identifier; highest existing remains D-034.

### 2026-09-06: Stage 06 value classification, repeat rules and real panel coverage

- **Verified method:** four kinds of entry are kept apart, since an absent cell, an uninterpretable text entry, a bounded result and an ordinary number are four different statements and none of the first three is a zero. Bounds are retained with direction and limit and yield no analysis value. Repeats are settled by an explicit rule per purpose, and a same-day conflict is left unresolved rather than decided arbitrarily.
- **Verified result:** 175,308 usable measurements from 210,442 rows, with none deleted and no value altered. 606 rows remain unresolved same-day conflicts.
- **Verified panel coverage, patients holding a usable measurement:** roughly 1,030 patients per chemistry and haematology test at cycle 2, near 1,000 at cycle 3 and 935 at cycle 4, with PSA higher at 1,403, 1,347 and 1,247. Cycle 1 is weak at 540 to 616 because EFC6546 barely measured it, which confirms Q-014's concern with numbers.
- **Verified weak test:** LDH reaches only 463 patients at cycle 2, less than half the coverage of every other panel test. Since LDH is a recognized prognostic marker in this disease, its inclusion is a genuine trade-off between a known signal and a halved sample.
- **Added Q-019.** Q-015 is now answered in method: the repeat rule selects the draw closest to what the visit is meant to describe. No new decision identifier; highest existing remains D-034.

### 2026-09-06: Stage 07 baselines and the completion of the authorized preparation

- **Verified method:** the baseline is the source's own flagged row where one is usable, otherwise the latest usable measurement on or before the first treatment day, otherwise none. Two disagreeing flags produce no baseline rather than an arbitrary pick. This resolves Q-013 in favour of the flag, with the timing check retained as a guard.
- **Verified and corrective:** a baseline is not the same thing as a pre-treatment visit. Most CELGENE baselines sit on the cycle 1 day 1 visit, at day 0, because that is the last draw before the first dose.
- **Verified result:** 38,623 baselines from 46,128 patient and test combinations, with 37,647 from the flag, 976 from the fallback and only 6 abandoned to conflicting flags. Panel coverage is roughly 1,500 to 1,565 of 1,600 patients for every test except sodium at 1,085 and LDH at 954.
- **Verified timing sanity:** median baseline day -2, and 38,551 of 38,623 within 28 days of the first dose. The 2,221 positive-day baselines are all exactly day 1 and all in EFC6546, consistent with a one-day numbering convention rather than a post-treatment measurement.
- **Status:** the authorized preparation is complete and the pipeline stops at the integrity checkpoint. No feature has been calculated and no model has been fitted.
- **Added Q-020.** No new decision identifier; highest existing remains D-034.

## Future update template

Copy this block for each future working session:

```markdown
### YYYY-MM-DD - Short session title

**Completed**

-

**Decisions**

- ID: decision and reason.

**Evidence / files**

-

**Problems or blockers**

-

**Next**

-
```


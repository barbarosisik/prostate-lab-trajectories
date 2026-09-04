# Research Log

Living record for decisions, plans, progress, blockers and changes in the **Prostate Lab Trajectories** project.

This file should be updated whenever we:

- Make or revise a research decision.
- Learn something material about a dataset.
- Change inclusion criteria, outcomes, features or modeling choices.
- Complete a task or encounter a blocker.
- Start or finish an analysis phase.

## Current snapshot

**Last updated:** 2026-09-04

**Project stage:** A5 complete; the dataset is fully audited at aggregate level; the blocking issue is now the pre-chemotherapy definition in the fixed question, recorded as Q-009

**Repository visibility:** Private

**Active objective:** Obtain the user's decision on Q-009, the meaning of pre-chemotherapy in the fixed research question, since the package supplies a median of only 2 distinct pre-treatment laboratory days per patient but a median of 7 across the full window. Then scope the analysable outcome families honestly before any cleaning. Cleaning at A9 and scientific analysis at A10 still require separate approval. The next agent reads the records, explains `docs/local-processing-and-cloud-storage-plan.md`, asks one approval question and waits at A0R. The agent-added BitLocker prerequisite is withdrawn at user direction, not passed. Cloud is storage only; cleaning and scientific analysis each require later approval. Local cleanup remains pending the all-files-backup exception or permitted backup and fresh exact-target confirmation.

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
| Q-009 | Does pre-chemotherapy in the fixed research question mean before docetaxel starts, or before each docetaxel cycle? | RESOLVED 2026-09-04 by the user: tests are taken around every chemotherapy cycle so that trends across cycles can be related to survival and recovery. The per-cycle reading is confirmed and the design is feasible |
| Q-005 | Which Vivli trials expose serial standard laboratory panels and chemotherapy-cycle dates? | External validation choice |
| Q-006 | Does Flatiron provide all standard blood values and reliable chemotherapy-cycle linkage, not only PSA? | Purchase/access decision |

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


# Research Log

Living record for decisions, plans, progress, blockers and changes in the **Prostate Lab Trajectories** project.

This file should be updated whenever we:

- Make or revise a research decision.
- Learn something material about a dataset.
- Change inclusion criteria, outcomes, features or modeling choices.
- Complete a task or encounter a blocker.
- Start or finish an analysis phase.

## Current snapshot

**Last updated:** 2026-08-25

**Project stage:** PDS access approved, dataset acquisition pending

**Repository visibility:** Private

**Active objective:** Obtain the approved PDS package when the user is home or has suitable protected storage, then verify the package, inspect the dictionary and run the tested aggregate inventory tool.

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
| D-017 | 2026-08-25 | Acquire the complete PDS bundle first, preserve it unchanged and verify checksum and ZIP safety before extraction. | The full bundle provides one traceable acquisition artifact while safe verification protects source integrity and the local filesystem. | Pending download |
| D-018 | 2026-08-25 | Maintain `PROJECT_CONTINUITY_LOG.md` as the operational memory and reminder queue, with methodological decisions also recorded in this research log. | The user needs durable cross-agent continuity, reminders and an exact account of developments while working away from home. | Active |

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
- [ ] Obtain the PDS DREAM data dictionary and supplied files. **Approved; manual download pending.**
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
| 4 | Obtain and inspect the PDS DREAM data dictionary. | Approved, download pending | User signed in and verified the PDS file listing; manual download is deferred until the user is home or has suitable protected storage |
| 5 | Define exact primary and secondary outcomes. | Planned | Statistical analysis plan section approved |
| 6 | Define pre-cycle timing and repeated-measure eligibility rules. | Planned | Frozen configuration and sensitivity windows |
| 7 | Prepare CHAARTED and external-validation access requests. | Planned | Submitted requests or documented access route |
| 8 | Produce the first source-coverage matrix. | Completed with documented unknowns | `docs/source-coverage-matrix.md`; source-column cells remain pending gated-file audit |
| 9 | Audit public CHAARTED fields and DREAM code clues. | Completed | `docs/chaarted-public-field-audit.md` and `docs/dream-public-code-audit.md` |
| 10 | Prepare a safe first-pass source inspector. | Completed | `src/audit/inventory_raw_data.py`; three synthetic-data tests pass |
| 11 | Create durable operational continuity and next-agent onboarding. | Completed | `PROJECT_CONTINUITY_LOG.md` and `NEXT_AGENT_ONBOARDING_PROMPT.md` |

## Open questions

| ID | Question | Needed for |
|---|---|---|
| Q-001 | Which PDS laboratory values have at least two eligible pre-cycle measurements in enough patients? | Final analysis feature set |
| Q-002 | Does the released ENTHUSE-33 package include the outcome fields needed for independent validation? | Discovery/validation split |
| Q-003 | Which treatment-tolerance variables are consistently dated across PDS trials? | Tolerance endpoint definition |
| Q-004 | Can progression be separated into radiographic, clinical and PSA progression in every source? | Outcome hierarchy |
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

## Update template

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


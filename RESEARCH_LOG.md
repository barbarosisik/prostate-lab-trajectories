# Research Log

Living record for decisions, plans, progress, blockers and changes in the **Prostate Lab Trajectories** project.

This file should be updated whenever we:

- Make or revise a research decision.
- Learn something material about a dataset.
- Change inclusion criteria, outcomes, features or modeling choices.
- Complete a task or encounter a blocker.
- Start or finish an analysis phase.

## Current snapshot

**Last updated:** 2026-08-24

**Project stage:** Setup and dataset-access preparation

**Repository visibility:** Private

**Active objective:** Confirm that PDS DREAM supports serial pre-chemotherapy laboratory trajectories linked to the required outcomes.

## Fixed research question

> Among patients with stage-IV metastatic prostate cancer receiving chemotherapy, how are serial pre-chemotherapy blood-test trajectories—individually and in combination—associated with survival, disease progression, treatment response and treatment tolerance, and how early can favorable or unfavorable patterns be detected?

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

## Master plan

### Phase 0 — Repository and protocol setup

**Goal:** Create a stable project home and freeze the first analysis definitions.

- [x] Select project name and private visibility.
- [x] Create research blueprint.
- [x] Create living research log.
- [ ] Add the data dictionary template.
- [ ] Draft the statistical analysis plan.
- [ ] Define outcome hierarchy and pre-cycle timing windows.

**Exit condition:** The project structure, inclusion criteria, endpoints and validation policy are documented before data modeling begins.

### Phase 1 — Data access and dataset audit

**Goal:** Prove which requested analyses are actually supported by the available fields.

- [ ] Create PDS and Synapse accounts if required.
- [ ] Obtain the PDS DREAM data dictionary and supplied files.
- [ ] Inventory tables, columns, join keys and date variables.
- [ ] Count patients and repeated observations per laboratory test and trial.
- [ ] Audit survival, progression, response and tolerance endpoints.
- [ ] Request CHAARTED D5, D7, D8, D9 and D11.
- [ ] Enquire about FIRSTANA, PROSELICA and TROPIC through Vivli.
- [ ] Request a Flatiron variable list and commercial-access details.

**Exit condition:** A source-by-source coverage matrix identifies which dataset supports which value, feature and outcome.

### Phase 2 — Cleaning and harmonization

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

### Phase 3 — Discovery analysis

**Goal:** Evaluate all usable laboratory trajectories in the PDS discovery data.

- [ ] Generate per-patient and population trajectory plots for every usable value.
- [ ] Calculate baseline, current level, changes, slopes, acceleration, volatility and threshold history.
- [ ] Test individual features against survival, progression, response and tolerance.
- [ ] Fit interpretable multivariable models.
- [ ] Explore nonlinear interactions and trajectory clusters where supported.
- [ ] Compare prediction landmarks after cycles 1, 2, 3 and 4.
- [ ] Report null, contradictory and unstable patterns.

**Exit condition:** Candidate findings are ranked with effect sizes, uncertainty, earliest detection time and internal cross-trial validation.

### Phase 4 — Controlled broadening

**Goal:** Test available findings in CHAARTED/E3805.

- [ ] Join linked CHAARTED submissions using common deidentified IDs.
- [ ] Rebuild longitudinal PSA features.
- [ ] Link PSA to dose, progression and survival.
- [ ] Apply frozen discovery definitions where compatible.
- [ ] Explain non-comparable fields instead of forcing a merge.

**Exit condition:** Findings are labeled portable, disease-setting-specific, unsupported or failed.

### Phase 5 — External validation and reporting

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
| 2 | Obtain and inspect the PDS DREAM data dictionary. | Planned | Saved field inventory and coverage matrix |
| 3 | Define exact primary and secondary outcomes. | Planned | Statistical analysis plan section approved |
| 4 | Define pre-cycle timing and repeated-measure eligibility rules. | Planned | Frozen configuration and sensitivity windows |
| 5 | Prepare CHAARTED and external-validation access requests. | Planned | Submitted requests or documented access route |

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

### 2026-08-24 — Project initialized

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

## Update template

Copy this block for each future working session:

```markdown
### YYYY-MM-DD — Short session title

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

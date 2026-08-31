# Prostate Lab Trajectories

A longitudinal data-science study of blood-test patterns measured before chemotherapy cycles in patients with stage-IV metastatic prostate cancer.

## Research question

> Among patients with stage-IV metastatic prostate cancer receiving chemotherapy, how are serial pre-chemotherapy blood-test trajectories, individually and in combination, associated with survival, disease progression, treatment response and treatment tolerance, and how early can favorable or unfavorable patterns be detected?

## What this project will produce

This is **not a PSA-only study**. Every sufficiently repeated laboratory value will be profiled, visualized and tested.

The intended outputs are interpretable statements such as:

- When value **X rises or falls faster** between specified chemotherapy cycles, the probability of outcome **Y** is higher, lower or unchanged by an estimated amount.
- A favorable or unfavorable pattern becomes detectable by **cycle N**, with uncertainty and validation results.
- When **X, Y and Z move together** in a particular way, survival, progression, response or treatment tolerance changes by an estimated amount.
- A value shows **no reliable relationship**, or its apparent relationship does not survive adjustment or validation.

These are association and early-warning results. They do not automatically prove that directly changing a blood value causes recovery.

## Initial study population

The discovery analysis starts narrowly with:

- Metastatic castration-resistant prostate cancer (mCRPC).
- Docetaxel-based chemotherapy.
- At least two usable blood measurements before chemotherapy cycles.
- Follow-up for at least one target outcome.

Starting narrowly keeps the treatment and disease setting coherent. Later phases test whether the findings generalize to broader metastatic populations. The project is not restricted to any country or ethnicity.

## Three-stage strategy

### 1. Discover

**Dataset:** Prostate Cancer DREAM Challenge / Project Data Sphere (PDS), using ASCENT2, MAINSAIL and VENICE, with ENTHUSE-33 assessed as an additional validation cohort.

**Work:** Analyze every usable repeated blood value alone and in combination. Measure starting level, change, slope, acceleration, instability and threshold crossings.

**Result:** A ranked map of favorable, unfavorable, null and potentially early-warning trajectories.

### 2. Broaden

**Dataset:** CHAARTED / E3805 linked submissions.

**Work:** Re-test the findings that are available, especially longitudinal PSA, in metastatic hormone-sensitive prostate cancer. Link longitudinal PSA, treatment exposure, progression and survival through the shared deidentified patient IDs.

**Result:** Evidence showing which signals generalize beyond the narrower discovery population and which appear disease-setting-specific.

### 3. Validate

**Dataset:** Independent Vivli chemotherapy trials or Flatiron Prostate Panoramic real-world data, after checking their data dictionaries.

**Work:** Freeze preprocessing, feature definitions, models and thresholds before testing them in patients not used for discovery or tuning.

**Result:** A final list of reproducible patterns, failed patterns and the earliest trustworthy detection windows.

## Dataset priorities

| Priority | Dataset | Intended role | Main gate |
|---|---|---|---|
| 1 | PDS DREAM | Multivariable trajectory discovery | Confirm released event-level laboratory and outcome fields, access terms and pre-cycle date linkage |
| 2 | CHAARTED / E3805 | Controlled broadening, especially PSA | Confirm and join D5, D7, D8, D9 and D11 using common patient IDs |
| 3A | Vivli trials | Independent chemotherapy-trial validation | Confirm FIRSTANA, PROSELICA and/or TROPIC availability and longitudinal laboratory fields |
| 3B | Flatiron Prostate Panoramic | Large real-world validation | Confirm CBC/CMP values, dates, chemotherapy cycles, dose changes, deaths and progression definitions before purchase |

Combining datasets will mean **harmonizing definitions and validating across sources**, not blindly appending rows from incompatible studies.

## Research foundations

The curated literature layer is in [`literature/`](literature/README.md):

- [`STUDY_CATALOG.md`](literature/STUDY_CATALOG.md) maps 22 studies to variables, outcomes, methods and limitations.
- [`references.bib`](literature/references.bib) contains reusable citations.
- [`download_manifest.csv`](literature/download_manifest.csv) records full-text access and validation status.
- Full-text PDFs and extracted text stay in the ignored local `literature/papers/` folder.

The active dataset-audit layer is in [`docs/`](docs/):

- [`dataset-field-coverage-checklist.md`](docs/dataset-field-coverage-checklist.md) defines every field, count and feasibility gate that must be checked.
- [`pds-dream-access-audit.md`](docs/pds-dream-access-audit.md) records the official PDS/Synapse package, file IDs, public table semantics and current access blocker.
- [`source-coverage-matrix.md`](docs/source-coverage-matrix.md) separates verified, partial, unknown and not-yet-audited coverage by source and PDS trial.
- [`chaarted-public-field-audit.md`](docs/chaarted-public-field-audit.md) records what the public CHAARTED submissions can and cannot support.
- [`dream-public-code-audit.md`](docs/dream-public-code-audit.md) records schema clues from public DREAM code without treating it as patient data.
- [`raw-data-inventory-tool.md`](docs/raw-data-inventory-tool.md) explains the read-only, aggregate inspection tool prepared for the approved files.

The project continuity layer is:

- [`PROJECT_CONTINUITY_LOG.md`](PROJECT_CONTINUITY_LOG.md), the operational memory, reminder queue, current blocker and exact execution plan.
- [`NEXT_AGENT_ONBOARDING_PROMPT.md`](NEXT_AGENT_ONBOARDING_PROMPT.md), the ready-to-paste prompt for the next GPT-5.6 Sol agent.
- [`RESEARCH_LOG.md`](RESEARCH_LOG.md), the formal research decisions, phase plan and dated scientific progress.

## Canonical project home

The canonical project is the private GitHub repository:

`https://github.com/barbarosisik/prostate-lab-trajectories`

No permanent local project copy should remain after an approved session closeout. Agents may use an authenticated temporary clone while working, but GitHub `main` is the project record. Raw data remains outside GitHub in approved protected storage.

When the user requests an onboarding prompt or next-agent handoff, also begin the publication-and-cleanup workflow in `NEXT_AGENT_ONBOARDING_PROMPT.md`. Verify the remote record, disclose local-only files, obtain fresh confirmation for exact deletion targets, remove the approved temporary project folders and recheck the filesystem. Future sessions can clone again. See `AGENTS.md` for the automatic agent entry point. This rule does not authorize publishing restricted files or deleting shared app history.

## Required data

### Essential identifiers and timing

- Deidentified patient ID and source trial/site.
- Chemotherapy date, regimen, dose and cycle number.
- Blood-sample collection date/time.
- Laboratory test name, numeric result, unit and reference limits.
- A reproducible rule linking each result to the next chemotherapy cycle.

### Essential patient and disease context

- Metastatic status and metastatic sites.
- Castration-resistant or hormone-sensitive disease setting.
- Baseline age and performance status, when available.
- Prior and concurrent cancer treatments.
- Baseline disease burden and important clinical characteristics.

### Target outcomes

- Overall survival time and death/censoring status.
- Dated clinical, radiographic and PSA progression when available.
- Dated PSA and imaging response assessments.
- Treatment delay, dose reduction, missed cycle, severe toxicity and discontinuation.

## Features calculated for every usable value

- Baseline level.
- Most recent level before each cycle.
- Absolute and percentage change from baseline and previous cycle.
- Slope: speed of rise or fall per day/week/cycle.
- Acceleration: whether the rise or fall is becoming faster or slower.
- Volatility: stability versus irregular jumps.
- Time outside the reference range.
- First threshold crossing and recovery time.
- Joint patterns and interactions among multiple values.

At least two observations are needed for a slope. At least three are required for acceleration, curvature or meaningful volatility.

## Analysis workflow

1. **Audit:** Count patients, tests, cycles and outcomes; measure missingness by trial and time.
2. **Harmonize:** Standardize test names, units, dates, reference ranges and outcome definitions while retaining original fields.
3. **Visualize:** Plot every usable value at patient and population level, grouped by outcomes.
4. **Screen individually:** Test levels and trajectory features for each value against all four outcome families.
5. **Model trajectories:** Use longitudinal, landmark, time-updated survival and joint models as appropriate.
6. **Combine values:** Begin with interpretable penalized models; compare nonlinear models for interactions when justified.
7. **Detect early:** Re-run predictions at cycles 1, 2, 3 and 4 to identify the earliest reliable signal.
8. **Validate:** Split by trial/source, freeze the analysis and test once in an untouched cohort.
9. **Report everything:** Include positive, negative, null, contradictory and non-reproducible results.

## Cleaning rules

- Never use future measurements when predicting an earlier outcome.
- Keep original values, units and test names alongside standardized versions.
- Never convert `NOT DONE`, below-detection or text values silently to zero.
- Remove exact duplicates and document how same-day repeat tests are resolved.
- Use the closest eligible pre-dose result inside a prespecified window; begin with 0–7 days and test 0–3 and 0–14 days as sensitivity analyses.
- Treat missingness as information to audit, not as automatically random noise.
- Harmonize censoring and endpoint definitions before pooling studies.
- Preserve a complete transformation log from source data to analysis tables.

## Planned repository structure

```text
prostate-lab-trajectories/
├── README.md
├── RESEARCH_LOG.md
├── PROJECT_CONTINUITY_LOG.md
├── NEXT_AGENT_ONBOARDING_PROMPT.md
├── literature/
│   ├── README.md
│   ├── STUDY_CATALOG.md
│   ├── references.bib
│   ├── download_manifest.csv
│   └── papers/           # Local only; ignored by Git
├── data/
│   ├── README.md
│   ├── raw/              # Never committed
│   ├── interim/          # Never committed if patient-level
│   └── processed/        # Only non-sensitive or approved outputs
├── docs/
│   ├── dataset-field-coverage-checklist.md
│   ├── pds-dream-access-audit.md
│   ├── source-coverage-matrix.md
│   ├── chaarted-public-field-audit.md
│   ├── dream-public-code-audit.md
│   └── raw-data-inventory-tool.md
├── notebooks/
├── src/
│   ├── audit/
│   ├── cleaning/
│   ├── features/
│   ├── models/
│   └── visualization/
├── tests/
└── results/              # Aggregated, disclosure-checked outputs only
```

## Data governance

- Do not commit patient-level, restricted, licensed or identifiable data.
- Store credentials only outside the repository.
- Follow the data-use agreement for every source.
- Commit only aggregated outputs after disclosure checks.
- Record every material methodological decision in [`RESEARCH_LOG.md`](RESEARCH_LOG.md).
- Record every operational development, blocker, reminder and exact next action in [`PROJECT_CONTINUITY_LOG.md`](PROJECT_CONTINUITY_LOG.md).

## Immediate next steps

1. The complete package is secured and checksum-verified in PDS-approved private Google Cloud Storage.
2. Obtain explicit approval before creating a paid private Google Cloud computing environment.
3. Extract and inspect the restricted package only inside that protected environment.
4. Inspect every sheet of the official data dictionary.
5. Run the tested aggregate inventory tool against every supplied CSV.
6. Confirm whether serial laboratory dates can be aligned to actual chemotherapy administrations rather than only nominal visits.
7. Explain the verified feasibility results in plain language and obtain user approval before cleaning.
8. Freeze the first data-cleaning and restructuring specification only after the actual columns are verified.
9. Prepare the CHAARTED patient-data request using the completed public compatibility audit.

## Project status

**Current stage:** PDS package secured in approved private Google Cloud Storage; local restricted copies removed after complete verification; protected cloud-computing audit pending approval.

Read [`PROJECT_CONTINUITY_LOG.md`](PROJECT_CONTINUITY_LOG.md) first for the current blocker, reminders and exact next action. See [`RESEARCH_LOG.md`](RESEARCH_LOG.md) for research decisions and dated scientific progress.


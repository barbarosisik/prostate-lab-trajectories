# Project Continuity Log

## Purpose

This is the operational memory and handoff file for the Prostate Lab Trajectories project. It complements, but does not replace, `RESEARCH_LOG.md`.

Use this file to preserve:

- What happened in each working session.
- What was verified and what remains an assumption.
- What the user must be reminded to do.
- Current access, storage and browser blockers.
- Exact next actions and their order.
- Decisions that a future agent must not silently reverse.
- Links to the detailed evidence and implementation files.

Every agent continuing this project must read this file first, then read `RESEARCH_LOG.md`, `README.md` and the relevant documents listed in the onboarding order below.

## Maintenance rules

1. Update the Current snapshot whenever the active blocker or next action changes.
2. Add a dated session entry after every meaningful action, discovery, failure, user decision or approval.
3. Put methodological decisions in `RESEARCH_LOG.md` as well as summarizing them here.
4. Never put passwords, login codes, private download links, patient identifiers or patient values in this file.
5. Clearly label facts as verified, pending, inferred or blocked.
6. Never report a download, file inspection or test as completed without direct evidence.
7. Keep raw and restricted data outside Git.
8. Do not use em dashes in project files or user-facing responses.

## Current snapshot

**Last updated:** 2026-08-25

**Project stage:** PDS access approved, dataset acquisition pending

**Primary source:** Project Data Sphere Prostate Cancer DREAM Challenge

**Current dataset page:** `https://data.projectdatasphere.org/projectdatasphere/html/content/0abbd47a-dcfb-42c2-a036-af1898ea3c1c`

**Current dataset ID:** `Prostat_na_2006_149`

**Current user situation:** The user is away from home and cannot complete the large download on the current computer. The user expects to download it later at home or use suitable protected storage.

**Immediate blocker:** No PDS file has been downloaded yet. The signed-in page shows the approved files, but automated activation of the Download links did not start a browser download. Manual download is required unless the site behavior changes.

**Immediate next action:** When the user is home, remind them to sign in to PDS and manually click Download beside `AllProvidedFiles_149.zip`. If local space is insufficient, review the access terms before choosing any alternative storage. Do not place restricted patient data in public or ordinary personal cloud storage.

**After download:** Locate the file, verify its name and size, calculate a SHA-256 checksum, list its contents without extracting, check for unsafe ZIP paths, store it under ignored restricted storage, then inspect the dictionary and run the aggregate inventory tool.

## User communication requirements

- Use simple, non-medical language first.
- Explain why a step is necessary before starting a new major stage.
- Ask for approval when a new major stage or consequential choice begins.
- Give brief summaries of what was done, reached, learned and planned.
- Do not use em dashes.
- Do not overwhelm the user with unexplained medical or statistical terms.
- If technical terms are necessary, define them immediately in everyday language.
- Remind the user of deferred tasks when their required situation arrives, especially the home download.

## Fixed research identity

### Research question

> Among patients with stage-IV metastatic prostate cancer receiving chemotherapy, how are serial pre-chemotherapy blood-test trajectories, individually and in combination, associated with survival, disease progression, treatment response and treatment tolerance, and how early can favorable or unfavorable patterns be detected?

### Non-negotiable scope

- This is not a PSA-only study.
- Analyze every blood-test value that repeats often enough to support a responsible analysis.
- Start with a narrow discovery group, then broaden, then validate independently.
- Do not restrict the project to one country or ethnicity.
- Treat results as associations unless causal evidence exists.
- Report positive, negative, null, contradictory and failed findings.

### Three-stage source strategy

1. **Discovery:** PDS DREAM training data from ASCENT2, MAINSAIL and VENICE.
2. **Controlled broadening:** CHAARTED/E3805, especially longitudinal PSA linked to survival and progression.
3. **Independent validation:** Vivli trials or Flatiron only after exact field availability is confirmed.

## Access and acquisition status

### Verified PDS approval state

- The PDS registration and data-access application was accepted on 2026-08-25.
- The user successfully signed in to PDS.
- The approved DREAM contribution is visible and marked Available for Download.
- The contribution contains 2,070 patients.
- The contribution page lists the complete file package, dictionary, training package, leaderboard package and final-scoring package.

### Verified PDS file listing

| Type | Filename | Current state |
|---|---|---|
| Complete package | `AllProvidedFiles_149.zip` | Visible, not downloaded |
| Data dictionary | `Challenge_data_dictionary v2.xlsx` | Visible, not downloaded |
| Training package | `prostate_cancer_challenge_data_training.zip` | Visible, not downloaded |
| Leaderboard package | `prostate_cancer_challenge_data_leaderboard.zip` | Visible, not downloaded |
| Final-scoring package | `prostate_cancer_challenge_data_finalscoringset.zip` | Visible, not downloaded |
| CRF location document | `PCDC Protocol, CRF Location.docx` | Visible, not downloaded |

### Verified training files listed inside the package

- `CoreTable_training.csv`
- `LabValue_training.csv`
- `LesionMeasure_training.csv`
- `MedHistory_training.csv`
- `PriorMed_training.csv`
- `VitalSign_training.csv`
- `Challenge_data_dictionary v2.xlsx`

### Browser download issue

The correct page and Download controls were verified. Automated attempts used the page's semantic link, visible DOM control and physical browser click. No browser download event occurred and no new file appeared in the Windows Downloads folder. Do not report the package as downloaded.

The user was therefore asked to manually download `AllProvidedFiles_149.zip` later at home. The dataset page was left open for handoff during the session, but future agents must not assume the browser tab or signed-in session still exists.

## Storage and privacy rules

### Required rules

- Never commit patient-level or restricted data to GitHub.
- Never paste patient rows into chat, logs, issues, commits or public documents.
- Never upload the package to ordinary cloud storage without first confirming the PDS terms permit it and the destination is appropriately protected.
- Never expose passwords, security codes, SAS credentials, session cookies or private signed URLs.
- Keep the original package unchanged.
- Keep checksums and acquisition metadata separate from patient values.
- Commit only aggregated, disclosure-checked outputs when permitted.

### Preferred local layout after download

```text
data/
  raw/
    pds_dream/
      source/
        AllProvidedFiles_149.zip
      extracted/
  interim/
    pds_inventory.json
```

Both `data/raw/` and `data/interim/` are ignored by Git. Before moving or copying the downloaded package, verify the exact source and destination paths. Preserve the original ZIP.

### If the user's home computer lacks space

Follow this order:

1. Check the actual download size and available disk space.
2. Consider an encrypted external drive controlled by the user.
3. Consider the secure PDS SAS environment if the data-use agreement and workflow support analysis there.
4. Consider another institution-approved protected location only after confirming authorization.
5. Do not use a public link, shared personal drive or ordinary cloud folder merely for convenience.

## Work completed so far

### Repository and protocol foundation

- Created the private `prostate-lab-trajectories` repository.
- Fixed the research question and three-stage strategy.
- Created `README.md` and `RESEARCH_LOG.md`.
- Established privacy rules and ignored raw/restricted data paths.
- Preserved the user's instruction to study all sufficiently repeated blood tests.

### Literature foundation

- Curated 22 core and supporting studies.
- Created `literature/STUDY_CATALOG.md`.
- Created `literature/references.bib`.
- Created `literature/download_manifest.csv`.
- Downloaded and validated 10 full-text papers locally.
- Kept papers and extracted text outside Git.

### PDS public audit

- Located official PDS contribution `Prostat_na_2006_149`.
- Confirmed DOI `10.34949/e6c8-v326`.
- Located official Synapse project `syn2813558` and public documentation.
- Confirmed event-level training laboratory data through approximately day 84.
- Confirmed likely fields such as `LBDT_PC`, `LBBLFL`, `LBSTRESC`, `LBSTAT`, `LBNRIND` and `VISIT`.
- Confirmed public release table families and documented absent or unproven treatment-administration, adverse-event and progression event tables.

### Public CHAARTED audit

- Confirmed D8 is described as longitudinal PSA.
- Confirmed D5 contains survival and several progression outcomes.
- Confirmed D7 includes treatment data and PSA progression.
- Confirmed D9 contains chemotherapy total dose.
- Confirmed linked submissions use common identifier `group_uid`.
- Kept exact per-cycle administration timing as unverified.

### Public DREAM code audit

- Inspected the public winning-solution repository without treating it as patient data.
- Confirmed likely core outcome fields including `RPT`, `STUDYID`, `DEATH`, `LKADT_P`, `DISCONT`, `ENDTRS_C` and `ENTRT_PC`.
- Identified baseline laboratory clues including albumin, hemoglobin, PSA, alkaline phosphatase, LDH, ALT, AST, calcium, creatinine, neutrophils, platelets, bilirubin, testosterone, WBC, magnesium, phosphorus, total protein and RBC.
- Recorded that public code does not prove longitudinal coverage, source counts or actual treatment dates.

### Safe inventory tool

- Implemented `src/audit/inventory_raw_data.py` using Python standard-library code.
- The tool reads CSV files without changing them.
- The report contains table names, columns, row counts, missingness, recognized field coverage and aggregate repeated-lab counts.
- It does not write patient identifiers or laboratory result values to the report.
- It warns when no recognized actual chemotherapy administration date is found.
- Added synthetic CoreTable and LabValue fixtures with invented patients.
- Added three unit tests.
- All three tests passed on 2026-08-25.

## Important evidence files

Read these before making source or analysis decisions:

1. `PROJECT_CONTINUITY_LOG.md`
2. `RESEARCH_LOG.md`
3. `README.md`
4. `docs/pds-dream-access-audit.md`
5. `docs/dataset-field-coverage-checklist.md`
6. `docs/source-coverage-matrix.md`
7. `docs/raw-data-inventory-tool.md`
8. `docs/chaarted-public-field-audit.md`
9. `docs/dream-public-code-audit.md`
10. `literature/README.md`
11. `literature/STUDY_CATALOG.md`
12. `literature/download_manifest.csv`
13. `literature/references.bib`

## Repository and Git state

**Canonical project home:** `https://github.com/barbarosisik/prostate-lab-trajectories`

**Canonical branch:** `main`

**Permanent local path:** None. The former path `C:\Users\BarbarosIsikGreenhou\Documents\Codex\2026-08-24\s\prostate-lab-trajectories` is retired and must not be treated as the project home.

**Future working copies:** Use a fresh authenticated clone in the active task workspace when needed. Verify the remote, branch and current GitHub commit before editing.

**Authorization boundary:** The user explicitly authorized publishing the current permitted project files and deleting the former local folder in the 2026-08-25 migration session. Future commits, pushes, history changes or repository-setting changes still require fresh explicit authorization.

## Core feasibility questions that remain unanswered

1. What are the exact columns and data types in the received dictionary and CSV files?
2. What is the complete laboratory-test list by trial?
3. How many patients have at least 2, 3 and 4 valid measurement days for each test?
4. Are exact chemotherapy administration dates present anywhere?
5. Can each lab measurement be linked to the next actual chemotherapy administration?
6. Are dose, cycle, reduction, delay or missed-cycle fields present?
7. Which survival, progression, response and treatment-tolerance outcomes are present and dated?
8. Does the current final-scoring package reveal useful ENTHUSE-33 longitudinal data or outcomes?
9. Are units and test names consistent enough for cross-trial use?
10. Are patient joins unique and complete across all tables?

No cleaning specification or scientific conclusion may be finalized before these questions are answered from the actual files.

## Execution plan from the current point

### Stage 1: Acquire the approved package

**Trigger:** User is home or has authorized protected storage.

**Actions:**

1. Remind the user to sign in to PDS.
2. Open the approved DREAM contribution.
3. Manually download `AllProvidedFiles_149.zip`.
4. Confirm the actual completed file path and size.
5. Check available storage before copying or extracting.
6. Review any download terms or restrictions shown by PDS.

**Completion evidence:** A real file exists at a verified path and has a nonzero size.

### Stage 2: Securely verify the package

**Actions:**

1. Calculate SHA-256.
2. Record filename, timestamp, size, source page and checksum in a non-sensitive acquisition record.
3. List ZIP members without extraction.
4. Reject absolute paths, parent-directory paths and other unsafe ZIP members.
5. Confirm expected dictionary and CSV names.
6. Extract only into ignored `data/raw/pds_dream/extracted/` after path validation.

**Completion evidence:** Safe member list, checksum and expected files verified.

### Stage 3: Inspect the official dictionary

**Actions:**

1. Read every dictionary sheet.
2. Record table, column, type, meaning, missing-value code, unit and timing definition.
3. Map documented fields to the field-coverage checklist.
4. Keep unknown or contradictory definitions explicit.

**Completion evidence:** Column-level dictionary audit with no patient values.

### Stage 4: Run the safe inventory

**Actions:**

1. Run the existing synthetic tests first.
2. Run `src/audit/inventory_raw_data.py` on the extracted CSV directory.
3. Save aggregate JSON only to ignored interim storage.
4. Check that no patient identifiers or result values appear in the report.
5. Summarize counts in plain language for the user.

**Completion evidence:** Aggregate inventory report, verified privacy properties and test results.

### Stage 5: Make the actual-timing decision

**Decision A:** Exact administrations are available.

- Define true pre-chemotherapy windows using actual administration dates.

**Decision B:** Only visits or relative days are available.

- Use visit-based or calendar-based language.
- Do not call the results true pre-administration findings.
- Consider whether another source is required for treatment tolerance and dose timing.

**User checkpoint:** Explain the evidence simply and obtain approval before cleaning begins.

### Stage 6: Freeze the cleaning and analysis specification

Define only after the audit:

- Patient inclusion and exclusion.
- Repeated-measure minimums.
- Lab name and unit mapping.
- Missing, `NOT DONE`, detection-limit and duplicate rules.
- Timing windows and tie-breaking.
- Survival and censoring definitions.
- Progression, response and treatment-tolerance definitions.
- Leakage prevention.
- Trial split and validation policy.

### Stage 7: Implement cleaning and quality checks

- Preserve raw files unchanged.
- Create reproducible derived tables.
- Add tests for joins, units, time ordering, duplicates and no-future-data rules.
- Produce missingness and data-quality reports.
- Do not publish patient-level outputs.

### Stage 8: Describe all usable laboratory trajectories

- Count and plot every usable value.
- Report starting level, changes, slopes, acceleration and instability where measurement counts support them.
- Explain sparse or unusable tests instead of silently dropping them.

### Stage 9: Discovery modeling

- Test each value against survival, disease progression, treatment response and treatment tolerance.
- Begin with interpretable models.
- Test combinations only after individual signals and data quality are understood.
- Compare earliest usable landmarks after treatment periods 1, 2, 3 and 4.
- Report uncertainty and multiplicity control.

### Stage 10: Controlled broadening and validation

- Request or obtain CHAARTED linked submissions.
- Rebuild longitudinal PSA features and test compatible findings.
- Select Vivli or Flatiron only after exact variables are confirmed.
- Freeze definitions before independent validation.
- Report successful, failed, source-specific and unresolved findings.

## Decision gates

| Gate | Evidence required | If evidence is absent |
|---|---|---|
| Package obtained | File exists, size verified, checksum recorded | Stop and resolve download/storage |
| Dictionary verified | All sheets and columns inspected | Do not write cleaning rules |
| Patient joins valid | Key uniqueness and unmatched counts known | Do not merge tables |
| Repeated labs sufficient | Counts by trial, test and patient | Restrict or describe sparse tests |
| Actual chemotherapy timing | Verified administration field and linkage | Use honest visit/calendar terminology |
| Outcomes available | Exact fields, definitions and timing | Narrow outcome claims |
| Cleaning frozen | Written rules and tests approved | Do not model |
| Internal validation ready | Trial/source split and leakage checks | Do not present performance as reliable |
| External source compatible | Column-level coverage confirmed | Do not purchase or request blindly |

## Reminder queue

### Highest priority reminder

When the user is back home:

> Please download `AllProvidedFiles_149.zip` from the approved PDS DREAM dataset page. Tell me the completed file path and whether the computer has enough space for safe extraction. Do not upload it to ordinary cloud storage.

### After the user says downloaded

- Verify the file exists before taking any other action.
- Ask before moving it if the destination changes the user's storage arrangement.
- Inspect and checksum before extraction.
- Review any applicable PDS conditions.
- Run dictionary audit and aggregate inventory before cleaning.

### Later reminders

- Explain timing feasibility to the user before cleaning.
- Ask for approval before finalizing outcome definitions.
- Request CHAARTED only after the PDS coverage gaps are known.
- Consider Vivli or Flatiron only after CHAARTED and PDS compatibility are clear.

## Dated operational history

### 2026-08-24: Project foundation

- Fixed the research question.
- Confirmed all sufficiently repeated blood values are in scope.
- Established discovery, broadening and validation stages.
- Created private repository, README and research log.
- Began curated literature foundation.

### 2026-08-24: Literature foundation

- Curated 22 studies and created catalog, BibTeX and manifest.
- Downloaded and validated 10 local papers.
- Kept full-text materials ignored by Git.

### 2026-08-25: PDS and Synapse public audit

- Located official dataset, dictionary, packages and Synapse IDs.
- Verified public lab timing and field clues.
- Identified actual administration timing as a critical unproven requirement.
- Created the field-coverage checklist and source matrix.

### 2026-08-25: PDS application and waiting-period work

- Submitted PDS application.
- Audited public CHAARTED descriptions and DREAM code.
- Built and tested the aggregate safe inventory tool using invented data.
- Deliberately postponed cleaning rules until actual columns can be inspected.

### 2026-08-25: PDS access approved

- User reported approval.
- Opened PDS login page in the in-app browser.
- User signed in successfully.
- Opened Access Data and found the approved DREAM contribution.
- Verified 2,070 patients and all listed packages.
- Tried automated download controls using several browser interaction methods.
- No download event occurred and no new file appeared in Downloads.
- Left the correct dataset page available and instructed the user to manually download `AllProvidedFiles_149.zip`.
- User explained they are currently away from home and need to postpone the large download or use suitable storage.

### 2026-08-25: Continuity system created

- Created this project continuity log at the user's request.
- Created `NEXT_AGENT_ONBOARDING_PROMPT.md` as a reusable handoff prompt.
- Updated core project status documents to reflect PDS approval and acquisition pending.

## Session update template

Append one block for every future working session:

```markdown
### YYYY-MM-DD: Short session title

**User situation and request**

-

**Completed**

-

**Verified evidence**

-

**Decisions**

-

**Problems or blockers**

-

**Reminder added or cleared**

-

**Exact next action**

-
```

## Onboarding pointer

Use `NEXT_AGENT_ONBOARDING_PROMPT.md` when starting a new GPT-5.6 Sol task. That prompt requires the next agent to read this continuity log and the evidence files before acting.


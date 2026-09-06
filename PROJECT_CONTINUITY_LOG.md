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

**Last updated:** 2026-09-06

**Verified current stage:** preparation Stages 01 to 05 are complete. Stage 05 found that the numeric value column `LBSTRESN` has been rounded to whole numbers throughout the source and rejected it in favour of `LBSTRESC`, and confirmed that every test code carries one name and one standardized unit. Stage 04 assigned one research purpose to each of the 210,442 rows with 3.4 per cent excluded, all reasons stated and no row deleted. A direct inspection of the outcome fields found that the laboratory clock and the outcome clock use different reference days. Stage 03 corroborated every cycle label against the recorded collection day with zero cycle order violations across 1,600 patients, and identified 922 patients holding timing-verified cycle starts at cycles 2 to 4. Stage 02 translated all 29 observed visit labels through an exhaustive per-trial lookup table, dispositioned all 210,442 laboratory rows with zero dropped, and wrote a value-free visit index. Stage 01 remains as recorded below. Its frozen roster retains 1,600 training patients. Zero duplicate core keys; zero unmatched joins across 412,575 event rows. All 18 source CSVs match the original archive. Output CSV read-back and 21 tests passed. Laboratory results and outcome codes were not transformed.

**Verified errors resolved for this stage:** three training tables contain non-UTF-8 bytes; a reversible byte parser checks ASCII keys without guessing free-text encoding. Withheld evaluation outcomes use literal `.` markers. Earlier attempts stopped before writing a roster. Semantic text encoding and outcome coding remain later checks.

**Verified patient locations:** `/Users/barbarosisik/PDS-Restricted-Work/goal-patient/` for PDFs; `/Users/barbarosisik/PDS-Restricted-Work/index-patient/` for extracted/transcribed data. Eight pre-existing PDFs were inspected for dates/cycle labels. The latest user-pasted report is now a labelled private four-page PDF with 58 current entries; all rows passed text read-back, and all rendered pages were inspected. Its original PDF is unavailable, latest cycle number is inferred only, and the missing unit is unresolved. Exact artifacts and hashes are in the data register.

**Verified documentation cleanup:** docs reduced from eleven to six. Five tracked duplicates removed after preserving useful content; no patient or untracked data file deleted. Patient paths, scope and TLDR/reasons/error-reporting instructions are durable in AGENTS and onboarding. No new research documentation files were created.

**Pending next action:** Stages 02 to 05 are complete and verified. The value column question is settled: use `LBSTRESC`, never `LBSTRESN`. Continue with Stage 06, separating real measurements from absent results, bounded results and duplicates. The laboratory and outcome clocks still differ and must be resolved before any analysis that mixes laboratory time with outcome time. A10 modeling remains separate. Continue the PDS-first user-side source search; no dbGaP application. Affiliation and Downloads duplicate housekeeping remain unanswered/unverified.

**Storage and Git:** this Mac only, approved private Google Cloud storage only, source unchanged. Restricted files remain local. See the data register for output preservation and exact-target cleanup status. Branch dataset-audit is published and verified at `721d84a` on both the local clean working tree and the GitHub remote, checked with a fresh `git ls-remote` on 2026-09-06. No restricted deletion occurred. Private Google Cloud is currently unreachable from this machine, so the authorized read and write connectivity test did not run.

## Data-plan execution tracker

Active run: `2026-09-04-audit-001`. Earlier approvals and publication are historical in A0/A1. A0R is complete. Stage 01 preparation was explicitly authorized 2026-09-06; do not reopen the initial-audit approval. Update this table after meaningful steps. Full plan: `docs/local-processing-and-cloud-storage-plan.md`; locations: `docs/data-location-register.md`.

| Step | Work and completion evidence | Status |
|---|---|---|
| A0 | Record approval of local setup, first read-only audit, verified cloud output upload and corrected data-free instruction publication | DONE: direct user approval recorded |
| A0R | After mandatory reading, the next agent explains the local data plan, locations, costs, outputs and later gates, asks one approval question, then waits | DONE: plan presented 2026-09-04; the user waived further explanation, replied "no need" and directed execution to begin with the run-root step. Later gates at A9 and A10 are unaffected |
| A1 | Commit only the ten reviewed data-free project documents to main, push normally and verify remote commit and required file contents | DONE: normal push and fresh `git ls-remote` verified `9843e5b86a89c4f5ca583a60f1906c69032ee9c8`; its content-addressed tree contains all ten documents and the approved tracker |
| A2 | After A0R approval, check only the intended local path, capacity, containment, non-synchronization and folder access | DONE 2026-09-04: realpath match, no symlink in the chain, mode 700 owned by `barbarosisik:staff`, outside Desktop/Documents/CloudStorage/Mobile Documents and outside the Git repo, 416 GiB free, zero files present. iCloud Drive confirmed effectively off. Encryption status deliberately not checked and not a gate |
| A3 | Register/create the exact local run root, configure its permissions and process temp paths, prepare local Google Cloud CLI sign-in and isolated Python dependencies | PARTIAL 2026-09-04: run root created, permissions set to 700, subfolders `source`/`extracted`/`interim`/`reports`/`tmp`/`verify` in place, and the path registered in `docs/data-location-register.md`. DONE 2026-09-04: run root created with mode 700 and registered; Python 3.12.8 installed and verified; Google Cloud CLI 583.0.0 installed at `~/tools/google-cloud-sdk` and confirmed to run with `CLOUDSDK_PYTHON` persisted in `~/.zshrc`; isolated environment `~/tools/venv-pds-audit` created with pinned `openpyxl==3.1.5`; all 3 synthetic-fixture tests pass on this machine; `gcloud auth login` completed as `barbarosisik7@gmail.com` with project `pds-dream-secure-storage` set. The first CLI attempt had failed because macOS Python is 3.9.6 and the CLI needs 3.10 or newer, and no macOS bundled-Python build is published. Tooling lives in `~/tools`, never in the restricted root. No restricted files exist |
| A4 | Refresh source/bucket security metadata, pin object generation, download to the registered path and verify exact bytes/SHA-256 | DONE 2026-09-04: bucket `EUROPE-WEST4`, public access prevention enforced, uniform bucket-level access on, no public IAM binding, and the source is the only object in the bucket. Generation `1787841139282260` pinned and downloaded to `runs/2026-09-04-audit-001/source/AllProvidedFiles_149.zip`, set to mode 400. Verified 6,227,480 bytes, SHA-256 `AB3ECA19...932391` matching the 2026-08-27 record, and MD5 `0F8633E474B581317CB66F1783A84AD8` matching live cloud metadata. Archive scanned without extracting: all entries CRC-clean, no absolute paths, no traversal, no symlinks, no encryption, expansion ratio 1.0x. Cloud object unchanged |
| A5 | Safely validate/extract archives; inspect every dictionary sheet; run synthetic tests and read-only schema/join/all-lab repetition/timing/four-outcome checks | DONE 2026-09-04: all three nested archives independently scanned clean, extracted to `extracted/` at mode 400, 110,112,522 bytes expanded. All six dictionary sheets read. Aggregate-only audit completed on the training partition. Key results are recorded in `docs/data-location-register.md` and summarized in the dataset report. No cleaning or transformation performed and no patient values written to any report |
| A6 | Apply disclosure checks and create feasibility, coverage, limitations and reproducibility reports | NOT STARTED: no patient IDs/results/free text may leave restricted storage |
| A7 | Upload new audit outputs/manifests to the private run prefix, re-download for checksum comparison and record all verified object generations | BLOCKED 2026-09-06: Stage 01 bundle prepared locally. Re-tested 2026-09-06: `storage.googleapis.com` and `oauth2.googleapis.com` both returned `URLError` and `gcloud storage buckets describe` timed out at 25 seconds, so the authorized read and write test did not run. No upload attempted and no new cloud generation verified |
| A8 | Stop processes, inventory exact local copies, obtain fresh deletion confirmation, remove only approved targets and verify absence | PENDING: restricted run copies verified present 2026-09-05. Verify preservation of required outputs and obtain fresh exact-target confirmation before deletion |
| A9 | Prepare the audited data in explicitly authorized stages | PARTIAL: Stages 01 to 05 completed 2026-09-06. 01 roster and joins; 02 visit vocabularies standardized; 03 timing corroborated with zero cycle order violations; 04 every row given one research purpose with a stated reason, 3.4 per cent excluded and none deleted; 05 test identity and units verified conflict-free and the rounded `LBSTRESN` column rejected in favour of `LBSTRESC`. Suite is 114 tests, all passing. Stages 06 and 07 authorized and outstanding. Integrity review remains required before features |
| A10 | After approved cleaning and checks, propose the scientific analysis plan before modeling | LATER APPROVAL REQUIRED: no modeling authorized now |

First-run limits to explain at the next approval: one local audit session, up to four hours of active work before checkpointing; no unattended recurring job; at most 100 MiB of output/verification data and 1,000 cloud operations in each priced class for the cost estimate. Expected first-audit/first-month cloud cost below USD 0.05; pause above the USD 0.10 projected incremental threshold or for a material change. No cloud computation. This tracker is not a billing cap or automatic background monitor.

## User communication requirements

- Use simple, non-medical language first.
- Explain the reason alongside every proposed step: what it enables or which error it prevents.
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
| Complete package | `AllProvidedFiles_149.zip` | Secured and verified in private Google Cloud Storage; not extracted |
| Data dictionary | `Challenge_data_dictionary v2.xlsx` | Verified as a bundle member; not yet inspected |
| Training package | `prostate_cancer_challenge_data_training.zip` | Verified as a bundle member; not yet extracted |
| Leaderboard package | `prostate_cancer_challenge_data_leaderboard.zip` | Verified as a bundle member; not yet extracted |
| Final-scoring package | `prostate_cancer_challenge_data_finalscoringset.zip` | Verified as a bundle member; not yet extracted |
| CRF location document | `PCDC Protocol, CRF Location.docx` | Verified as a bundle member; not yet opened |

### Verified training files listed inside the package

- `CoreTable_training.csv`
- `LabValue_training.csv`
- `LesionMeasure_training.csv`
- `MedHistory_training.csv`
- `PriorMed_training.csv`
- `VitalSign_training.csv`
- `Challenge_data_dictionary v2.xlsx`

### Historical browser download issue and resolution

The correct page and Download controls were verified. Earlier automated attempts used the page's semantic link, visible DOM control and physical browser click, but no browser download event occurred at that time.

This blocker was resolved on 2026-08-27. The user downloaded the complete package, it passed local integrity and ZIP path checks, Craig approved private Google Cloud storage, and the unchanged bytes were uploaded and verified there. The local restricted copies were removed only after complete cloud verification.

## Storage and privacy rules

### Verified private Google Cloud storage

- PDS approval for private Google Cloud storage was confirmed by the user on 2026-08-27.
- Google Cloud project: `pds-dream-secure-storage`.
- Private bucket: `pds-dream-secure-storage-eu-20260827`.
- Bucket location: `europe-west4`, Netherlands.
- Object: `gs://pds-dream-secure-storage-eu-20260827/prostate-lab-trajectories/data/raw/pds_dream/source/AllProvidedFiles_149 (1).zip`.
- Object size: 6,227,480 bytes.
- SHA-256: `AB3ECA19C5D0CC4106C96AC04E665DD1A5C9DF58F66328ECD24E8E1067932391`.
- MD5: `D4Yz5HS1gTF8tm8Xg6hK2A==` in Google Cloud metadata, matching local MD5 hex `0F8633E474B581317CB66F1783A84AD8`.
- CRC32C in Google Cloud metadata: `gx71ow==`.
- Public Access Prevention is enforced and Uniform Bucket-Level Access is enabled.
- No public principals were found. Access is through the approved project identity.
- Encryption uses Google-managed encryption keys.
- Object versioning is off. Soft delete is enabled for seven days. No retention policy or lifecycle deletion rule was added.
- Metadata-only authorized access was tested successfully. No patient row or laboratory value was displayed.
- The earlier empty United States multi-region bucket `pds-dream-secure-storage-raw-20260827` was deleted after explicit authorization.

### Verified local restricted-file cleanup

- Two identical restricted ZIP copies were found in the Windows Downloads folder.
- Both copies matched the verified cloud object size and MD5, and both had the expected SHA-256.
- Exact files removed permanently after fresh confirmation:
  - `C:\Users\BarbarosIsikGreenhou\Downloads\AllProvidedFiles_149 (1).zip`
  - `C:\Users\BarbarosIsikGreenhou\Downloads\AllProvidedFiles_149.zip`
- A fresh targeted Downloads scan found no remaining matching dataset files, extraction folders or partial browser downloads.
- Ordinary deletion on an SSD cannot guarantee forensic erasure because SSD wear-leveling may retain inaccessible physical remnants.
- No extraction occurred on this computer.

### Required rules

- Never commit patient-level or restricted data to GitHub.
- Never paste patient rows into chat, logs, issues, commits or public documents.
- Use the existing PDS-approved private bucket as the permanent data home. A different destination needs its own authorization; do not repeat the already-settled permission question for this bucket.
- Never expose passwords, security codes, SAS credentials, session cookies or private signed URLs.
- Keep the original package unchanged.
- Keep checksums and acquisition metadata separate from patient values.
- Commit only aggregated, disclosure-checked outputs when permitted.

### Required temporary local layout after approved download

```text
C:\Users\BarbarosIsikGreenhou\PDS-Restricted-Work\prostate-lab-trajectories\runs\2026-08-31-audit-001\
  data\raw\pds_dream\source\
  data\raw\pds_dream\extracted\
  data\interim\
  reports\reviewed\
  tmp\
  logs\
  manifest.json
```

This first-run path is proposed, not created. It is outside the Git clone, Desktop, Documents and Downloads. The repository's ignored `data/raw/` and `data/interim/` rules remain defense in depth, not permission to scatter copies. After plan approval, check folder permissions, non-synchronization, containment and ZIP safety. Register temporary and verification copies. Preserve the original cloud ZIP. The agent-added BitLocker gate was withdrawn; do not reintroduce it. See `docs/data-location-register.md` for state.

### If the user's home computer lacks space

Follow this order:

1. Check the actual download size and available disk space.
2. Consider an encrypted external drive controlled by the user.
3. Pause for approval of an adequate protected local volume if necessary.
4. Do not substitute cloud computing or another remote analysis environment for the user's local-processing direction.
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

Read the current onboarding order in `NEXT_AGENT_ONBOARDING_PROMPT.md`. The six necessary docs cover the real-data audit, data register, execution plan, field checklist, source matrix and CHAARTED fields. Older filenames in historical session entries refer to Git history, not documents to recreate.

## Repository and Git state

**Canonical project home:** `https://github.com/barbarosisik/prostate-lab-trajectories`

**Canonical branch:** `main`

**Temporary working copy pending cleanup:** `C:\Users\BarbarosIsikGreenhou\Desktop\prostate-lab-trajectories`. The user does not want it retained merely for future work.

**Verified state on 2026-08-27:** Remote is `https://github.com/barbarosisik/prostate-lab-trajectories.git`, branch is `main`, working tree was clean before this documentation update, and HEAD matched remote commit `d02eed8359229d19008efb60ba60a4cb3c08e903`.

**Fresh repository verification on 2026-08-31:** Before editing the cleanup policy, the Desktop clone was clean on `main` at `b4187a2b59286f81d5b2f9d6770c90cb71046d31`, matching a fresh `git ls-remote` check. The two known project folders contained 58 files / 318,578 bytes and 79 files / 19,305,428 bytes respectively, including local Git metadata. No directory links were found.

**Retired copy pending exact cleanup review:** `C:\Users\BarbarosIsikGreenhou\Documents\Codex\2026-08-24\s\prostate-lab-trajectories` still exists and must not be used for new work. It may contain local-only literature files and an older dirty working tree. Do not delete it until its exact contents are compared and the user receives an exact deletion list with a fresh action-time confirmation.

**Authorization boundary:** The user explicitly authorized publishing the current permitted project files and deleting the former local folder in the 2026-08-25 migration session. Future commits, pushes, history changes or repository-setting changes still require fresh explicit authorization.

**Session-closeout rule:** An onboarding or next-agent handoff request also starts the verified local-cleanup workflow in `NEXT_AGENT_ONBOARDING_PROMPT.md` and `AGENTS.md`. Publish approved permitted work, verify remote `main`, show exact deletion targets and local-only-file consequences, obtain fresh confirmation, delete the approved temporary project folders and recheck them. Do not retain a local clone just for future programming. Task history and shared app files require a separate supported app workflow.

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

### Stage 1: Prepare the approved temporary local run

**Trigger:** The next agent has explained the plan and received the user-requested fresh approval, then completed the scoped folder/path checks. Original PDS acquisition is already complete; do not restart it.

**Actions:**

1. Read the data-location register and resolve any prior incomplete run or pending local cleanup.
2. Check effective folder permissions, non-synchronization and available local capacity without a general Windows-security or BitLocker detour.
3. Record the exact run root before creating it or downloading files.
4. Refresh approved bucket access and pin the source object generation.
5. Download the unchanged source directly to the protected registered path with normal approved authentication.
6. Verify size and checksums against the recorded source before extraction.

**Completion evidence:** A real file exists at a verified path and has a nonzero size.

### Stage 2: Securely verify the package

**Actions:**

1. Calculate SHA-256.
2. Record filename, timestamp, size, source page and checksum in a non-sensitive acquisition record.
3. List ZIP members without extraction.
4. Reject absolute paths, parent-directory paths and other unsafe ZIP members.
5. Confirm expected dictionary and CSV names.
6. Extract only into `data/raw/pds_dream/extracted/` inside the registered protected local run folder after path and ZIP validation.

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
6. Complete the supplemental read-only join, repetition-validity, timing and outcome checks in the approved local plan.
7. Upload new audit outputs to their versioned private-cloud run prefix and verify the uploaded bytes before any local removal.
8. Update the data-location register, obtain fresh exact-path deletion confirmation, remove the approved local run folder and verify absence. Apply this workflow again after each later approved stage.

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

Before real-file inspection:

> The next agent must FIRST explain the data plan and ask one approval question, then wait. Do not start data work or substitute the rejected drive-encryption check. Cloud storage permission is settled. Maintain recorded local/cloud paths, verified uploads, later separate cleaning/analysis approval and fresh exact-target cleanup confirmation.

### Execution reminders after the requested next-agent approval

- Do not ask for further BitLocker commands, Windows security screens or recovery keys. The agent-added gate was withdrawn at the user's direction; encryption status is unknown and no new PDS mandate was established.
- Prepare a non-synchronized local run folder and local dependencies, with exact paths recorded before transfer. No cloud-compute API enablement is needed.
- Refresh bucket access/source checksums and use only approved user authentication. Existing Owner rights exceed transfer needs; no access expansion is included.
- Extract locally only after source integrity and ZIP path checks pass.
- Read every dictionary sheet before creating cleaning rules.
- Run tests and the aggregate inventory before cleaning.
- Verify that the aggregate report contains no patient identifiers or laboratory values.
- Upload new restricted outputs and verification metadata to the run's private cloud prefix. Verify every required output; then record cleanup as pending until fresh confirmation and post-deletion checks.
- Keep the first-audit cloud expectation below USD 0.05 under the plan's size/operation assumptions; pause above the USD 0.10 incremental approval threshold. No cloud-compute charge is planned.
- Corrected handoff publication is complete and independently verified at `0fa84856f526a7e647cf5f07b5acccfe39e645ea`. This corresponding receipt is within the same authorization. Future unrelated publication requires permission. Cleanup is not complete.

### Later reminders

- Complete the user-requested local project-folder closeout after the new policy is published and exact deletions are confirmed. Do not recreate a permanent local folder afterward.
- Explain timing feasibility to the user before cleaning.
- Ask for approval before finalizing outcome definitions.
- Request CHAARTED only after the PDS coverage gaps are known.
- Consider Vivli or Flatiron only after CHAARTED and PDS compatibility are clear.

## Dated operational history

### 2026-08-31: Verified corrected handoff publication and pending deletion

- Committed ten reviewed data-free documentation files in `0fa84856f526a7e647cf5f07b5acccfe39e645ea`; normal push to main succeeded. All three invented-data tests passed again; whitespace, code-fence, no-em-dash and credential-pattern checks passed. No restricted or publisher files were staged.
- Independent CLI reads then returned "Repository not found" twice. Used the authenticated GitHub connector, which independently resolved main to the exact new commit. Fetched every one of the ten documents and matched its Git blob SHA to the local committed tree, including onboarding, both logs, the data plan/register and closeout manifest. The Desktop worktree was clean before this receipt.
- Fresh filesystem inventory: Desktop clone 111 files / 710,653 bytes including Git metadata at that checkpoint; retired folder 79 files / 19,305,428 bytes. No reparse points were found. Desktop has no ignored/untracked files. Proposed restricted-data root still absent. This receipt will change the Desktop file totals.
- A proposed memory-removal note was rejected because creating another persistent project record would conflict with the cleanup request. No such note was created, and no memory file or task history was deleted. Do not retry through a workaround or claim app-managed cleanup occurred.
- Both exact project folders remain. Request explicit permission to discard the 27 unbacked local-only items as an exception to the all-files-backup condition, together with fresh confirmation of permanent deletion of both exact folders. Alternatively, wait for a permitted approved backup. Publication success does not waive that condition.
- Data execution remains at A0R, not started. The next agent must explain the local audit and verified-output plan before asking approval and proceeding.

### 2026-08-31: Publication authorized and retired files checked

- The user explicitly requested publication, followed by local project cleanup after GitHub preservation. This authorizes the corrected handoff and matching closeout documentation, not a data-processing run.
- Fresh authenticated remote main and local HEAD matched `f152628c4a23bccad0c8cbd671c4aa7d30d39814` before this publication. Nine prepared modified documents were preserved; no unrelated changes were overwritten.
- Compared all 19 permitted retired working files against reachable canonical history. Every file's text is already preserved; 13 differ in final newline formatting from Git blobs. Six are exact Git blob matches. Specific matching commits and excluded files are recorded in `docs/local-closeout-2026-08-31.md`.
- The 27 ignored local-only materials remain unbacked. Do not put publisher full text in GitHub. Both folders remain pending an explicit backup exception or approved alternative and fresh exact-target confirmation.
- The active task workspace has only its own Git metadata, not the project clone. The proposed restricted-data run root does not exist. No dataset was downloaded or opened.
- Task histories and memory are separate app-managed categories. No supported task-deletion tool is exposed in this task; archiving would not delete history. Shared session databases and credential stores must not be manually removed. Do not promise every trace is erased.
- Next: verify publication, request the remaining cleanup decision, and perform deletion only after that decision and fresh confirmation. The research handoff remains approval-first at A0R.

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

### 2026-08-27: Private cloud transfer and local restricted-file cleanup

- User reported that Craig at PDS approved private Google Cloud storage.
- Created and verified the dedicated private Netherlands-region bucket and protected object path listed above.
- Verified remote existence, exact size, matching MD5, CRC32C metadata, enforced public-access prevention, uniform bucket access and absence of public principals.
- Permanently removed only the two exact restricted ZIP copies from Windows Downloads after fresh user confirmation.
- Rechecked Downloads and found no matching dataset files, extraction folders or partial downloads.
- Authenticated Git securely through the normal browser flow and cloned the current private `main` branch to the actual Windows Desktop.
- Verified the clone at commit `d02eed8359229d19008efb60ba60a4cb3c08e903` and read every required onboarding, research, audit and literature record.
- Re-ran all three invented-data inventory tests successfully.
- No patient-level file was opened, extracted, downloaded from cloud or placed in GitHub.
- User explicitly authorized committing and pushing the current privacy-safe documentation and onboarding updates to `main`.
- This authorization does not approve creating paid cloud compute or beginning the real-file audit.
- Next gate is explicit approval for a protected cloud computing environment and the real-file audit.

### 2026-08-31: Onboarding-triggered local cleanup requested

- User clarified that permitted project files should live in private GitHub, with no permanent local project working folders after handoff.
- Added a session-closeout workflow to the onboarding prompt and an automatic agent entry point in `AGENTS.md`.
- Verified remote `main` and the clean Desktop clone at `b4187a2b59286f81d5b2f9d6770c90cb71046d31` before editing.
- Compared the retired folder to the Desktop clone using normalized text without printing data. Its code, tests, fixture files and literature metadata matched; its five older documents were found in commits reachable from remote `main`.
- Identified 10 research PDFs, 10 extracted-text copies, five temporary downloads and two Python cache files only in the retired copy. These are not backed up in GitHub and must be included in the explicit deletion warning. Do not upload their contents to GitHub as part of cleanup.
- Rechecked Windows Downloads and found zero matches for the known PDS dataset filename prefixes.
- Both exact project folders still exist. No project folder or Codex task-history file was deleted in this session at the time of this entry.
- Subsequent user decision: publishing the cleanup policy to `main` is explicitly approved. Deletion of both exact folders is conditional on all local files being pushed to GitHub first.
- That condition is not satisfied by the existing GitHub code/documentation backup: ignored full-text papers, text copies, temporary downloads and generated caches remain local only. Do not force-add excluded files or reinterpret bibliography links as file backups.
- Both project folders must remain until the user approves a permitted alternative backup or explicitly changes the condition. No alternative cloud transfer is authorized by a GitHub-only backup condition.
- Next action after publishing the rule: explain this remaining backup gap and request direction. Delete nothing while the condition is unresolved.
- Paid cloud compute, real-file inspection, cleaning and modeling remain unstarted by this session.

### 2026-08-31: Cloud approval clarified and next-agent execution plan requested

- User explicitly confirmed that Google Cloud use is approved and the project can go forward. The next agent should create or suggest concrete plans and ask for approval of those plans.
- Replaced stale current-status wording that treated cloud permission as unresolved. PDS storage permission remains confirmed, and user approval to move toward protected compute and the real-file audit is now explicit.
- Updated `AGENTS.md`, the onboarding prompt and current status documents so the next agent starts with onboarding, read-only verification and an actionable resource-and-audit plan.
- Exact resource choices, current costs, access configuration, protected processing steps and deliverables belong in that plan. Once approved, covered routine steps can proceed without repeated generic permission requests.
- The later cleaning/restructuring plan and scientific analysis plan remain separate approval checkpoints informed by real fields. No research question or privacy rule changed.
- This session changes and publishes documentation only. It creates no VM and starts no real-file inspection or modeling. Resource creation by another session must be checked live rather than assumed.
- Local-folder deletion remains conditional on the unresolved backup requirement; no alternative backup or deletion was authorized by this clarification.
- User explicitly authorized this documentation update to be committed and pushed to `main`.

### 2026-08-31: Live cloud onboarding and concrete audit proposal

Historical proposal only. The later same-day local-processing correction below supersedes the cloud-compute proposal; no such resources were created.

- Read all mandatory project records and the current code/tests. Verified a clean Desktop clone on `main` at `fb059b91df2fd38740ab305fb17058204e7d9096`, matching a fresh authenticated remote-main check.
- Re-ran all three invented-data tests successfully without generating Python caches in the clone. No real patient data was used.
- Refreshed bucket configuration and permissions through the signed-in Cloud Console: Netherlands, Standard, public access prevention, uniform access, Google-managed encryption, seven-day soft delete, versioning off and no lifecycle/retention policy remain visible.
- Confirmed the source object exists, is Not public, displays rounded size 6.2 MB and retains its August 27 last-modified timestamp. The console did not expose exact bytes or checksums, so those remain the historical acquisition values pending a metadata and protected SHA-256 refresh before extraction.
- Compute Engine showed an API Enable screen. Asset Inventory listed 30 resources without a compute, disk, network or notebook type, and the service-account list was empty. No API was enabled and no resource or permission was changed. Billing-enabled status and exact account charges were not verified.
- Verified Netherlands pricing through explicit region selection: `e2-small` USD 0.01844301/hour, standard disk USD 0.000060274/GiB-hour and Standard object storage USD 0.000027397/GiB-hour. Private DNS adds about USD 0.20/month plus queries. Proposed eight-hour base subtotal is about USD 0.1546; retained 10 GiB disk plus DNS is about USD 0.64/month.
- Drafted an uncommitted cloud setup plan covering private networking, identity, extraction, audit and shutdown. It was withdrawn and replaced with `docs/local-processing-and-cloud-storage-plan.md` after the user's correction.
- Identified limits in the existing first-pass script: no complete join audit, fixed aliases/missing markers, nonempty-result rather than fully numeric-valid repetition, inferred baseline labels and no small-group suppression. No code was changed. Proposed supplemental read-only checks are part of the approval request, not an implemented cleaning pipeline.
- Both known project folders still exist. The retired path was checked for existence only. No backup or deletion was performed or authorized.
- New documentation remains local and uncommitted. No commit, push, restricted transfer, extraction, real-file audit, cleaning or modeling was performed.
- Exact next action: approve or revise the specific setup-and-audit plan. General cloud-use permission remains settled.

### 2026-08-31: User corrected execution to local processing and cloud storage only

- The user explicitly said computations, tests and processes must run on the local computer. Cloud storage is for permanent access across computers, including later cleaned data and outputs. Do not reinterpret storage approval as cloud-compute permission.
- Adopted the per-stage cycle: register local path, download, verify, process locally, upload new versioned outputs, verify uploads, obtain fresh exact-path confirmation, delete local copies and verify absence. Original cloud source bytes remain unchanged; no redundant original re-upload is required.
- Added `docs/data-location-register.md` and replaced the unapproved VM proposal with `docs/local-processing-and-cloud-storage-plan.md`. Updated the agent instructions, onboarding, current snapshots and audit references. All proposed paths and unimplemented steps are labeled pending.
- Proposed local run: `C:\Users\BarbarosIsikGreenhou\PDS-Restricted-Work\prostate-lab-trajectories\runs\2026-08-31-audit-001`. The parent restricted-work directory did not exist at the check. No folder or restricted data was created there.
- Local C: capacity was checked at 266,093,146,112 free bytes. Encryption inspection via `manage-bde -status C:` was denied in both ordinary and escalated contexts; CIM RAM inspection was denied. Encryption remains a pre-download verification gate, not a claim that the device is unencrypted.
- Refreshed official Storage internet-transfer pricing: first-tier download to the Netherlands USD 0.12/GiB, incoming traffic free, regional Standard operations USD 0.005/1,000 Class A and USD 0.0004/1,000 Class B. Netherlands Standard storage had been verified at USD 0.000027397/GiB-hour. No cloud-compute resources or charges are proposed.
- The user explicitly requested remembering this workflow. Saved a small correction through the permitted memory-note mechanism; the project logs/register remain the authoritative detailed state.
- Verification after the correction: all three invented-data unit tests passed; `git diff --check` passed; all ten revised/new project documents contain no em dashes and have balanced code fences. No source or test code changed. The withdrawn cloud-plan file and proposed restricted-work directory are absent.
- No restricted download, extraction, real-file audit, cleaning, modeling, cloud output upload, commit, push or folder deletion occurred. The older local-only-paper backup condition remains separate and unresolved.
- Exact next action: approve the specific local audit/upload plan and explicitly authorize safe documentation publication if desired; then resolve local encryption verification and execute only the approved stage.

### 2026-08-31: Local audit approved and log-based execution tracking requested

- The user approved the specific local-audit plan and publishing the corrected data-free instructions to private GitHub main. The user asked for the plan to be written in this log and tracked until complete. Added tracker `LOCAL-AUDIT-2026-08-31-01` with explicit evidence/status and later approval gates.
- The first remote Git check failed after a tool approval was refused. The user explicitly requested a retry; the authenticated retry succeeded and remote main still matched local HEAD `fb059b91df2fd38740ab305fb17058204e7d9096`. No reset, overwrite or history rewrite was used.
- Retried `manage-bde -status C:` with the requested tool approval. It still returned access denied and requested administrative rights. Disk encryption remains unverified; no recovery key was queried or displayed.
- Read the Windows computer-use skill and required guidance. Its mandatory safety rules prohibit automation of Windows security apps, so no automated security-app inspection or settings change was attempted. The remaining encryption check needs a permitted manual user check, not an automation workaround.
- No restricted-work directory exists. No source download, extraction, real-file audit, cleaned dataset, cloud output upload or deletion has occurred. The source remains in the approved private bucket.
- Published the ten reviewed data-free documents in commit `9843e5b86a89c4f5ca583a60f1906c69032ee9c8`. A normal push succeeded, and a fresh authenticated `git ls-remote` independently returned that exact SHA for remote main. Verified all ten required paths and tracker content in the matching content-addressed commit. The working tree was clean immediately after publication. No raw data, patient values, credentials or publisher files were staged.
- All three invented-data tests passed again. Staged whitespace checks, balanced Markdown fences, no-em-dash checks and a credential-pattern scan passed. No source/test code changed.
- Marked tracker A1 done and retained A2 as waiting for the user's manual encryption check. This receipt update is within the approved corresponding status-log publication scope. Continue the approved plan after local security passes, without reopening generic cloud-storage or plan permission.

### 2026-08-31: Approval-first next-agent handoff requested; encryption detour rejected

- The user objected to the mandatory drive C: protection check and requested an onboarding prompt for the next GPT-5.6 Sol agent. The next agent must first explain the data-processing plan and ask for approval before starting it. The user also requested an explanation in chat before the existing GitHub onboarding file is modified.
- Explained the local download/audit/new-output upload/verification/cleanup cycle in chat before local draft editing. No GitHub change has been made in this revision. The first patch attempt failed to match an exact old paragraph and made no changes; it was corrected against the actual file.
- Removed the assistant-added mandatory BitLocker prerequisite from current instructions. It was an extra precaution, not a newly verified PDS rule. This does not establish that the drive is encrypted or unencrypted, authorize Windows-setting changes or weaken the no-patient-content/no-GitHub-data boundaries.
- Added A0R for the requested next-agent approval-first step; retained historical A0/A1 approval/publication and all later cleaning/analysis gates. No real data process was started.
- Reverified clean Desktop main and fresh authenticated remote main at `f152628c4a23bccad0c8cbd671c4aa7d30d39814` before editing.
- Started handoff cleanup with a contained, no-link-traversal inventory of only the two known project folders. Desktop: 97 files / 606,909 bytes including Git metadata, no PDFs/text/ignored files before this revision. Retired: 79 files / 19,305,428 bytes, 10 literature PDFs, 10 extracted text files, 5 temporary dictionary PDFs and 2 Python caches, plus its older modified/untracked work. No links were found. The initial Desktop git check from another cwd reported an ownership warning; a direct check in the verified Desktop workdir succeeded without changing global trust settings.
- Exact folders remain: `C:\Users\BarbarosIsikGreenhou\Desktop\prostate-lab-trajectories` and `C:\Users\BarbarosIsikGreenhou\Documents\Codex\2026-08-24\s\prostate-lab-trajectories`. The proposed restricted-data run folder is absent. No backup, deletion, restricted download or cloud write occurred.
- Cleanup is blocked by the unchanged all-files-backup condition and lack of fresh exact-target deletion confirmation. The handoff request does not permit uploading publisher files or deleting the only copy of older work. Do not delete either folder until those conditions are resolved.
- The new handoff/current-status revisions are local and uncommitted. Next: present the plain-language plan and request explicit publication authorization; after publication verify main, then address the separate local-only-file/deletion decision. Do not restart data work during this closeout.
- Validation: all nine revised documents passed whitespace, balanced-code-fence, no-em-dash and credential-pattern checks. No active onboarding/README/docs instruction still requires the withdrawn encryption check. All three invented-data unit tests passed again; no source/test code changed. The historical entries retain their earlier context rather than being rewritten as current facts.

### 2026-09-04: macOS working copy reconciled with remote main and 2026-08-26 state preserved

**User situation and request**

- The user asked whether the local documents were older than GitHub `main`, to pull the latest if so, and to push only if the local copy was the newer one.
- The user asked for shorter action-first replies and confirmed as a standing instruction that the logs must always be updated.
- The user asked where the project stands and what to do next.

**Completed**

- Fetched `origin` and compared both sides before changing any file.
- Preserved the unpushed 2026-08-26 working-tree state on the local-only branch `backup/local-2026-08-26-session`.
- Fast-forwarded `main` from `d02eed8` to `origin/main` at `7392d50`.
- Restored `docs/dataset-internet-search-audit.md` as an untracked file, because remote `main` never contained it.
- Completed the mandatory onboarding reading order and recorded this machine's tooling state.

**Verified evidence**

- Local `main` was 0 ahead and 7 behind `origin/main`. `git merge-base --is-ancestor` confirmed a pure fast-forward, so no merge commit was created.
- The uncommitted local files carried modification time 2026-08-26 20:03. Remote `main` head is dated 2026-08-31 15:08. The remote was therefore newer and NOTHING was pushed.
- The preserved branch tip is `a85919f` and holds all four files from the 2026-08-26 state.
- `git status` reports `main` level with `origin/main`, with only the untracked audit document remaining.
- `python3` and `git` are available. `gcloud` and `gsutil` are NOT installed on this machine. The Desktop volume reports 415 GiB free.
- No restricted data were downloaded, opened or moved. No run folder and no cloud output were created.

**Decisions**

- No research question, scope, source strategy, method or approval gate was changed.
- The superseded 2026-08-26 narrative was deliberately NOT merged into the current logs. Remote `main` records that PDS access was resolved and that the package is in the approved private bucket, whereas the 2026-08-26 text still described PDS as blocked and proposed MSK-CHORD as a partial substitute.
- No new `D-0xx` identifier was created. The 2026-08-26 draft had reused `D-019` and `D-020`, which upstream already assigns to the cloud storage and local-deletion decisions.

**Problems or blockers**

- The registered run path and the closeout deletion targets are Windows paths on the previous machine and are not reachable from this macOS working copy, so that cleanup cannot be verified or completed here.
- The Google Cloud CLI is absent on this machine, so A3 must include installing and signing in to it before A4 can download the source.
- The fate of the untracked `docs/dataset-internet-search-audit.md` and of the local-only preservation branch is undecided.

**Reminder added or cleared**

- The A0R approval requirement remains active. The explanation was delivered on 2026-09-04 and the answer is outstanding.
- Added a reminder to obtain a decision on the untracked 2026-08-26 audit document and on the local-only branch, neither of which exists on the remote.

**Exact next action**

- Wait for the user's A0R answer. Do not create a run folder, install cloud tooling or download the source before that answer.

### 2026-09-05: Mandatory reading and local state verification

- **Verified:** Read the onboarding prompt and mandatory records. Checked Git status, local and cached branch tips, source size/mode/SHA-256, directory metadata and source/test file inventory. No preparation implementation is present under `src`; the existing audit script remains the only source file listed.
- **Verified:** Corrected stale current snapshots and the A8 row without reopening settled approvals or changing the research question. Highest existing decision identifier is D-033; duplicate historical D-021 through D-026 identifiers remain date-qualified. No new decision was introduced.
- **Blocked:** Live remote verification failed at DNS resolution. No commit, push, pull request, data transformation, upload or deletion occurred. Tests were not rerun for this documentation-only task.
- **Pending:** A9 implementation approval, the user-side PDS search and affiliation answer, duplicate-record housekeeping, and publication decisions. Preserve all pre-existing worktree edits.

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

### 2026-09-06: Stage 01 executed, private transcription verified and documentation consolidated

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

### 2026-09-06: Publication verified, cloud unreachable and source facts measured before Stage 02

- **Verified publication:** local `dataset-audit` HEAD is `721d84a` with a clean working tree, and a fresh `git ls-remote origin dataset-audit` returned `721d84a1e9c8e8269988ebfaee83086d83a72d5b`. The documented Stage 01 implementation, its tests and the consolidated records are published. Nothing restricted was committed.
- **Blocked cloud connectivity:** direct HTTPS requests to `storage.googleapis.com` and `oauth2.googleapis.com` both failed with `URLError`, and `gcloud storage buckets describe` on the approved bucket stopped at a 25 second timeout. The authorized read test and new-object write test therefore did not run. A7 stays BLOCKED and no upload was attempted. This is a network reachability failure from this session, not evidence about bucket permissions.
- **Verified source facts for Stage 02 to 05, aggregate only, training partition:** the unknown laboratory code `.` is recoverable, since every one of its 6,151 rows carries `LBTEST` `SODIUM`, `LBCAT` `CHEMISTRY` and unit `MMOL/L`. No test code carries more than one non-missing `LBSTRESU` across the three trials, so no cross-trial standard-unit conversion is currently indicated at that column. Result formats are 194,714 numeric, 12,295 non-numeric text, 2,618 missing, and 815 originals carrying a `<` or `>` bound, of which 540 lose the bound in the standard character column and 3 become plain numbers. 112,167 rows have `LBSTRESN` and `LBSTRESC` that are not numerically equal and must be explained before any value is trusted.
- **Verified baseline-flag coverage:** `LBBLFL` equal to `Y` covers 22,129 CELGENE rows, 16,101 EFC6546 rows and 6,143 ASCENT2 rows; of these, 15,639, 4,141 and 322 respectively also carry a `CYCLE` visit label, so the flag and the cycle labels overlap and cannot be treated as independent baseline definitions.
- **Verified coverage limitation:** among rows with a `CYCLE` visit label, ASCENT2 contributes only `PSA` (1,882 rows). CELGENE and EFC6546 contribute the wider chemistry and haematology panels. Any multi-test per-cycle analysis is therefore effectively a two-trial analysis, and ASCENT2 can only support PSA trajectories.
- **Exact next action:** implement Stage 02 cycle-label standardization on the two-trial cycle vocabulary, keeping original `VISIT` text, and report its error points before Stage 03.

### 2026-09-06: Stage 02 executed, visit vocabularies standardized and cycle coverage measured

- **Verified user position:** the user noted that local possession of the dataset is already approved and asked whether a download is needed. It is not. The pinned source archive and all 18 extracted CSVs are present in the registered run root and were re-verified against `SOURCE_SHA256` during this run. Private Google Cloud remains a backup and output-preservation route, not a source of anything missing.
- **Verified Stage 02 implementation:** `src/preparation/stage02_visits.py` translates visit labels through an exhaustive 29-entry lookup table keyed by (trial, exact label). Nothing is stripped, upper-cased or pattern-matched, and an unenumerated label stops the stage with `UNKNOWN_VISIT_LABEL`. Original visit text is preserved. The output visit index is keyed by source CSV row number and deliberately contains no laboratory value, unit or result column, so the stage created no new copy of any patient measurement.
- **Verified execution:** all 210,442 laboratory rows received exactly one disposition and zero rows were dropped. Recorded row counts for every (trial, label) pair matched the audited source exactly. The index passed read-back verification, was written mode 600 without overwriting, and the source hashes were unchanged after the run. The suite is now 43 tests, all passing.
- **Verified role counts:** CELGENE contributes 81,076 cycle-start rows, 15,341 mid-cycle rows at cycle 1 day 14, 21,366 pre-treatment rows, 4,148 unscheduled and 1,820 discontinuation rows. EFC6546 contributes 58,839 cycle-start rows, 16,969 pre-treatment, 1,167 follow-up and 229 rows under `VISIT 99` retained as `unresolved_label`. ASCENT2 contributes 1,882 cycle-start rows and 7,605 pre-treatment rows.
- **Verified coverage limitation, decisive for the design:** at cycle-start visits, ASCENT2 carries exactly one test code, PSA, with a median of one test per patient, although its pre-enrolment panel holds 13 codes. EFC6546 cycle 1 carries a median of 4 test codes per patient against 26 at cycles 2 to 5, so its cycle 1 cannot supply a full panel. CELGENE is consistent, with a median of 34 to 41 codes at every cycle from 1 to 5. ASCENT2 cycles 6 to 10 contain 2 to 9 patients each and are negligible.
- **Verified assumption still untested:** 58,839 EFC6546 and 1,882 ASCENT2 cycle-start rows have a day that is assumed rather than stated by the label, because only CELGENE writes an explicit day. Stage 03 must test that assumption against the recorded relative day `LBDT_PC` before these are treated as comparable cycle starts.
- **Exact next action:** Stage 03, check visit labels against `LBDT_PC` under each trial's own time origin from `PER_REF_C`, count timing conflicts, and relabel nothing automatically.

### 2026-09-06: Stage 03 executed, visit labels corroborated by recorded collection days

- **Verified timing columns:** `LBDT_PC` is the collection day as a relative day count and `PER_REF_C` names the day it is measured from. The dictionary states this is the first treatment date for most patients and the consent date for a small number, which the data confirms: 209,970 rows use `1ST TREATMENT` and 472 use `CONSENT DATE` (128 ASCENT2, 344 CELGENE). Rows on the alternate origin are flagged, never compared on the same scale.
- **Verified cycle length, derived not assumed:** the median recorded day at cycle starts is 0, 21, 42, 63 and 84 for cycles 1 to 5, independently in all three trials. A 21 day cycle is therefore an observed property of this source, and it is used only as a consistency check with an explicit 10 day tolerance.
- **Verified strongest result:** zero cycle order violations across all 1,600 patients. No patient has a later cycle recorded on or before an earlier one. This check needs no schedule assumption at all, so it is the strongest available evidence that the Stage 02 labels genuinely agree with the recorded dates. The previously outstanding assumption over 60,721 cycle-start rows whose day was assumed rather than stated is now corroborated.
- **Verified flag counts across all 210,442 rows:** 514 rows have no recorded day (452 ASCENT2, 62 EFC6546), 472 use the alternate reference origin, 4,922 cycle-start rows fall outside the 10 day tolerance, and 1,165 pre-treatment rows are recorded on or after day zero. Off-schedule rows concentrate in EFC6546 (4,028) and in CELGENE cycle 4 (446). Median deviation is 0 days in every trial and cycle except EFC6546 cycle 1, at 1 day.
- **Verified usable sample:** 136,681 of 141,797 cycle-start rows, 96.4 per cent, pass every timing check. Counting patients with timing-verified cycle starts, 403 CELGENE and 519 EFC6546 patients, 922 in total, have all of cycles 2, 3 and 4; 319 and 407, 726 in total, have all of cycles 1 to 4.
- **Verified truncation:** the largest comparable recorded day anywhere in the source is 84. The laboratory record therefore ends at twelve weeks, so cycles 1 to 4 are complete and cycle 5 is a boundary case, not a full cycle.
- **Verified new caution:** 1,495 of 8,512 patient-visit groups span more than one recorded day, so a visit label denotes a short window rather than a single date. Stage 06 must decide how repeat draws inside one visit are handled.
- **Verified explanation of the earlier CELGENE cycle 1 anomaly:** it is a coverage effect, not a timing fault. CELGENE cycle 1 day 1 sits at a median day of 0 with a maximum of 0, so it is correctly placed; the 414 patients with cycle 1 laboratory rows are simply fewer than the 483 at cycle 2 because screening at a median of day -8 carried the earlier draw for some patients.
- **Verified execution discipline:** all 210,442 rows received exactly one disposition, zero rows were dropped, zero cycle labels were altered, no laboratory result was read, and the source hashes were unchanged after the run. The suite is now 69 tests, all passing.
- **Exact next action:** Stage 04, assign an explicit research role to non-cycle visits, then Stage 05 on test identity and units.

### 2026-09-06: Stage 04 executed and the outcome fields inspected directly

- **Verified Stage 04 implementation:** `src/preparation/stage04_roles.py` gives every row exactly one research purpose through a single ordered rule set, so two rows in the same situation cannot be treated differently. Purposes are baseline candidate, cycle measurement, mid-cycle measurement, context only and excluded. Every exclusion carries a fixed reason code and every excluded row stays in the output, so exclusion from an analysis is never deletion from the record.
- **Verified Stage 04 execution:** all 210,442 rows received a purpose and zero rows were deleted. 136,681 rows are cycle measurements, matching Stage 03's usable count exactly. 44,155 are baseline candidates, 15,341 are mid-cycle measurements, 7,135 are context only and 7,130, being 3.4 per cent, are excluded. The largest single exclusion reason is 4,028 EFC6546 off-schedule cycle rows, followed by 1,165 pre-treatment rows recorded on or after the first dose, 513 rows with no recorded day, 301 rows on the alternate time origin and 229 unresolved `VISIT 99` rows. The suite is now 89 tests, all passing.
- **Verified outcome fields, inspected directly as requested.** `DEATH` is coded `YES` or blank, and blank means alive at last contact rather than missing, so it is a censoring marker and not a gap. `LKADT_P` is the last known alive day and is present for all 1,600 patients. `DISCONT` carries a third value, a literal `.`, for 111 patients (106 CELGENE, 5 EFC6546), which is a genuinely absent discontinuation label. `ENTRT_PC`, the treatment stop day, is absent for 95 CELGENE patients. `ENDTRS_C` holds five stop reasons: AE, possible_AE, progression, complete and misce.
- **Verified outcome imbalance:** deaths are 433 of 598 in EFC6546 (72.4 per cent), 138 of 476 in ASCENT2 (29.0 per cent) and 92 of 526 in CELGENE (17.5 per cent). Median last known alive day is 642, 357 and 279 respectively. The difference is therefore largely follow-up length, so any pooled survival model must carry trial as a stratum or it will learn the trial rather than the patient.
- **Verified structural problem, the most serious found so far.** The laboratory clock and the outcome clock are different. `LBDT_PC` is measured from the first treatment date, while `LKADT_REF` and `PER_REF` state that the outcome day counts are measured from the consent date for ASCENT2 and CELGENE and from randomization for EFC6546. Two checks confirmed there is no bridge for the consent-referenced trials in the released data: no patient has laboratory rows on both origins, so no same-patient same-visit offset can be measured, and ASCENT2 shares no visit label between `LabValue` and `VitalSign`. For EFC6546 the offset is measurable through `VitalSign`, which uses randomization, at a median of 2 days. Until this is resolved, a landmark analysis that mixes a laboratory day with an outcome day cannot be stated as exact for ASCENT2 and CELGENE.
- **Verified censoring risk:** 63 patients have a last known alive day of 84 or less, so their follow-up ends inside the same twelve-week window the laboratory record covers. These are the informative-censoring cases and must be counted explicitly at the integrity checkpoint.
- **Exact next action:** Stage 05, establish test identity and units, and settle the 112,167-row disagreement between `LBSTRESN` and `LBSTRESC`.

### 2026-09-06: Stage 05 executed and the rounded value column rejected

- **Verified test identity:** the source holds 103 distinct laboratory test codes. Every code carries exactly one test name and exactly one standardized unit across all three trials, so there are zero identity conflicts and zero unit conflicts. The unusable code `.` was recovered as SODIUM from its accompanying test name only, and the stage refuses to recover it from any other name. All twelve panel tests are present in all three trials with a single unit each.
- **Verified units need no conversion:** 42 codes carry more than one original unit in `LBORRESU`, with a white cell count recorded 33 different ways, but `LBSTRESU` holds one standardized unit per code throughout. The sponsors harmonized units before release, so this stage converted nothing and altered no value. A check for a neutrophil percentage leaking into an absolute count found none: the 518 EFC6546 rows recorded originally as a percentage have standardized values in the same range as the counts.
- **Verified decisive finding, the value column.** This source stores every result twice, in `LBSTRESN` and `LBSTRESC`, and the data dictionary recommends both. They are not equivalent. All 194,814 parsable values in `LBSTRESN` are whole numbers, and 111,932 of the 112,167 disagreements, being 99.8 per cent, are explained exactly by rounding the character value to the nearest integer. `LBSTRESN` has therefore lost every decimal place in the source. Using it would destroy any test whose clinical range is smaller than one unit, which includes creatinine, bilirubin, potassium, calcium and the neutrophil count. `LBSTRESC` is now the authoritative value column, enforced in code by `select_value_column`, which stops the stage if a future source ever breaks the evidence behind that choice.
- **Verified result formats across 210,442 rows:** 194,714 ordinary numbers, 12,295 uninterpretable text entries, 2,618 absent and 815 bounded results such as a value below a detection limit. A further 543 rows carried a `<` or `>` bound in the original result that is absent from the standardized column, so the bound was lost upstream and those rows must not be read as exact numbers.
- **Verified new hazard for Stage 06:** 3,419 of 6,291 patient-visits hold more than one neutrophil row, because CELGENE records that test twice per visit. Repeat measurements inside one visit are therefore common and need an explicit selection rule.
- **Verified execution discipline:** no value was altered, no unit was converted, no patient row was written. The only output is a test-level catalogue. The suite is now 114 tests, all passing.
- **Exact next action:** Stage 06, separate real measurements from absent results, bounded results and duplicates, using `LBSTRESC` as the value column.

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


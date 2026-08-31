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

**Last updated:** 2026-08-31

**Project stage:** Restricted package secured in approved private Google Cloud Storage; cloud-computing and audit direction approved; concrete execution plan next

**Primary source:** Project Data Sphere Prostate Cancer DREAM Challenge

**Current dataset page:** `https://data.projectdatasphere.org/projectdatasphere/html/content/0abbd47a-dcfb-42c2-a036-af1898ea3c1c`

**Current dataset ID:** `Prostat_na_2006_149`

**Current storage state:** Craig at PDS confirmed that private Google Cloud storage is permitted. The unchanged package is stored in a dedicated private bucket in the Netherlands region. The two verified local restricted ZIP copies were permanently removed after cloud verification and fresh user confirmation.

**Current approval state:** On 2026-08-31 the user confirmed that private Google Cloud use is approved and the project can proceed toward protected computing and the real-file audit. Provider/storage permission is not a current blocker. The next agent must present exact implementation details and costs for plan-level approval, then execute the approved scope.

**Immediate next action:** Read the required records, verify repository and cloud metadata, and propose a concrete setup-and-audit execution plan covering resources, permissions, current costs, protected paths, outputs and shutdown. Ask for approval of that plan rather than asking again whether Google Cloud is allowed.

**Current session priority:** Publish the user's approval clarification and actionable next-agent plan. The separate local-folder deletion condition is unchanged: all local files must first be backed up as approved. Ignored papers, text copies, temporary downloads and generated caches are not backed up in GitHub, so neither folder may be deleted without an approved alternative backup or explicit exception. This cleanup issue does not block preparation of the cloud-work plan.

**After execution-plan approval:** Create or use the specified private computing environment, extract only inside protected storage, inspect every dictionary sheet, run the synthetic tests and aggregate inventory, check the report for privacy, and propose a cleaning plan for approval. Setup and audit can share one approval when the plan explicitly covers both. Historical dated entries below retain older approval states and do not override this current snapshot.

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

Before real-file inspection:

> Google Cloud use is approved. Present the exact private setup-and-audit execution plan, current cost, access controls, outputs and shutdown procedure for plan-level approval, then proceed within that approved scope. Keep restricted files in protected cloud storage.

### After the specific setup-and-audit execution plan is approved

- Verify the private compute identity can read only the approved bucket and object.
- Extract in protected cloud storage only after ZIP path checks are repeated there.
- Read every dictionary sheet before creating cleaning rules.
- Run tests and the aggregate inventory before cleaning.
- Verify that the aggregate report contains no patient identifiers or laboratory values.

### Later reminders

- Complete the user-requested local project-folder closeout after the new policy is published and exact deletions are confirmed. Do not recreate a permanent local folder afterward.
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


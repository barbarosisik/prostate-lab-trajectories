# Next agent onboarding

Updated 2026-09-06. Read this file and the listed records before research. Reply TLDR, numbered, action first. Explain why each action is needed, what was verified and what can still go wrong. No em dashes. Do not promise perfect data or permanent conversational memory; use these persistent records.

## Fixed goal and patient locations

Interpret one index patient's blood-test trajectories around chemotherapy cycles. His measured tests and timing determine dataset usefulness, D-027. The trial cohorts develop and test the method; the index patient is the application case, not independent survival-model validation.

- Patient PDFs: `/Users/barbarosisik/PDS-Restricted-Work/goal-patient/`.
- Extracted/transcribed patient data: `/Users/barbarosisik/PDS-Restricted-Work/index-patient/`.
- Latest supplied report: `goal-patient/2026-09-05-laboratory-transcription.pdf` under that restricted root. It is a labelled reconstruction from user-pasted text, not the original laboratory PDF.
- Its structured transcription is `index-patient/2026-09-05-user-supplied-transcription.json`. Rendering checks are in `index-patient/pdf-qa-2026-09-05/`.
- Verified: eight existing PDFs were read for dates and explicit cycle labels. Together with the new supplied report they support nine dated panels. The earlier report explicitly says before cycle 5; before cycle 6 for the new draw is inferred, not confirmed. Counting blood-test dates is not counting chemotherapy cycles.
- The new transcription has 58 current-result entries and 57 historical comparison entries. Do not treat comparison columns as new observations. Keep decimal commas, absolute versus percentage cell counts and inequality qualifiers distinct. A missing testosterone unit/reference remains unresolved.
- Source reports outrank derived summaries. An earlier comparison-date discrepancy is recorded privately; do not promote derived summaries over source reports.
- No patient name, identifier or individual result belongs in Git, logs, chat examples or external services. Do not move patient files into the repository.

The clinical setting is hormone-sensitive, a high-confidence inference rather than certainty. DREAM is castration-resistant and is only the methods cohort. Never report a DREAM survival estimate as this patient's prognosis.

## Mandatory reading order

1. `AGENTS.md`.
2. `PROJECT_CONTINUITY_LOG.md`, Current snapshot and tracker first.
3. `RESEARCH_LOG.md`, current snapshot and decision register. Historical D-021 to D-026 identifiers collide; qualify by date.
4. `docs/dream-dataset-audit-2026-09-04.md`.
5. `docs/data-location-register.md`.
6. `docs/local-processing-and-cloud-storage-plan.md` and `README.md`.
7. Before another source, `docs/source-coverage-matrix.md` and `docs/chaarted-public-field-audit.md`.

There are six necessary documents in `docs/`. Update them; create no additional log, status, register, audit or report files. The detailed field checklist is the sixth retained reference. Five duplicate or obsolete documents were removed locally at the user's request; older content is recoverable in Git history.

## Research question, unchanged D-003

> Among patients with stage-IV metastatic prostate cancer receiving chemotherapy, how are serial pre-chemotherapy blood-test trajectories, individually and in combination, associated with survival, disease progression, treatment response and treatment tolerance, and how early can favorable or unfavorable patterns be detected?

Q-009 is resolved: around each cycle, anchored to harmonized visit labels, not before treatment begins only. Analyze every sufficiently repeated blood value, not PSA alone. The primary window remains cycles 1 to 4. The earlier count of 1,179 complete visit sequences does not prove complete numeric coverage for all tests, or define the early-cycle prediction populations.

## Current verified execution

A0R, A2, A3, A4 and A5 are complete. Preparation Stage 01 was explicitly authorized on 2026-09-06 and is now complete: 1,600 training patients, zero duplicate core keys, zero unmatched rows across 412,575 event records. All 18 extracted CSV hashes match the original pinned package. The roster is `interim/stage01_training_roster.csv` inside the registered restricted run.

Code: `src/preparation/stage01_roster.py`. Twenty-one tests passed, including legacy-byte handling, missing-outcome markers, join failures, source tampering and no-overwrite checks. Source laboratory values and outcome codes were not transformed.

Errors found and handled: three training tables are not valid UTF-8. Stage 01 uses a reversible byte mapping and enforces ASCII keys, without establishing free-text encoding. Evaluation outcome cells contain literal `.` markers, not empty strings. Training death coding is YES or blank; no final outcome recoding is performed by Stage 01.

The 470 evaluation patients remain excluded from supervised work. DREAM has no actual chemotherapy administrations or dose delays/reductions, and no primary imaging-response endpoint. Primary endpoint families are survival and treatment discontinuation; PSA response is secondary. Feature and outcome definitions still require later work.

## Next action and authorization

The latest user instruction explicitly authorizes continuing preparation stages 02 to 07 sequentially toward cleaned data after first publishing the current work. Explain each step and its errors; do not re-request that cleaning approval. Modeling remains separate. Retain the integrity checkpoint after stages 01 to 07 and before features. Modeling at A10 remains a separate approval.

Two tracks remain active: develop methods on DREAM; user searches PDS first for a hormone-sensitive docetaxel trial matching the measured panel. Do not start dbGaP. Institutional affiliation is unanswered. CHAARTED is expected to confirm PSA findings only. Validate internally by leave-one-trial-out across the three DREAM training trials, comparing trends against baseline predictors and freezing the pipeline before the final run. Do not use the index patient or held-out trial to tune cleaning/model choices.

## Local and storage rules

This Mac is the only workspace. Use `/Users/barbarosisik/PDS-Restricted-Work/prostate-lab-trajectories/runs/2026-09-04-audit-001` for restricted DREAM computation. Tooling is under `~/tools`; Python environment `~/tools/venv-pds-audit`. Google Cloud is approved private storage only, never compute. `CLOUDSDK_PYTHON=/Library/Frameworks/Python.framework/Versions/3.12/bin/python3.12` is required by gcloud. Read the register for exact hashes, output preservation and cleanup status. The 2026-09-06 cloud metadata requests stalled/timed out and were stopped; no Stage 01 upload occurred. The verified local bundle is retained. Do not treat a planned cloud path as an upload receipt.

Keep original cloud generation `1787841139282260` unchanged. New derived DREAM versions may be preserved only in the approved private bucket. The patient PDFs are private local records and were not included in the DREAM output bundle. Do not repeat the settled cloud-storage or rejected encryption questions.

Restricted copies remain local. Delete only after verified required preservation and fresh exact-target confirmation. Do not delete the patient originals as part of DREAM run cleanup. The user's Downloads duplicates remain a separate unverified housekeeping reminder.

## Git and reporting

Branch `dataset-audit`; local HEAD `4b3dae83f669b06fd22a04035b253a692589f040` at this session. Changes, including new source/tests and documentation removals, are local and uncommitted. The latest user request explicitly authorizes committing and pushing the permitted developments before further cleaning. Verify live state, not cached remote refs.

Before any add, run `git ls-files --others --exclude-standard` and review every intended path. Commit only permitted code, invented tests and reviewed aggregates, with no assistant attribution. Never use `git add -A` blindly. Update the two existing root logs and current snapshot after meaningful work. Label facts verified, pending, inferred or blocked, and report actual checks rather than claiming perfection.

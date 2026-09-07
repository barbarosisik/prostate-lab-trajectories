# Next agent onboarding

Updated 2026-09-07 after the differential reconciliation closed Q-021 and the user approved the feature plan, D-037, on the landmark cohort design. Read this file first, then the records listed below, before doing any research work.

## 0. How to talk to this user

This matters as much as the technical content. Getting it wrong wastes the user's time and has been corrected repeatedly.

- **Always TLDR.** Lead with the answer and the action. The user has ADHD and has asked for short, action-first replies more than once. A long preamble will not be read.
- **Assume no medical training and only basic data science.** On 2026-09-06 the user said plainly: "I have the data science basics only for this project and that's all, nothing about the medicine also." Define every clinical term and every statistical term at the point of first use, in one or two plain sentences. This includes censoring, landmark analysis, stratification, confounding, non-random missingness, survival endpoints and baseline, not only the oncology words. Prefer a worked example over a precise abstract definition.
- **Make it concrete with the patient's own numbers.** An abstraction the user cannot connect to the index patient's record is a decision they cannot evaluate.
- **No em dashes**, in project files or in replies.
- **Document every function you write.** The user asked for this explicitly: "do documentation on your code next times please, explain the functions at least." Write the docstrings as part of the same change, never as a follow-up offer.
- **Report the error points at the end of every step.** The user asked for this as a standing requirement: what could still be wrong, what was verified, what was assumed.
- **Never claim perfection.** Label every fact verified, pending, inferred or blocked. Never report a download, a test or an upload as complete without direct evidence in that same session.
- **Do not create new documentation files.** The user closed that set: "no more log files, this is all we can have." Update the files that exist. There are six documents in `docs/` and two root logs. That is the complete set.

## 1. The real goal

The project exists to interpret **one real index patient's** blood-test trajectories around his chemotherapy cycles. The public trial data is the reference population and the place to develop the method. It is not the point.

A dataset is useful here only if it contains the tests this patient actually has measured, at comparable timing relative to chemotherapy, with outcomes attached. Coverage of a test he never has is close to worthless. This is decision D-027.

- Patient PDFs: `/Users/barbarosisik/PDS-Restricted-Work/goal-patient/`
- Extracted and transcribed patient data: `/Users/barbarosisik/PDS-Restricted-Work/index-patient/`
- Latest supplied report: `goal-patient/2026-09-05-laboratory-transcription.pdf`, a labelled reconstruction from user-pasted text, not the original laboratory PDF.
- Structured transcription: `index-patient/2026-09-05-user-supplied-transcription.json`. Rendering checks in `index-patient/pdf-qa-2026-09-05/`.

Handling rules, absolute: no patient name, identifier or individual result goes into Git, into the logs, into chat examples, into an artifact, or to any external service. Do not move patient files into the repository. The records are Turkish, from e-Nabiz and Medicana, with comma decimal separators. Keep absolute counts distinct from percentage counts, and keep inequality qualifiers such as `< 0,45` distinct from plain numbers.

The clinical setting is hormone-sensitive disease, which is a high-confidence inference and not a certainty. DREAM is castration-resistant disease and is only the methods cohort. **Never report a DREAM survival estimate as this patient's prognosis.**

The new draw being "before cycle 6" is inferred, not confirmed. Counting blood-test dates is not the same as counting chemotherapy cycles. A missing testosterone unit and reference range remain unresolved.

## 2. Mandatory reading order

1. `AGENTS.md`
2. `PROJECT_CONTINUITY_LOG.md`, the Current snapshot and the A0 to A10 tracker first, then the dated history from the bottom up
3. `RESEARCH_LOG.md`, current snapshot, decision register and open questions. Historical identifiers D-021 to D-026 collide from parallel sessions; qualify them by date. The highest existing identifier is **D-037**; check before adding a new one.
4. `docs/dream-dataset-audit-2026-09-04.md`
5. `docs/data-location-register.md`, which carries every output path and SHA-256
6. `docs/local-processing-and-cloud-storage-plan.md` and `README.md`
7. Only if evaluating another source: `docs/source-coverage-matrix.md` and `docs/chaarted-public-field-audit.md`

## 3. The research question, D-003, unchanged

> Among patients with stage-IV metastatic prostate cancer receiving chemotherapy, how are serial pre-chemotherapy blood-test trajectories, individually and in combination, associated with survival, disease progression, treatment response and treatment tolerance, and how early can favorable or unfavorable patterns be detected?

Q-009 is resolved: "pre-chemotherapy" means **before each cycle**, not only before treatment starts. Analyze every sufficiently repeated blood value, not PSA alone.

## 4. What the data actually is

The source is the DREAM 9.5 prostate cancer challenge package, obtained through Project Data Sphere, pinned and hash-verified. Three trials in the training partition, 1,600 patients, 210,442 laboratory rows.

| Trial | Patients | Character |
|---|---|---|
| CELGENE | 526 | Richest panel, states the day within the cycle |
| EFC6546 | 598 | Full panel from cycle 2 onward, cycle 1 nearly empty |
| ASCENT2 | 476 | PSA only at cycle visits, 13-test panel at pre-enrolment only |

The 470 leaderboard and final-scoring patients are permanently excluded: their outcome labels were never released, so they cannot support supervised work.

Things that are true of this source and cost real time to rediscover:

- **The cycle length is 21 days**, derived from the data, not assumed. Median cycle-start days are 0, 21, 42, 63, 84 in all three trials independently.
- **The laboratory record stops at day 84.** Cycles 1 to 4 are complete; cycle 5 is a truncated stub.
- **DREAM has no chemotherapy administration records**, so no dose delay or reduction can be established.
- Outcomes are `DEATH` (`YES` or blank, where blank means alive at last contact and **not** missing), `LKADT_P` (last known alive day, present for all 1,600), `DISCONT` (0, 1, or a literal `.` for 111 patients), `ENTRT_PC` (treatment stop day, absent for 95 CELGENE patients) and `ENDTRS_C` (five stop reasons).

## 5. Traps that will bite you

**5.1 The rounded value column.** The source stores every result twice. `LBSTRESN` has been rounded to whole numbers throughout: all 194,814 parsable values are integers and 99.8 per cent of the 112,167 disagreements are reproduced by rounding half up. The data dictionary recommends both columns, which is wrong. **Use `LBSTRESC` only.** Using `LBSTRESN` would destroy creatinine, potassium, bilirubin, calcium and neutrophil counts, whose entire clinical ranges span a few units. `stage05_tests_units.select_value_column` enforces this and stops the pipeline if the evidence ever changes.

**5.2 The clock mismatch, the leading unresolved risk.** Laboratory days (`LBDT_PC`) are counted from the **first treatment date**. Outcome days (`LKADT_P`, `ENTRT_PC`) are counted from the **consent date** for ASCENT2 and CELGENE and from **randomization** for EFC6546. Two checks confirmed no per-patient offset is recoverable for the consent-referenced trials: no patient has laboratory rows on both origins, and ASCENT2 shares no visit label between `LabValue` and `VitalSign`. EFC6546's offset is measurable through `VitalSign` at a median of 2 days. Any analysis mixing laboratory time with outcome time must state this limitation. See Q-016.

**5.3 The trials are not comparable on death.** Death rates are 72.4 per cent in EFC6546, 29.0 in ASCENT2 and 17.5 in CELGENE, tracking median follow-up of 642, 357 and 279 days. Trial must enter any pooled survival model as a stratum or the model will learn the trial rather than the patient.

**5.4 Baseline is not a screening visit.** 15,639 CELGENE baseline-flagged rows sit on cycle 1 day 1, because the last draw before the first dose happens that morning. Restricting baselines to pre-treatment visits would discard most CELGENE baselines. The flag plus the timing defines a baseline, never the visit's name.

**5.5 The `.` test code is sodium.** All 6,151 rows carry `LBTEST` = SODIUM, `LBCAT` = CHEMISTRY, unit MMOL/L. It is recovered from the name, never guessed from the size of a result.

**5.6 Requiring a test is not the same as studying one.** This was a genuine error made and corrected on 2026-09-06. Only a **required** test shrinks the cohort, because the cohort is the intersection of the required tests' groups. A test **studied** on its own group costs nothing. An earlier statement that LDH and sodium jointly cost 428 patients was misleading: sodium costs 2, LDH costs 392. Never lump tests together when reporting a coverage cost.

**5.7 Units are already harmonized.** `LBORRESU` is chaotic, recording a white cell count 33 different ways, but `LBSTRESU` holds exactly one standardized unit per test code across all three trials. Convert nothing. Blank units on used measurements are urine pH and specific gravity, which are genuinely dimensionless.

## 6. What has been completed and verified

All seven authorized preparation stages plus the integrity checkpoint. Code in `src/preparation/`, tests in `tests/`. **180 tests, all passing.** Run them with `/Users/barbarosisik/tools/venv-pds-audit/bin/python -m unittest discover -s tests`.

| Stage | File | What it established |
|---|---|---|
| 01 | `stage01_roster.py` | 1,600-patient roster, zero duplicate keys, zero unmatched joins across 412,575 event rows |
| 02 | `stage02_visits.py` | All 29 visit labels translated by an exhaustive per-trial lookup table; an unknown label stops the pipeline |
| 03 | `stage03_timing.py` | Labels corroborated against recorded days; **zero cycle order violations** across 1,600 patients |
| 04 | `stage04_roles.py` | One research purpose per row, 7,130 exclusions each with one of five stated reasons, nothing deleted |
| 05 | `stage05_tests_units.py` | 103 test codes, zero name conflicts, zero unit conflicts, rounded column rejected |
| 06 | `stage06_values.py` | Four value kinds kept apart, repeats settled, 175,308 usable measurements |
| 07 | `stage07_baseline.py` | 38,623 baselines, 37,647 from the sponsor flag, 976 from one stated fallback, 6 abandoned to conflicting flags |
| checkpoint | `integrity_review.py` | Every reconciliation passed; panel tiers derived from measured coverage |

Each stage runs from `src/preparation/` with the isolated interpreter, for example
`cd src/preparation && /Users/barbarosisik/tools/venv-pds-audit/bin/python stage06_values.py`.
Every stage writes mode 600 with exclusive creation, so **a stage will refuse to run twice**; delete the prior output deliberately if you need to re-run.

Standing guarantees that must not be broken by later work: **no laboratory value has been edited, no unit converted, no row deleted.** Every exclusion carries a reason and every excluded row is retained in the output.

### The current study size

Tests are tiered by their own usable group, meaning patients holding that test at cycles 2, 3 and 4 plus a baseline.

- **Primary panel, 18 tests, 600 or more patients each:** ALB, ALP, ALT, AST, CA, CREAT, GLU, HB, K, MG, NEU, PHOS, PLT, PSA, SODIUM, TBILI, TPRO, WBC. Required of every patient.
- **Analysis-ready cohort: 574 patients.**
- **Secondary panel, 22 tests, 300 to 599 patients each:** studied on their own groups, costing the cohort nothing. Includes LDH, RBC, HCT, the white cell differential, BUN, UREA, URAC, CL, HCO3 and the urine measures.
- 23 further tests are descriptive only. 63 of 103 codes have any usable data in the window.

## 7. The exact next action

**Q-021 is closed and D-037 was approved on 2026-09-07. The next action is to build the per-cycle landmark feature tables.**

**Step 1, done 2026-09-07.** The five `...LE` codes are not duplicates. Each pair is one cell type in two forms: a count of cells in `10^9/L` and that cell type's share of all white cells in `%`. All 14,380 paired readings reproduce `100 * count / WBC` within 1.0 percentage point, worst case 0.45, and the five counts total the white cell count while the five shares total a hundred. Both forms are kept. Because a share is fully determined by its count and `WBC`, `DERIVED_FROM` in `src/preparation/differential_reconciliation.py` records that dependency, and no feature may use all three as independent evidence. A recorded but unacted-on option: 75 readings hold a usable `NEULE` where Stage 06 left `NEU` contested, and the share plus `WBC` could settle those. That would be a data decision and needs its own approval.

**Step 2, presented and APPROVED 2026-09-07 as D-037.** Asked to choose between the landmark cohort and the certified 574-patient intersection, the user chose the landmark design. Build on it. Modeling at A10 is still a separate gate and may not be inferred from this approval. What the approved plan says and why:

- **Cohort.** Build a separate landmark cohort for each of cycles 2, 3 and 4, rather than the single 574-patient cohort that requires all 18 primary tests at all three cycles. The intersection design silently requires staying on treatment for 63 days and keeps only 6 of the 197 recorded discontinuations, against 39 at cycle 2, 25 at cycle 3 and 7 at cycle 4. Landmark sizes are 439, 786, 782 and 735 at cycles 1 to 4, all larger than 574, and the cycle-2 cohort matches the roster on death rate, 43.1 against 41.4 per cent.
- **Features per test at landmark cycle k:** the value at cycle k, the change from baseline to cycle k, and from cycle 3 onward one fitted slope across baseline to cycle k. 36 candidates at cycle 2, 54 at each of cycles 3 and 4, 144 in total. Cycle 1 is not used as a previous-cycle reference because EFC6546 cycle 1 is nearly empty.
- **Timing restriction.** Each landmark uses only data recorded up to its own cycle, follow-up starts at that cycle's day, and no patient is required to survive or remain on treatment beyond it.
- **Missingness, counted not worked around.** All 476 ASCENT2 patients are excluded from every multi-test cohort at every cycle, because that trial records only PSA at cycle visits; this resolves Q-012. A further 168 roster patients have no usable cycle-2 measurement at all and are the sickest group, 87 of them discontinued and 32 last known alive within 84 days. No per-cycle design can include them.
- **Endpoints at the cycle-2 landmark:** overall survival with 339 deaths, usable. `DISCONT` with 39 events and 96 missing, exploratory only, which bears on Q-017. `ENDTRS_C` as a reason for stopping, 307 progression, 122 adverse event, 260 possible adverse event, 96 miscellaneous, 1 completed, categorical and undated.
- **Trial as a stratum, not a covariate to ignore.** In the intersection cohort CELGENE shows 11.1 per cent deaths at median last-known day 280 against EFC6546 at 70.0 per cent and 730 days.
- **Candidate-signal control, Q-022:** one primary endpoint and one primary landmark giving 36 primary candidates, Benjamini-Hochberg false discovery rate at 5 per cent within each family, every other combination labelled exploratory, and a primary finding required to hold in CELGENE and EFC6546 separately.
- **Validation and its weakness:** leave-one-trial-out is only two-fold for the primary panel, since ASCENT2 contributes nobody. ASCENT2 supplies a genuine third trial for PSA alone, 367 patients at the cycle-2 landmark. Freeze the pipeline before reading any index-patient value and never tune on him.

Modeling itself is tracker step **A10** and needs its own separate approval. Do not infer it from the preparation approval.

## 8. Local environment and storage rules

This MacBook Pro is the only workspace. Ignore every reference to an earlier Windows machine; those are historical and out of scope.

- Git working copy: `/Users/barbarosisik/Desktop/prostate-lab-trajectories`
- Restricted run root: `/Users/barbarosisik/PDS-Restricted-Work/prostate-lab-trajectories/runs/2026-09-04-audit-001`
- Tooling: `~/tools`, Python environment `~/tools/venv-pds-audit`
- `gcloud` requires `CLOUDSDK_PYTHON=/Library/Frameworks/Python.framework/Versions/3.12/bin/python3.12`

Restricted patient data belongs only under the restricted run root. Never in the Git working copy, never in the tooling directory.

Google Cloud is approved **private storage only, never compute**. As of 2026-09-06 it is **unreachable from this machine**: `storage.googleapis.com` and `oauth2.googleapis.com` both fail at the network layer and `gcloud storage buckets describe` times out. That is a connectivity failure, not a permissions problem. No Stage 01 or later bundle has been uploaded. A planned cloud path is not an upload receipt. Keep original generation `1787841139282260` unchanged.

Restricted local copies stay local. Delete only after verified preservation and a fresh, exact-target confirmation from the user. Do not delete the patient originals as part of any DREAM cleanup.

## 9. Git and reporting discipline

Branch `dataset-audit`. Verify the live remote with `git ls-remote origin dataset-audit` rather than trusting a cached ref.

Before any add, run `git ls-files --others --exclude-standard` and review every intended path. Commit only code, invented-data tests, and reviewed aggregates. **Commit messages carry no assistant attribution or self-reference.** The restricted run root sits outside the repository and `goal-patient/` is ignored, but verify rather than trusting that.

After any meaningful action, discovery, failure, decision or approval, update both root logs as part of the same piece of work:

- `PROJECT_CONTINUITY_LOG.md`: refresh the Current snapshot, update the A0 to A10 tracker row, and append a dated session entry saying what was verified, what was assumed and the exact next action.
- `RESEARCH_LOG.md`: methodological decisions, the `D-0xx` register, the open-questions table.

Record new output files in `docs/data-location-register.md` with size and SHA-256.

## 10. Open questions that are live right now

| ID | Question |
|---|---|
| Q-016 | How to reconcile the laboratory clock with the outcome clock when no per-patient offset is recoverable for ASCENT2 and CELGENE |
| Q-017 | Whether the discontinuation endpoint is restricted to the 1,489 patients with a non-missing `DISCONT`, and how the 95 without a stop day are handled |
| Q-018 | How the 745 bounded results and the 543 rows whose bound was lost upstream are handled in a trajectory |
| Q-020 | Whether EFC6546 numbers its first treatment day as 1 rather than 0. All 2,221 positive-day baselines are exactly day 1 and all from that trial |
| Q-021 | RESOLVED 2026-09-07 by `differential_reconciliation.py`. The `...LE` codes are each cell type's share of the white cell count in `%`, not a duplicate of the count in `10^9/L`. All 14,380 paired readings reproduce `100 * count / WBC` within 1.0 percentage point. Both kept, nothing dropped, and `DERIVED_FROM` records each share as a function of its count and `WBC`. |
| Q-022 | How the number of candidate signals is controlled so chance findings are not reported as real |

Two tracks remain active. Develop the method on DREAM. Separately, the user searches Project Data Sphere first for a hormone-sensitive docetaxel trial matching the measured panel. Do not start a dbGaP application. Institutional affiliation is still unanswered. CHAARTED is expected to confirm PSA findings only.

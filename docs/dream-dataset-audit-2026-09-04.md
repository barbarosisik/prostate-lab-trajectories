# DREAM dataset audit and feasibility verdict, 2026-09-04

Aggregate-only audit of the Project Data Sphere Prostate Cancer DREAM package, run `2026-09-04-audit-001`. Every figure is a count or percentage computed locally. No patient identifier and no laboratory result value appears in this document.

Source verified at 6,227,480 bytes with SHA-256 `AB3ECA19C5D0CC4106C96AC04E665DD1A5C9DF58F66328ECD24E8E1067932391`, matching the 2026-08-27 record. Expanded size 110,112,522 bytes.

## Verdict

The data is genuinely useful, but it does NOT support the fixed research question as written. It supports a sharper and smaller version of that question well. Two of the four named outcome families are weak or absent, and the phrase "pre-chemotherapy trajectories" is feasible under only one of its two possible meanings.

## The goal being judged against

> Among patients with stage-IV metastatic prostate cancer receiving chemotherapy, how are serial pre-chemotherapy blood-test trajectories, individually and in combination, associated with survival, disease progression, treatment response and treatment tolerance, and how early can favorable or unfavorable patterns be detected?

That sentence makes five demands: serial blood values, four distinct outcome families, and early detection.

## Partitions and effective sample size

| Partition | Patients | Trials | Outcome labels | Lab rows |
|---|---|---|---|---|
| training | 1,600 | EFC6546 598, CELGENE 526, ASCENT2 476 | Present | 210,442 |
| leaderboard | 157 | AZ only | WITHHELD | 6,144 |
| finalscoringset | 313 | AZ only | WITHHELD | 12,065 |

The usable sample is 1,600, not 2,070. The two held-out partitions were the blinded DREAM competition test sets and their `DEATH` and `LKADT_P` fields are entirely blank, so they cannot train, validate or independently test an outcome model. The AZ trial is consequently unavailable, because it appears only in those partitions. The dictionary documents four trials; three are actually usable.

## Cohort uniformity, the dataset's best property

All 1,600 training patients carry `TRT1_ID = PLACEBO`, with 1,585 on `DOCETAXEL` and 1,581 on `PREDNISONE`. These are the control arms of three phase 3 trials in metastatic castration-resistant prostate cancer, so treatment exposure is almost uniform by construction. Treatment heterogeneity is the usual confounder in trajectory analysis and it is largely absent here.

## Laboratory coverage

210,442 measurements, 103 distinct `LBTESTCD` codes, 92.6% carrying a usable numeric `LBSTRESN`.

Tier 1, near universal at roughly 99.8% of patients, twelve tests: `ALP` 100.0%, `PSA` 99.9%, `CREAT` 99.9%, `ALT` 99.9%, `TBILI` 99.9%, `AST` 99.9%, `HB` 99.8%, `WBC` 99.8%, `PLT` 99.8%, `NEU` 99.8%, `CA` 99.8%, `TESTO` 99.2%.

Tier 2, roughly 70%: `GLU` 70.2%, `K` 70.2%, `ALB` 70.1%, `MG` 70.0%, `PHOS` 69.7%, `TPRO` 69.6%, `LDH` 62.8%.

Tier 3, roughly 33%, the full differential and extended chemistry: `RBC`, `HCT`, `LYM`, `MONO`, `EOS`, `BASO`, `CL`, `HCO3`, `URAC`.

Decision D-002 committed the project to analysing every sufficiently repeated blood test rather than PSA alone. That commitment is supportable, but across twelve tests only. Those twelve cover haematologic reserve, liver function, renal function, bone turnover and tumour burden, which includes the components most associated with chemotherapy tolerance. Differential-based features drop roughly two thirds of the cohort non-randomly, tracking trial membership, so they must remain a secondary sensitivity analysis.

## Measurement timing

Relative to first treatment on day 0: 50,777 measurements before treatment, 24.1%; 14,549 on day 0, 6.9%; 144,602 on or after treatment, 68.7%; 514 with no collection day, 0.2%.

## The pivotal finding: repeated measurement before treatment

Distinct pre-treatment laboratory days per patient: median 2, interquartile range 1 to 3, maximum 11. Only 98.9% have at least one, 51.1% have at least two, and 37.1% have at least three.

Across the whole observation window instead: median 7, interquartile range 5 to 8, maximum 33.

A trajectory needs at least three points. Under the reading that "pre-chemotherapy" means before docetaxel starts, half the cohort has two measurement days and the question is not feasible on this package. Under the reading that it means drawn before each chemotherapy cycle, which is standard oncology usage, the 144,602 on-treatment measurements are the pre-dose safety labs and the data is ample. That second reading also aligns better with the "how early can patterns be detected" clause, because early-cycle labs are actionable at the bedside whereas pre-treatment labs are only a baseline.

This is recorded as open question Q-009 and must be answered by the user, since the two readings produce different projects.

## The four outcome families, scored

**Survival: STRONG.** `LKADT_P` populated for all 1,600. `DEATH` records 663 events, a 41.4% event rate. Follow-up time is complete. Sufficient events for multivariable time-to-event modelling on a twelve-test feature set.

**Treatment tolerance: PARTIAL.** `ENDTRS_C` complete for all 1,600, separating `possible_AE` 594, `progression` 540, `AE` 239, `complete` 116, `misce` 111. `ENTRT_PC` gives the discontinuation day for 94.1%. `LBTOXGR` adds per-measurement toxicity grades. Dose reduction, dose delay and cumulative dose cannot be studied because no such data exists.

**Disease progression: WEAK.** `LesionMeasure` covers 1,123 patients, 70.2%, and ASCENT2 supplied no lesion data. Median assessment days per patient 2, maximum 6. Results are largely qualitative strings such as `PRESENT/STABLE` and `IR` rather than RECIST categories. The only cohort-wide signal is `ENDTRS_C = progression` at 540 patients, a coarse reason for stopping rather than a dated radiographic event.

**Treatment response: WEAK.** No RECIST response field exists anywhere in the package. A PSA response endpoint is derivable and PSA is excellent, 9,310 measurements across 99.9% of patients, but PSA response is a different and weaker endpoint and must be labelled as such.

## Confirmed absences

1. **Chemotherapy administration records.** `PriorMed` is 147,770 rows with `CMPRE = YES` on every row and ZERO rows starting on or after day 0. It is baseline prior medication only. Exactly one row names docetaxel, pre-treatment. No cycle dates, no per-cycle doses, no reductions, no delays.
2. **Outcome labels for 470 patients**, and with them the whole AZ trial.
3. **RECIST response categories.**
4. **Serum sodium in `CoreTable`.** The `NA` column is defined but empty for all 1,600 patients. Sodium is available only through `LabValue`.
5. **Usable creatinine clearance.** `CREACL` 5.9%, `CREACLCA` 3.2%. Renal function must be derived from creatinine.

## Data quality issues for the cleaning stage

A malformed test code of `.` carries 6,151 rows across 1,123 patients and needs an explicit exclusion or recovery rule. Separately, 15,628 laboratory rows, 7.4%, lack a usable numeric result, some legitimately flagged `LBSTAT = NOT DONE`, which must not be imputed as measured.

## What dies and what survives

Dies: radiographic progression as a primary endpoint; RECIST treatment response; anything involving chemotherapy dose intensity, delay or reduction; any use of the 470 held-out patients; any trajectory analysis restricted strictly to the pre-docetaxel window.

Survives, and survives well: a study of how serial trajectories across twelve routinely measured blood tests, taken before each chemotherapy cycle, relate to overall survival and to treatment discontinuation, in a 1,600 patient cohort on a near-identical first-line docetaxel regimen, with 663 death events and complete follow-up. Plus a secondary PSA-response analysis, and time-varying `ECOG PERFORMANCE STATUS` and `WEIGHT` from `VitalSign`, which covers all 1,600 patients across 36,841 records.

That surviving study is legitimate and publishable. The uniform treatment exposure is a genuine methodological advantage over the real-world databases considered earlier, and the event count supports multivariable modelling. The recommendation is to narrow the question to survival and tolerance on this package and treat progression and response as a separate future study requiring a source such as CHAARTED, rather than weakening endpoint definitions to fit what is available.

## Decisions required from the user

1. Which reading of "pre-chemotherapy" was intended, before docetaxel starts or before each cycle. Recommendation: before each cycle, on both feasibility and clinical relevance.
2. Whether to narrow the outcome families to survival and treatment discontinuation for this dataset, with PSA response as a labelled secondary, moving progression and RECIST response to a separate study.

No cleaning or modelling should begin until these are settled.

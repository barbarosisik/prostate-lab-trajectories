# DREAM dataset audit and feasibility verdict, 2026-09-04

Aggregate-only audit of the Project Data Sphere Prostate Cancer DREAM package, run `2026-09-04-audit-001`. Every figure is a count or percentage computed locally. No patient identifier and no laboratory result value appears in this document.

Source verified at 6,227,480 bytes with SHA-256 `AB3ECA19C5D0CC4106C96AC04E665DD1A5C9DF58F66328ECD24E8E1067932391`, matching the 2026-08-27 record. Expanded size 110,112,522 bytes.

## Verdict

**Verified limitation:** this is a methods cohort, not an index-patient prognosis dataset. DREAM cannot support actual chemotherapy dose/delay analyses or primary imaging-response claims. Its 1,600 training patients support investigation of visit-anchored laboratory trajectories with survival and treatment-stopping outcomes, subject to cleaning and later endpoint validation. The fixed research question is unchanged. Q-009 is resolved as around each cycle; D-024 to D-033 supersede the earlier open-question wording.

## The goal being judged against

> Among patients with stage-IV metastatic prostate cancer receiving chemotherapy, how are serial pre-chemotherapy blood-test trajectories, individually and in combination, associated with survival, disease progression, treatment response and treatment tolerance, and how early can favorable or unfavorable patterns be detected?

That sentence makes five demands: serial blood values, four distinct outcome families, and early detection.

## Partitions and effective sample size

| Partition | Patients | Trials | Outcome labels | Lab rows |
|---|---|---|---|---|
| training | 1,600 | EFC6546 598, CELGENE 526, ASCENT2 476 | Present | 210,442 |
| leaderboard | 157 | AZ only | WITHHELD | 6,144 |
| finalscoringset | 313 | AZ only | WITHHELD | 12,065 |

The usable sample is 1,600, not 2,070. The two held-out partitions were the blinded DREAM competition test sets and their `DEATH` and `LKADT_P` fields contain only missing markers, verified as literal `.` on 2026-09-06, so they cannot train, validate or independently test an outcome model. The AZ trial is consequently unavailable, because it appears only in those partitions. The dictionary documents four trials; three are actually usable.

## Cohort uniformity, the dataset's best property

All 1,600 training patients carry `TRT1_ID = PLACEBO`, with 1,585 on `DOCETAXEL` and 1,581 on `PREDNISONE`. These are the control arms of three phase 3 trials in metastatic castration-resistant prostate cancer, so treatment exposure is almost uniform by construction. Treatment heterogeneity is the usual confounder in trajectory analysis and it is largely absent here.

## Laboratory coverage

210,442 measurements, 103 distinct `LBTESTCD` codes, 92.6% carrying a usable numeric `LBSTRESN`.

Tier 1, near universal at roughly 99.8% of patients, twelve tests: `ALP` 100.0%, `PSA` 99.9%, `CREAT` 99.9%, `ALT` 99.9%, `TBILI` 99.9%, `AST` 99.9%, `HB` 99.8%, `WBC` 99.8%, `PLT` 99.8%, `NEU` 99.8%, `CA` 99.8%, `TESTO` 99.2%.

Tier 2, roughly 70%: `GLU` 70.2%, `K` 70.2%, `ALB` 70.1%, `MG` 70.0%, `PHOS` 69.7%, `TPRO` 69.6%, `LDH` 62.8%.

Tier 3, roughly 33%, the full differential and extended chemistry: `RBC`, `HCT`, `LYM`, `MONO`, `EOS`, `BASO`, `CL`, `HCO3`, `URAC`.

Decision D-002 committed the project to analysing every sufficiently repeated blood test rather than PSA alone. The twelve near-universal tests are primary candidates; every additional sufficiently repeated test remains in scope under D-002, with trial-specific coverage reported. Those twelve cover haematologic reserve, liver function, renal function, bone turnover and tumour burden, which includes the components most associated with chemotherapy tolerance. Differential-based features drop roughly two thirds of the cohort non-randomly, tracking trial membership, so they must remain a secondary sensitivity analysis.

## Measurement timing

Relative to first treatment on day 0: 50,777 measurements before treatment, 24.1%; 14,549 on day 0, 6.9%; 144,602 on or after treatment, 68.7%; 514 with no collection day, 0.2%.

## The pivotal finding: repeated measurement before treatment

Distinct pre-treatment laboratory days per patient: median 2, interquartile range 1 to 3, maximum 11. Only 98.9% have at least one, 51.1% have at least two, and 37.1% have at least three.

Across the whole observation window instead: median 7, interquartile range 5 to 8, maximum 33.

Two usable points permit a change or slope; acceleration needs at least three. Q-009 was resolved by the user on 2026-09-04 in favor of around-cycle measurements. Use harmonized visit labels, retaining within-cycle day and trial-specific time origins. On-treatment laboratory records are not proof of pre-dose timing because administration records are absent.

## The four outcome families, scored

**Survival: STRONG.** `LKADT_P` populated for all 1,600. `DEATH` records 663 events, a 41.4% event rate. Follow-up time is complete. These 663 events refer to the full training roster; the usable event count and supported model complexity must be recalculated after endpoint-specific landmark eligibility.

**Treatment tolerance: PARTIAL.** `ENDTRS_C` complete for all 1,600, separating `possible_AE` 594, `progression` 540, `AE` 239, `complete` 116, `misce` 111. `ENTRT_PC` gives the discontinuation day for 94.1%. `LBTOXGR` adds per-measurement toxicity grades. Dose reduction, dose delay and cumulative dose cannot be studied because no such data exists.

**Disease progression: WEAK.** `LesionMeasure` covers 1,123 patients, 70.2%, and ASCENT2 supplied no lesion data. Median assessment days per patient 2, maximum 6. Results are largely qualitative strings such as `PRESENT/STABLE` and `IR` rather than RECIST categories. The only cohort-wide signal is `ENDTRS_C = progression` at 540 patients, a coarse reason for stopping rather than a dated radiographic event.

**Treatment response: WEAK.** No RECIST response field exists anywhere in the package. A PSA response endpoint is derivable and PSA is excellent, 9,310 measurements across 99.9% of patients, but PSA response is a different and weaker endpoint and must be labelled as such.

## Confirmed absences

1. **Chemotherapy administration records.** `PriorMed` is 147,770 rows with `CMPRE = YES` on every row and ZERO rows starting on or after day 0. It is baseline prior medication only. Exactly one row names docetaxel, pre-treatment. No cycle dates, no per-cycle doses, no reductions, no delays.
2. **Outcome labels for 470 patients**, and with them the whole AZ trial.
3. **RECIST response categories.**
4. **Serum sodium in `CoreTable`.** The literal `NA.` column is defined but empty for all 1,600 patients. Sodium is available only through `LabValue`.
5. **Usable creatinine clearance.** `CREACL` 5.9%, `CREACLCA` 3.2%. Renal function must be derived from creatinine.

## Data quality issues for the cleaning stage

A malformed test code of `.` carries 6,151 rows across 1,123 patients and needs an explicit exclusion or recovery rule. Separately, 15,628 laboratory rows, 7.4%, lack a usable numeric result, some legitimately flagged `LBSTAT = NOT DONE`, which must not be imputed as measured.

## Agreed scope and index-patient relevance

Primary DREAM outcome families are survival and treatment discontinuation. PSA response is explicitly secondary and is not imaging response. Actual dose reduction, delay and cumulative dose are unsupported. The patient has measured counterparts for the twelve principal DREAM tests and additional tests; his clinical records and values remain outside Git in the registered patient folders.

The patient's hormone-sensitive setting is a high-confidence inference from prior records, with pathology, imaging and baseline-treatment documentation still incomplete. DREAM is castration-resistant. Do not present DREAM-derived survival estimates as his prognosis or claim that one application patient validates a predictive model. PDS-first search for a matching hormone-sensitive docetaxel source remains the parallel track.

The recorded 1,179 patients with visits across cycles 1 to 4 are not proven to have every test numerically complete at every cycle. Preserve the approved primary window while reporting actual test-level eligibility and avoiding future-completion selection for earlier prediction times.

## Public-code provenance retained after documentation consolidation

The [GuanLab original processing code](https://github.com/GuanLab/prostate_discontinuation/blob/master/code/OriginDataProcess.Rmd) uses `RPT`, `STUDYID`, baseline laboratory/context fields and core death/discontinuation variables. The [paper code](https://github.com/GuanLab/prostate_discontinuation/blob/master/code/PaperMainCode.Rmd) provides additional schema and historical model clues. This is documentary evidence, not source data or a final outcome definition. The official dictionary and checked received files remain authoritative.

The original inventory implementation uses fixed aliases, nonempty-result repetition and a baseline day heuristic. Those are not approved cleaning rules. Its three original invented-data tests were supplemented by Stage 01 tests. Current execution and errors are recorded below and in the two existing root logs.

## Stage 01 completed, 2026-09-06

**Verified:** 1,600 patients retained: ASCENT2 476, CELGENE 526 and EFC6546 598. Zero duplicate composite core keys. All 412,575 rows across five event tables join exactly once to the core roster. No test/cycle completeness exclusion, laboratory transformation or outcome recoding was applied.

| Table | Source/event rows | Unmatched rows |
|---|---:|---:|
| LabValue | 210,442 | 0 |
| LesionMeasure | 10,009 | 0 |
| MedHistory | 7,513 | 0 |
| PriorMed | 147,770 | 0 |
| VitalSign | 36,841 | 0 |

**Verified integrity:** all 18 CSVs match bytes from the nested archives in the SHA-256-pinned original package. Source files remain unchanged. The new mode-600 roster contains 1,600 records and passed exact CSV read-back verification. Code and output checksums are in the data register and existing restricted inventory. Twenty-one invented-data tests passed.

**Errors found, then handled:** MedHistory, PriorMed and VitalSign training files reject UTF-8 decoding. A reversible byte mapping allows Stage 01 to parse ASCII keys without replacing characters or guessing free-text encoding. The first run stopped before output. A second run detected that evaluation outcomes use literal `.` markers. Both issues have regression tests; the successful run preserved the source and excluded all 470 evaluation patients.

**Pending error points:** semantic free-text encoding, per-test units, visit/day consistency, duplicate laboratory measurements, baseline ambiguity and endpoint coding. The training death field has 663 YES and 937 blank entries; no claim that blanks mean a verified current alive state was added. Test success is not a guarantee that later cleaning or scientific models are correct.

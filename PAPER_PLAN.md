# Paper plan: what we will look for

Created 2026-10-09 at the user's explicit request, as the one place that says what the paper will test, with what, and what it cannot claim. Living document: update it in place. It holds no index-patient value and no patient-level DREAM row.

Every item carries a status: **APPROVED** (with its decision ID in `RESEARCH_LOG.md`), **PROPOSED** (waiting for the user), **LATER**, or **NOT POSSIBLE** (the data cannot support it).

## 1. The question, fixed by D-003

> Among patients with stage-IV metastatic prostate cancer receiving chemotherapy, how are serial pre-chemotherapy blood-test trajectories, individually and in combination, associated with survival, disease progression, treatment response and treatment tolerance, and how early can favorable or unfavorable patterns be detected?

**Scope, user decision 2026-10-09:** metastatic men on chemotherapy only. Widening to men who never had chemotherapy would change the question; the user will decide after the first results show how much this scope limits the work.

## 2. What the data cannot support, read this first

| Limit | Evidence | Consequence for the paper |
|---|---|---|
| No chemotherapy dose or administration records | `PriorMed` is baseline only (D-022, 2026-09-04) | No dose delay, reduction or missed-cycle analysis. Tolerance means stopping treatment only |
| Laboratory record ends at day 84 | Latest on-treatment day anywhere is 84; zero rows later (verified 2026-10-09) | The hormone-sensitive landmark studies (PSA at months 4 to 7, week 24) cannot be reproduced in DREAM |
| Every DREAM patient is castration-resistant | D-028 | No DREAM survival figure is anyone's prognosis, least of all a hormone-sensitive patient's |
| Laboratory clock and outcome clock start on different days | Q-016 | Hazard ratios are usable; absolute survival times carry an offset grid |
| Progression and response are weak | D-023 | Primary endpoint is overall survival. PSA response is secondary and labelled as such |
| Treatment stop is rare in the landmark cohorts | 39 stops at the cycle-2 landmark | Tolerance results are exploratory only |
| Multi-test cohorts come from two trials | ASCENT2 measured only PSA at cycle visits | Combined models are CELGENE plus EFC6546; ASCENT2 joins PSA-only analyses |

## 3. What we will look for, general to specific (D-039)

Terms: a **checkpoint (landmark)** is a fixed day; we keep only patients alive that day, use only blood values from before it, and count survival from it. A **hazard ratio** compares how fast deaths happen in two groups; 0.5 means half as fast. A **stratum** lets each trial keep its own baseline death rate, so the model cannot learn the trial instead of the patient.

| Level | Question in plain words | Who | Main result | Status |
|---|---|---|---|---|
| 1 Everyone | Which starting blood values go with survival? | All 1,600, each test on everyone holding a starting value | Hazard ratio per test, trial as stratum | APPROVED, not run |
| 2 Each test alone | Does the value at the checkpoint add anything to the starting value? | Everyone holding that test at the checkpoint | Likelihood-ratio test per test, Benjamini-Yekutieli across 18 tests | APPROVED (D-038), not run |
| 3 Combined | Does Model B (starting plus checkpoint values) predict survival better than Model A (starting values only)? | 786 patients, 339 deaths, cycle-2 checkpoint | Uno's C, time-dependent AUC, Brier score, calibration | APPROVED design; predictor list PROPOSED (D-040) |
| 3b How early | At which checkpoint does B first beat A? | Checkpoints at days 31, 52, 73 | Gain in Uno's C per checkpoint | APPROVED |
| 4 Subgroups and setting | Do patterns differ by trial, or between castration-resistant and hormone-sensitive men? | Later sources | Interaction tests | LATER |
| 5 Index patient | Is each change bigger than laboratory and personal noise, and where does it sit against a reference? | One patient | Reference change values, conditional centiles; no model output | APPROVED (D-038), descriptive only |

## 4. The model parameters

A **parameter** is one number a model learns, like a weight. Too many for the number of deaths and the model memorizes noise.

### 4.1 Layer 2, one test at a time, decided (D-038)

For each of the 18 primary tests (ALB, ALP, ALT, AST, CA, CREAT, GLU, HB, K, MG, NEU, PHOS, PLT, PSA, SODIUM, TBILI, TPRO, WBC), one stratified Cox model with exactly two parameters:

- weight 1 on the starting value;
- weight 2 on the value at the checkpoint.

The question is whether weight 2 is zero. Trial is a stratum and costs no parameter. Value and change from start are the same test once the start is in the model (Tennant 2022), so there is no separate change term. Values stay continuous; splines are a sensitivity analysis only.

**Scale rule, PROPOSED (D-040):** log scale for tests whose starting values are clearly right-skewed, judged from baselines only, before any outcome is read. Never percentage change.

### 4.2 Layer 3, the combined model, PROPOSED (D-040)

Budget from Riley et al. 2019 for 786 patients, recomputed locally:

| Assumed model strength (R2cs) | 0.10 | 0.119 | 0.15 | 0.20 | 0.25 |
|---|---|---|---|---|---|
| Parameters allowed | 9.26 | 11.18 | 14.33 | 19.75 | 25.58 |

Proposed predictors, chosen from the literature before any DREAM outcome is examined. Each costs two parameters in Model B: starting value and checkpoint value.

| Test | Scale | Why, with catalog IDs | Model A | Model B |
|---|---|---|---|---|
| PSA | log | Strongest on-treatment evidence: Petrylak 2006 (LIT-041), Armstrong 2007 (LIT-011); Halabi baseline model (LIT-007) | 1 | 2 |
| ALP | log | Halabi (LIT-007); change by day 90 in Sonpavde 2012 (LIT-012); Salfi 2025 (LIT-047) | 1 | 2 |
| HB | linear | Halabi (LIT-007); TAX327 nomogram (LIT-010); serial haemoglobin added to PSA in Vollmer 2002 (LIT-013) | 1 | 2 |
| ALB | linear | Halabi (LIT-007); falling albumin in Salfi 2025 (LIT-047) | 1 | 2 |
| NEU | log | Docetaxel exposure and tolerance: de Vries Schultink 2019 (LIT-019), Buttigliero 2018 (LIT-044); neutrophil ratio in van Soest 2015 (LIT-043) | 1 | 2 |
| **Total** | | | **5** | **10** |

- **Reserve, first in line:** SODIUM (Salfi 2025, exploratory), which would make Model B 12 parameters, within budget only if model strength is 0.13 or more.
- **Why 10 and not 14:** 10 fits the central budget of 11.18 with room to spare, but not the pessimistic 9.26. That margin is the reason not to add more.
- **Left out on purpose:** LDH (strong in Halabi, but requiring it shrinks the cohort; studied on its own 463-patient group); ECOG performance status (a clinical fitness score, not a blood test; added to both models as a sensitivity analysis); the differential percentage codes (D-036: derived from counts); the other 13 tests (Layer 2 only).
- **Weakness, inferred:** in the train-on-one-trial check, each training trial has about 400 patients, so the budget falls to about 5 or 6 parameters. That check is a transportability test, not the primary validation.

### 4.3 Prediction horizon, PROPOSED (D-040, answers Q-024)

- **Primary:** 180 days after each checkpoint. **Sensitivity:** 365 days.
- **Why (verified 2026-10-09, aggregate follow-up only, outcome clock):** 70.0 per cent of CELGENE patients are still followed at day 211 (cycle-2 checkpoint plus 180 days), but only 25.7 per cent at day 396 (plus 365 days). A one-year horizon would rest mostly on EFC6546.

## 5. Checks against published studies (exploratory replication)

Each published study is applied to DREAM with that study's own grouping rule, as closely as DREAM allows. Descriptive numbers below were computed on 2026-10-09 from usable post-first-dose values and Stage 07 baselines, by an exploratory aggregate script. No death field was read. The survival comparison runs only after D-040 is frozen.

| Study | Rule applied in DREAM | DREAM, descriptive | Published | Survival comparison |
|---|---|---|---|---|
| Petrylak 2006, Armstrong 2007 | Lowest PSA at least 30 per cent below start | 56.7% by day 52; 64.5% by day 73; 67.2% by day 84 (971 of 1,444) | 76% by 3 months, docetaxel plus estramustine (Petrylak) | Pending: checkpoint at day 73 and 84, adjusted for starting PSA |
| Sonpavde 2012 | Bone metastases, starting ALP 120 U/L or more, two or more later values; latest value back below 120 by day 84 | 734 of 1,526 (48.1%) meet the entry rule; 178 of 527 (33.8%) back below 120 | 159 of 601 (26.5%) by day 90 | Pending |
| Salfi 2025 | Any on-treatment value by day 84: ALP reaching 130 or doubling; albumin below 40 g/L; sodium 135 or less | ALP 4.3%; albumin 47.1% (24.3% already at start); sodium 13.4% (8.9% already at start) | Event shares not recorded in our notes | Pending; cross-setting, since Salfi's men were hormone-sensitive |
| Hussain 2006, Harshman 2018, Saad 2024 | PSA at months 4 to 7 or week 24 | NOT POSSIBLE: no DREAM value after day 84 | | NOT POSSIBLE |
| Wallis 2026 | Speed of PSA fall from a joint model | Formula unpublished | HR 0.71 per doubling of decline rate | LATER: Layer 4 mixed-model analogue |

Limits of this table: the "lowest value" rule favours patients with more draws, and CELGENE adds a day-14 draw in cycle 1. ASCENT2 has no on-treatment ALP, albumin or sodium. DREAM's windows end before most published ones, so its shares are lower bounds.

## 6. Rules that protect the result

- Checkpoints on the first-treatment clock: days 31, 52 and 73. Strict landmarking: only data observed by the checkpoint, in training and in validation (Gomon 2024).
- Outcome days moved onto the same clock with a grid of offsets: measured 2 days for EFC6546; each patient's lower bound, 14, 28 and 42 days for ASCENT2 and CELGENE (D-038).
- Trial is always a stratum.
- Validation: bootstrap optimism correction first; then train on one trial and test on the other, both directions reported.
- Report every result: positive, null, contradictory and failed.
- The pipeline is frozen before any index-patient value is read.

## 7. What the paper will show

1. Flow diagram from 1,600 patients to every analysis group, naming who drops out and why, including the 168 patients without a usable cycle-2 value and all of ASCENT2 from multi-test cohorts.
2. Table 1: patient characteristics by trial.
3. Table 2: Level 1 hazard ratios, every test.
4. Table 3: Layer 2 added-value tests, every test, with adjusted P values.
5. Table 4 and figure: Model A against Model B at each checkpoint, with calibration plots and the "how early" curve.
6. Supplement: the replication table above with survival results, the offset sensitivity grid, the ECOG and spline sensitivity analyses, and secondary tests on their own groups.

Reporting follows TRIPOD+AI, REMARK and PROBAST+AI (LIT-036).

## 8. Open questions that affect the paper

Q-016 clock offset; Q-017 treatment-stop endpoint; Q-018 bounded results; Q-020 EFC6546 day numbering; Q-023 the index patient's laboratory imprecision. Full text in `RESEARCH_LOG.md`.

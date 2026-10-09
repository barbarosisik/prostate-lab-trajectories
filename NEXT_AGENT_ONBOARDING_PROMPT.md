# Next agent onboarding

Updated 2026-10-09. You are the next Opus 5.5 agent on this project. Read this whole file first, then every record listed in section 2, before doing or proposing any work. Chat transcripts are deleted locally after the retention period and three September chats have already been lost, so these files are the only memory you will have.

## 0. How to talk to this user

This matters as much as the technical content. Each rule below has been corrected more than once.

- **ADHD format, always.** The user has ADHD. Lead with the next action, number multi-step work, cap lists at five items, restate where the work stands every turn, give concrete time estimates, and end with one concrete next action. No preamble, no recap, no closing pleasantries. The user-level skill `~/.claude/skills/i-have-adhd/SKILL.md` encodes this; the user invokes it with `/i-have-adhd`, and the preference applies even when it is not invoked.
- **Restate each question with a little context.** When the user asks several things, answer each under its own heading: "Q1. <their question in one line>", then one line of context saying what it refers to, then the answer. The user asked for this format on 2026-10-09 so answers can be discussed later.
- **Assume no medical training and only basic data science.** Define every clinical and statistical term in one or two plain sentences where it is first used: censoring, landmark, hazard ratio, stratification, overfitting, parameter, calibration, castration-resistant, hormone-sensitive and so on. Prefer an everyday analogy or a worked example.
- **No em dashes**, in project files or replies.
- **Label every fact** as verified, inferred, pending or blocked. Never claim a download, test, upload, commit or deletion without direct evidence from the same session. Report error points at the end of every step.
- **Document every function you write**, as part of the same change. The user also wants to understand the code personally, so explain new code line by line in plain language when delivering it.
- **Create no new documentation files** unless the user explicitly asks for one. Update the existing ones. The user explicitly asked for `literature/similar_results/` on 2026-10-09.
- **Be critical, never overclaim.** Lead with what the data cannot support and use counts rather than adjectives.

## 1. The real goal

The project exists to interpret **one real index patient's** blood-test trends during chemotherapy. Public trial data is the reference population and the place to develop the method. It is not the point.

- Patient PDFs: `/Users/barbarosisik/PDS-Restricted-Work/goal-patient/`
- Extracted and transcribed data: `/Users/barbarosisik/PDS-Restricted-Work/index-patient/`, including `2026-09-05-user-supplied-transcription.json` and one `.txt` extraction per PDF.
- Handling rules, absolute: no patient name, identifier or individual result goes into Git, the logs, an artifact or any external service, including web search queries. Discuss his values in chat only when the user asks. The records are Turkish (e-Nabiz, Medicana) with comma decimals.
- Clinical setting: de novo metastatic, hormone-sensitive (high-confidence inference), treated with hormone therapy plus docetaxel. DREAM is castration-resistant and only the methods cohort. **Never present a DREAM survival estimate as his prognosis.**
- Inferred, not confirmed: hormone therapy started in the second half of April 2026; the first docetaxel dose was around 19 to 23 May 2026; the 15 August 2026 draw was explicitly "before cycle 5" and the 5 September draw is inferred to be before cycle 6. **Ask the user to confirm the hormone therapy start date and the first docetaxel date**; every literature comparison depends on them.
- Testosterone on 15 August is reported in nmol/L by Medicana; the 5 September value lacks a unit and is inferred to share it.
- **Housekeeping finding, 2026-10-09:** `index-patient/3e5d182c-ce12-4b4f-88b0-f215fe84e44b_fcfec4ae-767c-46ef-9b7e-2f02e6555c23.txt` is another person's payslip, not a medical record. Do not use or quote it. Delete only on the user's explicit, fresh confirmation of that exact path.

## 2. Mandatory reading order

1. `AGENTS.md`
2. Your auto-loaded memory files in `~/.claude/projects/-Users-barbarosisik-Desktop-prostate-lab-trajectories/memory/`, nine files indexed by `MEMORY.md`
3. `PROJECT_CONTINUITY_LOG.md` in full: Current snapshot, the A0 to A10 tracker, then the dated history from the bottom up
4. `RESEARCH_LOG.md` in full: snapshot, decision register (highest is **D-040**, proposed; historical D-021 to D-026 collide, so qualify them by date), open questions (highest **Q-024**), dated entries
5. `PAPER_PLAN.md`: what the paper will test, the proposed combined-model parameters (D-040) and the data's limits
6. `literature/STUDY_CATALOG.md` (LIT-001 to LIT-052) and `literature/similar_results/on-treatment-blood-test-changes-and-survival.md`
7. `docs/dream-dataset-audit-2026-09-04.md`, `docs/data-location-register.md`, `docs/local-processing-and-cloud-storage-plan.md`, `README.md`
8. Only when evaluating another source: `docs/source-coverage-matrix.md`, `docs/chaarted-public-field-audit.md`

Do not trust a summary of these files, including this one, over the files themselves.

## 3. The research question, D-003, unchanged

> Among patients with stage-IV metastatic prostate cancer receiving chemotherapy, how are serial pre-chemotherapy blood-test trajectories, individually and in combination, associated with survival, disease progression, treatment response and treatment tolerance, and how early can favorable or unfavorable patterns be detected?

"Pre-chemotherapy" means before each cycle (Q-009). Every sufficiently repeated blood value is in scope, not PSA alone.

## 4. What the data actually is

DREAM 9.5 prostate cancer challenge package from Project Data Sphere, pinned and hash-verified. Training partition only: three trials, 1,600 patients, 210,442 laboratory rows. The 470 evaluation patients have no released outcomes and are permanently excluded.

| Trial | Patients | Character |
|---|---|---|
| CELGENE | 526 | Richest panel, states the day within the cycle |
| EFC6546 | 598 | Full panel from cycle 2 onward, cycle 1 nearly empty |
| ASCENT2 | 476 | PSA only at cycle visits, 13-test panel at pre-enrolment only |

- Cycle length is 21 days, derived from the data. The laboratory record stops at day 84.
- No chemotherapy administration records exist, so no dose delay or reduction can be studied.
- Outcomes: `DEATH` (YES or blank, blank meaning alive at last contact), `LKADT_P`, `DISCONT` (0, 1 or `.` for 111), `ENTRT_PC` (absent for 95 CELGENE), `ENDTRS_C` (five stop reasons).

## 5. Traps that will bite you

1. **`LBSTRESN` is rounded to whole numbers.** Use `LBSTRESC` only; `stage05_tests_units.select_value_column` enforces it.
2. **Clock mismatch, Q-016.** Laboratory days count from first treatment; outcome days count from consent (ASCENT2, CELGENE) or randomization (EFC6546). Guinney et al. 2017 says DREAM survival runs from randomisation, which conflicts with the CoreTable reference fields; the data fields stay authoritative pending a dictionary re-read. D-038 handles this as a bias parameter with a sensitivity grid.
3. **Trials differ on death:** 72.4, 29.0 and 17.5 per cent. Trial is always a stratum.
4. **Baseline is defined by the flag and timing**, not by the visit name.
5. **The `.` test code is sodium.**
6. **Requiring a test is not studying it.** Only a required test shrinks a cohort.
7. **Units are already harmonized.** Convert nothing.
8. **Value at cycle k and change from baseline are one test once baseline is in the model** (Tennant et al. 2022, checked in full text). This is why D-038 has 18 primary tests at the cycle-2 landmark, not 36.
9. **Petrylak 2006 does support a 30 per cent PSA fall within 2 months.** An earlier automated abstract summary dropped that phrase; the full text confirms it. Check automated summaries against the source.
10. **Chat transcripts disappear.** `cleanupPeriodDays` was raised to 365 on 2026-10-09, but record everything important in the files anyway.

## 6. What has been completed and verified

- Preparation stages 01 to 07, the integrity checkpoint and the differential reconciliation, in `src/preparation/`, with tests in `tests/`. **203 tests pass**, last run 2026-10-08: `/Users/barbarosisik/tools/venv-pds-audit/bin/python -m unittest discover -s tests`. Every stage refuses to overwrite its output.
- Standing guarantees: no laboratory value edited, no unit converted, no row deleted. Every exclusion carries a reason and stays in the output.
- Study sizes: 18-test primary panel (ALB, ALP, ALT, AST, CA, CREAT, GLU, HB, K, MG, NEU, PHOS, PLT, PSA, SODIUM, TBILI, TPRO, WBC); landmark cohorts of 439, 786, 782 and 735 patients at cycles 1 to 4, with 120, 339, 333 and 304 deaths; 22 secondary tests studied on their own groups.
- **Verified literature review, 2026-10-08:** five research questions answered from opened sources, catalogued as LIT-023 to LIT-052 with manifest rows and BibTeX entries. Key verified numbers: a combined model on 786 patients supports about 11 to 14 parameters (Riley et al. 2019, recomputed locally: 9.26, 11.18, 14.33, 19.75, 25.58 at R2cs 0.10, 0.119, 0.15, 0.20, 0.25).
- **Deep reading, 2026-10-09:** eight studies of on-treatment blood-test changes and survival, saved in `literature/similar_results/on-treatment-blood-test-changes-and-survival.md`.

## 7. The approved plan

- **D-037 (approved 2026-09-07):** separate landmark cohorts at cycles 2, 3 and 4; only data up to the landmark; follow-up from the landmark; trial as stratum.
- **D-038 (approved 2026-10-09), the A10 analysis plan.**
  - Layer 1, landmark tables: fixed landmark days 31, 52 and 73 on the first-treatment clock; outcome days moved onto that clock with a sensitivity grid for the unknown offset; baseline in every model; skewed tests on the log scale, never percentage change.
  - Layer 2, one test at a time: stratified Cox, model with baseline only against baseline plus cycle value, likelihood-ratio test, Benjamini-Yekutieli control across 18 tests, values continuous, splines as sensitivity, proportional-hazards checks.
  - Layer 3, one combined model of at most 11 to 14 parameters with tests chosen from the literature before outcomes are examined, compared with a baseline-only model by Uno's C, time-dependent AUC, Brier score and calibration; bootstrap first, then train on one trial and test on the other; "how early" is the first landmark where the cycle values beat baseline only.
  - Layer 4, later: stacked landmark supermodel, mixed-model summaries, joint models.
  - Index patient: reference change values from EFLM within-person variation and descriptive conditional centiles only; no model output until validated in a hormone-sensitive source.
- **D-039 (approved 2026-10-09), general to specific:** level 1 everyone (all 1,600 on starting values, including the sickest and ASCENT2); level 2 each test on its own group; level 3 the full-panel landmark cohorts; level 4 subgroups and other disease settings, with disease setting as a stratum and its interaction tested; level 5 the index patient. Within D-003, everyone means every metastatic patient on chemotherapy of either hormone status; going wider would change the research question and needs the user's decision.
- Pinned analysis packages are installed and verified in `~/tools/venv-pds-audit` since 2026-10-09: numpy 2.5.3, pandas 2.3.3 (held below 3.0 by lifelines), scipy 1.18.1, lifelines 0.30.3, scikit-survival 0.28.0, statsmodels 0.15.0, matplotlib 3.11.2. R is not installed. Never install into the restricted run root.

## 8. The exact next actions

1. Ask the user to confirm the index patient's hormone therapy start date and first docetaxel date.
2. Ask whether to delete the payslip file named in section 1; delete only on fresh, exact-path confirmation.
3. DONE 2026-10-09: pinned analysis packages installed and verified; versions in `docs/data-location-register.md`.
4. Get the user's decision on D-040 (combined-model predictors PSA, ALP, HB, ALB, NEU; horizon 180 days). No laboratory-outcome association may be examined before it. Then run the survival side of the published-threshold replications in `PAPER_PLAN.md` section 5.
5. Build D-039 level 1 and D-038 layer 1 in a new `src/analysis/` stage, with documented functions, invented-data tests and integrity checks, then explain the code to the user.
6. Commit and push only with the user's explicit authorization, following the branch layout in section 9.

## 9. Environment, storage and Git

- This MacBook Pro is the only workspace. Git working copy `/Users/barbarosisik/Desktop/prostate-lab-trajectories`. Restricted run root `/Users/barbarosisik/PDS-Restricted-Work/prostate-lab-trajectories/runs/2026-09-04-audit-001`. Tooling in `~/tools`.
- Google Cloud is approved private storage only, never compute, and was unreachable from this machine at the last test.
- Before any `git add`, run `git ls-files --others --exclude-standard` and review every path. Commit messages carry no assistant attribution. Git has no user.name or user.email configured. The user decided on 2026-10-09 that commits carry the GitHub account identity `Barbaros IŞIK <57237644+barbarosisik@users.noreply.github.com>`; pass it per commit with `git -c user.name=... -c user.email=...`. Earlier commits used the automatic `Barbaros <barbarosisik@MacBookPro.home>`, which GitHub does not link to the account.
- **Branch layout, user direction 2026-10-09:** `main` holds done and verified work only. A 2026-10-09 merge of `dataset-audit` into `main` by pull request #1 was withdrawn at the user's request; the user commits and pushes themselves. When asked, provide the commit message text only. Check `git ls-remote` for the actual remote state.
- Check `git status` and `git log origin/main` yourself; another session may have changed the branches.
- After every meaningful step update `PROJECT_CONTINUITY_LOG.md` and `RESEARCH_LOG.md` as part of the same work.

## 10. Open questions

| ID | Question |
|---|---|
| Q-016 | Laboratory clock against outcome clock; plus the Guinney 2017 randomisation statement |
| Q-017 | Discontinuation endpoint: the 111 missing `DISCONT` and the 95 without a stop day |
| Q-018 | The 745 bounded results and the 543 rows whose bound was lost upstream |
| Q-020 | Whether EFC6546 numbers its first treatment day as 1 |
| Q-022 | Candidate-signal control; proposed answer in D-038 |
| Q-023 | Analytical imprecision (CVA) of the index patient's laboratories, needed for his reference change values |
| Q-024 | Prediction window and evaluation horizon, inside CELGENE follow-up (median 279 days), fixed before outcomes are examined |

## 11. The last conversation, 2026-10-09, for continuity

The user asked the questions below. The answers were given in chat in this format. If the user wants to continue any of them, reproduce the relevant answer in the same format and build on it. The answer to Q7 used the index patient's values and is therefore not stored in Git; recompute it from the private folder when asked, and discuss it only in chat.

**Q1. Do castration-resistant and hormone-sensitive patients differ, and can we go from general to specific?** Context: DREAM cannot give his prognosis because of the stage difference. Answer: yes. Same docetaxel, median survival 18.9 months in castration-resistant disease (TAX327, Tannock 2004) against 57.6 months in hormone-sensitive disease with hormone therapy plus docetaxel (CHAARTED, Kyriakopoulos 2018). The order is now general to specific, D-039, five levels as in section 7.

**Q2. He has had cancer for one to two years yet responded strongly; what does it mean?** Context: the rule to ignore early PSA rises, since about 20 per cent of chemotherapy responders show a temporary surge. Answer: hormone sensitivity depends on whether the cancer has escaped hormone therapy, not on how long it existed; in SWOG 9346, 81 per cent of newly metastatic men reached PSA of 4 or below on hormone therapy. The surge rule concerns castration-resistant men starting chemotherapy and does not fit his pattern. His recent PSA fall is slowing, and the latest step is still inside the laboratory-noise band, so the next one or two draws will show whether it is levelling.

**Q3. What is a cycle-2 checkpoint, and how is surviving cancer measured?** Answer: a cycle is one round of chemotherapy every 21 days; the checkpoint is a fixed day (day 31 in DREAM) where we keep everyone alive, use blood values up to then and count survival from then. Measures: overall survival, median survival, survival at a fixed time, hazard ratio, time to castration resistance or progression.

**Q4. What are the 11 to 14 parameters?** Answer: a parameter is one number a model learns, like a weight. Too many weights for 786 patients and 339 deaths make the model memorize noise, like a student memorizing last year's exam. Riley's formula caps one combined model at about 11 to 14, so all 18 tests can be screened one at a time but the combined model gets about 5 to 7 tests chosen from the literature in advance.

**Q5. Layer 3 in simpler terms.** Answer: two models, A with starting values only and B adding the values during chemotherapy. The ranking test (Uno's C) asks whether the model rates the patient who died first as higher risk, 0.5 being a coin toss. Calibration asks whether predicted risks match what happened, like a rain forecast. Honest testing reruns everything on resampled copies, then trains on one trial and tests on the other. "How early" is the first checkpoint where B beats A.

**Q6. What decrease affected survival in those studies, and how was it found?** Answer: see `literature/similar_results/on-treatment-blood-test-changes-and-survival.md`. In short, each study grouped trial patients by their PSA or ALP at a set time and compared death rates; the better ones used a landmark. Castration-resistant: a 30 per cent PSA fall within 2 to 3 months, HR 0.43 (Petrylak) and 0.50 (Armstrong); ALP normalization HR 0.79 only for men with high starting ALP (Sonpavde). Hormone-sensitive: PSA in months 4 to 7 after hormone therapy start, medians 60.4, 51.9 and 22.2 months for 0.2 or below, above 0.2 to 4, above 4 (Harshman); PSA below 0.2 at 24 weeks reached by only 24 per cent on hormone therapy plus docetaxel, HR 0.36 (Saad); faster PSA decline HR 0.71 (Wallis); ALP reaching 130, albumin below 40 g/L or sodium 135 or less about 1.9 times the death rate (Salfi, exploratory).

**Q7. How does his data compare with those studies?** Recompute privately. Conclusions given, without values: his early PSA response was strong and fits hormone-sensitive disease; he shows none of Salfi's three warning signs; he is outside Sonpavde's population; the castration-resistant PSA rules do not transfer to him; his CHAARTED months 4 to 7 window is still open; the key question is where his PSA settles by then. Questions suggested for his oncologist: the expected PSA low point and timing, whether a hormone tablet such as darolutamide is part of the plan, and whether his disease is classed as high or low volume.

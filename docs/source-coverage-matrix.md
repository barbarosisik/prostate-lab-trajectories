# Source coverage and access evidence

Updated 2026-09-06. Current DREAM counts come from the completed local audit. Alternative-source statements below are historical public evidence, not new access or download verification.

## Current source decisions

| Source | Supported role and coverage | Limitation | Next action |
|---|---|---|---|
| DREAM training: ASCENT2, CELGENE, EFC6546 | Verified: 1,600 patients, serial routine labs and outcome fields; methods cohort | No actual dose records, no primary imaging-response endpoint; disease setting differs from index patient | Implement approved preparation locally |
| DREAM AZ leaderboard/final | Verified: 470 patients excluded from supervised work | Released death and follow-up fields blank | No independent validation claim |
| PDS hormone-sensitive docetaxel trial | Pending: candidate name, ID, actual test and timing coverage | None selected | User searches existing PDS account first, D-032 |
| CHAARTED/E3805 | Publicly documented: D8 repeated PSA, D12 testosterone, linked outcomes | Repeated full blood panel not publicly established; exact administrations unverified | PDS search first; no dbGaP application now |
| Vivli / Flatiron | Pending field-level compatibility | Advertised coverage is not actual source verification | No purchase or blind application |

D-027: assess every source against the index patient's actually measured tests and timing. D-030: DREAM is not his prognosis. D-031: leave-one-trial-out validation across the three training trials; no independent outcome-labeled holdout exists in this package. D-033: CHAARTED is expected to support PSA confirmation only. See [chaarted-public-field-audit.md](chaarted-public-field-audit.md) for submission details.

## Official DREAM provenance

- PDS contribution: [Prostate Cancer DREAM Challenge](https://data.projectdatasphere.org/projectdatasphere/html/content/0abbd47a-dcfb-42c2-a036-af1898ea3c1c), ID `Prostat_na_2006_149`, DOI [10.34949/e6c8-v326](https://doi.org/10.34949/e6c8-v326).
- Synapse project [syn2813558](https://www.synapse.org/Synapse:syn2813558), challenge folder `syn3325825`, dictionary `syn3348062`, training folder `syn3348064`, training ZIP `syn3350917`.
- [Official data-description wiki](https://www.synapse.org/Synapse:syn2813558/wiki/209583) and [access instructions](https://www.synapse.org/Synapse:syn2813558/wiki/209590).
- Training file IDs: CoreTable `syn3346724`; LabValue `syn3346726`; LesionMeasure `syn3346728`; MedHistory `syn3346730`; PriorMed `syn3346732`; VitalSign `syn3346734`.
- The six source tables are patient core records, laboratory events, lesion records, screening medical history, prior medications and vital signs. Exact local/cloud hashes and locations belong in [data-location-register.md](data-location-register.md).

## Timing and field cautions retained from the public audit

`STUDYID` and `RPT` are candidate composite keys, now checked by Stage 01. `LBDT_PC` is a relative collection day, `LBBLFL` the supplied baseline flag, `LBORRES`/`LBSTRESC` original/standardized character results, `LBSTAT` completion status and `LBNRIND` the supplied reference-range indicator. Verify numeric fields and units against the actual dictionary before conversion.

Trial/table reference dates may be first treatment, consent or randomization. Public documentation describes consent references in ASCENT2 and randomization references in some EFC6546 tables. Do not assume all relative days share one origin. Prior-medication end dates may have been censored at treatment start. Neither visit labels nor three-week spacing proves actual dose administration, reductions or delays. Historical duplicate counts from published processing are not counts for this run.

## Earlier alternative-source search, retained conclusions

These are the 2026-08-26 public-search conclusions, not authorization to acquire a new source. PDS access is now resolved, so old fallback acquisition instructions are retired.

| Candidate | Historical evidence | Why it does not replace DREAM |
|---|---|---|
| MSK-CHORD | [Original paper](https://www.nature.com/articles/s41586-024-08167-5), 3,211 prostate patients; [official cBioPortal study](https://www.cbioportal.org/study/summary?id=msk_chord_2024) | Tumour-marker tracks and treatment course intervals do not establish repeated routine panels or infusion dates |
| AACR GENIE BPC Prostate | [Public analytic guide](https://www.aacr.org/wp-content/uploads/2026/03/GENIE-BPC-Prostate-v1.0-public-Analytic-Data-Guide.pdf), 1,116 patients | PSA/testosterone and treatment intervals, not verified serial full blood panels or dosing |
| Metastatic Prostate Cancer Project | [Methods](https://mpcproject.org/Methods.pdf), 123 participants | Small, PSA-only laboratory coverage |
| Open Zenodo prostate cohort | [Dataset record](https://zenodo.org/records/15007105), 600 patients | Not a serial pre-cycle chemotherapy cohort |
| SWOG S0421 / general inpatient databases | Earlier field review | No verified matching full-panel, outpatient chemotherapy-cycle structure |

An unlicensed participant copy of DREAM was found in the earlier search and was not used. Continue using the licensed, checksum-verified official package. Do not seek a separate PSA dataset merely to add antigen coverage.

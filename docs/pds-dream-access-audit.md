# PDS DREAM Access and Release Audit

## Current result

The official PDS DREAM contribution and the official Synapse challenge metadata are located. PDS approved the user's access request on 2026-08-25, the user signed in successfully, and the contribution is marked Available for Download. Public documentation proves that the training release includes event-level laboratory results through day 84, but the six-file challenge release does not list an actual chemotherapy-administration table or an adverse-event event table.

The source files and dictionary have **not** yet been treated as obtained or column-verified because the large package still requires a manual download when the user is home or has suitable protected storage.

## Official dataset identity

| Item | Verified value |
|---|---|
| PDS contribution | [Prostate Cancer DREAM Challenge data sets](https://data.projectdatasphere.org/projectdatasphere/html/content/0abbd47a-dcfb-42c2-a036-af1898ea3c1c) |
| PDS UID | `Prostat_na_2006_149` |
| DOI | [10.34949/e6c8-v326](https://doi.org/10.34949/e6c8-v326) |
| Patients in PDS contribution | 2,070 |
| Synapse project | [syn2813558](https://www.synapse.org/Synapse:syn2813558) |
| Synapse challenge-data folder | `syn3325825` |
| Official dictionary | `Challenge_data_dictionary v2.xlsx` / `syn3348062` |
| Public data-description wiki | [wiki 209583](https://www.synapse.org/Synapse:syn2813558/wiki/209583) |
| Public access-instructions wiki | [wiki 209590](https://www.synapse.org/Synapse:syn2813558/wiki/209590) |

## Official PDS package listing

The current official PDS contribution lists:

| Type | Filename |
|---|---|
| All provided files | `AllProvidedFiles_149.zip` |
| Case-report-form location document | `PCDC Protocol, CRF Location.docx` |
| Data dictionary | `Challenge_data_dictionary v2.xlsx` |
| Training data | `prostate_cancer_challenge_data_training.zip` |
| Leaderboard data | `prostate_cancer_challenge_data_leaderboard.zip` |
| Final-scoring data | `prostate_cancer_challenge_data_finalscoringset.zip` |

## Synapse file inventory

### Training release

The official Synapse wiki identifies `syn3348064` as the training folder and `syn3350917` as the combined training ZIP. It reports 1,600 patients from ASCENT2, MAINSAIL and VENICE.

| Source file | Synapse ID | Publicly documented content |
|---|---|---|
| `CoreTable_training.csv` | `syn3346724` | Patient-level outcomes and summarized baseline/static covariates |
| `LabValue_training.csv` | `syn3346726` | Patient-event laboratory data |
| `LesionMeasure_training.csv` | `syn3346728` | Patient-event target/non-target lesion measurements |
| `MedHistory_training.csv` | `syn3346730` | Screening medical-history events |
| `PriorMed_training.csv` | `syn3346732` | Prior-medication events |
| `VitalSign_training.csv` | `syn3346734` | Patient-event vital signs |

### Leaderboard release

The official Synapse wiki identifies `syn3348063` as the leaderboard folder and `syn3350919` as its ZIP.

| Source file | Synapse ID |
|---|---|
| `CoreTable_leaderboard.csv` | `syn3346736` |
| `LabValue_leaderboard.csv` | `syn3346738` |
| `LesionMeasure_leaderboard.csv` | `syn3346745` |
| `MedHistory_leaderboard.csv` | `syn3346747` |
| `PriorMed_leaderboard.csv` | `syn3346750` |
| `VitalSign_leaderboard.csv` | `syn3346740` |

The original challenge split ENTHUSE-33/AZ into 157 leaderboard and 313 final-scoring patients. Its non-baseline longitudinal information and dependent outcomes were withheld from participants. Whether the current PDS final-scoring package now exposes any of those fields must be checked directly after download; it must not be inferred from the filename.

## Publicly verified table semantics

| Table | Timing/coverage verified in official public documentation | Important limitations |
|---|---|---|
| `CoreTable` | Patient-level; contains `DEATH`, `LKADT_P`, `DISCONT`, `ENTRT_PC`, `ENDTRS_C`, treatment IDs and summarized covariates | Summaries are not substitutes for administration, AE or longitudinal outcome events |
| `LabValue` | Event-level; training rows from screening through day 84; date field `LBDT_PC`; baseline flag `LBBLFL`; original and standardized results; `LBNRIND` | PDS reference day is usually first treatment but can be consent; baseline/date contradictions are documented; leaderboard/final challenge sets contain baseline only |
| `LesionMeasure` | Event-level through day 98 or cycle 4 for training; date field `LSDT_PC` | ASCENT2 has no event-level lesion table; reference day varies and may be randomization rather than first dose |
| `PriorMed` | Baseline medication events; dates `CMSTDT_PC` and `CMENDT_PC` | End dates after treatment start were censored to zero to avoid survival leakage |
| `MedHistory` | Screening diagnoses; date `MHSTDT_P` | ASCENT2 has no event-level medical-history table |
| `VitalSign` | Event-level through approximately day 84; date `VSDT_PC`; baseline flag `VSBLFL`; visit labels can encode cycles | Reference day differs by trial; ASCENT2 uses consent and EFC6546 uses randomization |

## Known laboratory fields and behavior

Public documentation or the curated DREAM processing paper identifies:

- `LBDT_PC`: lab-test day relative to a trial-specific reference date.
- `LBBLFL`: organizer-created/provided baseline flag.
- `LBORRES`: original laboratory result.
- `LBSTRESC`: standardized character result.
- `LBSTAT`: completion status, including `NOT DONE`.
- `LBNRIND`: study reference-range indicator.
- `VISIT`: used in baseline logic and therefore expected to be important for cycle/schedule auditing.
- Original and standardized units and numeric/reference-limit columns are required by the checklist but their exact names remain dictionary-pending.

LIT-008 documented 2,545 duplicate rows and 603 `NOT DONE`/missing-standard-result rows in its selected-test processing. Those historical counts are not reused as current audit results; they will be recomputed from the acquired source release.

## Feasibility finding: pre-cycle linkage

The public release inventory contains six tables and **does not list**:

- a chemotherapy-administration event table;
- a dose/cycle exposure table;
- an adverse-event event table;
- a radiographic/clinical/PSA progression event table.

Consequently:

1. Serial laboratory trajectories through approximately the first 84 days are plausible for the three training trials.
2. The critical link from a laboratory sample to the next **actual** docetaxel administration is not yet proven.
3. `LBDT_PC` plus `VISIT` may support nominal calendar-time or visit/cycle analyses, but it cannot establish actual dose timing, delay, missed cycle or dose reduction without additional fields.
4. `CoreTable.DISCONT` can support the historical early AE-discontinuation outcome, but it does not supply the complete treatment-tolerance family.
5. Progression and response availability must be confirmed from actual columns; lesion measurements alone do not establish source-defined progression dates.

No cleaning/restructuring specification will be frozen until the dictionary and all source columns are inspected.

## Access test and exact blocker

Checked on 2026-08-25:

- The PDS registration and data-access application was accepted.
- The user signed in successfully and opened the approved contribution.
- The contribution exposes Download controls for the complete bundle, dictionary, training, leaderboard, final-scoring and CRF-location files.
- The page reports 2,070 patients and Available for Download.
- Automated semantic, visible-DOM and physical browser clicks did not start a browser download.
- No new PDS file appeared in the Windows Downloads folder during the attempts.
- The user is away from home and cannot complete the large manual download on the current computer.
- Anonymous Synapse metadata access confirms the project and public wiki pages.
- The separately tested anonymous Synapse route still returns no read/download permission for `syn3348062` and reports unmet requirement `3325885`.
- This Synapse state does not cancel the verified PDS approval or visible PDS downloads. Use the approved PDS page as the current acquisition route unless the user separately completes Synapse access.

## Acquisition and verification procedure after access

1. When the user is home, manually download `AllProvidedFiles_149.zip` from the approved PDS contribution.
2. If local space is insufficient, review the PDS terms before using encrypted external or institution-approved protected storage. Do not use ordinary cloud storage.
3. Preserve the original ZIP unchanged under ignored `data/raw/pds_dream/source/` storage.
4. Record the source URL/Synapse ID, acquisition timestamp, size and SHA-256 checksum in a local restricted manifest; commit only non-sensitive metadata.
5. List ZIP members before extraction and reject unsafe paths.
6. Read all columns as strings for the raw inventory so mixed numeric/text values are preserved.
7. Produce row/column counts, column types, distinct-value summaries and join diagnostics without committing patient-level values.
8. Enumerate every laboratory test and unit before any inclusion filter.
9. Test actual cycle linkage before writing cleaning rules.

## Material sources

- Official PDS contribution page and file listing.
- Official Synapse project metadata and public wikis 209583 and 209590.
- Official Synapse REST metadata for project `syn2813558`, the public wiki tree and access actions for `syn3348062`.
- Curated local studies LIT-005, LIT-006 and LIT-008.

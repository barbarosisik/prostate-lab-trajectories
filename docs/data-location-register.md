# Data location and run register

Updated: 2026-09-04. This is non-sensitive operational metadata, not a dataset. Read it at onboarding and update it before and after every transfer, processing stage and cleanup. The continuity and research logs remain required.

## Single workspace, from 2026-09-04

The user confirmed that this MacBook Pro is the ONLY workspace for the project and instructed that any other machine be disregarded. All local paths in this register refer to macOS. Earlier Windows paths are retained below only as history and are NOT actionable. The previously open Windows all-files-backup condition and the 27 unbacked ignored files under the retired Windows folder are therefore OUT OF SCOPE, not outstanding blockers.

## Standing workflow

Private Google Cloud Storage is the permanent home for original and derived restricted data. Computations, tests and processing run locally in a recorded temporary folder. Upload new outputs, verify every required file, then obtain fresh confirmation and remove the exact local run folder. Never put restricted data in GitHub or leave an unrecorded local copy. No cloud computation is authorized by this workflow.

## Permanent storage

| Item | Location | Verified state |
|---|---|---|
| Code and safe documentation | `https://github.com/barbarosisik/prostate-lab-trajectories`, branch `main` | Corrected approval-first handoff published at `0fa84856f526a7e647cf5f07b5acccfe39e645ea`; authenticated connector independently confirmed main and all ten document blob hashes. This receipt follows that commit; verify current main at onboarding |
| Cloud project | `pds-dream-secure-storage` | Existing approved storage project |
| Private bucket | `gs://pds-dream-secure-storage-eu-20260827` | Netherlands `europe-west4`; access controls refreshed 2026-08-31 |
| Original package | `gs://pds-dream-secure-storage-eu-20260827/prostate-lab-trajectories/data/raw/pds_dream/source/AllProvidedFiles_149 (1).zip` | Exists in live console; 6,227,480 bytes and hashes verified 2026-08-27; exact metadata refresh before next download |

Source SHA-256, from the 2026-08-27 verification: `AB3ECA19C5D0CC4106C96AC04E665DD1A5C9DF58F66328ECD24E8E1067932391`. Google Cloud Storage does not store SHA-256, so this value is confirmed by computing it locally after download.

### Live source object metadata, refreshed 2026-09-04

Read-only `gcloud storage objects describe` against the pinned object returned:

| Property | Value |
|---|---|
| Object | `prostate-lab-trajectories/data/raw/pds_dream/source/AllProvidedFiles_149 (1).zip` |
| Size | 6,227,480 bytes, which MATCHES the 2026-08-27 record exactly |
| Generation | `1787841139282260` |
| Metageneration | 1 |
| MD5 | `D4Yz5HS1gTF8tm8Xg6hK2A==` base64, `0F8633E474B581317CB66F1783A84AD8` hex |
| CRC32C | `gx71ow==` base64 |
| Storage class | STANDARD |
| Content type | `application/x-zip-compressed` |

Download at A4 must pin this exact generation so a later overwrite cannot silently change the source. A full recursive listing confirmed this is the ONLY object in the bucket, so no unexpected copies or stray uploads exist.

Bucket security refreshed the same day: location `EUROPE-WEST4`, `public_access_prevention: enforced`, `uniform_bucket_level_access: true`, and an IAM policy scan found no `allUsers` or `allAuthenticatedUsers` binding.

Object versioning is NOT reported as enabled on this bucket, so the original object is protected by generation pinning and by not writing to its path, rather than by version history.

## Active and proposed runs

| Run ID | Stage and state | Exact local folder | Cloud output prefix | Upload verification | Local cleanup |
|---|---|---|---|---|---|
| `2026-08-31-audit-001` | RETIRED, never started. Superseded by `2026-09-04-audit-001`. Its Windows folder belonged to a machine that is no longer part of the project | `C:\Users\BarbarosIsikGreenhou\PDS-Restricted-Work\prostate-lab-trajectories\runs\2026-08-31-audit-001` (stale, replace on approval) | `gs://pds-dream-secure-storage-eu-20260827/prostate-lab-trajectories/data/interim/pds_dream/audits/2026-08-31-audit-001/` | Not uploaded; no outputs exist | Not applicable yet; local folder not created |

## Current machine, 2026-09-04

The active working copy is macOS at `/Users/barbarosisik/Desktop/prostate-lab-trajectories`, verified level with `origin/main` at `7392d50`. `python3` and `git` are present. The Google Cloud CLI is NOT installed, so `gcloud` and `gsutil` are unavailable until A3 installs them. The Desktop volume reports 415 GiB free, which is ample for a 6,227,480 byte source package.

### Registered macOS run root, verified 2026-09-04

Root: `/Users/barbarosisik/PDS-Restricted-Work`. Run folder:
`/Users/barbarosisik/PDS-Restricted-Work/prostate-lab-trajectories/runs/2026-09-04-audit-001`
with subfolders `source`, `extracted`, `interim`, `reports`, `tmp` and `verify`.

Verified at creation: the given path equals its `realpath`, so no symlink redirection; no symlink exists anywhere in the chain from `/` down to the run folder; every folder is mode `700` owned by `barbarosisik:staff`; the path lies outside `~/Desktop`, `~/Documents`, `~/Library/CloudStorage` and `~/Library/Mobile Documents`, and outside the Git working copy, with `git rev-parse` confirming it is not in any repository; the volume reports 416 GiB free against a 6,227,480 byte source package; and the run folder contains zero files, so no restricted bytes are present yet.

Synchronization state: iCloud Drive is effectively off for this account. `MOBILE_DOCUMENTS` reports `status=None`, no `com~apple~CloudDocs` container exists, and `~/Desktop` and `~/Documents` are ordinary local directories with no iCloud placeholder attributes. A stale `CLOUDDESKTOP status=active` flag and an empty read-only `~/Library/CloudStorage/iCloudDrive-iCloudDrive` mount remain, which is inert without iCloud Drive, but restricted data is kept out of Desktop and Documents regardless. No Dropbox, Google Drive or OneDrive client is present.

### A5 aggregate audit results, 2026-09-04

Extraction produced 110,112,522 bytes across three partitions, all files set to mode 400. Each nested archive passed an independent CRC, unsafe-path, symlink, encryption and expansion-ratio check before extraction. All six data dictionary sheets were read. Every figure below is an aggregate count; no patient identifier and no laboratory result value was written to any report.

Partitions and effective sample size:

| Partition | Patients | Trials | Outcome labels | Lab rows |
|---|---|---|---|---|
| training | 1,600 | EFC6546 598, CELGENE 526, ASCENT2 476 | PRESENT | 210,442 |
| leaderboard | 157 | AZ only | WITHHELD, `DEATH` and `LKADT_P` entirely blank | 6,144 |
| finalscoringset | 313 | AZ only | WITHHELD, `DEATH` and `LKADT_P` entirely blank | 12,065 |

CRITICAL consequence: the effective analysable sample is 1,600 patients, not 2,070. The two held-out DREAM partitions were the blinded challenge test sets and their outcome labels were never released, so they cannot support supervised analysis or independent validation of an outcome model. The AZ trial appears ONLY in those unlabelled partitions.

Cohort homogeneity: every one of the 1,600 training patients has `TRT1_ID=PLACEBO`, `TRT2_ID=DOCETAXEL` (1,585) and `TRT3_ID=PREDNISONE` (1,581). These are the control arms of three phase 3 trials in metastatic castration-resistant prostate cancer, which makes the treatment exposure unusually uniform.

Outcome availability in `CoreTable_training.csv`:

| Field | Filled | Meaning |
|---|---|---|
| `LKADT_P` | 1,600 of 1,600, 100% | Last known alive day, survival time |
| `DEATH` | 663 YES, 41.4% event rate | Survival event |
| `ENDTRS_C` | 1,600 of 1,600, 100% | Discontinuation reason: possible_AE 594, progression 540, AE 239, complete 116, misce 111 |
| `ENTRT_PC` | 1,505, 94.1% | Discontinuation day |
| `DISCONT` | 1,489, 93.1%; 197 positive | Curated discontinuation flag |

Longitudinal laboratory coverage in `LabValue_training.csv`: 210,442 rows, 1,600 patients, 103 distinct `LBTESTCD` codes, 92.6% with a usable numeric `LBSTRESN`. Timing relative to first treatment on day 0 is 24.1% before treatment, 6.9% on day 0 and 68.7% on or after treatment, with 0.2% missing a day.

DECISIVE FEASIBILITY NUMBER: distinct laboratory days per patient BEFORE first treatment have median 2, interquartile range 1 to 3, maximum 11. Only 51.1% of patients have 2 or more pre-treatment laboratory days and only 37.1% have 3 or more. Counting the whole observation window instead, distinct laboratory days per patient have median 7, interquartile range 5 to 8, maximum 33.

Twelve tests reach near-complete patient coverage at roughly 99.8%: `ALP`, `PSA`, `CREAT`, `ALT`, `TBILI`, `AST`, `NEU`, `HB`, `WBC`, `PLT`, `CA` and `TESTO`. A second tier at roughly 70% adds `GLU`, `K`, `ALB`, `TPRO`, `PHOS` and `MG`. A third tier at roughly 33% adds the full differential and chemistry panel including `LYM`, `MONO`, `BASO`, `EOS`, `HCT`, `RBC`, `CL`, `HCO3` and `URAC`. A malformed test code of `.` carries 6,151 rows and needs a cleaning rule. The `NA` sodium column in `CoreTable` is entirely empty despite being defined.

`PriorMed_training.csv` is 147,770 rows with `CMPRE=YES` on every single row and ZERO rows with a start day at or after day 0. It is therefore baseline prior medication only. The package contains NO chemotherapy administration records, no cycle dates, no per-cycle doses, no dose reductions and no dose delays. Only one row anywhere names docetaxel and it is pre-treatment.

`LesionMeasure_training.csv` is 10,009 rows covering only 1,123 patients, 70.2%, and only two of the three trials, since ASCENT2 supplied no event-level lesion data. Distinct assessment days per patient have median 2 and maximum 6, and results are largely qualitative such as `PRESENT/STABLE`, `YES` and `IR` rather than clean RECIST response categories.

`VitalSign_training.csv` is 36,841 rows covering all 1,600 patients, including repeated `ECOG PERFORMANCE STATUS`, `WEIGHT`, `BODY SURFACE AREA` and blood pressure, which are usable time-varying covariates.

### Cycle alignment, verified 2026-09-04

The `VISIT` field in `LabValue_training.csv` carries 28 distinct labels and names chemotherapy cycles explicitly, which makes per-cycle trajectory features possible even though the package holds no administration records. Three trial-specific vocabularies require harmonization: CELGENE uses `CYCLE 1 DAY 1` through `CYCLE 5 DAY 1` and also `CYCLE 1 DAY 14`; EFC6546 uses `CYCLE 1` through `CYCLE 5`; ASCENT2 uses `CYCLE #01` through `CYCLE #07`. Pre-treatment labels are `SCREENING` with 38,335 rows and `PRE-ENROLLMENT` with 7,605 rows.

Patient coverage per cycle, out of 1,600: cycle 1 has 1,450 at 90.6%, cycle 2 has 1,493 at 93.3%, cycle 3 has 1,433 at 89.6%, cycle 4 has 1,327 at 82.9%, cycle 5 has 769 at 48.1%, and cycles 6 through 10 together have 23 patients and are unusable. Complete-case counts are 1,367 patients for cycles 1 and 2, 1,292 for cycles 1 to 3, and 1,179 for all of cycles 1 to 4.

Cleaning rules still required: `UNSCHEDULED` at 4,148 rows, `TX PHASE DISCONTINUATION` at 1,820 rows and the follow-up visits each need explicit handling.

### A4 download and verification, 2026-09-04

The pinned source generation was downloaded to
`/Users/barbarosisik/PDS-Restricted-Work/prostate-lab-trajectories/runs/2026-09-04-audit-001/source/AllProvidedFiles_149.zip`
and set to mode `400` so the source bytes cannot be modified in place. The cloud object was read only and was NOT altered; its generation and metageneration are unchanged.

Three independent integrity checks all PASSED:

| Check | Expected | Result |
|---|---|---|
| Byte count | 6,227,480 | MATCH |
| SHA-256 | `AB3ECA19C5D0CC4106C96AC04E665DD1A5C9DF58F66328ECD24E8E1067932391` | MATCH, identical to the 2026-08-27 record |
| MD5 | `0F8633E474B581317CB66F1783A84AD8` | MATCH, identical to live cloud metadata |

The SHA-256 agreeing with the value recorded on the previous machine proves the package is byte-identical provenance, not a re-acquired or altered copy.

Archive safety was checked WITHOUT extracting, using `zipfile` in the pinned environment. Every entry passed a CRC integrity test. The scan found no absolute paths, no `..` traversal, no symlink entries and no encrypted entries. The expansion ratio is 1.0x, 6,410,321 uncompressed against 6,227,480 compressed, so there is no zip-bomb risk.

Top-level manifest, names and sizes only, with no file contents read and no patient values accessed:

| Type | Size (bytes) | Name |
|---|---|---|
| Workbook | 31,593 | `Challenge_data_dictionary v2.xlsx` |
| Document | 14,409 | `PCDC Protocol, CRF Location.docx` |
| Nested archive | 5,930,904 | `prostate_cancer_challenge_data_training.zip` |
| Nested archive | 279,647 | `prostate_cancer_challenge_data_leaderboard.zip` |
| Nested archive | 153,768 | `prostate_cancer_challenge_data_finalscoringset.zip` |

IMPORTANT structural finding for A5: the payload is three NESTED archives, not loose CSV files. Each nested archive must receive its own independent unsafe-path, symlink, encryption and expansion-ratio check before extraction. The training archive is the discovery set; leaderboard and final scoring set are held-out partitions and must not be blended into the discovery cohort without an explicit recorded decision.

### Toolchain, 2026-09-04

The Google Cloud CLI is NOT yet installed. The first attempt failed because macOS ships Python 3.9.6 and the CLI requires Python 3.10 or newer; its bundled `urllib3` uses PEP 604 union syntax that Python 3.9 cannot evaluate at import time. No macOS bundled-Python tarball is published by Google, so both candidate URLs return 404.

The user chose to install Python 3.12.8 from python.org rather than download the source through the browser console. The installer at `~/tools/python-3.12.8-macos11.pkg` was verified as signed by the Python Software Foundation, notarized by Apple, with a trusted timestamp. Installation succeeded on 2026-09-04 and `python3.12` reports 3.12.8 at `/Library/Frameworks/Python.framework/Versions/3.12/bin/python3.12`.

Verified toolchain state after installation:

| Item | Value | Verified state |
|---|---|---|
| Google Cloud CLI | `~/tools/google-cloud-sdk`, version 583.0.0 | Runs; `gcloud storage` available; `gsutil 5.37` and `bundled-python3-unix 3.14.7` components present |
| Interpreter for gcloud | `CLOUDSDK_PYTHON=/Library/Frameworks/Python.framework/Versions/3.12/bin/python3.12` | Persisted in `~/.zshrc`; required because macOS Python 3.9 cannot import the CLI |
| Audit environment | `~/tools/venv-pds-audit` on Python 3.12.8 | Created; `openpyxl==3.1.5` and `et_xmlfile==2.0.0` pinned in `~/tools/venv-pds-audit-requirements.txt` |
| Audit tool check | `python -m unittest discover -s tests` | All 3 synthetic-fixture tests pass on this machine; invented data only, no restricted data |
| Authentication | none | `gcloud auth list` reports no credentialed accounts; the user must run `gcloud auth login` |

The CLI installer additionally attempted to install its own Python 3.14 through `sudo` and failed because no terminal was available for the password. That failure is not a blocker, since the CLI runs on the configured Python 3.12 interpreter. The `~/.zshrc` file did not previously exist and was created by the installer; a copy of the pre-existing state was attempted at `~/.zshrc.backup-2026-09-04` before any edit.

The audit tool `src/audit/inventory_raw_data.py` imports only the Python standard library, so the pinned `openpyxl` dependency exists for reading the data dictionary workbook sheets rather than for the inventory tool itself.

Tooling is kept OUTSIDE the restricted root. The CLI tarball and extracted SDK were initially unpacked inside `~/PDS-Restricted-Work` by mistake and were relocated to `~/tools` the same day. The restricted root then contained only its README, and the run folder held zero files throughout, so no restricted data was ever involved in that relocation.

Disk-encryption status is deliberately NOT checked and is NOT a gate, per the user's standing rejection of that added prerequisite. It remains unknown rather than verified.

The Windows run root and the two Windows closeout deletion targets belonged to a machine that is no longer part of this project. Following the user's 2026-09-04 instruction that this Mac is the only workspace, those items are CLOSED AS OUT OF SCOPE and must not be reported as pending work.

| `2026-09-04-audit-001` | LOCAL_CREATED and ready for A4. Run root registered and verified, toolchain installed and authenticated, source metadata refreshed and generation pinned, all on 2026-09-04. Awaiting the user's go-ahead for the download | `/Users/barbarosisik/PDS-Restricted-Work/prostate-lab-trajectories/runs/2026-09-04-audit-001` | `gs://pds-dream-secure-storage-eu-20260827/prostate-lab-trajectories/data/interim/pds_dream/audits/2026-09-04-audit-001/` | Not uploaded; no outputs exist | Not applicable yet; folder is empty of data |

No cleaned dataset or real-file audit result has been produced. A proposed path is not evidence that a file exists.

## Required per-run record

- Run ID, machine label, actual absolute root, creation time, current stage and last checkpoint.
- Local source, extraction, interim, report, temporary and verification-copy paths. Unexpected copies must be recorded too.
- Cloud source URI, object generation, byte size and checksum; each output's explicit version URI, generation, size and checksum.
- Exact code and dependency version; include a source snapshot/hash if work is uncommitted.
- Security checks and transfer verification evidence, without credentials, signed URLs, patient IDs or patient values.
- Publication state of safe code/docs and exact next scientific approval gate.
- Cleanup targets, fresh confirmation state, deletion result and post-deletion check; outstanding items stay visible.

Use states such as `proposed`, `local_created`, `downloaded_verified`, `audited`, `uploaded_unverified`, `uploaded_verified`, `cleanup_pending_confirmation`, `local_removed_verified`, or `blocked_with_local_copy`. Never skip from upload started to cleaned up.

A detailed manifest belongs with the restricted cloud run bundle if filenames or metadata themselves need protection. Keep only reviewed operational metadata in this GitHub register. During execution, also upload a non-sensitive manifest/verification receipt to the run's cloud prefix so transfer state is available even before the next authorized GitHub publication. After local removal, update that receipt and the safe project record as authorized.

## Other known local folders, separate cleanup issue

| Exact folder | Purpose and state |
|---|---|
| `C:\Users\BarbarosIsikGreenhou\Desktop\prostate-lab-trajectories` | Temporary clone; corrected handoff publication verified at 0fa8485; corresponding receipt authorized. No restricted dataset downloaded here. Cleanup pending backup decision and fresh confirmation |
| `C:\Users\BarbarosIsikGreenhou\Documents\Codex\2026-08-24\s\prostate-lab-trajectories` | Retired, do not use for research. All 19 permitted working-file contents were matched to canonical Git history, allowing line-ending/final-newline normalization. Still holds 10 literature PDFs, 10 extracted text files, 5 temporary dictionary PDFs and 2 caches not backed up in GitHub. Nothing deleted |

Do not delete these folders or upload their publisher files under the dataset-processing approval. Their original backup condition and fresh exact-target confirmation still apply.

The latest publication-and-cleanup request starts closeout but does not resolve that backup condition. See `docs/local-closeout-2026-08-31.md` for the exact remaining files and preservation evidence. Shared task history and app memory are not part of these two directories and must not be manually erased.

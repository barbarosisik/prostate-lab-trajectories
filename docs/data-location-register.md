# Data locations and verification register

Updated 2026-09-06. This register contains operational metadata only. No individual laboratory value or patient identifier belongs here.

## Fixed locations and current authorization

This Mac is the only workspace. Computation is local. Google Cloud is the already-approved private storage destination, never compute. Preparation Stage 01 was explicitly authorized and completed; later preparation stages and A10 modeling remain pending scoped approval. No Git commit/push or restricted deletion was authorized in this session.

| Item | Exact location | Current state |
|---|---|---|
| Working repository | `/Users/barbarosisik/Desktop/prostate-lab-trajectories` | Verified branch dataset-audit at local HEAD 4b3dae8; local edits/new code/tests/removals are uncommitted |
| Patient PDFs | `/Users/barbarosisik/PDS-Restricted-Work/goal-patient/` | Verified mode 700; eight pre-existing PDFs plus one explicitly requested derived transcription |
| Patient extracted/transcribed records | `/Users/barbarosisik/PDS-Restricted-Work/index-patient/` | Verified mode 700; stays outside Git and outside the DREAM preservation bundle |
| Registered DREAM run | `/Users/barbarosisik/PDS-Restricted-Work/prostate-lab-trajectories/runs/2026-09-04-audit-001` | Verified present; restricted source and output copies remain local |
| Tooling | `/Users/barbarosisik/tools` | Local dependencies, never patient data |
| Approved cloud bucket | `gs://pds-dream-secure-storage-eu-20260827` | Private storage approval settled; current refresh/preservation status below |

Original run creation checks on 2026-09-04 verified containment, no symlinks, mode 700 and location outside synchronization folders. Stage 01 rechecked registered-path resolution and source/input redirection. Device encryption remains unknown and is not a prerequisite. No old machine is an active target.

## Unchanged source package

Cloud object: `gs://pds-dream-secure-storage-eu-20260827/prostate-lab-trajectories/data/raw/pds_dream/source/AllProvidedFiles_149 (1).zip`.

- Pinned generation: `1787841139282260`; metageneration 1 recorded 2026-09-04.
- Local source: `source/AllProvidedFiles_149.zip` relative to the registered run, mode 400.
- Verified size: 6,227,480 bytes.
- Verified local SHA-256: `AB3ECA19C5D0CC4106C96AC04E665DD1A5C9DF58F66328ECD24E8E1067932391`.
- Recorded MD5: `0F8633E474B581317CB66F1783A84AD8`; cloud base64 `D4Yz5HS1gTF8tm8Xg6hK2A==`; CRC32C `gx71ow==`.
- Last completed security verification, 2026-09-04: EUROPE-WEST4, public access prevention enforced, uniform bucket access on, no public IAM bindings. Versioning not enabled; seven-day soft delete recorded. These are dated observations, not claims of a successful new check.
- Stage 01 verified all 18 CSVs against the original nested archives, before roster creation, and verified they remained unchanged during processing.

The extracted directory was verified 2026-09-05 at 21 files and 110,158,524 bytes including ancillary files. The earlier 110,112,522-byte extraction figure is retained in the audit history. No source file was rewritten.

## Stage 01 output and provenance

All paths below are relative to the registered run. The roster retains all 1,600 training patients; no test-completeness filtering, laboratory transformation, cycle assignment or outcome recoding was applied. Five event tables contributed 412,575 rows with zero unmatched keys; zero duplicate core keys. Twenty-one invented-data tests passed.

| Artifact | Bytes / SHA-256 | State |
|---|---|---|
| `interim/stage01_training_roster.csv` | 78,123 bytes; `e91a6459da073c60a06d194dd4aadaba51b945a66f834bf0c4bffd6e61b350d8` | Verified mode 600 and exact CSV read-back; do not overwrite |
| `interim/stage01-2026-09-06-roster-001.zip` | 35,409 bytes; `76f55f10ce2398a23ede87e531e1b71657f09bb9b05aa5173aa312069249173f` | Verified local bundle containing roster, updated existing inventory, exact code/tests and dependency versions |
| `reports/inventory_training.json` | Existing report updated with `preparation_stage01` | Restricted provenance includes all input hashes and stage results; no new report file created |
| `reports/dream-audit-report.html` | Existing earlier audit artifact | Retained unchanged; not included in this Stage 01 bundle |
| `src/preparation/stage01_roster.py` in repository | `b1b24d74d10e00b8ad38cebbabd88f1c66619ed7141fdad0c375818c6323951a` | Exact executed code hash; also included in bundle |

**Verified source-format findings:** MedHistory, PriorMed and VitalSign training CSVs are not UTF-8. Stage 01 parses bytes reversibly as Latin-1 while requiring ASCII keys; free-text encoding remains unresolved. Evaluation DEATH/LKADT_P fields use `.` missing markers for all 470 patients. Training DEATH uses YES and empty cells; those codes remain unchanged.

## Stage 02 to 07 outputs and provenance

All files below sit under the registered restricted run root, are mode 600, were written with exclusive creation so no earlier output could be overwritten, and passed an exact CSV read-back. `stage06_measurements.csv` is the first preparation output that contains laboratory values, so it is patient-level restricted data and must never enter Git or leave the run root.

| File | Size and SHA-256 | Contents |
|---|---|---|
| `interim/stage02_visit_index.csv` | 12,045,462 bytes; `c3ab83097f991092c19f522ca09cfa15d27c87a2e5e75e16ce1f333078e3f0ae` | Visit label translation keyed by source row. Contains no laboratory value. |
| `interim/stage03_timing_flags.csv` | 18,968,836 bytes; `b6bc1c87df1e7003fab5d5ff2f5386329b0c44ff15ded3543c276898859e871f` | Timing verdicts against the recorded collection day. Contains no laboratory value. |
| `interim/stage04_analysis_roles.csv` | 16,522,691 bytes; `dcbc4b870d5ed70ba5671f214be6a732eba7b301ba904a4b9fb4e939088f0488` | One research purpose and, where excluded, one reason per row. Contains no laboratory value. |
| `interim/stage05_test_catalog.csv` | 7,504 bytes; `078651fa00f5c4eedce5086c90ac40c6296776e068acb7c241f7a82fa11c4b04` | Test-level catalogue of 103 codes with names, units and format counts. Aggregate only, no patient row. |
| `interim/stage07_baselines.csv` | 3,295,284 bytes; `dee1f9b05cb7deca6138548fa821b374bbdc29c1748cfec125f34468064910d4` | One starting value per patient and test, with the evidence it rests on. RESTRICTED. |
| `interim/stage06_measurements.csv` | 20,834,185 bytes; `f30b122a3a88f996762f5287b0d53f86e2b0e40f031a414a710abc5bd7be601b` | Patient-level measurements with value kind, analysis value, retained bounds and repeat status. RESTRICTED. |

## Differential reconciliation, 2026-09-07

`src/preparation/differential_reconciliation.py`, SHA-256 `c2c4247c046514c8989019a46edce57554075a61dd041f8ba9c73ed0d5f96b9e`, answers open question Q-021 and writes no file. It reads the Stage 05 catalogue and the Stage 06 measurements, reports aggregates only, and modifies nothing, so it adds no restricted artifact to preserve or delete. Its verdict is that the five `...LE` codes are shares of the white cell count in per cent rather than duplicates of the counts in `10^9/L`, and that each share is derived from its own count and `WBC`.

## Input CSV SHA-256 verification

| Path relative to run | SHA-256 |
|---|---|
| `extracted/finalscoringset/CoreTable_validation.csv` | `ff3d8ecc69c3f1150c9eae10f403376b616854dff4829717e40b54d3d66b31dc` |
| `extracted/finalscoringset/LabValue_validation.csv` | `17733b7ee283484742bc9a1577c601c22d6e180d2a77eeb14e024abdc31c07dc` |
| `extracted/finalscoringset/LesionMeasure_validation.csv` | `f816869fefe468549aece5f3010f7d42b37c671fa7776476df9f141f06fac4e2` |
| `extracted/finalscoringset/MedHistory_validation.csv` | `8f306d6312bb818a434c3d9b4152115c2d98d0b18171757839b6f37295e31c58` |
| `extracted/finalscoringset/PriorMed_validation.csv` | `ebc683bfb04610c9a2309fe2b3e4900ace2057903c7a30b40b478cd3f4ccb4c1` |
| `extracted/finalscoringset/VitalSign_validation.csv` | `80becdac2095f8a4c574affa7d5bdac82ac6502e99d33f17f155f9c9b2b72c60` |
| `extracted/leaderboard/CoreTable_leaderboard.csv` | `3a8ce9bec3b574a775979932a126005413665227cb5d6965738b23283a923055` |
| `extracted/leaderboard/LabValue_leaderboard.csv` | `fbdc852ec068f5ec9aa255ffcbaa90a977027d838cefae68a71ba0b52ad93c2d` |
| `extracted/leaderboard/LesionMeasure_leaderboard.csv` | `f2c7215b3fdc94a383f32210c6402f1509fd85a6554a69fb492b84b1744d47a7` |
| `extracted/leaderboard/MedHistory_leaderboard.csv` | `fc7294e3a5922bf090e62c0b6f957af64dcf269b7398eb254438d2327ffe3269` |
| `extracted/leaderboard/PriorMed_leaderboard.csv` | `b8e9c436fca069f5bf3943a5f3d119e093fe7ee0e7b3413cd259f41b181e4024` |
| `extracted/leaderboard/VitalSign_leaderboard.csv` | `43cf86eddf36e3e24826f21f3aa69db4b90a81dd48f650336c30791c69231cab` |
| `extracted/training/CoreTable_training.csv` | `989ebfcfb72824e570e0ca1277a7100c8caee14ce515c3503c5d77df97bf1fd4` |
| `extracted/training/LabValue_training.csv` | `ecc9615d67da8acd3e58fef225c7623b409b02eb037371e1652a231e7433ff7d` |
| `extracted/training/LesionMeasure_training.csv` | `ed3df99bbb49baf86c42598d484d03d7fdffdecd6e51caf14adb3e38e1fdfb90` |
| `extracted/training/MedHistory_training.csv` | `864b491618ecec209e8b9d24ebb8a5d8a9f76f8ea4a0a7a471e9758e2e14ffb9` |
| `extracted/training/PriorMed_training.csv` | `8c6196e49ac8e49478e097271e38c9417d76f75bb5c38828237863813c26c9b0` |
| `extracted/training/VitalSign_training.csv` | `fd3943928c1e9d3b08ad606eb58a0ad674c65bb1d86daefee1c3aca8d029f82a` |

## Latest private patient transcription

The user explicitly requested a PDF from pasted report text. These artifacts are outside Git and were not sent to external services or included in DREAM cloud storage.

| Artifact | Location relative to `/Users/barbarosisik/PDS-Restricted-Work` | Verified state |
|---|---|---|
| Derived PDF | `goal-patient/2026-09-05-laboratory-transcription.pdf` | Four pages, mode 600; all 58 current-result rows and comparison columns passed text extraction checks; all pages rendered and visually inspected |
| Structured transcription | `index-patient/2026-09-05-user-supplied-transcription.json` | Mode 600; source qualifiers and previous-result provenance retained |
| Private layout verification | `index-patient/pdf-qa-2026-09-05/` | Four page PNGs plus a contact sheet; local only, cleanup not performed |

PDF SHA-256: `34916edc6ef533145ca61e6fa7139c7be57fe7b8942ed855b103bb1d5a61e6cd`.
Structured transcription SHA-256: `896c9c4da60fdad078e191392c51d02b49bc95142428524103ec3b72e872eef1`.

**Pending:** comparison against the actual latest original PDF, which was not supplied. Testosterone unit/reference and confirmed latest cycle number remain unresolved. The ninth dated blood panel must not be called the ninth chemotherapy cycle. The latest inferred cycle label is stored privately with its evidence status. No medical conclusion was derived from the transcription process.

## Local toolchain

Python 3.12.8: `/Library/Frameworks/Python.framework/Versions/3.12/bin/python3.12`. Audit/PDF environment: `/Users/barbarosisik/tools/venv-pds-audit`. Exact installed versions are pinned in the existing `/Users/barbarosisik/tools/venv-pds-audit-requirements.txt` and included in the Stage 01 bundle.

PDF creation dependencies installed and verified 2026-09-06: reportlab 5.0.1, pypdfium2 5.13.0, Pillow 12.3.0 and charset-normalizer 3.5.1. Existing pypdf 6.16.2 handles text read-back. Poppler was not installed; local PDFium rendered the pages. The PDF operation marker ran successfully with the existing application-bundled Node runtime; no system Node installation was required.

Google Cloud CLI 583.0.0 remains under `~/tools/google-cloud-sdk`. Set `CLOUDSDK_PYTHON` to the Python 3.12 path above. Do not print credentials or place tooling inside restricted data folders.

## Preservation and cleanup status

**Blocked, verified 2026-09-06:** the read-only bucket metadata request stalled and was stopped. A noninteractive retry exceeded its 30-second limit and was terminated. No upload was attempted, no new cloud generation was created, and no claim of fresh cloud privacy/source verification is made. Create-only preservation of the new Stage 01 bundle remains pending. Planned destination: `gs://pds-dream-secure-storage-eu-20260827/prostate-lab-trajectories/data/processed/pds_dream/stage01/2026-09-06-roster-001.zip`. This path is a plan, not an upload receipt. No original-source overwrite is permitted.

All restricted local copies remain. Verify every required preserved artifact by generation, size and a re-downloaded SHA-256 before proposing removal. Fresh exact-target confirmation is required. Patient originals are not part of DREAM run cleanup. Downloads duplicates have not been inventoried or removed in this session. No restricted deletion, Git commit or push occurred.

The six retained docs are the dataset audit, this register, the execution plan, the field checklist, the source matrix and the CHAARTED audit. Five obsolete/duplicate tracked documents were removed locally under the user's explicit cleanup request, with useful content consolidated and their prior versions recoverable in Git at 4b3dae8. No new documentation file was created.

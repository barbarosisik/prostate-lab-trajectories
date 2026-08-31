# Data location and run register

Updated: 2026-08-31. This is non-sensitive operational metadata, not a dataset. Read it at onboarding and update it before and after every transfer, processing stage and cleanup. The continuity and research logs remain required.

## Standing workflow

Private Google Cloud Storage is the permanent home for original and derived restricted data. Computations, tests and processing run locally in a recorded temporary folder. Upload new outputs, verify every required file, then obtain fresh confirmation and remove the exact local run folder. Never put restricted data in GitHub or leave an unrecorded local copy. No cloud computation is authorized by this workflow.

## Permanent storage

| Item | Location | Verified state |
|---|---|---|
| Code and safe documentation | `https://github.com/barbarosisik/prostate-lab-trajectories`, branch `main` | Corrected approval-first handoff published at `0fa84856f526a7e647cf5f07b5acccfe39e645ea`; authenticated connector independently confirmed main and all ten document blob hashes. This receipt follows that commit; verify current main at onboarding |
| Cloud project | `pds-dream-secure-storage` | Existing approved storage project |
| Private bucket | `gs://pds-dream-secure-storage-eu-20260827` | Netherlands `europe-west4`; access controls refreshed 2026-08-31 |
| Original package | `gs://pds-dream-secure-storage-eu-20260827/prostate-lab-trajectories/data/raw/pds_dream/source/AllProvidedFiles_149 (1).zip` | Exists in live console; 6,227,480 bytes and hashes verified 2026-08-27; exact metadata refresh before next download |

Source SHA-256: `AB3ECA19C5D0CC4106C96AC04E665DD1A5C9DF58F66328ECD24E8E1067932391`.

## Active and proposed runs

| Run ID | Stage and state | Exact local folder | Cloud output prefix | Upload verification | Local cleanup |
|---|---|---|---|---|---|
| `2026-08-31-audit-001` | NOT STARTED; latest handoff requires next-agent explanation and fresh approval at A0R; added BitLocker gate withdrawn, not passed | `C:\Users\BarbarosIsikGreenhou\PDS-Restricted-Work\prostate-lab-trajectories\runs\2026-08-31-audit-001` | `gs://pds-dream-secure-storage-eu-20260827/prostate-lab-trajectories/data/interim/pds_dream/audits/2026-08-31-audit-001/` | Not uploaded; no outputs exist | Not applicable yet; local folder not created |

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

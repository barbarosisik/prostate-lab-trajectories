# Data location and run register

Updated: 2026-08-31. This is non-sensitive operational metadata, not a dataset. Read it at onboarding and update it before and after every transfer, processing stage and cleanup. The continuity and research logs remain required.

## Standing workflow

Private Google Cloud Storage is the permanent home for original and derived restricted data. Computations, tests and processing run locally in a recorded temporary folder. Upload new outputs, verify every required file, then obtain fresh confirmation and remove the exact local run folder. Never put restricted data in GitHub or leave an unrecorded local copy. No cloud computation is authorized by this workflow.

## Permanent storage

| Item | Location | Verified state |
|---|---|---|
| Code and safe documentation | `https://github.com/barbarosisik/prostate-lab-trajectories`, branch `main` | Corrected data-free instructions/tracker published and remote verified at `9843e5b86a89c4f5ca583a60f1906c69032ee9c8`; continuity A1 is done. Later receipt commits may follow; verify current main at onboarding |
| Cloud project | `pds-dream-secure-storage` | Existing approved storage project |
| Private bucket | `gs://pds-dream-secure-storage-eu-20260827` | Netherlands `europe-west4`; access controls refreshed 2026-08-31 |
| Original package | `gs://pds-dream-secure-storage-eu-20260827/prostate-lab-trajectories/data/raw/pds_dream/source/AllProvidedFiles_149 (1).zip` | Exists in live console; 6,227,480 bytes and hashes verified 2026-08-27; exact metadata refresh before next download |

Source SHA-256: `AB3ECA19C5D0CC4106C96AC04E665DD1A5C9DF58F66328ECD24E8E1067932391`.

## Active and proposed runs

| Run ID | Stage and state | Exact local folder | Cloud output prefix | Upload verification | Local cleanup |
|---|---|---|---|---|---|
| `2026-08-31-audit-001` | APPROVED, NOT STARTED; local encryption verification pending; continuity tracker `LOCAL-AUDIT-2026-08-31-01` | `C:\Users\BarbarosIsikGreenhou\PDS-Restricted-Work\prostate-lab-trajectories\runs\2026-08-31-audit-001` | `gs://pds-dream-secure-storage-eu-20260827/prostate-lab-trajectories/data/interim/pds_dream/audits/2026-08-31-audit-001/` | Not uploaded; no outputs exist | Not applicable yet; local folder not created |

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
| `C:\Users\BarbarosIsikGreenhou\Desktop\prostate-lab-trajectories` | Temporary code/documentation clone; initial safe instruction publication verified and continuity A1 complete; no restricted dataset downloaded here in this session |
| `C:\Users\BarbarosIsikGreenhou\Documents\Codex\2026-08-24\s\prostate-lab-trajectories` | Retired folder, do not use; existence rechecked; historical local-only papers/text remain subject to the unresolved all-files-backup condition |

Do not delete these folders or upload their publisher files under the dataset-processing approval. Their original backup condition and fresh exact-target confirmation still apply.

# Local closeout record, 2026-08-31

> HISTORICAL RECORD, CLOSED 2026-09-04. The user confirmed that the MacBook Pro is the only workspace for this project and instructed that any other machine be disregarded. Every Windows path, deletion target, backup condition and unbacked-file list below is retained for provenance only. None of it is outstanding work. Do not re-raise these items as blockers.

## Authorization and state

The user explicitly authorized publication of the corrected handoff and corresponding closeout records, then requested local project cleanup after preservation in GitHub. This does not authorize publishing restricted data, publisher full text or credentials. It does not resolve the existing all-files-backup condition or replace fresh exact-target deletion confirmation.

State after publication: corrected handoff committed and pushed at `0fa84856f526a7e647cf5f07b5acccfe39e645ea`. The authenticated GitHub connector independently resolved main to that commit and all ten required file blob hashes matched. Both project folders are still present; deletion is pending. This corresponding receipt is within the user's publication authorization. A later verified chat receipt may record post-deletion results without recreating a local clone. No data processing occurred during this closeout. The next research agent must explain the local data plan and obtain approval at A0R.

## Exact project folder targets

1. `C:\Users\BarbarosIsikGreenhou\Desktop\prostate-lab-trajectories`
2. `C:\Users\BarbarosIsikGreenhou\Documents\Codex\2026-08-24\s\prostate-lab-trajectories`

Before deletion, independently verify remote main, re-inventory both folders, reject unexpected links/reparse points, present these targets and obtain fresh confirmation. Deletion must include only these approved folders and their contained project files/Git metadata. PowerShell permanent deletion bypasses the Recycle Bin. Ordinary SSD deletion cannot guarantee forensic erasure.

The active task root `C:\Users\BarbarosIsikGreenhou\Documents\ChatGPT\barbaros proje` is not a deletion target. Its inspection found only its own Git metadata, not project working files. The proposed `C:\Users\BarbarosIsikGreenhou\PDS-Restricted-Work` root does not exist. No broad drive search was performed.

## Preservation check for retired working files

All 19 permitted files below match content in canonical main's reachable Git history after normalizing CRLF/LF and trailing newlines. Six audit documents are also exact Git blob matches. The other 13 have final-newline formatting differences, not unique substantive work. This is a content-preservation check, not a byte-for-byte archive of the retired directory or its Git metadata. Do not call ignored files backed up on this basis.

| Retired relative path | Matching canonical commit |
|---|---|
| `.gitignore` | `6a74793c23192c201fc1ee61b2d682e1e969fa08` |
| `README.md` | `ea6ce597b71a7ddf966aeb8e194e1be04ebee8cd` |
| `RESEARCH_LOG.md` | `fe3486e255bcfcbaa5584d1893a6e0e5d926579d` |
| `NEXT_AGENT_ONBOARDING_PROMPT.md` | `fd0a18d33a6fefaf9b81966f1cb18afc6540b57d` |
| `PROJECT_CONTINUITY_LOG.md` | `9e45311bbc2e28106a896f2f7af8602f18db6eda` |
| `docs/chaarted-public-field-audit.md` | `a3a9eb5567f4c793e3ab79a3e4f9c8c2c11d6ab9` |
| `docs/dataset-field-coverage-checklist.md` | `dfff3ec5acf743606909425ce23c435c442afd4b` |
| `docs/dream-public-code-audit.md` | `dfff3ec5acf743606909425ce23c435c442afd4b` |
| `docs/pds-dream-access-audit.md` | `dfff3ec5acf743606909425ce23c435c442afd4b` |
| `docs/raw-data-inventory-tool.md` | `dfff3ec5acf743606909425ce23c435c442afd4b` |
| `docs/source-coverage-matrix.md` | `dfff3ec5acf743606909425ce23c435c442afd4b` |
| `literature/README.md` | `b8a9d267147199df3a48975a93ee0db468b618da` |
| `literature/STUDY_CATALOG.md` | `3848704cd86285349fa223f4ec1631043d304cdc` |
| `literature/download_manifest.csv` | `26653216b1f38e1ef029d55933bfe38322e1f2f2` |
| `literature/references.bib` | `58b1c6ce3e5f5d56ebd5de6ecd08942c2a46c039` |
| `src/audit/inventory_raw_data.py` | `5b3e27ee40f0e1334531447e38df9d98c366cc95` |
| `tests/fixtures/synthetic_pds/CoreTable_training.csv` | `e3c507fc8651d0cc8253412f70ee0a73d2ca98c9` |
| `tests/fixtures/synthetic_pds/LabValue_training.csv` | `d02eed8359229d19008efb60ba60a4cb3c08e903` |
| `tests/test_inventory_raw_data.py` | `084506b6eac19fafb84811965f069289744e0d80` |

The fixture CSVs contain invented test data, not the PDS release. Historical versions are preserved for provenance, not instructions that supersede the current handoff.

## Files not backed up in GitHub

The following 27 files are relative to the exact retired folder above. Their deletion requires an explicit exception to the all-files-backup condition or a permitted alternative backup approved and verified first. Bibliography links are not backups. Do not upload publisher full text to GitHub, including private GitHub, to satisfy an "everything" request.

```text
literature/papers/LIT-001_pcwg4_2026.pdf
literature/papers/LIT-002_pcwg3_2016.pdf
literature/papers/LIT-005_dream_overall_survival_2017.pdf
literature/papers/LIT-006_dream_early_discontinuation_2017.pdf
literature/papers/LIT-007_halabi_prognostic_model_2014.pdf
literature/papers/LIT-008_dream_labvalue_model_2016.pdf
literature/papers/LIT-009_dream_tolerance_model_2020.pdf
literature/papers/LIT-014_persistent_nlr_2016.pdf
literature/papers/LIT-017_rsf_landmarking_2021.pdf
literature/papers/LIT-019_docetaxel_neutropenia_2019.pdf
literature/papers/text/LIT-001_pcwg4_2026.txt
literature/papers/text/LIT-002_pcwg3_2016.txt
literature/papers/text/LIT-005_dream_overall_survival_2017.txt
literature/papers/text/LIT-006_dream_early_discontinuation_2017.txt
literature/papers/text/LIT-007_halabi_prognostic_model_2014.txt
literature/papers/text/LIT-008_dream_labvalue_model_2016.txt
literature/papers/text/LIT-009_dream_tolerance_model_2020.txt
literature/papers/text/LIT-014_persistent_nlr_2016.txt
literature/papers/text/LIT-017_rsf_landmarking_2021.txt
literature/papers/text/LIT-019_docetaxel_neutropenia_2019.txt
src/audit/__pycache__/inventory_raw_data.cpython-314.pyc
tests/__pycache__/test_inventory_raw_data.cpython-314.pyc
tmp/pdfs/chaarted/NCT00309985-D11-Data-Dictionary.pdf
tmp/pdfs/chaarted/NCT00309985-D5-Data-Dictionary.pdf
tmp/pdfs/chaarted/NCT00309985-D7-Data-Dictionary.pdf
tmp/pdfs/chaarted/NCT00309985-D8-Data-Dictionary.pdf
tmp/pdfs/chaarted/NCT00309985-D9-Data-Dictionary.pdf
```

## Separate app-managed records

Task histories, memory, browser history and shared app records are not erased by removing these project folders. No supported task-deletion tool is exposed to this task; an archive action is not deletion. Do not manually remove shared session databases, credential stores or arbitrary app files, and do not publish them as a backup. A memory deletion request is not proof of physical erasure. Any unresolved app-managed records must be disclosed in the final cleanup report.

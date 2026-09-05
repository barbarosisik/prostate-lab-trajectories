# Local preparation and storage plan

Updated 2026-09-06. **Verified authorization:** the user requested starting preparation Stage 01 locally. The subsequent user instruction authorizes preparation stages 02 to 07 sequentially after initial GitHub publication. Modeling remains a separate gate. A0R and the source audit are complete; do not repeat them as approval gates.

## Purpose and boundaries

Develop the DREAM method around the index patient's measured blood tests and timing. His private records are located in `~/PDS-Restricted-Work/goal-patient/`; extracted and transcribed records are in `~/PDS-Restricted-Work/index-patient/`. Never put their values or identifiers in this repository. His records are an application case, not a statistically independent validation cohort. DREAM-derived survival is not his prognosis.

Use only this Mac. All restricted computation and derived patient tables stay in the registered run folder in [data-location-register.md](data-location-register.md). Dependencies stay under `~/tools`. Google Cloud is approved private storage only; no cloud compute. Source bytes remain unchanged.

## Preparation sequence and stopping points

| Stage | Work | Why and error checks | State |
|---|---|---|---|
| 01 | Freeze the 1,600-patient training roster and check all five event-table joins | Prevent duplicate patients, incorrect joins and withheld-partition contamination; preserve patients with incomplete tests | Authorized; execution evidence in the dataset audit and register |
| 02 | Harmonize cycle labels and retain within-cycle day | Prevent mid-cycle results from silently becoming cycle-start results | Pending |
| 03 | Compare visit labels with collection days and trial time origins | Detect timing contradictions without inventing dose dates or delays | Pending |
| 04 | Specify unscheduled, discontinuation and unknown-visit handling | Keep unlike visit purposes separate and preserve reviewable exclusions | Pending |
| 05 | Map test identities and verify units | Prevent false trends caused by different units or tests | Pending |
| 06 | Handle exact duplicates, conflicting repeats, missing and bounded results | Preserve uncertainty and usable measurements; never convert NOT DONE to zero | Pending |
| 07 | Resolve baseline flags, timing and duplicate baselines | Define consistent starting measurements with explicit ambiguity handling | Pending |

Show aggregate integrity results before features. A complete visit sequence does not prove complete numeric coverage for every test. Later features, endpoint construction and modeling require the appropriate separate approval. Keep the approved cycles 1 to 4 primary window; do not require future visit completion for an earlier prediction time.

## Stage 01 implementation and checks

Code: `src/preparation/stage01_roster.py`. Tests: `tests/test_stage01_roster.py` plus existing inventory tests.

```sh
PYTHONDONTWRITEBYTECODE=1 ~/tools/venv-pds-audit/bin/python -m unittest discover -s tests -v
PYTHONDONTWRITEBYTECODE=1 ~/tools/venv-pds-audit/bin/python src/preparation/stage01_roster.py
```

The command only accepts the registered local run. It verifies all 18 extracted CSVs against the nested archives in the pinned source ZIP, checks core uniqueness and all five many-to-one event joins, confirms evaluation labels remain withheld, and exclusively creates `interim/stage01_training_roster.csv` at mode 600. It rereads that CSV to check exact output fidelity. Repeated execution must fail rather than overwrite a frozen roster. Source hashes and exact code hash accompany the aggregate result.

**Verified implementation issue found during execution:** three training tables are not valid UTF-8. Stage 01 uses a reversible Latin-1 byte mapping for CSV parsing and requires ASCII join keys. This does not infer or normalize the semantic encoding of free text. All original bytes remain unchanged; later semantic text processing requires its own encoding review.

The observed death coding is YES or blank. Stage 01 preserves it and does not construct a survival event variable. Outcome definitions and censoring remain a later dictionary-based step.

## Existing inventory tool

`src/audit/inventory_raw_data.py` is a read-only first-pass inventory, not the cleaning pipeline. Its fixed aliases, nonempty-result repetition counts and baseline day heuristic are not final transformation rules. Its output still needs disclosure review. Use invented fixtures under `tests/fixtures/synthetic_pds/`; never create real-data test fixtures.

## Publication and restricted-output preservation

Maintain this plan, the existing dataset audit, data register and two root logs. Create no additional documentation or per-step report files. Patient-level derived tables and the specifically requested private patient PDF are separate authorized data artifacts, not repository documentation.

Before preserving a stage output in the approved bucket: record exact source/code/output hashes, use a new object path with create-only conditions, verify private access and generation/size/checksum, then re-download into the registered run for an independent SHA-256 comparison. Never overwrite the pinned original source. Do not treat upload success alone as verification.

Local removal requires fresh confirmation of exact absolute targets after all required outputs are preserved. Retain pending local copies until then. Git publication requires authorization and a fresh check of `git ls-files --others --exclude-standard` before any add. Only code, invented tests and privacy-reviewed aggregate documentation may enter Git.

Historical transfer limits remain: at most 100 MiB output/verification data and 1,000 operations per priced class for the original estimate; pause above USD 0.10 projected incremental cost. Prices were checked 2026-08-31, not refreshed in this session. No paid compute or access-policy changes are included.

# Literature Library

This folder turns the scientific literature into inputs for the analysis rather than a pile of links.

## What is tracked in Git

- [`STUDY_CATALOG.md`](STUDY_CATALOG.md): what each study contributes, its limits and how we will use it.
- [`references.bib`](references.bib): reusable BibTeX citations.
- [`download_manifest.csv`](download_manifest.csv): download/access status for every selected study.

## What stays local

`literature/papers/` contains downloaded PDFs and extracted searchable text. It is excluded by `.gitignore` so publisher files are not redistributed through GitHub.

## Fast reading order

1. **Dataset reality:** LIT-005, LIT-006, LIT-008 and LIT-009.
2. **Outcome definitions:** LIT-001, LIT-002 and LIT-003.
3. **Direct trajectory examples:** LIT-011, LIT-012, LIT-013, LIT-014 and LIT-019.
4. **Adjustment variables:** LIT-007, LIT-010 and LIT-018.
5. **Modeling approach:** LIT-015, LIT-016 and LIT-017.
6. **Source-trial context:** LIT-004, LIT-020, LIT-021 and LIT-022.
7. **A10 analysis plan, 2026-10-08:** architecture LIT-023 to LIT-029, rigor LIT-030 to LIT-036, time traps LIT-037 to LIT-040, clinical evidence LIT-041 to LIT-048, single-patient interpretation LIT-049 to LIT-052.
8. **How the key on-treatment studies were done, 2026-10-09:** [`similar_results/on-treatment-blood-test-changes-and-survival.md`](similar_results/on-treatment-blood-test-changes-and-survival.md), eight studies read in full where accessible.

## Rules for using the literature

- Treat a paper as evidence for a **specific population, treatment, time window and outcome**.
- Distinguish baseline evidence from true within-patient trajectory evidence.
- Distinguish prognostic association, treatment-effect prediction, surrogate endpoints and causation.
- Use reported cutoffs as comparison candidates, not universal truths.
- Prefer continuous trends and uncertainty estimates before thresholding.
- Do not infer that making a laboratory value rise or fall will itself improve the outcome.
- Record every added or removed study in `RESEARCH_LOG.md` and update the manifest.

## Current library status

- 52 studies cataloged: LIT-001 to LIT-022 from 2026-08-24 and LIT-023 to LIT-052 from the verified review of 2026-10-08.
- 10 full-text PDFs were downloaded and validated on the retired Windows machine. They are not on this Mac (checked 2026-10-08), so only the catalog, bibliography and manifest survive.
- Remaining studies are link-only because a legitimate full-text PDF was unavailable or unnecessary.
- Every downloaded PDF passed file-signature, page-count and extractable-text checks.


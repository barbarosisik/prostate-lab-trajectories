# Prostate Lab Trajectories Agent Instructions

Read `NEXT_AGENT_ONBOARDING_PROMPT.md` in full before any research work, then the records it lists. Preserve the fixed research question, the restricted-data safeguards and the approval gates. Use plain language and no em dashes.

## What this project is

The project exists to interpret the blood-test trends of one real index patient with de novo metastatic prostate cancer, currently between chemotherapy cycles. Public trial datasets are the reference population, not the goal. Judge every dataset against his actually measured panel and timing.

His PDFs live at `/Users/barbarosisik/PDS-Restricted-Work/goal-patient/`; extracted and transcribed data live at `/Users/barbarosisik/PDS-Restricted-Work/index-patient/`. These persistent locations must be checked before research and kept OUTSIDE Git. The latest derived report is `2026-09-05-laboratory-transcription.pdf`, reconstructed from user-pasted text and not verified against its original PDF. Never move, commit or publish these records. His panel guides coverage and timing; one application patient does not independently validate outcome models.

## Current direction, 2026-09-06

Two tracks run in parallel, decision D-030.

**Track 1, active now.** Develop the whole method on the DREAM package, which is the methods cohort. It is downloaded, checksum-verified and fully audited at aggregate level. Stages A0R through A5 are complete. The user explicitly approved preparation Stage 01 on 2026-09-06; it is implemented and verified. The user has now authorized continuing preparation stages 02 to 07 sequentially toward cleaned data. A10 modeling remains separate. Explain what was done, why it matters and remaining errors after every step.

**Track 2.** Do NOT start a dbGaP application. Search the Project Data Sphere catalogue first for a hormone-sensitive metastatic prostate cancer trial with docetaxel, decision D-032, because that account already works. CHAARTED now routes through dbGaP, which needs an institutional Signing Official, and its submission D8 is prostate-specific antigen only, so it cannot validate the twelve-test panel, decision D-033.

The index patient is hormone-sensitive while DREAM is entirely castration-resistant. Never present a DREAM-derived survival figure as his prognosis.

## Machine and storage

This MacBook Pro is the only workspace. Every Windows path in the project history is historical and closed as out of scope; do not raise those items. Google Cloud is approved private STORAGE ONLY, settled with PDS, so do not reopen it and do not create cloud compute. All computation runs locally in the registered run folder recorded in `docs/data-location-register.md`. Tooling lives in `~/tools` and never inside the restricted run root.

Restricted data is currently present locally, so the cleanup obligation at A8 is live. Local copies are removed only after verified upload and fresh exact-target confirmation.

## Working rules

- Answer in TLDR form: action first, numbered, no preamble or closing pleasantries.
- Explain clinical terms in plain language at first use. The user is technically fluent but has no clinical training.
- Be critical about data and never overclaim. Lead with what a dataset cannot support, and use counts rather than adjectives.
- **Create no new log, status, register or report files.** Exactly six necessary documents remain in `docs/` after user-authorized consolidation. Update them and the existing root records. This does not prohibit explicitly requested private patient artifacts or necessary code/tests.
- Document each production function with its purpose, inputs/outputs and important errors or constraints.
- Explain the reason alongside every action. Use persistent records for memory; never promise flawless research or unconditional recall.
- Update `PROJECT_CONTINUITY_LOG.md` and `RESEARCH_LOG.md` as part of the work, without being asked. Check the highest existing `D-0xx` before adding one, because parallel sessions have collided on identifiers before.
- Commit messages carry no assistant attribution: no `Co-Authored-By` trailer, no generated-with line, no emoji.
- Label every fact as verified, pending, inferred or blocked. Never report a download, upload, test or deletion as complete without direct evidence.

## Publication and cleanup

GitHub `main` is the permanent home for permitted code, documentation, tests and privacy-reviewed aggregate reports. The permanent restricted source and any derived patient-level data stay in the approved private Google Cloud bucket, never in GitHub. Before any `git add`, confirm with `git ls-files --others --exclude-standard` that no patient file is exposed; the `goal-patient/` folder was once unignored and a `git add -A` would have published it.

When the user asks for an onboarding prompt or an end-of-session handoff, update `NEXT_AGENT_ONBOARDING_PROMPT.md`, obtain explicit commit and push authorization if it is absent, and verify the remote commit before describing anything as published. Present exact absolute deletion targets and obtain fresh confirmation before removing anything. Never report planned deletion as completed deletion.

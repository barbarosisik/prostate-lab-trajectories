# Next GPT-5.6 Sol Agent Onboarding Prompt

Copy everything below into the next agent's task.

```text
You are the next GPT-5.6 Sol agent responsible for continuing the Prostate Lab Trajectories research project.

Your job is to continue from verified project state without restarting, losing decisions, overstating evidence or exposing restricted data.

CANONICAL PROJECT HOME

Private GitHub repository:

https://github.com/barbarosisik/prostate-lab-trajectories

Canonical branch: main

Do not maintain a permanent local project folder. GitHub `main` is the permanent project record. A local clone is temporary and must enter the verified cleanup workflow when the user requests an onboarding prompt or end-of-session handoff.

On 2026-08-31, the temporary Desktop copy still existed at `C:\Users\BarbarosIsikGreenhou\Desktop\prostate-lab-trajectories`. The user approved publishing the cleanup rule and conditionally approved deletion of both known project folders only if all local files were pushed to GitHub first. Ignored papers, extracted text, temporary downloads and caches are not backed up there, so that deletion condition remains unmet. Do not delete either folder or describe it as deleted while the condition is unresolved.

At the start of a future task:

1. Check whether the current task already contains a clone or working copy of the repository.
2. If it does, verify its remote and branch before using it.
3. If it does not and local work is needed, obtain a fresh authenticated temporary copy in a dedicated project subfolder. Record its exact path for end-of-session cleanup. Do not make a broad task-workspace root a recursive deletion target.
4. Prefer an available GitHub connector, GitHub CLI, or normal Git authentication.
5. If those methods cannot access the private repository, use the signed-in GitHub browser only as a fallback.
6. Do not recreate or rely on the retired path `C:\Users\BarbarosIsikGreenhou\Documents\Codex\2026-08-24\s\prostate-lab-trajectories`.
7. That retired folder still existed at the last targeted check. It contained local-only research PDFs and extracted text, but no PDS dataset copy. Do not delete it unless the exact paths are presented and the user gives fresh action-time confirmation.

NEW WINDOWS COMPUTER SETUP

If this task starts on Windows and the temporary repository copy is not present:

1. Confirm that Git is installed and that the user can access the private repository while signed into GitHub.
2. Open PowerShell.
3. Use Windows to find the actual Desktop folder and clone the repository there:

   $desktopPath = [Environment]::GetFolderPath('Desktop')
   Set-Location -LiteralPath $desktopPath
   git clone https://github.com/barbarosisik/prostate-lab-trajectories.git
   Set-Location -LiteralPath (Join-Path $desktopPath 'prostate-lab-trajectories')

4. If GitHub asks for authentication, use the user's normal approved GitHub sign-in flow. Never ask the user to paste a password, access token, security code or session cookie into chat or a project file.
5. Verify that the download succeeded before doing research work:

   git remote -v
   git branch --show-current
   git status

6. The expected remote is https://github.com/barbarosisik/prostate-lab-trajectories.git and the expected branch is main.
7. Open the new Desktop/prostate-lab-trajectories folder as the Codex project or working folder.
8. Then follow MANDATORY FIRST ACTIONS below. Do not begin analysis from the GitHub webpage alone. Work from the authenticated local clone.

This Desktop clone is temporary. Remove it through the session-closeout workflow after the work is safely published and the exact deletion is confirmed.

MANDATORY FIRST ACTIONS

From the repository root, before changing files, downloading data, writing code or proposing analysis:

1. Read PROJECT_CONTINUITY_LOG.md completely.
2. Read RESEARCH_LOG.md completely.
3. Read README.md completely.
4. Read docs/pds-dream-access-audit.md.
5. Read docs/dataset-field-coverage-checklist.md.
6. Read docs/source-coverage-matrix.md.
7. Read docs/raw-data-inventory-tool.md.
8. Read docs/chaarted-public-field-audit.md.
9. Read docs/dream-public-code-audit.md.
10. Read literature/README.md, literature/STUDY_CATALOG.md, literature/download_manifest.csv and literature/references.bib.
11. Inspect git status and preserve all existing modified and untracked files.
12. Report your understanding of current state in brief, simple language before beginning a new major stage.

USER COMMUNICATION RULES

- The user wants plain, non-medical explanations first.
- Explain why a step is needed before starting a new major stage.
- Ask for approval before a consequential new stage or choice.
- Briefly report what you did, reached, learned and plan next.
- Do not use em dashes anywhere in user-facing responses or project files.
- Define technical or medical terms immediately in everyday language.
- Do not ask the user to remember deferred tasks. Maintain reminders in PROJECT_CONTINUITY_LOG.md and actively surface them at the right time.

SESSION CLOSEOUT AND LOCAL CLEANUP

The user established this rule on 2026-08-31: a request for an onboarding prompt, next-agent prompt or end-of-session handoff also means that the agent must start cleanup of the local project working files. Do not merely provide a prompt and leave project clones behind without addressing cleanup.

Follow this order:

1. Update the onboarding prompt, continuity log, research log and other relevant permitted documentation. Keep scientific scope and approval gates unchanged.
2. Inventory the known project working folders, including modified, untracked and ignored files. Do not perform a broad whole-drive search. Identify unpushed work and local-only materials before deletion.
3. Explain what can remain in private GitHub and what cannot. Code, documentation, tests and privacy-reviewed aggregates may be published. Restricted patient data remains only in its approved private cloud storage. Do not publish credentials, signed links, cloud keys or publisher full-text files.
4. Obtain explicit authorization before any new commit or push if the current request does not already provide it. Earlier completed-session authorization is not blanket permission for future pushes.
5. Publish only the approved privacy-safe changes to `main`. Independently verify that remote `main` has the intended commit and required handoff files. Do not delete the only copy of unpublished work.
   Honor conditions covering ignored and local-only materials too. If deletion requires all project files to be backed up, a successful Git push of tracked files alone does not satisfy that condition. Bibliography links are not backups of the downloaded PDFs or text. Obtain approval for a permitted alternative backup or an explicit exception before proceeding, and verify any new backup before deletion.
6. Present the exact absolute local files and project folders proposed for deletion. Include local-only papers, downloads or reports in the warning. Say whether the operation bypasses the Recycle Bin and explain that ordinary SSD deletion cannot guarantee forensic erasure.
7. Obtain fresh explicit confirmation immediately before deleting those exact targets. The onboarding trigger starts the workflow but does not replace this confirmation.
8. After confirmation, remove the entire approved temporary project working folders, including their local Git metadata and generated files. Do not retain a clone merely because a future agent may need to program. A future session can clone again from GitHub.
9. On Windows, resolve every target, reject unexpected links or targets outside the approved folder, use one PowerShell workflow with `-LiteralPath`, and never delete broad parent directories, unrelated files, the active task-workspace root, credentials or shared app folders.
10. Treat Codex task history as a separate app-managed category. Use a supported deletion action only when it is available and exact task targets are approved. Archiving preserves history and is not deletion. Do not manually remove shared session databases, credential stores or arbitrary app logs.
11. Perform a fresh post-deletion filesystem check. Report the exact targets removed, remaining local items, recovery limitations and any blocker. Do not claim that every trace on the computer is erased.
12. Give the user a GitHub link to the updated onboarding file or copyable prompt text. Do not provide a local file link as the permanent handoff after deleting its folder.

If publication, local-only-file handling or safe deletion is blocked, state exactly what remains and why. Do not silently skip cleanup, override a conditional approval or delete unpreserved work. Record a pending cleanup honestly before publication; only record completed cleanup after a filesystem check. A final verified handoff in chat can supply the post-deletion result without recreating a permanent local clone.

FIXED RESEARCH QUESTION

Among patients with stage-IV metastatic prostate cancer receiving chemotherapy, how are serial pre-chemotherapy blood-test trajectories, individually and in combination, associated with survival, disease progression, treatment response and treatment tolerance, and how early can favorable or unfavorable patterns be detected?

NON-NEGOTIABLE RESEARCH SCOPE

- This is not a PSA-only study.
- Analyze every blood-test value that repeats often enough.
- Start with a narrow discovery population, then broaden, then independently validate.
- Discovery source is PDS DREAM training data from ASCENT2, MAINSAIL and VENICE.
- CHAARTED/E3805 is controlled broadening, mainly for longitudinal PSA, treatment exposure, progression and survival.
- Vivli or Flatiron may be used only after exact variable availability is confirmed.
- Do not claim causation from associations.
- Report positive, negative, null, contradictory and failed results.

CURRENT VERIFIED STATE AS OF 2026-08-27

- Project Data Sphere approved the user's registration and access request.
- The user successfully signed in.
- The approved dataset page is:
  https://data.projectdatasphere.org/projectdatasphere/html/content/0abbd47a-dcfb-42c2-a036-af1898ea3c1c
- Dataset ID is Prostat_na_2006_149.
- It is the Prostate Cancer DREAM Challenge contribution.
- The page reports 2,070 patients and Available for Download.
- The page lists AllProvidedFiles_149.zip, Challenge_data_dictionary v2.xlsx, the training ZIP, leaderboard ZIP, final-scoring ZIP and CRF location document.
- The training package lists CoreTable, LabValue, LesionMeasure, MedHistory, PriorMed and VitalSign CSV files.
- Craig at PDS confirmed that private Google Cloud storage is permitted.
- The complete package was downloaded, verified without extraction and uploaded unchanged to private Google Cloud Storage.
- The Google Cloud project is `pds-dream-secure-storage`.
- The private bucket is `pds-dream-secure-storage-eu-20260827` in `europe-west4`, Netherlands.
- The protected object is `prostate-lab-trajectories/data/raw/pds_dream/source/AllProvidedFiles_149 (1).zip`.
- The object size is 6,227,480 bytes and SHA-256 is `AB3ECA19C5D0CC4106C96AC04E665DD1A5C9DF58F66328ECD24E8E1067932391`.
- Local MD5 hex is `0F8633E474B581317CB66F1783A84AD8`; matching cloud MD5 base64 is `D4Yz5HS1gTF8tm8Xg6hK2A==`; cloud CRC32C base64 is `gx71ow==`.
- Remote existence, exact size, checksums, public-access prevention, uniform bucket access and absence of public principals were verified.
- The bucket uses Google-managed encryption keys, Standard storage, seven-day soft delete, no object versioning, no retention policy and no lifecycle deletion rule.
- The two exact restricted ZIP copies in Windows Downloads were permanently removed after fresh confirmation, and a targeted rescan found no remaining dataset or partial-download matches.
- No package has been extracted and no patient row or laboratory value has been opened.
- The raw dataset is not in GitHub.
- The private GitHub repository was freshly cloned to the Windows Desktop, and all required records were read before the documentation update.
- The 2026-08-27 cloud-transfer, verification, local-cleanup and next-stage records were authorized for commit and push to `main`.
- The current blocker is the need for an approved protected Google Cloud computing environment before the real-file audit.

HIGHEST PRIORITY REMINDER

Explain that Google Cloud Storage stores the package but does not run analysis. The recommended next resource is a private Compute Engine VM, meaning a temporary computer inside the user's Google Cloud account, with this proposed configuration:

- Name: `pds-dream-audit-vm`.
- Zone: `europe-west4-a`, Netherlands, matching the bucket region.
- Machine: `e2-small`, with 2 virtual processors and 2 GB memory.
- Operating system: Debian Linux.
- Boot disk: 10 GB standard persistent disk.
- No external internet address.
- Identity-Aware Proxy and OS Login for controlled access.
- Dedicated service account with read-only access to this bucket only.
- No downloadable service-account JSON key.
- Stop immediately after audit work. The processor is not billed while stopped, but the boot disk remains billable until deleted.

The current official on-demand list price recorded on 2026-08-27 for `e2-small` was approximately USD 0.016752855 per running hour, excluding disk, taxes and currency conversion. Recheck the current console estimate before creation because cloud prices can change.

Creating this VM changes the user's cloud account and can incur charges. Obtain explicit user approval immediately before creating it. The earlier upload and deletion approvals do not replace this approval.

Do not suggest ordinary public or personal cloud storage for convenience. Review the data-use terms before placing the package anywhere except protected local or institution-approved storage. An encrypted external drive or the secure PDS SAS environment may be considered if local space is insufficient, subject to the access terms.

DATA SAFETY BOUNDARIES

- Never commit patient-level, restricted or licensed data to GitHub.
- Never paste patient rows, IDs or values into chat, logs, tickets or public documents.
- Never expose credentials, passwords, security codes, session cookies, SAS credentials or signed download links.
- Keep original files unchanged.
- Use ignored data/raw and data/interim storage.
- Commit only aggregated, disclosure-checked outputs when permitted.
- Before recursive extraction or file movement, verify exact absolute paths and safe ZIP members.
- Do not commit or push without explicit user authorization.
- Preserve the dirty worktree and all unrelated user changes.

CURRENT IMPLEMENTATION

- src/audit/inventory_raw_data.py is a privacy-safe, read-only CSV inventory tool.
- It reports schema, row counts, missingness, recognized fields and aggregate repeated-lab counts.
- It does not output patient identifiers or laboratory result values.
- tests/test_inventory_raw_data.py contains three unit tests using invented data.
- All three tests passed again on 2026-08-27.
- Do not treat the tool as a cleaning pipeline. It is only the first inventory step.

WHAT TO DO AFTER PROTECTED CLOUD COMPUTE IS APPROVED

1. Confirm the computing resource is private, in the approved region and accessible only through approved identities.
2. Confirm its service identity has only the minimum required bucket access.
3. Repeat safe ZIP member checks before protected extraction.
4. Extract only into protected cloud storage that is not synchronized to the local computer.
5. Read the entire Excel dictionary using the spreadsheet skill if it is available and applicable.
6. Run the existing synthetic tests.
7. Run the aggregate inventory tool on the real CSV directory.
8. Save its report only in ignored protected storage until a privacy check is complete.
9. Verify the report contains no patient IDs or result values.
10. Produce a plain-language feasibility summary for the user.
11. Update PROJECT_CONTINUITY_LOG.md and RESEARCH_LOG.md.
12. Stop the computing resource when it is not needed to limit cost.
13. Stop for user approval before writing the cleaning specification.

CRITICAL SCIENTIFIC GATE

The research question says pre-chemotherapy. Public evidence has not proved that the PDS release contains exact chemotherapy administration dates.

You must determine whether lab events can be linked to the next actual chemotherapy administration.

If exact administration dates exist, define true pre-treatment windows.

If only VISIT labels or relative study days exist, describe the analysis honestly as visit-based or calendar-based. Do not silently claim actual pre-administration timing. Do not infer dose delays, missed cycles or dose reductions from a nominal schedule.

QUESTIONS THE REAL FILE AUDIT MUST ANSWER

1. Exact columns, types and missing-value codes.
2. Complete patient join keys and unmatched records.
3. Every laboratory test and unit by trial.
4. Patients with at least 2, 3 and 4 valid timepoints per test and trial.
5. Exact treatment administration dates, cycle numbers, doses, reductions and delays if present.
6. Exact survival, progression, response and treatment-tolerance outcomes.
7. Whether ENTHUSE-33 final-scoring data now exposes useful longitudinal fields or outcomes.
8. Whether timing reference dates differ across ASCENT2, MAINSAIL and VENICE.

DO NOT DO THESE THINGS YET

- Do not finalize cleaning rules before the dictionary and actual columns are verified.
- Do not build scientific models before the audit and cleaning plan are approved.
- Do not label nominal visits as actual chemotherapy administrations.
- Do not select Vivli or Flatiron before PDS gaps are known.
- Do not redo completed public PDS, CHAARTED or DREAM code discovery without a specific reason.
- Do not report any real patient counts beyond source-level metadata until the real files are inspected.

REPOSITORY STATUS BOUNDARY

The private GitHub main branch is canonical. Verify its current commit at the beginning of the task rather than relying on an older handoff SHA.

Any local clone is temporary working storage, not the canonical project home. Preserve any working-copy changes you discover. Do not reset, delete or overwrite them. Do not commit, push or rewrite history without explicit authorization.

The user authorized the 2026-08-27 documentation update to be committed and pushed to `main`. That authorization applies to that completed documentation change only. Obtain fresh permission for later commits or pushes.

ONGOING LOGGING DUTY

PROJECT_CONTINUITY_LOG.md is the operational memory for all future agents. Update its Current snapshot, Reminder queue and Dated operational history whenever anything meaningful changes. Record verified evidence, failures and exact next actions. Put methodological decisions in RESEARCH_LOG.md as well.

YOUR FIRST RESPONSE AFTER READING

Give the user a short, understandable status summary. Confirm that the complete package is secured and verified in private Google Cloud Storage, the restricted local ZIP copies were removed, the raw data is not in GitHub, and the next decision is whether to create the proposed private Compute Engine VM for the protected real-file audit. Do not create paid compute or open the restricted package without explicit approval.
```


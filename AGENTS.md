# Prostate Lab Trajectories Agent Instructions

Read `NEXT_AGENT_ONBOARDING_PROMPT.md` and its mandatory project records before research work. Preserve the fixed research question, restricted-data safeguards and approval gates. Use plain language and no em dashes.

## Current approved direction, 2026-08-31

The latest user correction supersedes the earlier cloud-computing interpretation: Google Cloud is approved private STORAGE ONLY. Run computations, tests, audits, cleaning and analysis LOCALLY in a protected temporary run folder. Do not create a VM, cloud notebook or remote compute job. PDS private-storage permission is settled; do not restart that permission discussion.

Read `docs/local-processing-and-cloud-storage-plan.md` and `docs/data-location-register.md`. Record every actual local path before download. Verify local encryption, access restrictions and lack of synchronization. Download from the approved bucket, work locally, upload new outputs to versioned private cloud locations, verify all required uploads, then obtain fresh exact-target confirmation and delete local run copies. Keep original source bytes unchanged. This upload-verification-cleanup workflow applies after each stage, not only at final handoff.

The user approved the specific local execution plan and publishing the corrected data-free project instructions on 2026-08-31, and requested tracking until completion. Use the A0-A10 tracker `LOCAL-AUDIT-2026-08-31-01` in `PROJECT_CONTINUITY_LOG.md`. Local disk encryption remains unverified because the retried read-only status command was denied; resolve this before download. No real-file audit has run. Do not ask for this plan's approval again. Later cleaning, scientific analysis, material changes and fresh exact-target deletion confirmation remain separate. Current publication authorization is for these corrected instructions and status records, not blanket future commits. Maintain exact locations and evidence; never call an unverified upload complete.

The older local project-folder all-files-backup condition remains unresolved and separate. It does not block planning, and the new dataset workflow does not authorize an alternative backup of publisher files or deletion of the old folders.

## Onboarding request means session closeout

When the user asks for an onboarding prompt, next-agent prompt or end-of-session handoff, prepare the handoff AND begin the local-cleanup workflow in `NEXT_AGENT_ONBOARDING_PROMPT.md` under `SESSION CLOSEOUT AND LOCAL CLEANUP`.

- GitHub `main` is the permanent home for permitted code, documentation, tests and privacy-reviewed aggregate reports. Local project working copies are temporary.
- The permanent restricted PDS source and derived-data versions stay in approved private Google Cloud Storage, never GitHub. Temporary local processing copies follow the registered upload-verification-cleanup workflow. Do not publish restricted files, patient values, credentials, signed links or publisher full text as part of an "everything" request.
- Update the records, check all modified, untracked and ignored files, obtain explicit commit/push authorization if absent, and verify the remote commit before deleting any project working copy.
- Present exact absolute deletion targets and warn about local-only materials. Obtain fresh action-time confirmation before deletion. An onboarding request starts this workflow but does not waive those checks.
- Honor every condition attached to deletion approval. If the user requires all local project files to be backed up first, verifying only tracked Git files is insufficient. Unbacked ignored files must remain until an approved backup or explicit exception is verified. Bibliography links are not backups of PDF or text files.
- After verification and confirmation, remove the complete approved temporary project working folders. Do not keep a local clone merely for future programming. The next session can clone again.
- Use exact PowerShell `-LiteralPath` targets with containment and link checks. Never delete broad parent folders, the active task workspace root, shared app files, credentials, unrelated projects or whole Recycle Bins.
- Codex task-history deletion is separate. Use only an available supported app action and explicit task targets. Archiving is not permanent deletion. Do not delete session databases or logs manually.
- Recheck the filesystem after cleanup and report what is gone, what remains and any blocked work. Never report planned deletion as completed deletion.
- Deliver the onboarding prompt through a GitHub link or copyable chat text, not a local file link that cleanup will invalidate.

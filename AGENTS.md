# Prostate Lab Trajectories Agent Instructions

Read `NEXT_AGENT_ONBOARDING_PROMPT.md` and its mandatory project records before research work. Preserve the fixed research question, restricted-data safeguards and approval gates. Use plain language and no em dashes.

## Current approved direction, 2026-08-31

The latest user correction supersedes the earlier cloud-computing interpretation: Google Cloud is approved private STORAGE ONLY. Run computations, tests, audits, cleaning and analysis LOCALLY in a protected temporary run folder. Do not create a VM, cloud notebook or remote compute job. PDS private-storage permission is settled; do not restart that permission discussion.

Read `docs/local-processing-and-cloud-storage-plan.md` and `docs/data-location-register.md`. Record every actual local path before download, keep access limited and avoid synchronized locations. Download from the approved bucket, work locally, upload new outputs to versioned private cloud locations, verify all required uploads, then obtain fresh exact-target confirmation and delete local run copies. Keep original source bytes unchanged. This workflow applies after each stage, not only at final handoff.

LATEST HANDOFF DIRECTION: after mandatory read-only onboarding, the next agent must explain the data plan in plain language, ask one clear approval question and WAIT before any data work. This user-requested checkpoint supersedes the earlier instruction to resume without asking again. Prior approval/publication remain historical facts, not permission to skip the requested first reply. Track this in `LOCAL-AUDIT-2026-08-31-01`, including A0R. Cleaning and scientific analysis each require later approval; exact-target deletion confirmation stays separate.

The user rejected the previous agent's added mandatory BitLocker/disk-encryption check. Do not pursue more encryption-status commands, security-app inspection, Windows-setting changes or recovery-key requests as a prerequisite to this handoff or the first data-plan response. Encryption status is unknown, not verified on/off; the added gate was not established as a new PDS requirement. Preserve agreed file privacy and data handling without inventing additional requirements.

The user explicitly authorized publication of this corrected handoff and corresponding closeout records on 2026-08-31. Verify remote main before reporting publication complete. This authorization does not approve data execution, future unrelated pushes, an alternative backup of publisher files or deletion without the required exact-target confirmation.

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

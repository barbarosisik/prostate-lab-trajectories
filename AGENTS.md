# Prostate Lab Trajectories Agent Instructions

Read `NEXT_AGENT_ONBOARDING_PROMPT.md` and its mandatory project records before research work. Preserve the fixed research question, restricted-data safeguards and approval gates. Use plain language and no em dashes.

## Current approved direction, 2026-08-31

Private Google Cloud use is approved. PDS storage permission is already confirmed, and the user has approved proceeding toward protected cloud computing and the real-file audit. Do not describe Google Cloud use as unapproved or restart the provider-permission discussion.

After onboarding, prepare a concrete execution plan with exact resources, region, access controls, current costs, audit steps, outputs and shutdown arrangements. Ask for approval of that specific plan before resource creation and restricted-file execution. Setup and audit may be approved together when the plan explicitly covers both. Execute the approved scope without asking again for each routine step. Ask again for a material change or a later research stage not covered by the approved plan.

Cloud approval does not mean a cloud computer (virtual machine, or VM) already exists or an audit has run. Verify actual state. The local cleanup backup condition is separate and remains unresolved; it does not prevent read-only onboarding or preparation of the approved cloud-work plan.

## Onboarding request means session closeout

When the user asks for an onboarding prompt, next-agent prompt or end-of-session handoff, prepare the handoff AND begin the local-cleanup workflow in `NEXT_AGENT_ONBOARDING_PROMPT.md` under `SESSION CLOSEOUT AND LOCAL CLEANUP`.

- GitHub `main` is the permanent home for permitted code, documentation, tests and privacy-reviewed aggregate reports. Local project working copies are temporary.
- The restricted PDS source stays in its approved private Google Cloud location, never GitHub. Do not upload restricted files, patient values, credentials, signed links or publisher full text as part of an "everything" request.
- Update the records, check all modified, untracked and ignored files, obtain explicit commit/push authorization if absent, and verify the remote commit before deleting any project working copy.
- Present exact absolute deletion targets and warn about local-only materials. Obtain fresh action-time confirmation before deletion. An onboarding request starts this workflow but does not waive those checks.
- Honor every condition attached to deletion approval. If the user requires all local project files to be backed up first, verifying only tracked Git files is insufficient. Unbacked ignored files must remain until an approved backup or explicit exception is verified. Bibliography links are not backups of PDF or text files.
- After verification and confirmation, remove the complete approved temporary project working folders. Do not keep a local clone merely for future programming. The next session can clone again.
- Use exact PowerShell `-LiteralPath` targets with containment and link checks. Never delete broad parent folders, the active task workspace root, shared app files, credentials, unrelated projects or whole Recycle Bins.
- Codex task-history deletion is separate. Use only an available supported app action and explicit task targets. Archiving is not permanent deletion. Do not delete session databases or logs manually.
- Recheck the filesystem after cleanup and report what is gone, what remains and any blocked work. Never report planned deletion as completed deletion.
- Deliver the onboarding prompt through a GitHub link or copyable chat text, not a local file link that cleanup will invalidate.

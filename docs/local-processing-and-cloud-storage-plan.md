# Local processing and private cloud storage plan

Updated: 2026-08-31. Status: earlier approval is recorded, but the latest handoff request requires the next agent to explain this plan and obtain fresh approval FIRST, before data work. The assistant-added mandatory disk-encryption gate has been withdrawn at the user's direction, not passed. No restricted download, extraction, real-file audit, cleaning or modeling has run. Track completion and new A0R checkpoint in `PROJECT_CONTINUITY_LOG.md`, plan ID `LOCAL-AUDIT-2026-08-31-01`.

## Standing direction

The user's latest correction supersedes the earlier cloud-computing proposal. Google Cloud is the permanent private file store, not the place to run computations. Run tests, audits, cleaning and analysis on the user's local computer. At each completed stage, upload new outputs to private cloud storage, verify them, then remove the temporary local copies after fresh exact-target confirmation. Do not create a cloud computer, cloud notebook, remote analysis job or paid network service.

The unchanged source remains in its existing cloud location. Do not re-upload or overwrite it after every process. Upload new stage outputs as new versions, retaining their connection to the original source and the code that produced them. Later agents download the verified version they need to their own recorded temporary local run folder.

## Verified state and unresolved checks

- The authenticated Desktop clone is on `main`; HEAD matched remote `main` at `fb059b91df2fd38740ab305fb17058204e7d9096` at this session's initial verification. It was clean before these documentation changes. GitHub remains the permanent code/documentation record.
- The approved project is `pds-dream-secure-storage`; bucket `pds-dream-secure-storage-eu-20260827` is Standard storage in `europe-west4`, Netherlands.
- Live 2026-08-31 console inspection confirmed the source object remains visible, Not public, with rounded size 6.2 MB and its August 27 modified timestamp. Exact bytes and hashes below are the 2026-08-27 verified values, not a newly computed hash.
- Public access prevention and uniform bucket access remain enabled. Google-managed encryption, seven-day soft delete, no object versioning, no retention policy and no lifecycle rule were visible. IP filtering is not configured: access is identity-controlled, not limited to a private network.
- Project IAM, the access-permission list, displayed the existing user as Owner. Bucket convenience groups for project owners/editors/viewers remain present. No public principals were displayed. Future project membership could broaden access, so refresh effective permissions before transfers.
- No cloud computer or service account was created. Compute Engine showed an API Enable screen; the resource inventory displayed no compute/disk/network/notebook resource types. Leave compute disabled.
- Git, PowerShell and Python 3.14 are available locally. The three existing invented-data tests passed. The C: drive had 266,093,146,112 free bytes at the local check. This is a capacity check, not proof of device security.
- The proposed restricted-work directory does not yet exist. No dataset has been downloaded in this session. Google Cloud CLI is not installed.
- Historical checks: `manage-bde -status C:` and CIM RAM inspection were denied. These errors do not establish that encryption is off or RAM is insufficient. The user rejected the agent's mandatory encryption-check detour; do not pursue it or ask for security-app inspection/recovery keys. This was an added precaution, not a newly verified PDS condition. No Windows setting was changed. Ordinary restricted-folder privacy and the stated data-handling controls remain in scope.

## Exact locations

Permanent source, unchanged:

```text
gs://pds-dream-secure-storage-eu-20260827/prostate-lab-trajectories/data/raw/pds_dream/source/AllProvidedFiles_149 (1).zip
```

Expected size: 6,227,480 bytes. SHA-256: `AB3ECA19C5D0CC4106C96AC04E665DD1A5C9DF58F66328ECD24E8E1067932391`. MD5: `0F8633E474B581317CB66F1783A84AD8` in hex, `D4Yz5HS1gTF8tm8Xg6hK2A==` in cloud base64. CRC32C: `gx71ow==` in cloud base64.

Proposed first temporary local run folder, outside the Git clone, Downloads, Desktop and Documents:

```text
C:\Users\BarbarosIsikGreenhou\PDS-Restricted-Work\prostate-lab-trajectories\runs\2026-08-31-audit-001
```

Within that one folder:

| Relative location | Purpose |
|---|---|
| `data/raw/pds_dream/source/` | Byte-identical downloaded source ZIP |
| `data/raw/pds_dream/extracted/` | Safely extracted, unmodified source files |
| `data/interim/` | Unreviewed audit outputs, treated as restricted |
| `reports/reviewed/` | Output that has passed the disclosure checks |
| `tmp/` | Process-specific temporary files and upload verification downloads |
| `logs/` | Sanitized operational status, never source rows or values |
| `manifest.json` | File list, byte sizes, SHA-256 hashes, source/code versions and stage state |

Permanent audit outputs, created only after plan approval:

```text
gs://pds-dream-secure-storage-eu-20260827/prostate-lab-trajectories/data/interim/pds_dream/audits/2026-08-31-audit-001/
```

Proposed convention for later separately approved cleaning stages:

```text
gs://pds-dream-secure-storage-eu-20260827/prostate-lab-trajectories/data/processed/pds_dream/<cleaning-version>/
```

Version names must be explicit and recorded. Never depend on an unexplained folder named `latest`. Do not create a cleaned-data version before cleaning is approved and passes quality checks.

## Local setup and access

1. Before downloading, record the proposed and then actual absolute path in `docs/data-location-register.md` and the continuity log. Resolve the real user-profile path on another computer rather than copying this computer's username. A new machine needs its own local security/path check.
2. After the requested next-agent plan approval, check sufficient space and confirm the recorded destination resolves to the intended local folder, not a link or synchronized folder. Keep the check limited to this task's paths and actual file-access needs. Do not reinstate a mandatory BitLocker check, general device-security audit or unrequested Windows-setting change. If a concrete problem is found, explain the evidence and ask about that specific change.
3. Create only the dedicated run directory. Restrict its Windows permissions to the current user, SYSTEM and local administrators; remove broad inherited access on this new folder only, then inspect the effective permissions. Do not alter the whole user profile or unrelated folders. Do not switch off endpoint protection.
4. Prefer a locally installed official Google Cloud CLI with normal interactive user sign-in. If installation is needed, it is part of this proposed setup, in the user's normal application location. Keep credentials in the CLI's managed credential store, never in Git, the data folder, chat or a manifest. No downloaded service-account key, shared secret or signed URL. Do not use Cloud Shell to compute or inspect data. Follow the [official installation instructions](https://docs.cloud.google.com/sdk/docs/install-sdk) and [user sign-in documentation](https://docs.cloud.google.com/sdk/docs/authenticate). Stored user credentials make the local account and filesystem permissions important; never print or inspect credential contents.
5. Use only the existing approved user identity and explicit project/bucket/object arguments. Required transfer operations are source read and metadata checks, plus create/read of new output objects. The existing account has Owner rights, which are broader than these operations; do not represent it as least privilege. This plan adds no members, roles, keys or public access. A separate narrower identity is an optional later permission change, not silently created here.
6. Pin the source object generation, Google's identifier for a specific stored object version, when downloading. Refresh bucket policy and source metadata first. Use encrypted HTTPS transfers directly to the recorded path, with no browser preview and no default Downloads copy. Verify byte size and SHA-256 before extraction. If any check differs, stop without opening the content.
7. Run scripts locally in an isolated Python environment. Install and test dependencies before restricted files are opened. Route process temporary files into the recorded run folder. Do not open patient files in an editor, spreadsheet preview, ordinary notebook or external AI tool. Disable content-bearing debug output in project scripts; catch errors without printing source rows. Do not claim that these controls eliminate all operating-system caches or forensic traces.

## First audit scope

The audit describes what exists; it does not change patient data or fit models.

1. Recheck outer and nested ZIP members before extraction. Reject absolute paths, `..`, drive/UNC paths, alternate data streams, links, Windows reserved names, case-insensitive collisions and paths escaping the resolved run root. Bound total expanded bytes to 2 GiB and nested depth to three archive levels for this first run. If the package exceeds those guards, pause and revise the plan rather than extracting anyway. Record safe package metadata, not patient-bearing content.
2. Read every sheet of the official Excel dictionary locally, including hidden sheets. Use the spreadsheet skill if applicable, but never upload the workbook or patient data to an external tool. Preserve original names, definitions, result/status codes and units. Only dictionary/schema information that passes review may be shown to the agent. Do not evaluate workbook formulas or enable external links.
3. Run `python -B -m unittest discover -s tests -v` on the existing invented-data tests. Extend read-only audit coverage and tests as needed for the actual dictionary, keeping test fixtures invented.
4. Run the existing CSV inventory with its output directed to the protected run folder. Add narrowly scoped read-only checks for complete patient/trial joins, duplicate keys, unmatched counts, field coverage and all dictionary-defined timing/outcome columns. Do not let identifiers or source records reach standard output.
5. Enumerate every laboratory test and unit by trial. Count patients with at least 2, 3 and 4 distinct timepoints. Report source-observed repetitions separately from dictionary-supported usable numeric observations. Distinguish empty, `NOT DONE`, qualified results such as inequality values, nonnumeric results and invalid/nonfinite days. Preserve them all; these audit classifications are not final cleaning decisions.
6. Establish whether actual chemotherapy administration dates, cycles, doses, reductions or delays exist. Check date-reference definitions across ASCENT2, MAINSAIL and VENICE and whether a lab can be linked to the next actual administration. Same-day dates without ordering information can be ambiguous. VISIT labels and nominal schedules do not establish actual treatment timing.
7. Audit survival, progression, response and treatment tolerance separately, documenting source fields, definitions and missingness. Inspect ENTHUSE-33 leaderboard/final-scoring availability without fitting models or using it for discovery.
8. Record encoding problems, dictionary contradictions, unsupported questions, incomplete coverage and failures. Do not infer that a field is absent merely because the current script lacks an alias for its name.

### Limits of the current inventory script

The current script is a first pass. It does not perform a complete join audit or small-group suppression; its field aliases and missing markers are fixed. Its existing repetition count uses a nonempty result, not full numeric validity, and it can infer baseline from nonpositive days. Source labels also require disclosure checks. The three passing tests do not establish that every output is safe to release. Audit extensions and privacy tests are included in this proposal; cleaning remains a separate approval stage.

## Privacy review and deliverables

Keep all initial outputs restricted. Use a strict output-field allowlist and verify trial/test/unit labels against reviewed metadata before exposing reports to chat or Git. Reject patient identifiers, individual lab result values, row samples, dates of individual events, free text, unexpected labels and content-bearing error messages. Test with invented identifier-like labels and malicious or malformed input. Do not simply print the full report to inspect whether it is safe.

For reports leaving restricted storage, propose suppressing nonzero patient groups below 10 and related totals that could reveal them by subtraction. Check overlapping reports too. This is a conservative project rule, not a claim of a PDS-prescribed threshold or a guarantee of anonymity. Retain unsuppressed diagnostics only in restricted storage.

Deliverables:

- Schema inventory: supplied files, columns, documented meanings/types and missing codes.
- Join-quality report: aggregate linkage, duplicates and unmatched records, without identifiers.
- All-lab repetition report: tests, units and patients with 2/3/4 timepoints by trial, with explicit validity definitions and disclosure controls.
- Timing and four-outcome coverage report, including actual-administration feasibility and ENTHUSE-33 limitations.
- Plain-language feasibility report: supported questions, unsupported questions, uncertainties and the proposed next cleaning decisions.
- Reproducibility manifest: exact inputs, hashes, code/dependency version and output cloud locations; no credentials or patient content.

## Upload verification and cleanup after every stage

1. Stop local processing and finish all writes. Compute size and SHA-256 for every output to preserve. Include a snapshot/hash of the exact scripts and dependency versions in the private run bundle, since the Git commit alone does not describe uncommitted audit code.
2. Upload the restricted output bundle and manifest to the new run/version prefix in the existing private bucket. Use create-only preconditions so an existing object is not overwritten. No bucket deletion, source replacement, IAM change or new service is included.
3. Verify destination, effective privacy controls, generation, byte size and cloud checksums. Re-download the newly uploaded bundle into this same protected `tmp/` directory and compare SHA-256 with the local original. Delete nothing merely because an upload command reported success. The extra verification copy is part of the recorded cleanup inventory.
4. Mark the run `uploaded_verified` only after every required output is accounted for. Upload a non-sensitive verification receipt linking the manifest and object generations. A partial upload or interrupted run remains explicitly incomplete. Preserve resumable work locally until its permitted cloud copy is verified.
5. Update the data-location register, continuity log and research log with the completed stage, exact locations and next approval gate. Publish only code, safe documentation and reviewed aggregates to GitHub when explicitly authorized. Do not describe local-only documentation as already available to another computer.
6. Present the exact run folder and any unexpected extra copies, warn that deletion bypasses the Recycle Bin and cannot guarantee forensic SSD erasure, then obtain fresh confirmation immediately before deletion. A completed stage starts this cleanup workflow even if no handoff was requested.
7. Resolve targets again, reject links and paths outside the approved run folder, remove approved targets in a single PowerShell `-LiteralPath` workflow, and freshly check that those targets are absent. Do not delete the broad restricted-work root, profile, active task workspace, credential store or unrelated files.
8. Record verified cleanup. Stop project processes and release file handles; do not shut down the user's computer. No cloud computer exists to stop. Report residual items or blockers honestly. Future agents must check the register for incomplete uploads or pending cleanup before starting another run.

The older Desktop and retired project-folder cleanup remains separate. Their local-only papers and extracted text are not backed up as required by the user's prior condition. This new restricted-dataset workflow does not authorize uploading publisher files, inventing an alternative backup or deleting those folders.

## Costs and run limits

Official Google Cloud Storage prices checked on 2026-08-31. USD list estimates before taxes, currency conversion, credits and account-specific pricing. The Netherlands storage rate was verified by region selection in the official pricing page; billing-account charges were not inspected.

| Item | Current basis | Expected first-audit effect |
|---|---|---|
| Cloud computation | None | USD 0; no VM, notebook, disk, NAT or DNS service |
| Standard storage, Netherlands | USD 0.000027397 per GiB-hour, about USD 0.020 per GiB-month | Existing ZIP about USD 0.00012/month; 100 MiB extra outputs about USD 0.002/month |
| Download to a Netherlands computer | USD 0.12 per GiB at the first general internet-transfer tier | Existing ZIP about USD 0.00070 per download; 100 MiB verification download about USD 0.01172 |
| Upload network traffic | Incoming traffic free | Object-write operations still charged |
| Regional Standard operations, flat namespace | USD 0.005 per 1,000 Class A; USD 0.0004 per 1,000 Class B | Small for a few files; metadata checks can add operations |

Plan one bounded local audit session, initially up to four hours of active work, with no unattended recurring job. Checkpoint and stop at that limit if incomplete; do not start cleaning or modeling. Expect cloud charges below USD 0.05 for this audit and the first month of its outputs, assuming at most 100 MiB of output/verification data and 1,000 operations of each class. Pause if projected incremental spending would exceed USD 0.10, the transfer/output limit is exceeded, or more resources are needed. This is an operational approval threshold, not a provider-enforced billing cap. Local electricity and internet charges are not quoted.

Cloud storage continues to be billed after local cleanup. Seven-day soft-deleted objects can also remain billable if objects are later deleted or replaced. Preserve the source and versioned outputs; no cloud cleanup or retention-policy change is proposed here.

Source: [Google Cloud Storage pricing](https://cloud.google.com/storage/pricing).

## Approval checkpoints

The user earlier approved local setup, first read-only audit and upload verification, with publication completed at 9843e5b and f152628. The latest handoff request requires the NEXT agent to explain the plan and obtain fresh approval before starting. That checkpoint remains open; the run folder, dependency installation, download, audit extensions, restricted execution and output uploads remain unperformed. Do not ask for a drive-encryption check instead of explaining the plan. The user has now explicitly authorized publication of this corrected handoff and corresponding closeout records, not execution of this data plan.

Routine steps inside the approved scope do not need repeated generic cloud-storage permission. Pause for a material change to cost, local security, identity/access, destinations or scope. Obtain later approval of cleaning transformations, then of the scientific analysis plan. Fresh exact-target local deletion confirmation remains separate at action time.

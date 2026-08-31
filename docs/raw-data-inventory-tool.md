# Safe Raw-Data Inventory Tool

## Purpose

This tool answers the first practical questions after access is approved:

- Which CSV files and columns did we receive?
- Which important fields are present or absent?
- Which blood tests repeat often enough to study change over time?
- Is there an exact chemotherapy administration date, or only a planned visit label?

It does not clean, reshape or overwrite the source files. It does not intentionally print patient identifiers or blood-test values. Its JSON output is intended to contain aggregate counts and schema information, but source-derived labels and counts still require a disclosure check before release.

## Run it

Run locally, from the repository root, only after approval of the specific local audit plan and the registered local security checks. Use explicit protected run paths, not a cloud computer or the repository's default data directory. Example for the currently proposed run, which has not been created:

```powershell
python src/audit/inventory_raw_data.py "C:\Users\BarbarosIsikGreenhou\PDS-Restricted-Work\prostate-lab-trajectories\runs\2026-08-31-audit-001\data\raw\pds_dream\extracted" --output "C:\Users\BarbarosIsikGreenhou\PDS-Restricted-Work\prostate-lab-trajectories\runs\2026-08-31-audit-001\data\interim\pds_inventory.json"
```

Both locations are outside the Git clone and are restricted until reviewed. See `local-processing-and-cloud-storage-plan.md` and `data-location-register.md` for output upload verification and local cleanup. The repository ignore rules remain defense in depth, not permission to publish a report automatically.

## What the report contains

- Table names, row counts and column names.
- Missing-value counts for every column.
- Recognized patient, trial, lab, timing, treatment and outcome fields.
- For each trial and blood test, patient counts with at least two, three and four valid measurement days.
- A clear warning if no recognized actual chemotherapy administration date is present.

## Important limit

This first-pass tool uses fixed aliases/missing markers, does not perform complete joins or small-group suppression, and its current repetition logic accepts nonempty rather than fully numeric-valid results. It can infer baseline from nonpositive study days. The approved audit must supplement these checks using the actual dictionary without silently converting them into cleaning rules. Three passing invented-data tests are not proof that every real-data report is disclosure-safe.

Finding a `VISIT` or `CYCLE` column is not proof that treatment happened on that day. Delays, skipped visits and dose changes are possible. The research can call a measurement "pre-chemotherapy" only if the received data provide a defensible link to an actual treatment administration. Otherwise, the result must be described as visit-based or calendar-based.

## Test it without restricted data

```powershell
python -m unittest discover -s tests -v
```

The tests use three invented patients. No real or restricted patient information is included in the repository.

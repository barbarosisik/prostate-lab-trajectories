# Safe Raw-Data Inventory Tool

## Purpose

This tool answers the first practical questions after access is approved:

- Which CSV files and columns did we receive?
- Which important fields are present or absent?
- Which blood tests repeat often enough to study change over time?
- Is there an exact chemotherapy administration date, or only a planned visit label?

It does not clean, reshape or overwrite the source files. It does not print patient identifiers or blood-test values. Its JSON output contains aggregate counts and schema information only.

## Run it

From the repository root:

```powershell
python src/audit/inventory_raw_data.py data/raw/pds_dream --output data/interim/pds_inventory.json
```

Both input and output locations are excluded from Git because they may be governed by the data-use agreement.

## What the report contains

- Table names, row counts and column names.
- Missing-value counts for every column.
- Recognized patient, trial, lab, timing, treatment and outcome fields.
- For each trial and blood test, patient counts with at least two, three and four valid measurement days.
- A clear warning if no recognized actual chemotherapy administration date is present.

## Important limit

Finding a `VISIT` or `CYCLE` column is not proof that treatment happened on that day. Delays, skipped visits and dose changes are possible. The research can call a measurement "pre-chemotherapy" only if the received data provide a defensible link to an actual treatment administration. Otherwise, the result must be described as visit-based or calendar-based.

## Test it without restricted data

```powershell
python -m unittest discover -s tests -v
```

The tests use three invented patients. No real or restricted patient information is included in the repository.

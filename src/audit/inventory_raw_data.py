#!/usr/bin/env python3
"""Create a privacy-safe inventory of clinical CSV files.

The tool reads source files without changing them. Its report contains table,
column, missingness, field-coverage, and repeated-laboratory counts only. It
never writes patient identifiers or laboratory result values to the report.
"""

from __future__ import annotations

import argparse
import csv
import json
import re
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable


MISSING_MARKERS = {"", ".", "NA", "N/A", "NAN", "NULL", "NONE", "MISSING"}
NOT_DONE_MARKERS = {"NOT DONE", "NOT_DONE", "ND"}

FIELD_ALIASES = {
    "study_id": ["STUDYID", "STUDY_ID", "TRIAL", "TRIAL_ID", "STUDY"],
    "patient_id": ["RPT", "GROUP_UID", "PATIENTID", "PATIENT_ID", "PATID", "PATREF"],
    "lab_test": ["LBTEST", "LBTESTCD", "TEST", "TEST_NAME", "LAB_TEST"],
    "lab_day": ["LBDT_PC", "LAB_DAY", "COLLECTION_DAY", "STUDY_DAY", "DAYS_FROM_BASELINE"],
    "lab_result": ["LBSTRESC", "LBSTRESN", "LBORRES", "RESULT", "RESULT_VALUE", "LAB_VALUE"],
    "lab_unit": ["LBSTRESU", "LBORRESU", "UNIT", "UNITS"],
    "lab_status": ["LBSTAT", "LAB_STATUS"],
    "lab_baseline": ["LBBLFL", "BASELINE_FLAG"],
    "visit": ["VISIT", "VISITNUM", "VISIT_NUMBER"],
    "actual_chemo_date": [
        "ACTUAL_CHEMO_DATE",
        "ADMINISTRATION_DATE",
        "DRUG_ADMIN_DATE",
        "TRTDT",
        "EXSTDTC",
        "DOSE_DATE",
        "TREATMENT_DATE",
    ],
    "cycle_number": ["CYCLE", "CYCLE_NUMBER", "CYCLENUM", "VISIT_CYCLE"],
    "dose": ["DOSE", "TOTAL_DOSE", "CHEMO_TOTAL_DOSE", "EXDOSE"],
    "dose_reduction": ["DOSE_REDUCED", "DOSE_REDUCTION", "REDUCED_DOSE"],
    "death_status": ["DEATH", "DEAD"],
    "survival_time": ["LKADT_P", "OS", "OVERALL_SURVIVAL"],
    "progression_status": ["CRPC", "CLINICAL_PD", "RADIOGRAPHIC_PD", "PROGRESSION"],
    "progression_time": ["TT_CRPC", "TT_CLINICAL_PD", "TIME_TO_PROGRESSION"],
    "discontinuation": ["DISCONT"],
    "treatment_end_reason": ["ENDTRS_C", "TX_NEV_STRT_REAS"],
    "treatment_end_day": ["ENTRT_PC", "ENDTRT_PC"],
}


def normalize_name(value: str) -> str:
    """Normalize a column name for exact alias matching."""
    return re.sub(r"[^a-z0-9]", "", value.casefold())


def is_missing(value: object) -> bool:
    if value is None:
        return True
    return str(value).strip().upper() in MISSING_MARKERS


def matched_fields(fieldnames: Iterable[str]) -> dict[str, str]:
    normalized_columns = {normalize_name(name): name for name in fieldnames}
    matches: dict[str, str] = {}
    for logical_field, aliases in FIELD_ALIASES.items():
        for alias in aliases:
            match = normalized_columns.get(normalize_name(alias))
            if match is not None:
                matches[logical_field] = match
                break
    return matches


def safe_percent(numerator: int, denominator: int) -> float:
    return round(100.0 * numerator / denominator, 2) if denominator else 0.0


def read_csv_rows(path: Path):
    with path.open("r", encoding="utf-8-sig", errors="replace", newline="") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames is None:
            return
        for row in reader:
            yield row


def inspect_table(path: Path, input_directory: Path) -> dict:
    with path.open("r", encoding="utf-8-sig", errors="replace", newline="") as handle:
        reader = csv.DictReader(handle)
        columns = list(reader.fieldnames or [])
        missing_counts = {column: 0 for column in columns}
        row_count = 0
        for row in reader:
            row_count += 1
            for column in columns:
                if is_missing(row.get(column)):
                    missing_counts[column] += 1

    return {
        "file": path.relative_to(input_directory).as_posix(),
        "rows": row_count,
        "column_count": len(columns),
        "columns": columns,
        "matched_fields": matched_fields(columns),
        "missingness": {
            column: {
                "count": missing_counts[column],
                "percent": safe_percent(missing_counts[column], row_count),
            }
            for column in columns
        },
    }


def parse_day(value: object) -> float | None:
    if is_missing(value):
        return None
    try:
        return float(str(value).strip())
    except ValueError:
        return None


def is_not_done(row: dict[str, str], status_column: str | None) -> bool:
    if status_column is None:
        return False
    return str(row.get(status_column, "")).strip().upper() in NOT_DONE_MARKERS


def summarize_laboratory_file(path: Path, table_summary: dict) -> list[dict]:
    fields = table_summary["matched_fields"]
    patient_column = fields.get("patient_id")
    test_column = fields.get("lab_test")
    if patient_column is None or test_column is None:
        return []

    study_column = fields.get("study_id")
    day_column = fields.get("lab_day")
    result_column = fields.get("lab_result")
    unit_column = fields.get("lab_unit")
    status_column = fields.get("lab_status")
    baseline_column = fields.get("lab_baseline")

    groups: dict[tuple[str, str], dict] = defaultdict(
        lambda: {
            "rows": 0,
            "patients": set(),
            "valid_days": defaultdict(set),
            "missing_result_rows": 0,
            "not_done_rows": 0,
            "baseline_rows": 0,
            "postbaseline_rows": 0,
            "units": set(),
        }
    )

    for row in read_csv_rows(path):
        patient = str(row.get(patient_column, "")).strip()
        test = str(row.get(test_column, "")).strip()
        if not patient or not test:
            continue
        study = str(row.get(study_column, "ALL")).strip() if study_column else "ALL"
        study = study or "MISSING"
        key = (study, test)
        group = groups[key]
        group["rows"] += 1
        group["patients"].add(patient)

        result_missing = result_column is None or is_missing(row.get(result_column))
        not_done = is_not_done(row, status_column)
        if result_missing:
            group["missing_result_rows"] += 1
        if not_done:
            group["not_done_rows"] += 1

        day = parse_day(row.get(day_column)) if day_column else None
        if day is not None and not result_missing and not not_done:
            group["valid_days"][patient].add(day)

        baseline_flag = str(row.get(baseline_column, "")).strip().upper() if baseline_column else ""
        if baseline_flag in {"Y", "YES", "1", "TRUE"} or (not baseline_flag and day is not None and day <= 0):
            group["baseline_rows"] += 1
        elif day is not None and day > 0:
            group["postbaseline_rows"] += 1

        if unit_column and not is_missing(row.get(unit_column)):
            group["units"].add(str(row.get(unit_column)).strip())

    summaries = []
    for (study, test), group in sorted(groups.items()):
        timepoint_counts = [len(days) for days in group["valid_days"].values()]
        summaries.append(
            {
                "file": table_summary["file"],
                "study": study,
                "test": test,
                "rows": group["rows"],
                "patients": len(group["patients"]),
                "patients_with_2plus_valid_timepoints": sum(count >= 2 for count in timepoint_counts),
                "patients_with_3plus_valid_timepoints": sum(count >= 3 for count in timepoint_counts),
                "patients_with_4plus_valid_timepoints": sum(count >= 4 for count in timepoint_counts),
                "missing_result_rows": group["missing_result_rows"],
                "not_done_rows": group["not_done_rows"],
                "baseline_rows": group["baseline_rows"],
                "postbaseline_rows": group["postbaseline_rows"],
                "units": sorted(group["units"]),
            }
        )
    return summaries


def build_field_coverage(tables: list[dict]) -> dict[str, dict]:
    coverage: dict[str, dict] = {}
    for logical_field in FIELD_ALIASES:
        matches = []
        for table in tables:
            column = table["matched_fields"].get(logical_field)
            if column:
                matches.append({"file": table["file"], "column": column})
        coverage[logical_field] = {
            "status": "found" if matches else "absent",
            "matches": matches,
        }
    return coverage


def inventory_directory(input_directory: Path) -> dict:
    input_directory = input_directory.resolve()
    if not input_directory.is_dir():
        raise ValueError(f"Input directory does not exist: {input_directory}")

    csv_files = sorted(path for path in input_directory.rglob("*.csv") if path.is_file())
    tables = [inspect_table(path, input_directory) for path in csv_files]
    laboratory_summaries = []
    for path, table in zip(csv_files, tables):
        laboratory_summaries.extend(summarize_laboratory_file(path, table))

    coverage = build_field_coverage(tables)
    warnings = []
    if not csv_files:
        warnings.append("No CSV files were found.")
    if coverage["actual_chemo_date"]["status"] == "absent":
        warnings.append(
            "No recognized actual chemotherapy administration date was found. "
            "Do not treat nominal visits or calendar schedules as actual administrations."
        )
    if coverage["patient_id"]["status"] == "absent":
        warnings.append("No recognized patient identifier column was found.")

    return {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "input_directory": str(input_directory),
        "privacy_notice": (
            "Aggregate inventory only. Patient identifiers and laboratory result values "
            "are read for counting but are never written to this report."
        ),
        "table_count": len(tables),
        "tables": tables,
        "field_coverage": coverage,
        "laboratory_summaries": laboratory_summaries,
        "warnings": warnings,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input_dir", type=Path, help="Directory containing source CSV files")
    parser.add_argument("--output", type=Path, help="Optional JSON report path")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        report = inventory_directory(args.input_dir)
    except ValueError as exc:
        raise SystemExit(str(exc)) from exc

    rendered = json.dumps(report, indent=2, ensure_ascii=False)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered + "\n", encoding="utf-8")
    else:
        print(rendered)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())


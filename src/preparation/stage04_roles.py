"""Give every laboratory row one explicit research purpose, with a reason.

Stages 02 and 03 established what a row's visit label says and whether its
recorded day agrees. Stage 04 answers the question those two stages leave
open: what is this row allowed to be used for, and if it is not allowed, why
not.

The distinction that matters is between excluding a row from an analysis and
deleting it. Nothing is deleted here. Every one of the 210,442 rows leaves this
stage carrying a purpose and, where it is excluded, a fixed reason code. A row
excluded from the cycle analysis remains available to a later question that
can justify using it.

Purposes are assigned by a single ordered rule set in `assign_purpose`, so two
rows in the same situation can never receive different treatment. Priority
matters: a row that cannot be placed in time is excluded before its visit role
is considered, because a measurement with no usable date cannot support a
trajectory whatever its label says.

No laboratory result is read, and no cycle label or recorded day is altered.
"""
from __future__ import annotations

import argparse
import csv
import json
from collections import Counter, defaultdict
from pathlib import Path

import stage01_roster as stage01
from stage01_roster import REGISTERED_RUN, IntegrityError, digest, records
import stage02_visits as stage02
import stage03_timing as stage03

# Research purposes. Every row receives exactly one.
BASELINE_CANDIDATE = 'baseline_candidate'        # Describes the patient before treatment.
CYCLE_MEASUREMENT = 'cycle_measurement'          # A timing-verified cycle start.
MID_CYCLE_MEASUREMENT = 'mid_cycle_measurement'  # Inside a cycle, kept apart from starts.
CONTEXT_ONLY = 'context_only'                    # Real and retained, but not a scheduled cycle point.
EXCLUDED = 'excluded'                            # Not usable for any of the above, reason recorded.

# Exclusion reasons. Fixed codes, never free text, so counts stay comparable.
NO_RECORDED_DAY = 'no_recorded_day'
ALTERNATE_TIME_ORIGIN = 'alternate_time_origin'
VISIT_MEANING_NOT_ESTABLISHED = 'visit_meaning_not_established'
CYCLE_DAY_OFF_SCHEDULE = 'cycle_day_off_schedule'
CYCLE_ORDER_VIOLATION = 'cycle_order_violation'
PRE_TREATMENT_NOT_BEFORE_FIRST_DOSE = 'pre_treatment_not_before_first_dose'

# Roles that describe a real clinical moment but not a scheduled cycle point.
# They are retained so a later question can use them on stated grounds.
CONTEXT_ROLES = (stage02.UNSCHEDULED, stage02.DISCONTINUATION, stage02.FOLLOW_UP)

OUTPUT_FIELDS = ('source_row', 'STUDYID', 'RPT', 'visit_original', 'visit_role',
                 'cycle_number', 'recorded_day', 'analysis_purpose', 'exclusion_reason')


def assign_purpose(role: str, day: str, flags: dict[str, str]) -> tuple[str, str]:
    """Return one row's (purpose, exclusion reason) from its role and flags.

    The rules are applied in a fixed order.

    First, a visit whose meaning was never established is excluded, because no
    purpose can be defended for it. Second, roles that need no date at all are
    kept as context. Third, any remaining row that has no recorded day, or that
    is measured from a different origin, is excluded, since it cannot be placed
    on the shared timeline. Only then is the row's role used to choose a
    purpose, and a cycle start must additionally have survived Stage 03's
    schedule and ordering checks.

    A pre-treatment row recorded on or after the first dose is excluded,
    because a measurement taken after treatment began cannot describe the
    patient before it, whatever the label says.
    """
    if role == stage02.UNRESOLVED:
        return EXCLUDED, VISIT_MEANING_NOT_ESTABLISHED
    if role in CONTEXT_ROLES:
        return CONTEXT_ONLY, ''
    if flags['day_missing'] == 'Y':
        return EXCLUDED, NO_RECORDED_DAY
    if flags['alternate_reference_origin'] == 'Y':
        return EXCLUDED, ALTERNATE_TIME_ORIGIN
    if role == stage02.PRE_TREATMENT:
        if flags['pre_treatment_not_before_day_zero'] == 'Y':
            return EXCLUDED, PRE_TREATMENT_NOT_BEFORE_FIRST_DOSE
        return BASELINE_CANDIDATE, ''
    if role == stage02.CYCLE_START:
        if flags['cycle_order_violation'] == 'Y':
            return EXCLUDED, CYCLE_ORDER_VIOLATION
        if flags['off_schedule'] == 'Y':
            return EXCLUDED, CYCLE_DAY_OFF_SCHEDULE
        return CYCLE_MEASUREMENT, ''
    if role == stage02.WITHIN_CYCLE:
        return MID_CYCLE_MEASUREMENT, ''
    raise IntegrityError('UNHANDLED_VISIT_ROLE')


def load_timing_flags(path: Path) -> dict[int, dict]:
    """Return the Stage 03 flag table keyed by source CSV row number.

    A repeated row number would mean one source row carries two timing
    verdicts, so it stops the stage rather than letting the last one win.
    """
    flags: dict[int, dict] = {}
    for _, row in records(path, set(stage03.OUTPUT_FIELDS)):
        line = int(row['source_row'])
        if line in flags:
            raise IntegrityError('DUPLICATE_TIMING_ROW')
        flags[line] = row
    if not flags:
        raise IntegrityError('EMPTY_TIMING_TABLE')
    return flags


def build_roles(timing: dict[int, dict]):
    """Assign a purpose to every row and summarize the outcome.

    Returns the role rows together with an aggregate report giving counts by
    purpose, by exclusion reason, and the number of distinct patients holding
    each purpose. Row counts are checked so that no row can be lost or
    duplicated between stages.
    """
    rows: list[dict] = []
    purposes = Counter()
    reasons = Counter()
    patients: dict[str, set] = defaultdict(set)
    cycle_patients: dict[tuple[str, int], set] = defaultdict(set)

    for line in sorted(timing):
        entry = timing[line]
        role = entry['visit_role']
        purpose, reason = assign_purpose(role, entry['recorded_day'], entry)
        purposes[(entry['STUDYID'], purpose)] += 1
        if reason:
            reasons[(entry['STUDYID'], reason)] += 1
        patients[purpose].add((entry['STUDYID'], entry['RPT']))
        if purpose == CYCLE_MEASUREMENT:
            cycle_patients[(entry['STUDYID'], int(entry['cycle_number']))].add(entry['RPT'])
        rows.append({'source_row': line, 'STUDYID': entry['STUDYID'], 'RPT': entry['RPT'],
                     'visit_original': entry['visit_original'], 'visit_role': role,
                     'cycle_number': entry['cycle_number'], 'recorded_day': entry['recorded_day'],
                     'analysis_purpose': purpose, 'exclusion_reason': reason})

    if len(rows) != len(timing):
        raise IntegrityError('ROW_DISPOSITION_INCOMPLETE')
    if sum(purposes.values()) != len(rows):
        raise IntegrityError('PURPOSE_COUNT_MISMATCH')

    report = {
        'stage': '04',
        'rows_read': len(rows),
        'rows_assigned_a_purpose': sum(purposes.values()),
        'rows_deleted': 0,
        'rows_by_trial_and_purpose': {f'{t}|{p}': n for (t, p), n in sorted(purposes.items())},
        'excluded_rows_by_trial_and_reason': {f'{t}|{r}': n for (t, r), n in sorted(reasons.items())},
        'patients_by_purpose': {p: len(v) for p, v in sorted(patients.items())},
        'cycle_measurement_patients_by_trial_and_cycle': {
            f'{t}|cycle_{c}': len(v) for (t, c), v in sorted(cycle_patients.items())},
        'excluded_rows_retained_in_output': True,
        'cycle_labels_or_days_altered': False,
        'laboratory_values_read_or_transformed': False,
    }
    return rows, report


def write_roles(path: Path, rows: list[dict]) -> str:
    """Exclusively create the private role table and verify its read-back.

    Uses Stage 01's write rules: mode 600, `O_EXCL`, fsync and a full
    comparison of the file as read back against the rows held in memory.
    """
    if not rows:
        raise IntegrityError('EMPTY_ROLE_TABLE')
    if tuple(rows[0]) != OUTPUT_FIELDS:
        raise IntegrityError('UNEXPECTED_OUTPUT_SCHEMA')
    return stage01.write_roster(path, rows)


def main():
    """Run Stage 04 at the registered location and print aggregate evidence.

    Re-verifies the pinned archive, loads the Stage 03 flags, assigns a purpose
    to every row, then writes the table only if every check passed. Returns 0
    on verified success or 1 with a fixed, disclosure-safe code. Never prints a
    patient key or a laboratory value.
    """
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--run-root', type=Path, default=REGISTERED_RUN)
    args = parser.parse_args()
    run = args.run_root
    try:
        if run != REGISTERED_RUN or run.resolve() != run:
            raise IntegrityError('UNREGISTERED_RUN_ROOT')
        input_hashes = stage01.verify_archive(run)
        timing_path = run / 'interim/stage03_timing_flags.csv'
        if timing_path.is_symlink() or not timing_path.is_file():
            raise IntegrityError('STAGE03_FLAGS_MISSING')
        timing = load_timing_flags(timing_path)
        rows, report = build_roles(timing)
        if any(digest(run / p) != h for p, h in input_hashes.items()):
            raise IntegrityError('SOURCE_CHANGED_DURING_RUN')
        output = run / 'interim/stage04_analysis_roles.csv'
        report['analysis_roles_sha256'] = write_roles(output, rows)
        report['stage03_flags_sha256'] = digest(timing_path)
        report['source_code_sha256'] = digest(Path(__file__))
        report['source_unchanged'] = True
        report['roles_roundtrip_verified'] = True
        print(json.dumps(report, sort_keys=True, indent=2))
    except IntegrityError as error:
        print(json.dumps({'status': 'blocked', 'error_code': str(error)}))
        return 1
    except (OSError, UnicodeError, csv.Error, ValueError):
        print(json.dumps({'status': 'blocked', 'error_code': 'IO_OR_FORMAT_ERROR'}))
        return 1
    return 0


if __name__ == '__main__':
    raise SystemExit(main())

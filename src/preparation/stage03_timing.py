"""Check Stage 02's cycle labels against each row's recorded collection day.

A visit label can be parsed perfectly and still disagree with when the blood
was actually drawn. Stage 03 tests that agreement and does nothing else. It
never rewrites a cycle number, never deletes a row and never reads a
laboratory result. Its whole output is a per-row flag table plus aggregate
evidence, so a later stage can exclude rows on stated grounds.

Two source columns carry the timing.

`LBDT_PC` is the collection day expressed as a relative day count.
`PER_REF_C` names the day that count is measured from. The data dictionary
states this is the first treatment date for most patients and the consent date
for a small number. Rows measured from a different origin sit on a different
scale and are flagged rather than silently compared.

The expected schedule in `EXPECTED_CYCLE_DAY` was derived from the data, not
assumed. The median recorded day at each cycle start is 0, 21, 42, 63 and 84
in all three trials independently, so a 21 day cycle is an observed property
of this source. It is used here only as a consistency check with an explicit
tolerance, never as a replacement for a recorded day.
"""
from __future__ import annotations

import argparse
import csv
import json
import statistics
from collections import Counter, defaultdict
from pathlib import Path

import stage01_roster as stage01
from stage01_roster import REGISTERED_RUN, IntegrityError, digest, key, records
import stage02_visits as stage02

# The reference origin the great majority of rows use. Any other origin puts a
# row on a different day scale.
PRIMARY_REFERENCE = '1ST TREATMENT'

# Observed cycle length in days, measured from this source's own medians.
CYCLE_LENGTH_DAYS = 21

# How far a recorded day may sit from its cycle's expected day before the row
# is flagged. Chosen to be wider than an ordinary dose delay and narrower than
# a whole cycle, so a genuine delay is not called an error and a mislabelled
# cycle is not called a delay.
SCHEDULE_TOLERANCE_DAYS = 10

# Flags. A row may carry several; they are recorded in separate columns so no
# information is lost by ranking one above another.
FLAG_FIELDS = ('day_missing', 'alternate_reference_origin', 'off_schedule',
               'pre_treatment_not_before_day_zero', 'cycle_order_violation')

OUTPUT_FIELDS = ('source_row', 'STUDYID', 'RPT', 'visit_original', 'visit_role',
                 'cycle_number', 'recorded_day', 'reference_origin',
                 'expected_day', 'schedule_deviation_days', *FLAG_FIELDS, 'usable_for_cycle_analysis')


def expected_day(cycle: int) -> int:
    """Return the scheduled relative day for a numbered cycle start.

    Cycle 1 starts on day 0 because the reference origin is the first
    treatment. Each later cycle adds one observed cycle length.
    """
    return (cycle - 1) * CYCLE_LENGTH_DAYS


def parse_day(value: str) -> float | None:
    """Return the recorded relative day, or None when no day was recorded.

    Empty strings and the literal `.` used by this source both mean absent.
    A value that is present but not a finite number is a data fault and stops
    the stage rather than being treated as missing, because those two cases
    call for different handling downstream.
    """
    text = value.strip()
    if text in ('', '.'):
        return None
    try:
        day = float(text)
    except ValueError:
        raise IntegrityError('NON_NUMERIC_COLLECTION_DAY') from None
    if day != day or day in (float('inf'), float('-inf')):
        raise IntegrityError('NON_NUMERIC_COLLECTION_DAY')
    return day


def classify_timing(role: str, cycle: int | None, day: float | None, reference: str,
                    tolerance: int = SCHEDULE_TOLERANCE_DAYS) -> dict:
    """Flag one row's timing without changing its cycle label.

    Reports whether the day is absent, whether the row is measured from a
    different origin, how far a cycle start sits from its scheduled day, and
    whether a pre-treatment measurement was taken before treatment began.
    The cycle ordering check is not decided here, because it needs the
    patient's other cycles; `build_timing_flags` fills it in afterwards.
    """
    flags = dict.fromkeys(FLAG_FIELDS, False)
    flags['day_missing'] = day is None
    flags['alternate_reference_origin'] = reference != PRIMARY_REFERENCE
    deviation = None
    comparable = day is not None and reference == PRIMARY_REFERENCE
    if comparable and role == stage02.CYCLE_START:
        deviation = day - expected_day(cycle)
        flags['off_schedule'] = abs(deviation) > tolerance
    if comparable and role == stage02.PRE_TREATMENT:
        # The origin is the first treatment day, so a measurement described as
        # pre-treatment should not be recorded on or after that day.
        flags['pre_treatment_not_before_day_zero'] = day >= 0
    return {'flags': flags, 'schedule_deviation_days': deviation, 'comparable': comparable}


def cycle_order_violations(cycle_days: dict[tuple[str, str], dict[int, list[float]]]) -> set[tuple[str, str, int]]:
    """Return the (trial, patient, cycle) groups whose day breaks cycle order.

    Cycles are administered in sequence, so a patient's cycle N must not be
    collected on or after the day of cycle N+1. This check needs no schedule
    assumption at all, which makes it the strongest evidence available that a
    label and a date genuinely disagree. The later cycle of the offending pair
    is flagged, since the earlier one is corroborated by the cycles before it.
    """
    violations = set()
    for (trial, patient), by_cycle in cycle_days.items():
        ordered = sorted(by_cycle)
        for earlier, later in zip(ordered, ordered[1:]):
            if statistics.median(by_cycle[later]) <= statistics.median(by_cycle[earlier]):
                violations.add((trial, patient, later))
    return violations


def build_timing_flags(extracted: Path, visit_index: dict[int, dict],
                       tolerance: int = SCHEDULE_TOLERANCE_DAYS):
    """Flag the timing of every laboratory row and summarize the result.

    Joins each source row to its Stage 02 classification by row number, checks
    its recorded day, then applies the per-patient cycle ordering check in a
    second pass. Returns the flag rows and an aggregate report. No laboratory
    result is read and no cycle label is altered.
    """
    rows: list[dict] = []
    cycle_days: dict[tuple[str, str], dict[int, list[float]]] = defaultdict(lambda: defaultdict(list))
    visit_days: dict[tuple[str, str, str], set[float]] = defaultdict(set)
    references = Counter()
    deviations: dict[tuple[str, int], list[float]] = defaultdict(list)
    max_day = None

    required = {'STUDYID', 'RPT', 'VISIT', 'LBDT_PC', 'PER_REF_C'}
    for line, row in records(extracted / 'training/LabValue_training.csv', required):
        entry = visit_index.get(line)
        if entry is None:
            raise IntegrityError('VISIT_INDEX_ROW_MISSING')
        patient = key(row)
        if (entry['STUDYID'], entry['RPT']) != patient or entry['visit_original'] != row['VISIT']:
            raise IntegrityError('VISIT_INDEX_ROW_MISALIGNED')
        role = entry['visit_role']
        cycle = int(entry['cycle_number']) if entry['cycle_number'] != '' else None
        day = parse_day(row['LBDT_PC'])
        reference = row['PER_REF_C']
        references[(patient[0], reference)] += 1
        verdict = classify_timing(role, cycle, day, reference, tolerance)
        if verdict['comparable']:
            max_day = day if max_day is None else max(max_day, day)
            visit_days[(patient[0], patient[1], row['VISIT'])].add(day)
            if role == stage02.CYCLE_START:
                cycle_days[patient][cycle].append(day)
                deviations[(patient[0], cycle)].append(verdict['schedule_deviation_days'])
        rows.append({'source_row': line, 'STUDYID': patient[0], 'RPT': patient[1],
                     'visit_original': row['VISIT'], 'visit_role': role,
                     'cycle_number': '' if cycle is None else cycle,
                     'recorded_day': '' if day is None else day,
                     'reference_origin': reference,
                     'expected_day': expected_day(cycle) if role == stage02.CYCLE_START else '',
                     'schedule_deviation_days': '' if verdict['schedule_deviation_days'] is None
                                                else verdict['schedule_deviation_days'],
                     **{f: 'Y' if v else 'N' for f, v in verdict['flags'].items()},
                     'usable_for_cycle_analysis': ''})

    violations = cycle_order_violations(cycle_days)
    flagged = 0
    for entry in rows:
        if entry['visit_role'] == stage02.CYCLE_START and entry['cycle_number'] != '':
            if (entry['STUDYID'], entry['RPT'], entry['cycle_number']) in violations:
                entry['cycle_order_violation'] = 'Y'
                flagged += 1
        # A cycle row is usable only if it is on the primary scale, has a day,
        # and neither the schedule check nor the ordering check objected.
        usable = (entry['visit_role'] == stage02.CYCLE_START
                  and entry['day_missing'] == 'N'
                  and entry['alternate_reference_origin'] == 'N'
                  and entry['off_schedule'] == 'N'
                  and entry['cycle_order_violation'] == 'N')
        entry['usable_for_cycle_analysis'] = 'Y' if usable else 'N'

    if len(rows) != len(visit_index):
        raise IntegrityError('ROW_DISPOSITION_INCOMPLETE')

    counts = Counter()
    for entry in rows:
        for field in FLAG_FIELDS:
            counts[field] += entry[field] == 'Y'
    cycle_rows = [e for e in rows if e['visit_role'] == stage02.CYCLE_START]
    report = {
        'stage': '03',
        'rows_read': len(rows),
        'rows_assigned_a_disposition': len(rows),
        'rows_dropped': 0,
        'rows_relabelled': 0,
        'cycle_length_days_observed': CYCLE_LENGTH_DAYS,
        'schedule_tolerance_days': tolerance,
        'reference_origin_counts': {f'{t}|{r}': n for (t, r), n in sorted(references.items())},
        'flag_counts': dict(sorted(counts.items())),
        'cycle_start_rows': len(cycle_rows),
        'cycle_start_rows_usable': sum(e['usable_for_cycle_analysis'] == 'Y' for e in cycle_rows),
        'cycle_order_violation_groups': len(violations),
        'median_deviation_by_trial_and_cycle': {
            f'{t}|cycle_{c}': statistics.median(v) for (t, c), v in sorted(deviations.items())},
        'patient_visits_spanning_more_than_one_day': sum(1 for v in visit_days.values() if len(v) > 1),
        'patient_visits_checked': len(visit_days),
        'max_comparable_recorded_day': max_day,
        'cycle_labels_altered': False,
        'laboratory_values_read_or_transformed': False,
    }
    return rows, report


def load_visit_index(path: Path) -> dict[int, dict]:
    """Return the Stage 02 visit index keyed by source CSV row number.

    A duplicated row number would mean two classifications for one source row,
    so it stops the stage rather than letting the later one win.
    """
    index: dict[int, dict] = {}
    for _, row in records(path, set(stage02.OUTPUT_FIELDS)):
        line = int(row['source_row'])
        if line in index:
            raise IntegrityError('DUPLICATE_VISIT_INDEX_ROW')
        index[line] = row
    if not index:
        raise IntegrityError('EMPTY_VISIT_INDEX')
    return index


def write_flags(path: Path, rows: list[dict]) -> str:
    """Exclusively create the private timing flag table and verify read-back.

    Uses Stage 01's write rules: mode 600, `O_EXCL`, fsync, and a full
    comparison of the file as read back against the rows in memory.
    """
    if not rows:
        raise IntegrityError('EMPTY_TIMING_TABLE')
    if tuple(rows[0]) != OUTPUT_FIELDS:
        raise IntegrityError('UNEXPECTED_OUTPUT_SCHEMA')
    return stage01.write_roster(path, rows)


def main():
    """Run Stage 03 at the registered location and print aggregate evidence.

    Re-verifies the pinned archive, loads the Stage 02 index, flags timing for
    every row, then writes the table only if every check passed. Returns 0 on
    verified success or 1 with a fixed, disclosure-safe code. Never prints a
    patient key or a laboratory value.
    """
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--run-root', type=Path, default=REGISTERED_RUN)
    parser.add_argument('--tolerance-days', type=int, default=SCHEDULE_TOLERANCE_DAYS)
    args = parser.parse_args()
    run = args.run_root
    try:
        if run != REGISTERED_RUN or run.resolve() != run:
            raise IntegrityError('UNREGISTERED_RUN_ROOT')
        input_hashes = stage01.verify_archive(run)
        index_path = run / 'interim/stage02_visit_index.csv'
        if index_path.is_symlink() or not index_path.is_file():
            raise IntegrityError('STAGE02_INDEX_MISSING')
        visit_index = load_visit_index(index_path)
        rows, report = build_timing_flags(run / 'extracted', visit_index, args.tolerance_days)
        if any(digest(run / p) != h for p, h in input_hashes.items()):
            raise IntegrityError('SOURCE_CHANGED_DURING_RUN')
        output = run / 'interim/stage03_timing_flags.csv'
        report['timing_flags_sha256'] = write_flags(output, rows)
        report['stage02_index_sha256'] = digest(index_path)
        report['source_code_sha256'] = digest(Path(__file__))
        report['source_unchanged'] = True
        report['flags_roundtrip_verified'] = True
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

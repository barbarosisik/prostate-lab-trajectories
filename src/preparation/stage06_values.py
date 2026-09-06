"""Separate real measurements from absent results, bounds, text and duplicates.

Stage 05 established which column holds the measurement and what unit it is
in. Stage 06 turns those raw entries into an analysis value, or records why no
analysis value exists. It is the first stage that writes laboratory results,
so its output is a restricted patient-level file.

Two problems are settled here.

The first is that an entry that looks like a number may not be one. An empty
cell, the text `NOT DONE`, and a result reported as `<0.1` because the
instrument could not measure lower are three different statements, and none of
them is the number zero. Each keeps its own kind, and only an ordinary number
becomes an analysis value. A bound is retained as a bound, with its direction
and its limit stored separately, so a later stage can decide what to do with it
on stated grounds rather than inheriting a guess made here.

The second is that one patient can have several rows for the same test at the
same visit, in 4.3 per cent of cases. Those fall into three situations that
must not be treated alike. Rows recorded on the same day with the same value
are duplicate records, so one is kept and the rest are marked as duplicates.
Rows recorded on different days are genuine repeat draws, so the draw closest
to what that visit is meant to represent is selected and the others are
retained but not selected. Rows recorded on the same day with different values
cannot be separated by timing at all, so none is selected and the conflict is
recorded.

Nothing is deleted, no value is edited, and no unit is converted.
"""
from __future__ import annotations

import argparse
import csv
import json
from collections import Counter, defaultdict
from pathlib import Path

import stage01_roster as stage01
from stage01_roster import REGISTERED_RUN, IntegrityError, digest, key, records
import stage03_timing as stage03
import stage04_roles as stage04
import stage05_tests_units as stage05

# What each visit's measurement is meant to represent, as a day on the shared
# timeline. A repeat draw is judged by how close it sits to this day.
BASELINE_TARGET_DAY = 0     # The description of the patient closest to the first dose.

# Repeat outcomes. Every row in a repeated group receives exactly one.
SINGLE = 'single'                              # The only row for this test at this visit.
DUPLICATE_KEPT = 'duplicate_kept'              # One of several identical records; this one is used.
DUPLICATE_NOT_USED = 'duplicate_not_used'      # An identical record already represented.
REPEAT_SELECTED = 'repeat_selected'            # A genuine repeat draw, chosen for this visit.
REPEAT_NOT_SELECTED = 'repeat_not_selected'    # A genuine repeat draw, retained but not chosen.
CONFLICT_UNRESOLVED = 'conflict_unresolved'    # Same day, different values, no basis to choose.

# Purposes that need an analysis value. Context rows are retained without one.
VALUED_PURPOSES = (stage04.CYCLE_MEASUREMENT, stage04.BASELINE_CANDIDATE,
                   stage04.MID_CYCLE_MEASUREMENT)

OUTPUT_FIELDS = ('source_row', 'STUDYID', 'RPT', 'test_code', 'test_unit',
                 'visit_original', 'analysis_purpose', 'cycle_number', 'recorded_day',
                 'value_kind', 'analysis_value', 'bound_direction', 'bound_value',
                 'repeat_status', 'usable_measurement')


def target_day(purpose: str, cycle: str, recorded_day: str) -> float | None:
    """Return the day a visit's measurement is meant to describe.

    A cycle measurement should describe the start of its cycle, so its target
    is that cycle's scheduled day. A baseline candidate should describe the
    patient immediately before treatment, so its target is the first treatment
    day itself and the latest pre-treatment draw wins. A mid-cycle measurement
    is judged against its own recorded day, since the label already states the
    day it is meant to fall on. Returns None when no target applies.
    """
    if purpose == stage04.CYCLE_MEASUREMENT and cycle != '':
        return float(stage03.expected_day(int(cycle)))
    if purpose == stage04.BASELINE_CANDIDATE:
        return float(BASELINE_TARGET_DAY)
    if purpose == stage04.MID_CYCLE_MEASUREMENT:
        return float(recorded_day) if recorded_day != '' else None
    return None


def read_value(text: str) -> tuple[str, str, str, str]:
    """Return (kind, analysis value, bound direction, bound value) for one entry.

    An ordinary number becomes an analysis value. A bounded result keeps its
    direction and limit but yields no analysis value, because the laboratory
    did not report where inside the bound the true value lies. Absent and
    uninterpretable entries yield nothing at all. None of these ever becomes a
    zero.
    """
    kind = stage05.classify_result(text)
    if kind == 'numeric':
        return kind, str(stage05.parse_decimal(text)), '', ''
    if kind == 'bounded':
        stripped = text.strip()
        limit = stage05.parse_decimal(stripped[1:])
        if limit is None:
            return 'non_numeric_text', '', '', ''
        return kind, '', stripped[0], str(limit)
    return kind, '', '', ''


def resolve_repeats(rows: list[dict]) -> None:
    """Assign a repeat status in place to every row for one test at one visit.

    Rows are the entries sharing a patient, a test and a visit. Only ordinary
    numbers can be selected. Identical records recorded on the same day are
    duplicates, so the first is kept. Draws on different days are genuine
    repeats and the one closest to the visit's target day wins, with the
    earlier draw breaking a tie. Draws on the same day with different values
    leave the whole group unresolved, because no evidence here can choose
    between them.
    """
    if len(rows) == 1:
        rows[0]['repeat_status'] = SINGLE
        return
    for row in rows:
        row['repeat_status'] = REPEAT_NOT_SELECTED

    candidates = [r for r in rows if r['value_kind'] == 'numeric' and r['recorded_day'] != '']
    if not candidates:
        return
    if len(candidates) == 1:
        # The siblings carried no usable number, so this row is the one that
        # represents the visit. It is a selection, not a duplicate.
        candidates[0]['repeat_status'] = REPEAT_SELECTED
        return

    if len({(r['recorded_day'], r['analysis_value']) for r in candidates}) == 1:
        for row in candidates:
            row['repeat_status'] = DUPLICATE_NOT_USED
        candidates[0]['repeat_status'] = DUPLICATE_KEPT
        return

    by_day = defaultdict(set)
    for row in candidates:
        by_day[row['recorded_day']].add(row['analysis_value'])
    if any(len(values) > 1 for values in by_day.values()):
        for row in candidates:
            row['repeat_status'] = CONFLICT_UNRESOLVED
        return

    target = candidates[0]['target_day']
    if target is None:
        chosen = min(candidates, key=lambda r: (float(r['recorded_day']), r['source_row']))
    else:
        chosen = min(candidates, key=lambda r: (abs(float(r['recorded_day']) - target),
                                                float(r['recorded_day']), r['source_row']))
    chosen['repeat_status'] = REPEAT_SELECTED


def build_values(extracted: Path, roles: dict[int, dict]):
    """Read every laboratory row, classify its value and settle repeats.

    Joins each source row to its Stage 04 purpose by row number, reads the
    authoritative value column, groups rows by patient, test and visit, then
    applies the repeat rules. Returns the value rows and an aggregate report.
    """
    rows: list[dict] = []
    groups: dict[tuple, list[dict]] = defaultdict(list)
    kinds = Counter()

    required = {'STUDYID', 'RPT', 'VISIT', 'LBTESTCD', 'LBTEST', 'LBSTRESU',
                stage05.AUTHORITATIVE_VALUE_COLUMN}
    for line, row in records(extracted / 'training/LabValue_training.csv', required):
        entry = roles.get(line)
        if entry is None:
            raise IntegrityError('ROLE_ROW_MISSING')
        patient = key(row)
        if (entry['STUDYID'], entry['RPT']) != patient or entry['visit_original'] != row['VISIT']:
            raise IntegrityError('ROLE_ROW_MISALIGNED')
        code = stage05.resolve_test_code(row['LBTESTCD'].strip(), row['LBTEST'])
        kind, value, direction, bound = read_value(row[stage05.AUTHORITATIVE_VALUE_COLUMN])
        kinds[kind] += 1
        record = {'source_row': line, 'STUDYID': patient[0], 'RPT': patient[1],
                  'test_code': code, 'test_unit': row['LBSTRESU'].strip(),
                  'visit_original': row['VISIT'], 'analysis_purpose': entry['analysis_purpose'],
                  'cycle_number': entry['cycle_number'], 'recorded_day': entry['recorded_day'],
                  'value_kind': kind, 'analysis_value': value,
                  'bound_direction': direction, 'bound_value': bound,
                  'repeat_status': '', 'usable_measurement': ''}
        record['target_day'] = target_day(entry['analysis_purpose'], entry['cycle_number'],
                                          entry['recorded_day'])
        rows.append(record)
        groups[(patient[0], patient[1], code, row['VISIT'])].append(record)

    for group in groups.values():
        resolve_repeats(group)

    statuses = Counter()
    usable_by = Counter()
    patients_by_cycle: dict[tuple[str, str, int], set] = defaultdict(set)
    for record in rows:
        del record['target_day']
        status = record['repeat_status']
        statuses[status] += 1
        usable = (record['value_kind'] == 'numeric'
                  and record['analysis_purpose'] in VALUED_PURPOSES
                  and status in (SINGLE, DUPLICATE_KEPT, REPEAT_SELECTED))
        record['usable_measurement'] = 'Y' if usable else 'N'
        if usable:
            usable_by[(record['STUDYID'], record['analysis_purpose'])] += 1
            if record['analysis_purpose'] == stage04.CYCLE_MEASUREMENT:
                patients_by_cycle[(record['STUDYID'], record['test_code'],
                                   int(record['cycle_number']))].add(record['RPT'])

    if len(rows) != len(roles):
        raise IntegrityError('ROW_DISPOSITION_INCOMPLETE')
    if any(not r['repeat_status'] for r in rows):
        raise IntegrityError('REPEAT_STATUS_INCOMPLETE')

    panel = ('ALP', 'ALT', 'AST', 'CA', 'CREAT', 'HB', 'LDH', 'NEU', 'PLT', 'PSA',
             'TBILI', 'WBC', 'SODIUM')
    report = {
        'stage': '06',
        'rows_read': len(rows),
        'rows_deleted': 0,
        'values_edited': 0,
        'units_converted': 0,
        'value_kind_counts': dict(sorted(kinds.items())),
        'repeat_status_counts': dict(sorted(statuses.items())),
        'patient_test_visit_groups': len(groups),
        'groups_with_repeats': sum(1 for g in groups.values() if len(g) > 1),
        'usable_measurements_by_trial_and_purpose': {
            f'{t}|{p}': n for (t, p), n in sorted(usable_by.items())},
        'usable_measurements_total': sum(usable_by.values()),
        'panel_patients_by_test_and_cycle': {
            f'{code}|cycle_{c}': len(set().union(*[patients_by_cycle[(t, code, c)]
                                                   for t in ('CELGENE', 'EFC6546', 'ASCENT2')]))
            for code in panel for c in (1, 2, 3, 4)},
        'bounds_retained_not_converted_to_numbers': kinds['bounded'],
        'absent_entries_never_treated_as_zero': kinds['absent'],
    }
    return rows, report


def load_roles(path: Path) -> dict[int, dict]:
    """Return the Stage 04 role table keyed by source CSV row number.

    A repeated row number would mean one source row carries two purposes, so
    it stops the stage rather than letting the last one win.
    """
    roles: dict[int, dict] = {}
    for _, row in records(path, set(stage04.OUTPUT_FIELDS)):
        line = int(row['source_row'])
        if line in roles:
            raise IntegrityError('DUPLICATE_ROLE_ROW')
        roles[line] = row
    if not roles:
        raise IntegrityError('EMPTY_ROLE_TABLE')
    return roles


def write_values(path: Path, rows: list[dict]) -> str:
    """Exclusively create the private value table and verify its read-back.

    This file holds patient measurements, so it stays under the registered
    restricted run root and is written mode 600 with `O_EXCL`, an fsync and a
    full read-back comparison, exactly as every other output.
    """
    if not rows:
        raise IntegrityError('EMPTY_VALUE_TABLE')
    if tuple(rows[0]) != OUTPUT_FIELDS:
        raise IntegrityError('UNEXPECTED_OUTPUT_SCHEMA')
    return stage01.write_roster(path, rows)


def main():
    """Run Stage 06 at the registered location and print aggregate evidence.

    Re-verifies the pinned archive, loads the Stage 04 roles, classifies every
    value, settles repeats, then writes the table only if every check passed.
    Returns 0 on verified success or 1 with a fixed, disclosure-safe code.
    Never prints a patient key or an individual laboratory value.
    """
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--run-root', type=Path, default=REGISTERED_RUN)
    args = parser.parse_args()
    run = args.run_root
    try:
        if run != REGISTERED_RUN or run.resolve() != run:
            raise IntegrityError('UNREGISTERED_RUN_ROOT')
        input_hashes = stage01.verify_archive(run)
        roles_path = run / 'interim/stage04_analysis_roles.csv'
        if roles_path.is_symlink() or not roles_path.is_file():
            raise IntegrityError('STAGE04_ROLES_MISSING')
        roles = load_roles(roles_path)
        rows, report = build_values(run / 'extracted', roles)
        if any(digest(run / p) != h for p, h in input_hashes.items()):
            raise IntegrityError('SOURCE_CHANGED_DURING_RUN')
        output = run / 'interim/stage06_measurements.csv'
        report['measurements_sha256'] = write_values(output, rows)
        report['stage04_roles_sha256'] = digest(roles_path)
        report['source_code_sha256'] = digest(Path(__file__))
        report['source_unchanged'] = True
        report['values_roundtrip_verified'] = True
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

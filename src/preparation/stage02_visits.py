"""Translate the three DREAM visit vocabularies into one cycle structure.

Stage 02 answers a single question for every laboratory row: which treatment
cycle, if any, does this row's visit label describe, and what kind of visit is
it. It does not read, convert or judge any laboratory result, and it does not
use recorded dates. Checking the labels against the recorded relative day
`LBDT_PC` is Stage 03's job, deliberately kept separate so that a label error
and a timing error cannot hide each other.

The translation is an exhaustive lookup table, not a pattern guess. The three
training trials use 29 distinct visit labels in total, all enumerated in
`VISIT_MAP` below. Any label outside that table stops the stage with
`UNKNOWN_VISIT_LABEL` rather than being silently parsed, so a changed or
extended source cannot pass through unnoticed.

The output is a visit index keyed by source CSV row number. It deliberately
carries no laboratory value, unit or result column, so this stage adds no new
copy of any patient measurement to disk. Errors carry fixed codes and never
contain source rows, patient identifiers or results.
"""
from __future__ import annotations

import argparse
import csv
import json
from collections import Counter
from pathlib import Path

import stage01_roster as stage01
from stage01_roster import REGISTERED_RUN, IntegrityError, digest, key, records

# Visit roles. A role records what kind of clinical moment a label describes,
# so later stages can include or exclude a row on stated grounds instead of on
# the shape of its text.
PRE_TREATMENT = 'pre_treatment'          # Before cycle 1; a baseline candidate.
CYCLE_START = 'cycle_start'              # The measurement opening a numbered cycle.
WITHIN_CYCLE = 'within_cycle'            # A measurement inside a cycle, not at its start.
UNSCHEDULED = 'unscheduled'              # Taken outside the planned schedule.
DISCONTINUATION = 'discontinuation'      # Taken around treatment stopping.
FOLLOW_UP = 'follow_up'                  # After the treatment phase.
UNRESOLVED = 'unresolved_label'          # Meaning not established from the label alone.

# The complete observed vocabulary, as (trial, original label) ->
# (cycle number, day within cycle, day stated by the label, role).
# `None` for the cycle number means the label names no numbered cycle.
# `None` for the day means the label does not state a day; it does not mean
# day zero, and Stage 03 must not treat it as a measured time.
VISIT_MAP: dict[tuple[str, str], tuple[int | None, int | None, bool, str]] = {
    # ASCENT2 writes a zero-padded cycle number and states no day.
    ('ASCENT2', 'PRE-ENROLLMENT'): (None, None, False, PRE_TREATMENT),
    **{('ASCENT2', f'CYCLE #{n:02d}'): (n, None, False, CYCLE_START) for n in range(1, 11)},

    # CELGENE states the day explicitly, which makes CYCLE 1 DAY 14 a
    # mid-cycle measurement that must never be pooled with a cycle start.
    ('CELGENE', 'SCREENING'): (None, None, False, PRE_TREATMENT),
    ('CELGENE', 'CYCLE 1 DAY 1'): (1, 1, True, CYCLE_START),
    ('CELGENE', 'CYCLE 1 DAY 14'): (1, 14, True, WITHIN_CYCLE),
    ('CELGENE', 'CYCLE 2 DAY 1'): (2, 1, True, CYCLE_START),
    ('CELGENE', 'CYCLE 3 DAY 1'): (3, 1, True, CYCLE_START),
    ('CELGENE', 'CYCLE 4 DAY 1'): (4, 1, True, CYCLE_START),
    ('CELGENE', 'CYCLE 5 DAY 1'): (5, 1, True, CYCLE_START),
    ('CELGENE', 'UNSCHEDULED'): (None, None, False, UNSCHEDULED),
    ('CELGENE', 'TX PHASE DISCONTINUATION'): (None, None, False, DISCONTINUATION),

    # EFC6546 names the cycle but never the day, so its cycle starts are
    # assumed rather than stated. Stage 03 tests that assumption.
    ('EFC6546', 'SCREENING'): (None, None, False, PRE_TREATMENT),
    **{('EFC6546', f'CYCLE {n}'): (n, None, False, CYCLE_START) for n in range(1, 6)},
    ('EFC6546', 'FOLLOW-UP 0 (30 DAYS)'): (None, None, False, FOLLOW_UP),
    ('EFC6546', 'FOLLOW-UP 1'): (None, None, False, FOLLOW_UP),
    # A bare visit number establishes no cycle and no timing. It is carried
    # through as unresolved instead of being guessed at or discarded.
    ('EFC6546', 'VISIT 99'): (None, None, False, UNRESOLVED),
}

# Row counts measured on the pinned training source. A mismatch means the input
# is not the audited file, so the stage stops instead of producing an index that
# silently describes different data.
EXPECTED_VISIT_ROWS: dict[tuple[str, str], int] = {
    ('ASCENT2', 'PRE-ENROLLMENT'): 7605, ('ASCENT2', 'CYCLE #01'): 463,
    ('ASCENT2', 'CYCLE #02'): 426, ('ASCENT2', 'CYCLE #03'): 392,
    ('ASCENT2', 'CYCLE #04'): 351, ('ASCENT2', 'CYCLE #05'): 227,
    ('ASCENT2', 'CYCLE #06'): 5, ('ASCENT2', 'CYCLE #07'): 9,
    ('ASCENT2', 'CYCLE #08'): 4, ('ASCENT2', 'CYCLE #09'): 3,
    ('ASCENT2', 'CYCLE #10'): 2,
    ('CELGENE', 'SCREENING'): 21366, ('CELGENE', 'CYCLE 1 DAY 1'): 16079,
    ('CELGENE', 'CYCLE 1 DAY 14'): 15341, ('CELGENE', 'CYCLE 2 DAY 1'): 18615,
    ('CELGENE', 'CYCLE 3 DAY 1'): 18365, ('CELGENE', 'CYCLE 4 DAY 1'): 17196,
    ('CELGENE', 'CYCLE 5 DAY 1'): 10821, ('CELGENE', 'UNSCHEDULED'): 4148,
    ('CELGENE', 'TX PHASE DISCONTINUATION'): 1820,
    ('EFC6546', 'SCREENING'): 16969, ('EFC6546', 'CYCLE 1'): 6443,
    ('EFC6546', 'CYCLE 2'): 16126, ('EFC6546', 'CYCLE 3'): 15655,
    ('EFC6546', 'CYCLE 4'): 14428, ('EFC6546', 'CYCLE 5'): 6187,
    ('EFC6546', 'FOLLOW-UP 0 (30 DAYS)'): 1119, ('EFC6546', 'FOLLOW-UP 1'): 48,
    ('EFC6546', 'VISIT 99'): 229,
}

OUTPUT_FIELDS = ('source_row', 'STUDYID', 'RPT', 'visit_original', 'cycle_number',
                 'cycle_day', 'day_stated_by_label', 'visit_role')


def classify_visit(studyid: str, visit: str) -> tuple[int | None, int | None, bool, str]:
    """Return the standardized cycle fields for one trial's visit label.

    Look the exact (trial, label) pair up in `VISIT_MAP`. Nothing is stripped,
    upper-cased or pattern-matched, because a label that differs by so much as
    a space is a label this stage has not been shown and must not interpret.
    Raise `UNKNOWN_VISIT_LABEL` for any pair outside the table.
    """
    try:
        return VISIT_MAP[(studyid, visit)]
    except KeyError:
        raise IntegrityError('UNKNOWN_VISIT_LABEL') from None


def load_roster_keys(roster_path: Path) -> set[tuple[str, str]]:
    """Return the (trial, patient) keys frozen by Stage 01.

    Stage 02 attaches cycle structure only to patients Stage 01 already
    accepted, so that a row cannot acquire a cycle label while belonging to
    nobody in the research roster.
    """
    keys = set()
    for _, row in records(roster_path, {'STUDYID', 'RPT'}):
        keys.add(key(row))
    if not keys:
        raise IntegrityError('EMPTY_ROSTER')
    return keys


def build_visit_index(extracted: Path, roster_keys: set[tuple[str, str]],
                      expected_rows: dict[tuple[str, str], int] | None = None):
    """Translate every laboratory row's visit label and count the outcome.

    Every input row receives exactly one disposition, so no row can be lost
    silently. Returns the index rows together with an aggregate report holding
    per-trial and per-role counts, the observed cycle range, and the labels
    whose day is assumed rather than stated. No laboratory value is read.
    """
    expected = EXPECTED_VISIT_ROWS if expected_rows is None else expected_rows
    index: list[dict] = []
    observed = Counter()
    roles = Counter()
    cycles = Counter()
    patients_by_cycle: dict[tuple[str, int], set] = {}
    day_assumed = Counter()

    required = {'STUDYID', 'RPT', 'VISIT'}
    for line, row in records(extracted / 'training/LabValue_training.csv', required):
        patient = key(row)
        if patient not in roster_keys:
            raise IntegrityError('LAB_ROW_OUTSIDE_STAGE01_ROSTER')
        visit = row['VISIT']
        cycle, day, day_stated, role = classify_visit(patient[0], visit)
        observed[(patient[0], visit)] += 1
        roles[(patient[0], role)] += 1
        if role == CYCLE_START:
            cycles[(patient[0], cycle)] += 1
            patients_by_cycle.setdefault((patient[0], cycle), set()).add(patient[1])
            if not day_stated:
                day_assumed[patient[0]] += 1
        index.append({'source_row': line, 'STUDYID': patient[0], 'RPT': patient[1],
                      'visit_original': visit, 'cycle_number': '' if cycle is None else cycle,
                      'cycle_day': '' if day is None else day,
                      'day_stated_by_label': 'Y' if day_stated else 'N',
                      'visit_role': role})

    if dict(observed) != expected:
        raise IntegrityError('VISIT_LABEL_COUNT_MISMATCH')
    if len(index) != sum(expected.values()):
        raise IntegrityError('ROW_DISPOSITION_INCOMPLETE')

    report = {
        'stage': '02',
        'rows_read': len(index),
        'rows_assigned_a_disposition': len(index),
        'rows_dropped': 0,
        'distinct_visit_labels': {trial: sum(1 for t, _ in expected if t == trial)
                                  for trial in sorted({t for t, _ in expected})},
        'rows_by_trial_and_role': {f'{t}|{r}': n for (t, r), n in sorted(roles.items())},
        'cycle_start_rows_by_trial_and_cycle': {f'{t}|cycle_{c}': n for (t, c), n in sorted(cycles.items())},
        'cycle_start_patients_by_trial_and_cycle': {f'{t}|cycle_{c}': len(p)
                                                    for (t, c), p in sorted(patients_by_cycle.items())},
        'cycle_start_rows_with_day_assumed_not_stated': dict(sorted(day_assumed.items())),
        'original_visit_text_preserved': True,
        'timing_checked_against_recorded_day': False,
        'laboratory_values_read_or_transformed': False,
    }
    return index, report


def write_index(path: Path, index: list[dict]) -> str:
    """Exclusively create the private visit index and verify its read-back.

    Reuses Stage 01's write rules: mode 600, `O_EXCL` so no earlier output or
    symlink is overwritten, an fsync, and a full read-back comparison before
    the file is trusted. Returns the verified output's SHA-256.
    """
    if not index:
        raise IntegrityError('EMPTY_VISIT_INDEX')
    if tuple(index[0]) != OUTPUT_FIELDS:
        raise IntegrityError('UNEXPECTED_OUTPUT_SCHEMA')
    return stage01.write_roster(path, index)


def main():
    """Run Stage 02 at the registered location and print aggregate evidence.

    Re-verify the pinned archive, load the Stage 01 roster, translate every
    visit label, then write the index only if every check passed. Returns 0 on
    verified success or 1 with a fixed, disclosure-safe code. Never prints a
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
        roster_path = run / 'interim/stage01_training_roster.csv'
        if roster_path.is_symlink() or not roster_path.is_file():
            raise IntegrityError('STAGE01_ROSTER_MISSING')
        roster_keys = load_roster_keys(roster_path)
        index, report = build_visit_index(run / 'extracted', roster_keys)
        if any(digest(run / p) != h for p, h in input_hashes.items()):
            raise IntegrityError('SOURCE_CHANGED_DURING_RUN')
        output = run / 'interim/stage02_visit_index.csv'
        report['visit_index_sha256'] = write_index(output, index)
        report['stage01_roster_sha256'] = digest(roster_path)
        report['roster_patients'] = len(roster_keys)
        report['source_code_sha256'] = digest(Path(__file__))
        report['source_unchanged'] = True
        report['index_roundtrip_verified'] = True
        print(json.dumps(report, sort_keys=True, indent=2))
    except IntegrityError as error:
        print(json.dumps({'status': 'blocked', 'error_code': str(error)}))
        return 1
    except (OSError, UnicodeError, csv.Error):
        print(json.dumps({'status': 'blocked', 'error_code': 'IO_OR_FORMAT_ERROR'}))
        return 1
    return 0


if __name__ == '__main__':
    raise SystemExit(main())

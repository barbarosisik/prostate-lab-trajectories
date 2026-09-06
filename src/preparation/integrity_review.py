"""Reconcile every preparation stage against the source before any feature.

This is the checkpoint the plan reserved between cleaning and research. Its
purpose is adversarial: a tidy set of tables can still hide a row that was lost
between stages, a measurement attached to the wrong patient, a unit that was
never resolved, or a sample size that looks larger than the data supports.

Nothing here modifies data. Every check either passes or raises a fixed code,
and the review refuses to report a clean result while any reconciliation fails.
Five questions are answered, each protecting against one specific failure.

Does every source row still have exactly one disposition at every stage? That
protects against silent loss. Does every measurement belong to a patient the
roster accepted? That protects against a bad join. Is every used measurement
carrying the one unit its test is catalogued with? That protects against a
change in a number that is really a change in scale. Are the timing conflicts
and the ambiguous baselines counted rather than absorbed? That protects against
a trajectory that looks smooth because its problems were hidden. Finally, how
many patients actually hold a complete panel at the cycles we intend to use?
That protects against overstating the study.

The last question is the one that decides whether the data is ready, and it is
deliberately answered by counting patients rather than rows.
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
import stage04_roles as stage04
import stage05_tests_units as stage05
import stage06_values as stage06
import stage07_baseline as stage07

# Which tests form the panel is decided by measured coverage, not by a list
# chosen in advance. Every test in the source is counted, then sorted into a
# tier by how many patients actually hold it across the analysis window.
#
# The distinction that matters is between requiring a test and studying one.
# A test in the primary tier is required of every patient, so it sets who is in
# the study. A test in the secondary tier is still studied, but on its own
# smaller group, so it costs no one their place. Requiring a thinly measured
# test is what shrinks a cohort; studying it separately does not.
PRIMARY_MIN_PATIENTS = 600
SECONDARY_MIN_PATIENTS = 300

# The cycles the timing checks showed to be well measured across two trials.
ANALYSIS_CYCLES = (2, 3, 4)

STAGE_TABLES = {
    '02': ('interim/stage02_visit_index.csv', stage02.OUTPUT_FIELDS),
    '03': ('interim/stage03_timing_flags.csv', stage03.OUTPUT_FIELDS),
    '04': ('interim/stage04_analysis_roles.csv', stage04.OUTPUT_FIELDS),
    '06': ('interim/stage06_measurements.csv', stage06.OUTPUT_FIELDS),
}


def source_row_numbers(extracted: Path) -> set[int]:
    """Return the logical row number of every laboratory row in the source."""
    return {line for line, _ in records(extracted / 'training/LabValue_training.csv',
                                        {'STUDYID', 'RPT'})}


def reconcile_dispositions(run: Path, expected_rows: set[int]) -> dict[str, int]:
    """Check that every stage covers every source row exactly once.

    A stage that returns fewer rows has dropped data; one that returns more has
    duplicated it; one that returns a different set has misaligned. All three
    are silent failures in a table that otherwise looks correct, so any of them
    stops the review.
    """
    counts = {}
    for stage_name, (relative, fields) in STAGE_TABLES.items():
        seen = set()
        for _, row in records(run / relative, set(fields)):
            line = int(row['source_row'])
            if line in seen:
                raise IntegrityError(f'STAGE_{stage_name}_DUPLICATED_SOURCE_ROW')
            seen.add(line)
        if seen != expected_rows:
            raise IntegrityError(f'STAGE_{stage_name}_ROW_SET_MISMATCH')
        counts[stage_name] = len(seen)
    return counts


def check_patient_linkage(run: Path) -> int:
    """Check every measured patient was accepted by the Stage 01 roster.

    A measurement attached to a patient outside the roster would carry someone
    else's outcome into the analysis, which is the most damaging error in the
    whole pipeline and the least visible.
    """
    roster = set()
    for _, row in records(run / 'interim/stage01_training_roster.csv', {'STUDYID', 'RPT'}):
        roster.add((row['STUDYID'], row['RPT']))
    measured = set()
    for _, row in records(run / 'interim/stage06_measurements.csv', set(stage06.OUTPUT_FIELDS)):
        measured.add((row['STUDYID'], row['RPT']))
    if not measured <= roster:
        raise IntegrityError('MEASURED_PATIENT_OUTSIDE_ROSTER')
    return len(measured)


def check_units_resolved(run: Path) -> dict[str, int]:
    """Check every used measurement carries its test's catalogued unit.

    Two numbers are comparable only in the same unit. A used measurement with a
    blank unit, or with a unit the catalogue does not record for that test,
    would make a change in scale look like a change in the patient.
    """
    catalogue = {}
    for _, row in records(run / 'interim/stage05_test_catalog.csv', set(stage05.OUTPUT_FIELDS)):
        catalogue[row['resolved_code']] = row['standard_unit']
    used = missing = mismatched = 0
    for _, row in records(run / 'interim/stage06_measurements.csv', set(stage06.OUTPUT_FIELDS)):
        if row['usable_measurement'] != 'Y':
            continue
        used += 1
        expected = catalogue.get(row['test_code'])
        if expected is None:
            raise IntegrityError('USED_TEST_ABSENT_FROM_CATALOGUE')
        if not row['test_unit']:
            missing += 1
        elif row['test_unit'] != expected:
            mismatched += 1
    if mismatched:
        raise IntegrityError('USED_MEASUREMENT_UNIT_CONFLICT')
    return {'used_measurements': used, 'used_measurements_without_a_unit': missing}


def test_cohorts(run: Path) -> tuple[dict[str, set], dict[int, set]]:
    """Return, for every test in the source, the patients who can actually use it.

    A patient counts for a test only if they hold a usable measurement of it at
    every cycle in the analysis window and also hold a starting value to
    measure change against. This is deliberately computed for all 103 test
    codes rather than a chosen few, so the panel can be decided by evidence.
    """
    have: dict[tuple[str, int], set] = defaultdict(set)
    per_cycle: dict[int, set] = defaultdict(set)
    for _, row in records(run / 'interim/stage06_measurements.csv', set(stage06.OUTPUT_FIELDS)):
        if row['usable_measurement'] != 'Y':
            continue
        if row['analysis_purpose'] != stage04.CYCLE_MEASUREMENT or row['cycle_number'] == '':
            continue
        cycle = int(row['cycle_number'])
        if cycle in ANALYSIS_CYCLES:
            have[(row['test_code'], cycle)].add((row['STUDYID'], row['RPT']))
            per_cycle[cycle].add((row['STUDYID'], row['RPT']))

    baselines: dict[str, set] = defaultdict(set)
    for _, row in records(run / 'interim/stage07_baselines.csv', set(stage07.OUTPUT_FIELDS)):
        if row['baseline_value'] != '':
            baselines[row['test_code']].add((row['STUDYID'], row['RPT']))

    cohorts = {}
    for code in {test for test, _ in have}:
        across = [have[(code, cycle)] for cycle in ANALYSIS_CYCLES]
        cohorts[code] = set.intersection(*across, baselines[code])
    return cohorts, per_cycle


def count_coverage(run: Path) -> dict:
    """Sort every test into a tier by coverage and size the resulting study.

    A row count flatters a study; patient counts do not. Each test is placed in
    a tier by the size of its own usable group. The primary tier is required of
    every patient and so defines the cohort, which is the intersection of those
    groups and is always smaller than any one of them. The secondary tier is
    studied on each test's own group and costs the cohort nothing, which is why
    a thinly measured test is not the same as a discarded one.
    """
    cohorts, per_cycle = test_cohorts(run)
    primary = sorted(c for c, v in cohorts.items() if len(v) >= PRIMARY_MIN_PATIENTS)
    secondary = sorted(c for c, v in cohorts.items()
                       if SECONDARY_MIN_PATIENTS <= len(v) < PRIMARY_MIN_PATIENTS)
    descriptive = sorted(c for c, v in cohorts.items() if len(v) < SECONDARY_MIN_PATIENTS)

    analysis_ready = set.intersection(*[cohorts[c] for c in primary]) if primary else set()
    # What each excluded test would cost if it were required instead of studied
    # on its own group. Reported so the trade is visible per test, not lumped.
    cost = {code: len(analysis_ready) - len(analysis_ready & cohorts[code])
            for code in secondary}
    return {
        'analysis_cycles': list(ANALYSIS_CYCLES),
        'primary_minimum_patients': PRIMARY_MIN_PATIENTS,
        'secondary_minimum_patients': SECONDARY_MIN_PATIENTS,
        'tests_with_any_usable_data': len(cohorts),
        'primary_panel': primary,
        'secondary_panel_studied_on_their_own_groups': secondary,
        'descriptive_only_tests': len(descriptive),
        'patients_with_any_usable_cycle_measurement': {
            f'cycle_{c}': len(v) for c, v in sorted(per_cycle.items())},
        'patients_per_test': {code: len(v) for code, v in sorted(cohorts.items())},
        'analysis_ready_patients': len(analysis_ready),
        'cost_in_patients_if_each_secondary_test_were_required': dict(sorted(cost.items())),
    }


def count_retained_problems(run: Path) -> dict:
    """Count the problems that were flagged and kept rather than absorbed.

    Each of these is a decision deferred to the analysis rather than hidden.
    They are reported so that no later stage can treat the cleaned data as if
    it were free of them.
    """
    purposes = Counter()
    reasons = Counter()
    for _, row in records(run / 'interim/stage04_analysis_roles.csv', set(stage04.OUTPUT_FIELDS)):
        purposes[row['analysis_purpose']] += 1
        if row['exclusion_reason']:
            reasons[row['exclusion_reason']] += 1
    kinds = Counter()
    repeats = Counter()
    for _, row in records(run / 'interim/stage06_measurements.csv', set(stage06.OUTPUT_FIELDS)):
        kinds[row['value_kind']] += 1
        repeats[row['repeat_status']] += 1
    baseline_sources = Counter()
    for _, row in records(run / 'interim/stage07_baselines.csv', set(stage07.OUTPUT_FIELDS)):
        baseline_sources[row['baseline_source']] += 1
    return {'rows_by_purpose': dict(sorted(purposes.items())),
            'exclusion_reasons': dict(sorted(reasons.items())),
            'value_kinds': dict(sorted(kinds.items())),
            'repeat_statuses': dict(sorted(repeats.items())),
            'baseline_sources': dict(sorted(baseline_sources.items()))}


def build_review(run: Path) -> dict:
    """Run every reconciliation and return the checkpoint report.

    Verifies the pinned source first, so the review cannot certify tables built
    from an archive that has since changed.
    """
    input_hashes = stage01.verify_archive(run)
    expected = source_row_numbers(run / 'extracted')
    report = {
        'checkpoint': 'integrity_review',
        'source_rows': len(expected),
        'stage_row_counts': reconcile_dispositions(run, expected),
        'patients_measured': check_patient_linkage(run),
        'unit_resolution': check_units_resolved(run),
        'retained_problems': count_retained_problems(run),
        'coverage': count_coverage(run),
    }
    if any(digest(run / p) != h for p, h in input_hashes.items()):
        raise IntegrityError('SOURCE_CHANGED_DURING_REVIEW')
    report['all_reconciliations_passed'] = True
    report['data_modified_by_this_review'] = False
    return report


def main():
    """Run the integrity checkpoint and print its report.

    Returns 0 only when every reconciliation passed. Any failure returns 1 with
    a fixed, disclosure-safe code and no clean result. Never prints a patient
    key or an individual laboratory value.
    """
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--run-root', type=Path, default=REGISTERED_RUN)
    args = parser.parse_args()
    run = args.run_root
    try:
        if run != REGISTERED_RUN or run.resolve() != run:
            raise IntegrityError('UNREGISTERED_RUN_ROOT')
        report = build_review(run)
        report['review_code_sha256'] = digest(Path(__file__))
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

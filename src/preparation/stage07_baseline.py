"""Choose each patient's starting value for each test, and say where it came from.

Every later statement of the form "this went up" or "this fell" is measured
against a starting value. Choosing that value badly does not produce an obvious
error; it produces a plausible-looking change that is not real. So this stage
records not only the value but the evidence it rests on, and refuses to invent
one where the evidence is absent or contradictory.

The source supplies its own answer. `LBBLFL` is described in the data
dictionary as the field to use for parsing out the baseline laboratory value,
and it is remarkably clean here: 44,373 flagged rows across 44,333 patient and
test combinations, with only 40 combinations carrying two flags. That flag is
therefore the primary rule.

One thing about it is easy to get wrong. The flagged row is often not a
screening visit. In CELGENE, 15,639 flagged rows sit on cycle start visits,
because the last blood draw before the first dose is taken on the first day of
cycle 1. A baseline is therefore defined by the flag and the timing, not by the
visit's name, and this stage does not restrict itself to pre-treatment visits.

Where the flag is missing, one explicit fallback applies: the latest usable
measurement recorded on or before the first treatment day. Where two flagged
rows disagree, no baseline is chosen at all, because picking one would be a
coin toss recorded as a fact. Every outcome is counted in the report.
"""
from __future__ import annotations

import argparse
import csv
import json
from collections import Counter, defaultdict
from pathlib import Path

import stage01_roster as stage01
from stage01_roster import REGISTERED_RUN, IntegrityError, digest, key, records
import stage05_tests_units as stage05
import stage06_values as stage06

# The value of `LBBLFL` that marks a row as the source's own baseline.
BASELINE_FLAG = 'Y'

# The first treatment day. A baseline must not be measured after it.
FIRST_TREATMENT_DAY = 0.0

# Where a baseline came from, or why there is none.
FROM_SPONSOR_FLAG = 'sponsor_baseline_flag'
FROM_FALLBACK = 'fallback_latest_on_or_before_first_dose'
NO_BASELINE_CONFLICTING_FLAGS = 'none_conflicting_flags'
NO_BASELINE_NO_EVIDENCE = 'none_no_usable_measurement'

OUTPUT_FIELDS = ('STUDYID', 'RPT', 'test_code', 'test_unit', 'baseline_value',
                 'baseline_day', 'baseline_source', 'baseline_source_row',
                 'flagged_rows', 'candidate_rows_on_or_before_first_dose')


def usable_candidates(rows: list[dict]) -> list[dict]:
    """Return the rows that could serve as a starting value.

    A candidate must be an ordinary number that Stage 06 accepted as the
    measurement representing its visit, and it must carry a recorded day, since
    a starting value that cannot be placed in time cannot be shown to precede
    anything.
    """
    return [r for r in rows
            if r['usable_measurement'] == 'Y' and r['recorded_day'] != ''
            and r['value_kind'] == 'numeric']


def choose_baseline(rows: list[dict]) -> tuple[dict | None, str]:
    """Return the baseline row and its source for one patient and one test.

    The source's own flag is preferred. Two flagged rows that agree on a value
    are one answer recorded twice, so the first is taken; two that disagree
    leave the choice unmade. Where no flag survives, the fallback is the latest
    usable measurement on or before the first treatment day, which is the
    closest description of the patient at the moment treatment began. Where
    nothing qualifies, no baseline is returned and the reason is stated.
    """
    candidates = usable_candidates(rows)
    flagged = [r for r in candidates if r['baseline_flag'] == BASELINE_FLAG]
    if flagged:
        if len({r['analysis_value'] for r in flagged}) > 1:
            return None, NO_BASELINE_CONFLICTING_FLAGS
        return min(flagged, key=lambda r: r['source_row']), FROM_SPONSOR_FLAG

    before = [r for r in candidates if float(r['recorded_day']) <= FIRST_TREATMENT_DAY]
    if before:
        # The latest such draw is the one nearest the start of treatment.
        return max(before, key=lambda r: (float(r['recorded_day']), -r['source_row'])), FROM_FALLBACK
    return None, NO_BASELINE_NO_EVIDENCE


def load_measurements(path: Path) -> dict[int, dict]:
    """Return the Stage 06 measurement table keyed by source CSV row number."""
    rows: dict[int, dict] = {}
    for _, row in records(path, set(stage06.OUTPUT_FIELDS)):
        line = int(row['source_row'])
        if line in rows:
            raise IntegrityError('DUPLICATE_MEASUREMENT_ROW')
        row['source_row'] = line
        rows[line] = row
    if not rows:
        raise IntegrityError('EMPTY_MEASUREMENT_TABLE')
    return rows


def build_baselines(extracted: Path, measurements: dict[int, dict]):
    """Attach the source's baseline flag, then choose one baseline per test.

    The flag lives only in the original file, so it is read here and joined to
    the Stage 06 measurements by source row number. Returns one row per patient
    and test that has any measurement at all, together with an aggregate report
    counting how each baseline was decided.
    """
    groups: dict[tuple[str, str, str], list[dict]] = defaultdict(list)
    flagged_after_first_dose = 0

    required = {'STUDYID', 'RPT', 'LBTESTCD', 'LBTEST', 'LBBLFL'}
    for line, row in records(extracted / 'training/LabValue_training.csv', required):
        entry = measurements.get(line)
        if entry is None:
            raise IntegrityError('MEASUREMENT_ROW_MISSING')
        patient = key(row)
        code = stage05.resolve_test_code(row['LBTESTCD'].strip(), row['LBTEST'])
        if (entry['STUDYID'], entry['RPT'], entry['test_code']) != (*patient, code):
            raise IntegrityError('MEASUREMENT_ROW_MISALIGNED')
        entry['baseline_flag'] = row['LBBLFL'].strip()
        if (entry['baseline_flag'] == BASELINE_FLAG and entry['recorded_day'] != ''
                and float(entry['recorded_day']) > FIRST_TREATMENT_DAY):
            flagged_after_first_dose += 1
        groups[(patient[0], patient[1], code)].append(entry)

    baselines = []
    sources = Counter()
    by_trial_test = Counter()
    for (trial, patient, code) in sorted(groups):
        rows = groups[(trial, patient, code)]
        chosen, source = choose_baseline(rows)
        candidates = usable_candidates(rows)
        sources[(trial, source)] += 1
        if chosen is not None:
            by_trial_test[(trial, code)] += 1
        baselines.append({
            'STUDYID': trial, 'RPT': patient, 'test_code': code,
            'test_unit': chosen['test_unit'] if chosen else '',
            'baseline_value': chosen['analysis_value'] if chosen else '',
            'baseline_day': chosen['recorded_day'] if chosen else '',
            'baseline_source': source,
            'baseline_source_row': chosen['source_row'] if chosen else '',
            'flagged_rows': sum(r['baseline_flag'] == BASELINE_FLAG for r in rows),
            'candidate_rows_on_or_before_first_dose': sum(
                1 for r in candidates if float(r['recorded_day']) <= FIRST_TREATMENT_DAY),
        })

    if any(b['baseline_value'] == '' and b['baseline_source'].startswith(('sponsor', 'fallback'))
           for b in baselines):
        raise IntegrityError('BASELINE_SOURCE_WITHOUT_VALUE')

    panel = ('ALP', 'ALT', 'AST', 'CA', 'CREAT', 'HB', 'LDH', 'NEU', 'PLT', 'PSA',
             'TBILI', 'WBC', 'SODIUM')
    decided = [b for b in baselines if b['baseline_value'] != '']
    report = {
        'stage': '07',
        'patient_test_combinations': len(baselines),
        'baselines_established': len(decided),
        'baselines_not_established': len(baselines) - len(decided),
        'baseline_source_counts': {f'{t}|{s}': n for (t, s), n in sorted(sources.items())},
        'baseline_flag_rows_recorded_after_the_first_dose': flagged_after_first_dose,
        'panel_patients_with_a_baseline': {
            code: sum(1 for b in decided if b['test_code'] == code) for code in panel},
        'baseline_is_defined_by_flag_and_timing_not_visit_name': True,
        'values_edited': 0,
        'baselines_invented_where_evidence_was_absent': 0,
    }
    return baselines, report


def write_baselines(path: Path, rows: list[dict]) -> str:
    """Exclusively create the private baseline table and verify its read-back.

    This file holds patient measurements, so it stays inside the registered
    restricted run root and is written mode 600 with `O_EXCL`, an fsync and a
    full read-back comparison.
    """
    if not rows:
        raise IntegrityError('EMPTY_BASELINE_TABLE')
    if tuple(rows[0]) != OUTPUT_FIELDS:
        raise IntegrityError('UNEXPECTED_OUTPUT_SCHEMA')
    return stage01.write_roster(path, rows)


def main():
    """Run Stage 07 at the registered location and print aggregate evidence.

    Re-verifies the pinned archive, loads the Stage 06 measurements, joins the
    source's baseline flag, chooses one baseline per patient and test, then
    writes the table only if every check passed. Returns 0 on verified success
    or 1 with a fixed, disclosure-safe code. Never prints a patient key or an
    individual laboratory value.
    """
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--run-root', type=Path, default=REGISTERED_RUN)
    args = parser.parse_args()
    run = args.run_root
    try:
        if run != REGISTERED_RUN or run.resolve() != run:
            raise IntegrityError('UNREGISTERED_RUN_ROOT')
        input_hashes = stage01.verify_archive(run)
        measurements_path = run / 'interim/stage06_measurements.csv'
        if measurements_path.is_symlink() or not measurements_path.is_file():
            raise IntegrityError('STAGE06_MEASUREMENTS_MISSING')
        measurements = load_measurements(measurements_path)
        baselines, report = build_baselines(run / 'extracted', measurements)
        if any(digest(run / p) != h for p, h in input_hashes.items()):
            raise IntegrityError('SOURCE_CHANGED_DURING_RUN')
        output = run / 'interim/stage07_baselines.csv'
        report['baselines_sha256'] = write_baselines(output, baselines)
        report['stage06_measurements_sha256'] = digest(measurements_path)
        report['source_code_sha256'] = digest(Path(__file__))
        report['source_unchanged'] = True
        report['baselines_roundtrip_verified'] = True
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

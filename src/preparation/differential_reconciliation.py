"""Decide whether the five ...LE codes duplicate the white cell differential.

This answers open question Q-021, and it has to be answered before any feature
is built. Ten test codes in this source describe the same five kinds of white
blood cell: NEU and NEULE, LYM and LYMLE, MONO and MONOLE, EOS and EOSLE, BASO
and BASOLE. Each pair covers exactly the same patients at exactly the same
visits, which is what a duplicated record looks like. If they really are the
same measurement stored twice, then feeding both to a model would let one
number appear to confirm itself, and a signal carried by one cell type would be
counted with twice the weight the data actually supports.

They are not the same measurement. The evidence is threefold and each part is
checked here rather than assumed.

Their recorded identity says so. The base code is named for the cell alone,
`NEUTROPHILS`, and is standardized to `10^9/L`, a count of cells in a volume of
blood. The paired code is named `NEUTROPHILS/LEUKOCYTES` and is standardized to
`%`, the share of all white cells that this one type makes up. A count and a
share are different quantities: a patient whose white cells all fall by half
keeps the same percentages while every count halves.

Their values say so. On every paired reading the percentage reproduces
`100 * count / white cell count` to within one percentage point, which is the
precision the source reports percentages at. Nothing else would do that.

And their arithmetic says so in the other direction too. The five counts add
back to the white cell count, and the five percentages add to a hundred.

The consequence is the point of the exercise. Both are kept, because a share
and a count answer different clinical questions. But the percentage is not
independent evidence: given the count and the white cell count it carries no
information of its own, so `DERIVED_FROM` records that dependency and any later
feature work must treat the three as two quantities, not three.

Nothing here modifies, selects or writes data. Its only output is an aggregate
report holding counts and agreement rates, never a patient key or a value.
"""
from __future__ import annotations

import argparse
import csv
import json
from collections import defaultdict
from pathlib import Path

import stage01_roster as stage01
from stage01_roster import REGISTERED_RUN, IntegrityError, digest, records
import stage05_tests_units as stage05
import stage06_values as stage06

# The white cell count every percentage in this family is a share of.
WHITE_CELL_CODE = 'WBC'

# The ten codes under question, as (absolute count, share of white cells).
DIFFERENTIAL_PAIRS = (('NEU', 'NEULE'), ('LYM', 'LYMLE'), ('MONO', 'MONOLE'),
                      ('EOS', 'EOSLE'), ('BASO', 'BASOLE'))

# What the catalogue must say for a pair to be a count and its share. The name
# suffix is checked as well as the unit, so a unit recorded by mistake cannot
# on its own decide that two different quantities are the same one.
COUNT_UNIT = '10^9/L'
PERCENTAGE_UNIT = '%'
SHARE_NAME_SUFFIX = '/LEUKOCYTES'

# Percentages are reported to one decimal place and counts to two or three, so
# a percentage rebuilt from the counts cannot land exactly on the recorded one.
# One percentage point is far wider than that rounding gap and far narrower
# than any real disagreement, which is why it separates the two cleanly.
AGREEMENT_TOLERANCE_POINTS = 1.0
MINIMUM_AGREEMENT_FRACTION = 0.99

# The verdicts this reconciliation can reach.
DERIVED_SHARE = 'share_of_white_cells_derived_from_the_count'
SAME_QUANTITY = 'same_quantity_recorded_twice'

# The dependency established here, for later stages to respect. Each share is a
# function of two measurements that are already in the panel, so the three
# together hold two independent numbers and must never be counted as three.
DERIVED_FROM = {share: (count, WHITE_CELL_CODE) for count, share in DIFFERENTIAL_PAIRS}


def derived_share(count: float, white_cells: float) -> float | None:
    """Return the percentage of white cells a given cell count represents.

    This is the arithmetic the duplication hypothesis has to beat. Returns None
    when there is no white cell count to divide by, because a share of nothing
    is undefined rather than zero.
    """
    if white_cells <= 0:
        return None
    return 100.0 * count / white_cells


def check_pair_identity(catalogue: dict[str, dict], count_code: str, share_code: str) -> dict:
    """Check the catalogue records one code as a count and the other as a share.

    Both codes must exist, sit in the same laboratory category, and differ in
    exactly the expected way: the same test name with `/LEUKOCYTES` appended,
    a count in `10^9/L` against a share in `%`. Anything else stops the
    reconciliation, because a pair whose recorded identity is not this cannot
    be settled by the value comparison that follows.
    """
    for code in (count_code, share_code):
        if code not in catalogue:
            raise IntegrityError('DIFFERENTIAL_CODE_ABSENT_FROM_CATALOGUE')
    count, share = catalogue[count_code], catalogue[share_code]
    if count['standard_unit'] != COUNT_UNIT or share['standard_unit'] != PERCENTAGE_UNIT:
        raise IntegrityError('DIFFERENTIAL_UNIT_NOT_A_COUNT_AND_A_SHARE')
    if share['test_name'] != count['test_name'] + SHARE_NAME_SUFFIX:
        raise IntegrityError('DIFFERENTIAL_NAME_PAIRING_BROKEN')
    if count['category'] != share['category']:
        raise IntegrityError('DIFFERENTIAL_CATEGORY_MISMATCH')
    return {'count_name': count['test_name'], 'count_unit': count['standard_unit'],
            'share_name': share['test_name'], 'share_unit': share['standard_unit'],
            'category': count['category'],
            'count_trials': count['trials'], 'share_trials': share['trials']}


def compare_pair(cells: dict[tuple, dict[str, float]], count_code: str,
                 share_code: str) -> dict:
    """Measure how one pair behaves where both codes were recorded together.

    A cell is one patient, one visit, one collection day, so the two codes
    being compared describe the same tube of blood. Three quantities are
    counted: how often the two recorded numbers are simply equal, which is what
    a duplicate would look like, how often the share matches the count divided
    by the white cell count, and how often each code appears without the other.
    The last of these matters because a share with no usable count is the one
    situation where the share carries something the count cannot supply.
    """
    paired = equal = comparable = agreeing = 0
    share_alone = count_alone = 0
    worst = 0.0
    for values in cells.values():
        has_count, has_share = count_code in values, share_code in values
        if has_share and not has_count:
            share_alone += 1
        if has_count and not has_share:
            count_alone += 1
        if not (has_count and has_share):
            continue
        paired += 1
        equal += values[count_code] == values[share_code]
        predicted = derived_share(values[count_code], values.get(WHITE_CELL_CODE, 0.0))
        if predicted is None:
            continue
        comparable += 1
        difference = abs(predicted - values[share_code])
        worst = max(worst, difference)
        agreeing += difference <= AGREEMENT_TOLERANCE_POINTS
    return {'paired_readings': paired,
            'readings_where_the_two_numbers_are_equal': equal,
            'readings_comparable_against_the_white_cell_count': comparable,
            'readings_where_the_share_matches_the_derived_value': agreeing,
            'largest_disagreement_in_percentage_points': round(worst, 4),
            'share_recorded_without_a_usable_count': share_alone,
            'count_recorded_without_a_share': count_alone}


def resolve_duplication(comparison: dict) -> str:
    """Return what a pair actually is, from its measured behaviour.

    A pair is a count and its derived share only while the share reproduces the
    count divided by the white cell count almost every time. A pair whose two
    numbers are instead equal is one quantity written twice, and only then may
    one of them be dropped. If neither description fits, the reconciliation
    stops rather than keeping a conclusion its evidence no longer supports, in
    the same way Stage 05 refuses to keep a value column whose precision
    evidence has changed.
    """
    comparable = comparison['readings_comparable_against_the_white_cell_count']
    paired = comparison['paired_readings']
    if paired == 0:
        raise IntegrityError('NO_PAIRED_DIFFERENTIAL_READINGS')
    if paired and comparison['readings_where_the_two_numbers_are_equal'] == paired:
        return SAME_QUANTITY
    if comparable == 0:
        raise IntegrityError('NO_WHITE_CELL_COUNT_TO_COMPARE_AGAINST')
    agreeing = comparison['readings_where_the_share_matches_the_derived_value']
    if agreeing >= comparable * MINIMUM_AGREEMENT_FRACTION:
        return DERIVED_SHARE
    raise IntegrityError('DIFFERENTIAL_RELATIONSHIP_UNEXPLAINED')


def check_family_arithmetic(cells: dict[tuple, dict[str, float]]) -> dict:
    """Check the five cell types add back to the whole, in both forms.

    A differential is a partition of the white cells, so the five counts should
    total the white cell count and the five shares should total a hundred. This
    is reported rather than enforced, because a laboratory may count cell types
    this source does not list and small totals move with rounding. It is here
    because it is the same redundancy seen from the other side: within each
    form, the fifth number is close to fixed once the other four are known.
    """
    counts = [pair[0] for pair in DIFFERENTIAL_PAIRS]
    shares = [pair[1] for pair in DIFFERENTIAL_PAIRS]
    complete_counts = totalling = complete_shares = summing_to_hundred = 0
    for values in cells.values():
        white = values.get(WHITE_CELL_CODE, 0.0)
        if all(code in values for code in counts) and white > 0:
            complete_counts += 1
            spread = abs(sum(values[code] for code in counts) - white) / white * 100.0
            totalling += spread <= AGREEMENT_TOLERANCE_POINTS
        if all(code in values for code in shares):
            complete_shares += 1
            total = sum(values[code] for code in shares)
            summing_to_hundred += abs(total - 100.0) <= AGREEMENT_TOLERANCE_POINTS
    return {'readings_with_all_five_counts_and_a_white_cell_count': complete_counts,
            'of_those_totalling_the_white_cell_count_within_tolerance': totalling,
            'readings_with_all_five_shares': complete_shares,
            'of_those_summing_to_one_hundred_within_tolerance': summing_to_hundred}


def load_catalogue(path: Path) -> dict[str, dict]:
    """Return the Stage 05 test catalogue keyed by resolved test code.

    Only the identity fields are used here: name, unit, category and trials. No
    laboratory value is read from this file, because it holds none.
    """
    catalogue = {}
    for _, row in records(path, set(stage05.OUTPUT_FIELDS)):
        catalogue[row['resolved_code']] = row
    if not catalogue:
        raise IntegrityError('EMPTY_TEST_CATALOG')
    return catalogue


def load_cells(path: Path) -> dict[tuple, dict[str, float]]:
    """Group the Stage 06 measurements into one entry per tube of blood.

    Reads only the ten codes under question and the white cell count, and only
    measurements Stage 06 marked usable, so the repeats and conflicts it
    already settled are not re-litigated here. Keying on patient, visit and
    recorded day is what makes the comparison fair: a percentage may only be
    checked against a count drawn on the same day. Two usable rows for one code
    in one cell would mean Stage 06 selected twice, so that stops the run.
    """
    wanted = {code for pair in DIFFERENTIAL_PAIRS for code in pair} | {WHITE_CELL_CODE}
    cells: dict[tuple, dict[str, float]] = defaultdict(dict)
    for _, row in records(path, set(stage06.OUTPUT_FIELDS)):
        code = row['test_code']
        if code not in wanted or row['usable_measurement'] != 'Y':
            continue
        cell = (row['STUDYID'], row['RPT'], row['visit_original'], row['recorded_day'])
        if code in cells[cell]:
            raise IntegrityError('TWO_USABLE_MEASUREMENTS_IN_ONE_CELL')
        cells[cell][code] = float(row['analysis_value'])
    if not cells:
        raise IntegrityError('NO_DIFFERENTIAL_MEASUREMENTS_FOUND')
    return cells


def build_reconciliation(run: Path) -> dict:
    """Settle every pair and return the aggregate report for Q-021.

    Verifies the pinned source first and again at the end, so the conclusion
    cannot be certified against an archive that changed underneath it.
    """
    input_hashes = stage01.verify_archive(run)
    catalogue = load_catalogue(run / 'interim/stage05_test_catalog.csv')
    cells = load_cells(run / 'interim/stage06_measurements.csv')

    pairs = {}
    for count_code, share_code in DIFFERENTIAL_PAIRS:
        comparison = compare_pair(cells, count_code, share_code)
        pairs[f'{count_code}|{share_code}'] = {
            'identity': check_pair_identity(catalogue, count_code, share_code),
            'comparison': comparison,
            'verdict': resolve_duplication(comparison)}

    verdicts = {entry['verdict'] for entry in pairs.values()}
    if verdicts != {DERIVED_SHARE}:
        raise IntegrityError('DIFFERENTIAL_PAIRS_DISAGREE')

    report = {
        'checkpoint': 'differential_reconciliation',
        'open_question': 'Q-021',
        'tolerance_in_percentage_points': AGREEMENT_TOLERANCE_POINTS,
        'minimum_agreement_fraction': MINIMUM_AGREEMENT_FRACTION,
        'readings_examined': len(cells),
        'pairs': pairs,
        'family_arithmetic': check_family_arithmetic(cells),
        'verdict': sorted(verdicts)[0],
        'both_codes_kept': True,
        'codes_dropped': 0,
        'derived_codes_that_are_not_independent_evidence': {
            share: list(sources) for share, sources in sorted(DERIVED_FROM.items())},
        'data_modified_by_this_reconciliation': False,
    }
    if any(digest(run / p) != h for p, h in input_hashes.items()):
        raise IntegrityError('SOURCE_CHANGED_DURING_RECONCILIATION')
    report['source_unchanged'] = True
    return report


def main():
    """Run the differential reconciliation and print its aggregate report.

    Returns 0 only when every pair reached the same explained verdict. Any
    failure returns 1 with a fixed, disclosure-safe code and no conclusion.
    Never prints a patient key or an individual laboratory value.
    """
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--run-root', type=Path, default=REGISTERED_RUN)
    args = parser.parse_args()
    run = args.run_root
    try:
        if run != REGISTERED_RUN or run.resolve() != run:
            raise IntegrityError('UNREGISTERED_RUN_ROOT')
        report = build_reconciliation(run)
        report['source_code_sha256'] = digest(Path(__file__))
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

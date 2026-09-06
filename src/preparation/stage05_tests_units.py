"""Establish what each test is, what unit it is in, and which value column to use.

Two numbers can only be compared if they measure the same thing in the same
unit. Stage 05 checks that, and settles one further question the earlier stages
deliberately left open: this source stores every result twice, and the two
copies disagree on 112,167 rows.

The two copies are `LBSTRESN`, described in the data dictionary as the numeric
standardized result, and `LBSTRESC`, the character standardized result. The
dictionary recommends both. They are not equivalent. Every one of the 194,714
parsable values in `LBSTRESN` is a whole number, and 111,932 of the 112,167
disagreements are explained exactly by rounding the character value to the
nearest integer. `LBSTRESN` has therefore lost every decimal place in the
source, which destroys tests whose entire clinical range is smaller than one
unit. `LBSTRESC` is the column that preserves the measurement, so it is the
authoritative one here and `select_value_column` enforces that.

Units need less work than expected, because the trial sponsors already
harmonized them. The original unit column `LBORRESU` is chaotic, recording a
white cell count 33 different ways, but `LBSTRESU` holds exactly one
standardized unit for every test code across all three trials. This stage
verifies that rather than assuming it, and would stop if it were ever untrue.

This stage reads laboratory values in order to check their format and
precision. It writes no patient row: its only output is a test-level catalogue
containing codes, names, units and counts.
"""
from __future__ import annotations

import argparse
import csv
import json
from collections import Counter, defaultdict
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP
from pathlib import Path

import stage01_roster as stage01
from stage01_roster import REGISTERED_RUN, IntegrityError, digest, records

# The column that preserves the measurement. See the module docstring.
AUTHORITATIVE_VALUE_COLUMN = 'LBSTRESC'
ROUNDED_VALUE_COLUMN = 'LBSTRESN'

# Test codes this source leaves unusable, and the evidence that recovers them.
# A code is only recovered when its test name is unambiguous across every row
# that carries it, so identity is never inferred from the size of a result.
CODE_RECOVERY = {'.': 'SODIUM'}

# Markers this source uses for an absent result.
ABSENT = ('', '.')

OUTPUT_FIELDS = ('test_code', 'resolved_code', 'test_name', 'standard_unit', 'category',
                 'trials', 'rows', 'rows_with_numeric_value', 'rows_bounded',
                 'rows_non_numeric_text', 'rows_absent', 'distinct_original_units')


def resolve_test_code(code: str, name: str) -> str:
    """Return a usable test code, recovering the ones this source left blank.

    The code `.` carries no identity of its own. It is recovered only from its
    accompanying test name, and only for names listed in `CODE_RECOVERY`. An
    unrecognized combination stops the stage rather than being guessed at or
    silently dropped.
    """
    if code not in CODE_RECOVERY:
        if not code or code != code.strip():
            raise IntegrityError('BLANK_OR_PADDED_TEST_CODE')
        return code
    if CODE_RECOVERY[code] != name.strip():
        raise IntegrityError('UNRECOVERABLE_TEST_CODE')
    return CODE_RECOVERY[code]


def parse_decimal(text: str) -> Decimal | None:
    """Return a finite Decimal, or None when the text is not a plain number.

    Decimal is used rather than float so that the precision comparison between
    the two value columns is exact. Absent markers and any text that is not a
    plain number, including bounded results such as a value below a detection
    limit, return None here; classifying those is `classify_result` 's job.
    """
    stripped = text.strip()
    if stripped in ABSENT:
        return None
    try:
        value = Decimal(stripped)
    except InvalidOperation:
        return None
    return value if value.is_finite() else None


def classify_result(text: str) -> str:
    """Return the kind of result a standardized character value holds.

    Four kinds are distinguished because they mean different things and must
    not be merged: an ordinary number, a bounded result such as `<0.1` where
    the instrument could not measure below a limit, uninterpretable text, and
    an absent result. Collapsing a bound into a plain number would invent
    precision the laboratory never reported.
    """
    stripped = text.strip()
    if stripped in ABSENT:
        return 'absent'
    if stripped[:1] in ('<', '>'):
        return 'bounded'
    return 'numeric' if parse_decimal(stripped) is not None else 'non_numeric_text'


def select_value_column(numeric_whole: int, numeric_total: int, disagreements: int,
                        explained_by_rounding: int) -> str:
    """Return the value column to trust, given the measured precision evidence.

    The character column is authoritative only while the numeric column is
    demonstrably the coarser copy. That holds when every numeric value is a
    whole number and the disagreements are explained by rounding. If a future
    source ever violates that, the stage stops rather than silently keeping a
    choice its evidence no longer supports.
    """
    if numeric_total == 0:
        raise IntegrityError('NO_NUMERIC_VALUES_TO_COMPARE')
    if numeric_whole != numeric_total:
        raise IntegrityError('NUMERIC_COLUMN_PRECISION_ASSUMPTION_BROKEN')
    if disagreements and explained_by_rounding * 100 < disagreements * 99:
        raise IntegrityError('DISAGREEMENT_NOT_EXPLAINED_BY_ROUNDING')
    return AUTHORITATIVE_VALUE_COLUMN


def build_test_catalog(extracted: Path):
    """Catalogue every test code and gather the value-column evidence.

    Verifies that each code carries exactly one test name and exactly one
    standardized unit across all three trials, recovers the codes this source
    left blank, and counts result formats per code. Returns the catalogue rows
    and an aggregate report. No patient row is written or returned.
    """
    names: dict[str, set[str]] = defaultdict(set)
    units: dict[str, set[str]] = defaultdict(set)
    original_units: dict[str, set[str]] = defaultdict(set)
    categories: dict[str, set[str]] = defaultdict(set)
    trials: dict[str, set[str]] = defaultdict(set)
    formats: dict[str, Counter] = defaultdict(Counter)

    numeric_total = numeric_whole = 0
    disagreements = explained = 0
    bounded_lost = 0

    required = {'STUDYID', 'LBTESTCD', 'LBTEST', 'LBCAT', 'LBSTRESU', 'LBORRESU',
                'LBORRES', 'LBSTRESC', 'LBSTRESN'}
    for _, row in records(extracted / 'training/LabValue_training.csv', required):
        code = resolve_test_code(row['LBTESTCD'].strip(), row['LBTEST'])
        names[code].add(row['LBTEST'].strip())
        units[code].add(row['LBSTRESU'].strip())
        original_units[code].add(row['LBORRESU'].strip())
        categories[code].add(row['LBCAT'].strip())
        trials[code].add(row['STUDYID'])
        formats[code][classify_result(row['LBSTRESC'])] += 1

        character = parse_decimal(row['LBSTRESC'])
        numeric = parse_decimal(row['LBSTRESN'])
        if numeric is not None:
            numeric_total += 1
            numeric_whole += numeric == numeric.to_integral_value()
        if numeric is not None and character is not None and numeric != character:
            disagreements += 1
            explained += numeric == character.quantize(Decimal('1'), rounding=ROUND_HALF_UP)
        # A bound recorded in the original result but absent from the
        # standardized one is a silent loss of information, not a number.
        if row['LBORRES'].strip()[:1] in ('<', '>') and classify_result(row['LBSTRESC']) != 'bounded':
            bounded_lost += 1

    conflicts = {'test_name': sorted(c for c, v in names.items() if len(v) > 1),
                 'standard_unit': sorted(c for c, v in units.items() if len(v - {''}) > 1)}
    if conflicts['test_name']:
        raise IntegrityError('TEST_CODE_NAME_CONFLICT')
    if conflicts['standard_unit']:
        raise IntegrityError('TEST_CODE_UNIT_CONFLICT')

    catalog = []
    for code in sorted(names):
        counts = formats[code]
        catalog.append({
            'test_code': next(k for k, v in CODE_RECOVERY.items() if v == code) if code in CODE_RECOVERY.values() else code,
            'resolved_code': code,
            'test_name': next(iter(names[code])),
            'standard_unit': next(iter(units[code] - {''}), ''),
            'category': '|'.join(sorted(categories[code])),
            'trials': '|'.join(sorted(trials[code])),
            'rows': sum(counts.values()),
            'rows_with_numeric_value': counts['numeric'],
            'rows_bounded': counts['bounded'],
            'rows_non_numeric_text': counts['non_numeric_text'],
            'rows_absent': counts['absent'],
            'distinct_original_units': len(original_units[code] - {''}),
        })

    column = select_value_column(numeric_whole, numeric_total, disagreements, explained)
    report = {
        'stage': '05',
        'distinct_test_codes': len(catalog),
        'codes_recovered_from_test_name': sorted(CODE_RECOVERY.values()),
        'test_code_name_conflicts': 0,
        'test_code_standard_unit_conflicts': 0,
        'authoritative_value_column': column,
        'rejected_value_column': ROUNDED_VALUE_COLUMN,
        'numeric_column_values_parsed': numeric_total,
        'numeric_column_values_that_are_whole_numbers': numeric_whole,
        'value_column_disagreements': disagreements,
        'disagreements_explained_by_rounding_to_integer': explained,
        'original_results_whose_bound_is_absent_from_the_standard_column': bounded_lost,
        'codes_with_more_than_one_original_unit': sum(
            1 for c in original_units if len(original_units[c] - {''}) > 1),
        'result_format_totals': {k: sum(f[k] for f in formats.values())
                                 for k in ('numeric', 'bounded', 'non_numeric_text', 'absent')},
        'units_converted_by_this_stage': 0,
        'values_altered_by_this_stage': 0,
    }
    return catalog, report


def write_catalog(path: Path, catalog: list[dict]) -> str:
    """Exclusively create the test catalogue and verify its read-back.

    The catalogue is test-level and holds no patient row, but it is written
    under the same rules as every other output: mode 600, `O_EXCL`, fsync and
    a full read-back comparison.
    """
    if not catalog:
        raise IntegrityError('EMPTY_TEST_CATALOG')
    if tuple(catalog[0]) != OUTPUT_FIELDS:
        raise IntegrityError('UNEXPECTED_OUTPUT_SCHEMA')
    return stage01.write_roster(path, catalog)


def main():
    """Run Stage 05 at the registered location and print aggregate evidence.

    Re-verifies the pinned archive, catalogues every test code, chooses the
    authoritative value column from measured evidence, then writes the
    catalogue only if every check passed. Returns 0 on verified success or 1
    with a fixed, disclosure-safe code. Never prints a laboratory value.
    """
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--run-root', type=Path, default=REGISTERED_RUN)
    args = parser.parse_args()
    run = args.run_root
    try:
        if run != REGISTERED_RUN or run.resolve() != run:
            raise IntegrityError('UNREGISTERED_RUN_ROOT')
        input_hashes = stage01.verify_archive(run)
        catalog, report = build_test_catalog(run / 'extracted')
        if any(digest(run / p) != h for p, h in input_hashes.items()):
            raise IntegrityError('SOURCE_CHANGED_DURING_RUN')
        output = run / 'interim/stage05_test_catalog.csv'
        report['test_catalog_sha256'] = write_catalog(output, catalog)
        report['source_code_sha256'] = digest(Path(__file__))
        report['source_unchanged'] = True
        report['catalog_roundtrip_verified'] = True
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

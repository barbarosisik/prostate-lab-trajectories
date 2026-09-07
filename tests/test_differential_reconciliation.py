"""Differential reconciliation tests. Every patient key and value is invented.

The question this module answers is whether two codes hold one measurement or
two. Getting that wrong in either direction is costly, so the tests push it
both ways: a genuine count and share must be recognised as such, a code pair
that really is written twice must be reported as duplicated rather than
explained away, and a pair whose numbers fit neither description must stop the
reconciliation instead of receiving a verdict it has not earned.
"""
import csv
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src/preparation'))
import stage04_roles as stage04
import stage05_tests_units as stage05
import stage06_values as stage06
import differential_reconciliation as reconciliation


# One invented tube of blood. The counts total the white cell count and the
# shares are their true percentages, so a correct reconciliation must explain
# every pair without any code being dropped.
INVENTED_CELL = {'WBC': 10.0,
                 'NEU': 7.0, 'NEULE': 70.0,
                 'LYM': 2.0, 'LYMLE': 20.0,
                 'MONO': 0.6, 'MONOLE': 6.0,
                 'EOS': 0.3, 'EOSLE': 3.0,
                 'BASO': 0.1, 'BASOLE': 1.0}

TEST_NAMES = {'WBC': 'WHITE BLOOD CELLS', 'NEU': 'NEUTROPHILS', 'LYM': 'LYMPHOCYTES',
              'MONO': 'MONOCYTES', 'EOS': 'EOSINOPHILS', 'BASO': 'BASOPHILS'}


class ReconciliationFixture(unittest.TestCase):
    """Builds an invented catalogue and measurement table under a temporary run."""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.run = Path(self.tmp.name)
        (self.run / 'interim').mkdir()
        self.write_catalogue()
        self.write_measurements(INVENTED_CELL)

    def write(self, relative, fields, rows):
        with (self.run / relative).open('w', encoding='utf-8', newline='') as stream:
            writer = csv.DictWriter(stream, fieldnames=list(fields))
            writer.writeheader()
            writer.writerows(rows)

    def catalogue_row(self, code, name, unit):
        return {'test_code': code, 'resolved_code': code, 'test_name': name,
                'standard_unit': unit, 'category': 'HEMATOLOGY', 'trials': 'CELGENE',
                'rows': 1, 'rows_with_numeric_value': 1, 'rows_bounded': 0,
                'rows_non_numeric_text': 0, 'rows_absent': 0, 'distinct_original_units': 1}

    def write_catalogue(self, overrides=None):
        """Write a catalogue naming and unitting every code in the family."""
        rows = [self.catalogue_row('WBC', TEST_NAMES['WBC'], reconciliation.COUNT_UNIT)]
        for count_code, share_code in reconciliation.DIFFERENTIAL_PAIRS:
            rows.append(self.catalogue_row(count_code, TEST_NAMES[count_code],
                                           reconciliation.COUNT_UNIT))
            rows.append(self.catalogue_row(
                share_code, TEST_NAMES[count_code] + reconciliation.SHARE_NAME_SUFFIX,
                reconciliation.PERCENTAGE_UNIT))
        for row in rows:
            row.update((overrides or {}).get(row['resolved_code'], {}))
        self.write('interim/stage05_test_catalog.csv', stage05.OUTPUT_FIELDS, rows)

    def measurement(self, line, code, value, patient='INVENTED-ONE', day='21',
                    visit='CYCLE 2 DAY 1', usable='Y'):
        return {'source_row': line, 'STUDYID': 'CELGENE', 'RPT': patient,
                'test_code': code, 'test_unit': reconciliation.COUNT_UNIT,
                'visit_original': visit, 'analysis_purpose': stage04.CYCLE_MEASUREMENT,
                'cycle_number': '2', 'recorded_day': day, 'value_kind': 'numeric',
                'analysis_value': str(value), 'bound_direction': '', 'bound_value': '',
                'repeat_status': 'single', 'usable_measurement': usable}

    def write_measurements(self, *cells, extra=()):
        """Write one measurement row per code per invented cell, plus extras."""
        rows, line = [], 2
        for index, cell in enumerate(cells):
            for code, value in cell.items():
                rows.append(self.measurement(line, code, value,
                                             patient=f'INVENTED-{index}'))
                line += 1
        for row in extra:
            row.setdefault('source_row', line)
            rows.append(row)
            line += 1
        self.write('interim/stage06_measurements.csv', stage06.OUTPUT_FIELDS, rows)

    def cells(self):
        return reconciliation.load_cells(self.run / 'interim/stage06_measurements.csv')

    def catalogue(self):
        return reconciliation.load_catalogue(self.run / 'interim/stage05_test_catalog.csv')


class IdentityTests(ReconciliationFixture):
    """The catalogue must describe a count and a share, or the run stops."""

    def test_a_count_and_its_share_are_accepted(self):
        identity = reconciliation.check_pair_identity(self.catalogue(), 'NEU', 'NEULE')
        self.assertEqual(identity['count_unit'], reconciliation.COUNT_UNIT)
        self.assertEqual(identity['share_unit'], reconciliation.PERCENTAGE_UNIT)

    def test_two_codes_in_the_same_unit_stop_the_reconciliation(self):
        self.write_catalogue({'NEULE': {'standard_unit': reconciliation.COUNT_UNIT}})
        with self.assertRaises(reconciliation.IntegrityError) as caught:
            reconciliation.check_pair_identity(self.catalogue(), 'NEU', 'NEULE')
        self.assertEqual(str(caught.exception),
                         'DIFFERENTIAL_UNIT_NOT_A_COUNT_AND_A_SHARE')

    def test_a_share_not_named_for_its_count_stops_the_reconciliation(self):
        self.write_catalogue({'NEULE': {'test_name': 'LYMPHOCYTES/LEUKOCYTES'}})
        with self.assertRaises(reconciliation.IntegrityError) as caught:
            reconciliation.check_pair_identity(self.catalogue(), 'NEU', 'NEULE')
        self.assertEqual(str(caught.exception), 'DIFFERENTIAL_NAME_PAIRING_BROKEN')

    def test_a_missing_code_stops_the_reconciliation(self):
        rows = [r for r in self.catalogue().values() if r['resolved_code'] != 'NEULE']
        self.write('interim/stage05_test_catalog.csv', stage05.OUTPUT_FIELDS, rows)
        with self.assertRaises(reconciliation.IntegrityError) as caught:
            reconciliation.check_pair_identity(self.catalogue(), 'NEU', 'NEULE')
        self.assertEqual(str(caught.exception), 'DIFFERENTIAL_CODE_ABSENT_FROM_CATALOGUE')

    def test_codes_from_different_categories_stop_the_reconciliation(self):
        self.write_catalogue({'NEULE': {'category': 'CHEMISTRY'}})
        with self.assertRaises(reconciliation.IntegrityError) as caught:
            reconciliation.check_pair_identity(self.catalogue(), 'NEU', 'NEULE')
        self.assertEqual(str(caught.exception), 'DIFFERENTIAL_CATEGORY_MISMATCH')


class ComparisonTests(ReconciliationFixture):
    """A share is compared only against a count drawn from the same tube."""

    def test_a_true_share_agrees_with_the_derived_value(self):
        comparison = reconciliation.compare_pair(self.cells(), 'NEU', 'NEULE')
        self.assertEqual(comparison['paired_readings'], 1)
        self.assertEqual(comparison['readings_where_the_share_matches_the_derived_value'], 1)
        self.assertEqual(comparison['readings_where_the_two_numbers_are_equal'], 0)
        self.assertEqual(reconciliation.resolve_duplication(comparison),
                         reconciliation.DERIVED_SHARE)

    def test_a_count_and_a_share_from_different_days_are_not_paired(self):
        self.write_measurements(INVENTED_CELL)
        with (self.run / 'interim/stage06_measurements.csv').open(encoding='utf-8') as stream:
            rows = list(csv.DictReader(stream))
        for row in rows:
            if row['test_code'] == 'NEULE':
                row['recorded_day'] = '22'
        self.write('interim/stage06_measurements.csv', stage06.OUTPUT_FIELDS, rows)
        comparison = reconciliation.compare_pair(self.cells(), 'NEU', 'NEULE')
        self.assertEqual(comparison['paired_readings'], 0)
        self.assertEqual(comparison['share_recorded_without_a_usable_count'], 1)
        self.assertEqual(comparison['count_recorded_without_a_share'], 1)

    def test_a_share_without_a_usable_count_is_counted_separately(self):
        cell = dict(INVENTED_CELL)
        del cell['NEU']
        self.write_measurements(cell)
        comparison = reconciliation.compare_pair(self.cells(), 'NEU', 'NEULE')
        self.assertEqual(comparison['share_recorded_without_a_usable_count'], 1)
        self.assertEqual(comparison['paired_readings'], 0)

    def test_measurements_stage06_rejected_are_ignored(self):
        extra = [self.measurement(0, 'NEULE', 99.0, patient='INVENTED-0',
                                  visit='CYCLE 3 DAY 1', usable='N')]
        self.write_measurements(INVENTED_CELL, extra=extra)
        comparison = reconciliation.compare_pair(self.cells(), 'NEU', 'NEULE')
        self.assertEqual(comparison['paired_readings'], 1)
        self.assertEqual(comparison['share_recorded_without_a_usable_count'], 0)

    def test_two_usable_rows_for_one_code_in_one_cell_stop_the_run(self):
        extra = [self.measurement(0, 'NEU', 8.0, patient='INVENTED-0')]
        self.write_measurements(INVENTED_CELL, extra=extra)
        with self.assertRaises(reconciliation.IntegrityError) as caught:
            self.cells()
        self.assertEqual(str(caught.exception), 'TWO_USABLE_MEASUREMENTS_IN_ONE_CELL')

    def test_rounding_within_tolerance_still_agrees(self):
        cell = dict(INVENTED_CELL, NEULE=70.4)
        self.write_measurements(cell)
        comparison = reconciliation.compare_pair(self.cells(), 'NEU', 'NEULE')
        self.assertEqual(comparison['readings_where_the_share_matches_the_derived_value'], 1)

    def test_a_share_with_no_white_cell_count_is_not_comparable(self):
        cell = dict(INVENTED_CELL)
        del cell['WBC']
        self.write_measurements(cell)
        comparison = reconciliation.compare_pair(self.cells(), 'NEU', 'NEULE')
        self.assertEqual(comparison['paired_readings'], 1)
        self.assertEqual(comparison['readings_comparable_against_the_white_cell_count'], 0)
        with self.assertRaises(reconciliation.IntegrityError) as caught:
            reconciliation.resolve_duplication(comparison)
        self.assertEqual(str(caught.exception), 'NO_WHITE_CELL_COUNT_TO_COMPARE_AGAINST')


class VerdictTests(ReconciliationFixture):
    """The verdict must follow the evidence, in both directions."""

    def test_a_genuinely_duplicated_pair_is_reported_as_duplicated(self):
        cell = dict(INVENTED_CELL, NEULE=INVENTED_CELL['NEU'])
        self.write_measurements(cell)
        comparison = reconciliation.compare_pair(self.cells(), 'NEU', 'NEULE')
        self.assertEqual(reconciliation.resolve_duplication(comparison),
                         reconciliation.SAME_QUANTITY)

    def test_a_relationship_that_fits_neither_description_stops_the_run(self):
        cell = dict(INVENTED_CELL, NEULE=12.5)
        self.write_measurements(cell)
        comparison = reconciliation.compare_pair(self.cells(), 'NEU', 'NEULE')
        with self.assertRaises(reconciliation.IntegrityError) as caught:
            reconciliation.resolve_duplication(comparison)
        self.assertEqual(str(caught.exception), 'DIFFERENTIAL_RELATIONSHIP_UNEXPLAINED')

    def test_a_pair_never_recorded_together_stops_the_run(self):
        cell = dict(INVENTED_CELL)
        del cell['NEULE']
        self.write_measurements(cell)
        comparison = reconciliation.compare_pair(self.cells(), 'NEU', 'NEULE')
        with self.assertRaises(reconciliation.IntegrityError) as caught:
            reconciliation.resolve_duplication(comparison)
        self.assertEqual(str(caught.exception), 'NO_PAIRED_DIFFERENTIAL_READINGS')

    def test_a_minority_of_disagreeing_readings_does_not_change_the_verdict(self):
        cells = [INVENTED_CELL] * 199 + [dict(INVENTED_CELL, NEULE=12.5)]
        self.write_measurements(*cells)
        comparison = reconciliation.compare_pair(self.cells(), 'NEU', 'NEULE')
        self.assertEqual(reconciliation.resolve_duplication(comparison),
                         reconciliation.DERIVED_SHARE)

    def test_enough_disagreeing_readings_do_change_it(self):
        cells = [INVENTED_CELL] * 95 + [dict(INVENTED_CELL, NEULE=12.5)] * 5
        self.write_measurements(*cells)
        comparison = reconciliation.compare_pair(self.cells(), 'NEU', 'NEULE')
        with self.assertRaises(reconciliation.IntegrityError):
            reconciliation.resolve_duplication(comparison)


class FamilyArithmeticTests(ReconciliationFixture):
    """The five cell types should add back to the whole, in both forms."""

    def test_a_complete_differential_totals_the_white_cell_count(self):
        arithmetic = reconciliation.check_family_arithmetic(self.cells())
        self.assertEqual(arithmetic['readings_with_all_five_counts_and_a_white_cell_count'], 1)
        self.assertEqual(arithmetic['of_those_totalling_the_white_cell_count_within_tolerance'], 1)
        self.assertEqual(arithmetic['readings_with_all_five_shares'], 1)
        self.assertEqual(arithmetic['of_those_summing_to_one_hundred_within_tolerance'], 1)

    def test_a_differential_that_does_not_add_up_is_counted_not_hidden(self):
        cell = dict(INVENTED_CELL, NEU=3.0, NEULE=30.0)
        self.write_measurements(cell)
        arithmetic = reconciliation.check_family_arithmetic(self.cells())
        self.assertEqual(arithmetic['readings_with_all_five_counts_and_a_white_cell_count'], 1)
        self.assertEqual(arithmetic['of_those_totalling_the_white_cell_count_within_tolerance'], 0)
        self.assertEqual(arithmetic['of_those_summing_to_one_hundred_within_tolerance'], 0)

    def test_an_incomplete_differential_is_not_judged(self):
        cell = dict(INVENTED_CELL)
        del cell['BASO']
        del cell['BASOLE']
        self.write_measurements(cell)
        arithmetic = reconciliation.check_family_arithmetic(self.cells())
        self.assertEqual(arithmetic['readings_with_all_five_counts_and_a_white_cell_count'], 0)
        self.assertEqual(arithmetic['readings_with_all_five_shares'], 0)


class DerivationTests(unittest.TestCase):
    """The recorded dependency is what stops a number corroborating itself."""

    def test_every_share_is_recorded_as_derived_from_two_measurements(self):
        for count_code, share_code in reconciliation.DIFFERENTIAL_PAIRS:
            with self.subTest(share=share_code):
                self.assertEqual(reconciliation.DERIVED_FROM[share_code],
                                 (count_code, reconciliation.WHITE_CELL_CODE))

    def test_no_count_is_marked_derived(self):
        for count_code, _ in reconciliation.DIFFERENTIAL_PAIRS:
            self.assertNotIn(count_code, reconciliation.DERIVED_FROM)
        self.assertNotIn(reconciliation.WHITE_CELL_CODE, reconciliation.DERIVED_FROM)

    def test_a_share_of_no_white_cells_is_undefined_rather_than_zero(self):
        self.assertIsNone(reconciliation.derived_share(0.0, 0.0))
        self.assertEqual(reconciliation.derived_share(7.0, 10.0), 70.0)


if __name__ == '__main__':
    unittest.main()

"""Stage 05 tests. Every laboratory value here is invented.

The risks under test are the ones that would silently corrupt every later
number: trusting the coarser of the two value columns, merging a below-limit
result into an ordinary number, letting one test code carry two identities or
two units, and guessing at a test code that the source left blank.
"""
import csv
from decimal import Decimal
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src/preparation'))
import stage05_tests_units as stage


class ResolveTestCodeTests(unittest.TestCase):
    """A code is recovered from evidence, or not at all."""

    def test_an_ordinary_code_is_returned_unchanged(self):
        self.assertEqual(stage.resolve_test_code('HB', 'HEMOGLOBIN'), 'HB')

    def test_the_blank_code_is_recovered_only_from_its_test_name(self):
        self.assertEqual(stage.resolve_test_code('.', 'SODIUM'), 'SODIUM')

    def test_the_blank_code_with_an_unexpected_name_stops_the_stage(self):
        with self.assertRaises(stage.IntegrityError) as caught:
            stage.resolve_test_code('.', 'POTASSIUM')
        self.assertEqual(str(caught.exception), 'UNRECOVERABLE_TEST_CODE')

    def test_a_blank_or_padded_code_is_refused(self):
        for code in ('', ' HB', 'HB '):
            with self.subTest(code=code), self.assertRaises(stage.IntegrityError) as caught:
                stage.resolve_test_code(code, 'HEMOGLOBIN')
            self.assertEqual(str(caught.exception), 'BLANK_OR_PADDED_TEST_CODE')


class ClassifyResultTests(unittest.TestCase):
    """Four kinds of result that must never be merged into one."""

    def test_an_ordinary_measurement_is_numeric(self):
        for text in ('13.5', '-0.4', '0', '1E2'):
            with self.subTest(text=text):
                self.assertEqual(stage.classify_result(text), 'numeric')

    def test_a_below_or_above_limit_result_keeps_its_own_kind(self):
        for text in ('<0.1', '>2000', '< 0.1'):
            with self.subTest(text=text):
                self.assertEqual(stage.classify_result(text), 'bounded')

    def test_absent_markers_are_absent_and_not_zero(self):
        for text in ('', '   ', '.'):
            with self.subTest(text=text):
                self.assertEqual(stage.classify_result(text), 'absent')
                self.assertIsNone(stage.parse_decimal(text))

    def test_uninterpretable_text_is_kept_apart_from_missing(self):
        for text in ('NOT DONE', 'HEMOLYSED', 'nan'):
            with self.subTest(text=text):
                self.assertEqual(stage.classify_result(text), 'non_numeric_text')

    def test_a_bounded_result_never_parses_as_a_plain_number(self):
        self.assertIsNone(stage.parse_decimal('<0.1'))

    def test_parsing_is_exact_rather_than_floating_point(self):
        self.assertEqual(stage.parse_decimal('0.1') * 3, Decimal('0.3'))


class SelectValueColumnTests(unittest.TestCase):
    """The choice of column must follow the evidence, not a preference."""

    def test_the_character_column_wins_when_the_numeric_one_is_coarser(self):
        self.assertEqual(stage.select_value_column(100, 100, 60, 60), 'LBSTRESC')

    def test_agreement_everywhere_still_selects_the_character_column(self):
        self.assertEqual(stage.select_value_column(100, 100, 0, 0), 'LBSTRESC')

    def test_a_numeric_column_with_real_decimals_stops_the_stage(self):
        with self.assertRaises(stage.IntegrityError) as caught:
            stage.select_value_column(99, 100, 0, 0)
        self.assertEqual(str(caught.exception), 'NUMERIC_COLUMN_PRECISION_ASSUMPTION_BROKEN')

    def test_disagreements_that_rounding_cannot_explain_stop_the_stage(self):
        with self.assertRaises(stage.IntegrityError) as caught:
            stage.select_value_column(100, 100, 100, 50)
        self.assertEqual(str(caught.exception), 'DISAGREEMENT_NOT_EXPLAINED_BY_ROUNDING')

    def test_nothing_to_compare_stops_the_stage(self):
        with self.assertRaises(stage.IntegrityError) as caught:
            stage.select_value_column(0, 0, 0, 0)
        self.assertEqual(str(caught.exception), 'NO_NUMERIC_VALUES_TO_COMPARE')


class BuildTestCatalogTests(unittest.TestCase):
    """End-to-end cataloguing over invented laboratory rows."""

    FIELDS = ['STUDYID', 'LBTESTCD', 'LBTEST', 'LBCAT', 'LBSTRESU', 'LBORRESU',
              'LBORRES', 'LBSTRESC', 'LBSTRESN']

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name) / 'extracted'

    def build(self, rows):
        path = self.root / 'training/LabValue_training.csv'
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open('w', encoding='utf-8', newline='') as stream:
            writer = csv.writer(stream)
            writer.writerow(self.FIELDS)
            writer.writerows(rows)
        return stage.build_test_catalog(self.root)

    def test_a_clean_catalogue_records_identity_unit_and_counts(self):
        rows = [['CELGENE', 'HB', 'HEMOGLOBIN', 'HEMATOLOGY', 'G/DL', 'G/DL', '13.5', '13.5', '14'],
                ['EFC6546', 'HB', 'HEMOGLOBIN', 'HEMATOLOGY', 'G/DL', 'G/L', '135', '13.5', '14']]
        catalog, report = self.build(rows)
        self.assertEqual(len(catalog), 1)
        entry = catalog[0]
        self.assertEqual(entry['test_name'], 'HEMOGLOBIN')
        self.assertEqual(entry['standard_unit'], 'G/DL')
        self.assertEqual(entry['trials'], 'CELGENE|EFC6546')
        self.assertEqual(entry['rows_with_numeric_value'], 2)
        self.assertEqual(entry['distinct_original_units'], 2)
        self.assertEqual(report['codes_with_more_than_one_original_unit'], 1)
        self.assertEqual(report['units_converted_by_this_stage'], 0)
        self.assertEqual(report['values_altered_by_this_stage'], 0)

    def test_the_recovered_code_appears_under_its_recovered_identity(self):
        rows = [['CELGENE', '.', 'SODIUM', 'CHEMISTRY', 'MMOL/L', 'MMOL/L', '140', '140', '140']]
        catalog, report = self.build(rows)
        self.assertEqual(catalog[0]['resolved_code'], 'SODIUM')
        self.assertEqual(catalog[0]['test_code'], '.')
        self.assertEqual(report['codes_recovered_from_test_name'], ['SODIUM'])

    def test_the_rounded_column_is_rejected_and_the_evidence_is_reported(self):
        rows = [['CELGENE', 'K', 'POTASSIUM', 'CHEMISTRY', 'MMOL/L', 'MMOL/L', '4.5', '4.5', '5'],
                ['CELGENE', 'K', 'POTASSIUM', 'CHEMISTRY', 'MMOL/L', 'MMOL/L', '4.2', '4.2', '4']]
        _, report = self.build(rows)
        self.assertEqual(report['authoritative_value_column'], 'LBSTRESC')
        self.assertEqual(report['rejected_value_column'], 'LBSTRESN')
        self.assertEqual(report['value_column_disagreements'], 2)
        self.assertEqual(report['disagreements_explained_by_rounding_to_integer'], 2)
        self.assertEqual(report['numeric_column_values_that_are_whole_numbers'], 2)

    def test_two_names_for_one_code_stop_the_stage(self):
        rows = [['CELGENE', 'HB', 'HEMOGLOBIN', 'HEMATOLOGY', 'G/DL', 'G/DL', '13.5', '13.5', '14'],
                ['EFC6546', 'HB', 'HAEMOGLOBIN A1C', 'HEMATOLOGY', 'G/DL', 'G/DL', '5.5', '5.5', '6']]
        with self.assertRaises(stage.IntegrityError) as caught:
            self.build(rows)
        self.assertEqual(str(caught.exception), 'TEST_CODE_NAME_CONFLICT')

    def test_two_standard_units_for_one_code_stop_the_stage(self):
        rows = [['CELGENE', 'HB', 'HEMOGLOBIN', 'HEMATOLOGY', 'G/DL', 'G/DL', '13.5', '13.5', '14'],
                ['EFC6546', 'HB', 'HEMOGLOBIN', 'HEMATOLOGY', 'G/L', 'G/L', '135', '135', '135']]
        with self.assertRaises(stage.IntegrityError) as caught:
            self.build(rows)
        self.assertEqual(str(caught.exception), 'TEST_CODE_UNIT_CONFLICT')

    def test_a_bound_lost_between_the_original_and_standard_columns_is_counted(self):
        rows = [['CELGENE', 'PSA', 'PROSTATE SPECIFIC ANTIGEN', 'CHEMISTRY', 'NG/ML', 'NG/ML', '<0.1', '0.1', '0'],
                ['CELGENE', 'PSA', 'PROSTATE SPECIFIC ANTIGEN', 'CHEMISTRY', 'NG/ML', 'NG/ML', '<0.1', '<0.1', '']]
        catalog, report = self.build(rows)
        self.assertEqual(report['original_results_whose_bound_is_absent_from_the_standard_column'], 1)
        self.assertEqual(catalog[0]['rows_bounded'], 1)
        self.assertEqual(catalog[0]['rows_with_numeric_value'], 1)

    def test_result_formats_are_counted_separately_and_add_up(self):
        rows = [['CELGENE', 'PSA', 'PROSTATE SPECIFIC ANTIGEN', 'CHEMISTRY', 'NG/ML', 'NG/ML', '5', '5', '5'],
                ['CELGENE', 'PSA', 'PROSTATE SPECIFIC ANTIGEN', 'CHEMISTRY', 'NG/ML', 'NG/ML', '<0.1', '<0.1', ''],
                ['CELGENE', 'PSA', 'PROSTATE SPECIFIC ANTIGEN', 'CHEMISTRY', 'NG/ML', 'NG/ML', '', '.', ''],
                ['CELGENE', 'PSA', 'PROSTATE SPECIFIC ANTIGEN', 'CHEMISTRY', 'NG/ML', 'NG/ML', 'NOT DONE', 'NOT DONE', '']]
        catalog, report = self.build(rows)
        entry = catalog[0]
        self.assertEqual((entry['rows_with_numeric_value'], entry['rows_bounded'],
                          entry['rows_absent'], entry['rows_non_numeric_text']), (1, 1, 1, 1))
        self.assertEqual(entry['rows'], 4)
        self.assertEqual(sum(report['result_format_totals'].values()), 4)


class WriteCatalogTests(unittest.TestCase):
    """The catalogue is written under the same rules as every other output."""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.path = Path(self.tmp.name) / 'stage05_test_catalog.csv'
        self.rows = [dict(zip(stage.OUTPUT_FIELDS,
                              ('HB', 'HB', 'HEMOGLOBIN', 'G/DL', 'HEMATOLOGY',
                               'CELGENE', 2, 2, 0, 0, 0, 1)))]

    def test_the_catalogue_reads_back_identically(self):
        stage.write_catalog(self.path, self.rows)
        with self.path.open(encoding='utf-8', newline='') as stream:
            self.assertEqual(list(csv.DictReader(stream)),
                             [{k: str(v) for k, v in self.rows[0].items()}])

    def test_an_existing_catalogue_is_never_overwritten(self):
        self.path.write_text('invented existing content', encoding='utf-8')
        with self.assertRaises(OSError):
            stage.write_catalog(self.path, self.rows)

    def test_an_empty_catalogue_is_refused(self):
        with self.assertRaises(stage.IntegrityError) as caught:
            stage.write_catalog(self.path, [])
        self.assertEqual(str(caught.exception), 'EMPTY_TEST_CATALOG')


if __name__ == '__main__':
    unittest.main()

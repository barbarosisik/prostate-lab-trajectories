"""Integrity checkpoint tests. Every patient key and value here is invented.

A checkpoint that cannot fail is worthless, so these tests are mostly about
making it fail: a row dropped between stages, a row duplicated, a measurement
belonging to a patient the roster never accepted, and a unit that contradicts
the catalogue. Each must stop the review rather than be reported as clean.
"""
import csv
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src/preparation'))
import stage04_roles as stage04
import stage06_values as stage06
import integrity_review as review


class ReviewFixture(unittest.TestCase):
    """Builds a minimal, internally consistent set of stage outputs."""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.run = Path(self.tmp.name)
        (self.run / 'interim').mkdir()
        (self.run / 'extracted/training').mkdir(parents=True)
        self.rows = [2, 3]
        self.write_source()
        self.write_stage_tables()

    def write(self, relative, fields, rows):
        path = self.run / relative
        with path.open('w', encoding='utf-8', newline='') as stream:
            writer = csv.DictWriter(stream, fieldnames=list(fields))
            writer.writeheader()
            writer.writerows(rows)

    def write_source(self):
        self.write('extracted/training/LabValue_training.csv', ['STUDYID', 'RPT'],
                   [{'STUDYID': 'CELGENE', 'RPT': 'INVENTED-ONE'},
                    {'STUDYID': 'CELGENE', 'RPT': 'INVENTED-ONE'}])

    def measurement(self, line, test='HB', unit='G/DL', patient='INVENTED-ONE', cycle='2'):
        return {'source_row': line, 'STUDYID': 'CELGENE', 'RPT': patient,
                'test_code': test, 'test_unit': unit, 'visit_original': 'CYCLE 2 DAY 1',
                'analysis_purpose': stage04.CYCLE_MEASUREMENT, 'cycle_number': cycle,
                'recorded_day': '21', 'value_kind': 'numeric', 'analysis_value': '13.5',
                'bound_direction': '', 'bound_value': '', 'repeat_status': 'single',
                'usable_measurement': 'Y'}

    def write_stage_tables(self, measurements=None, drop_from=None, duplicate_in=None):
        stub = {'02': lambda l: {'source_row': l, 'STUDYID': 'CELGENE', 'RPT': 'INVENTED-ONE',
                                 'visit_original': 'CYCLE 2 DAY 1', 'cycle_number': '2',
                                 'cycle_day': '1', 'day_stated_by_label': 'Y',
                                 'visit_role': 'cycle_start'},
                '03': lambda l: {'source_row': l, 'STUDYID': 'CELGENE', 'RPT': 'INVENTED-ONE',
                                 'visit_original': 'CYCLE 2 DAY 1', 'visit_role': 'cycle_start',
                                 'cycle_number': '2', 'recorded_day': '21',
                                 'reference_origin': '1ST TREATMENT', 'expected_day': '21',
                                 'schedule_deviation_days': '0', 'day_missing': 'N',
                                 'alternate_reference_origin': 'N', 'off_schedule': 'N',
                                 'pre_treatment_not_before_day_zero': 'N',
                                 'cycle_order_violation': 'N', 'usable_for_cycle_analysis': 'Y'},
                '04': lambda l: {'source_row': l, 'STUDYID': 'CELGENE', 'RPT': 'INVENTED-ONE',
                                 'visit_original': 'CYCLE 2 DAY 1', 'visit_role': 'cycle_start',
                                 'cycle_number': '2', 'recorded_day': '21',
                                 'analysis_purpose': stage04.CYCLE_MEASUREMENT,
                                 'exclusion_reason': ''}}
        for name, (relative, fields) in review.STAGE_TABLES.items():
            if name == '06':
                rows = measurements if measurements is not None else [
                    self.measurement(2), self.measurement(3, test='WBC', unit='10^9/L')]
            else:
                rows = [stub[name](line) for line in self.rows]
            if drop_from == name:
                rows = rows[:-1]
            if duplicate_in == name:
                rows = rows + [rows[0]]
            self.write(relative, fields, rows)
        self.write('interim/stage01_training_roster.csv', ['STUDYID', 'RPT'],
                   [{'STUDYID': 'CELGENE', 'RPT': 'INVENTED-ONE'}])
        self.write('interim/stage05_test_catalog.csv', review.stage05.OUTPUT_FIELDS,
                   [{'test_code': 'HB', 'resolved_code': 'HB', 'test_name': 'HEMOGLOBIN',
                     'standard_unit': 'G/DL', 'category': 'HEMATOLOGY', 'trials': 'CELGENE',
                     'rows': 1, 'rows_with_numeric_value': 1, 'rows_bounded': 0,
                     'rows_non_numeric_text': 0, 'rows_absent': 0, 'distinct_original_units': 1},
                    {'test_code': 'WBC', 'resolved_code': 'WBC', 'test_name': 'WHITE CELLS',
                     'standard_unit': '10^9/L', 'category': 'HEMATOLOGY', 'trials': 'CELGENE',
                     'rows': 1, 'rows_with_numeric_value': 1, 'rows_bounded': 0,
                     'rows_non_numeric_text': 0, 'rows_absent': 0, 'distinct_original_units': 1}])
        self.write('interim/stage07_baselines.csv', review.stage07.OUTPUT_FIELDS,
                   [{'STUDYID': 'CELGENE', 'RPT': 'INVENTED-ONE', 'test_code': 'HB',
                     'test_unit': 'G/DL', 'baseline_value': '13.8', 'baseline_day': '-3',
                     'baseline_source': review.stage07.FROM_SPONSOR_FLAG,
                     'baseline_source_row': 2, 'flagged_rows': 1,
                     'candidate_rows_on_or_before_first_dose': 1}])


class ReconciliationTests(ReviewFixture):
    """The checks that must fail when a stage disagrees with the source."""

    def test_a_consistent_set_of_tables_reconciles(self):
        expected = review.source_row_numbers(self.run / 'extracted')
        self.assertEqual(expected, set(self.rows))
        self.assertEqual(review.reconcile_dispositions(self.run, expected),
                         {'02': 2, '03': 2, '04': 2, '06': 2})

    def test_a_row_dropped_between_stages_stops_the_review(self):
        for stage_name in review.STAGE_TABLES:
            with self.subTest(stage=stage_name):
                self.write_stage_tables(drop_from=stage_name)
                with self.assertRaises(review.IntegrityError) as caught:
                    review.reconcile_dispositions(self.run, set(self.rows))
                self.assertEqual(str(caught.exception), f'STAGE_{stage_name}_ROW_SET_MISMATCH')

    def test_a_row_duplicated_within_a_stage_stops_the_review(self):
        self.write_stage_tables(duplicate_in='04')
        with self.assertRaises(review.IntegrityError) as caught:
            review.reconcile_dispositions(self.run, set(self.rows))
        self.assertEqual(str(caught.exception), 'STAGE_04_DUPLICATED_SOURCE_ROW')

    def test_a_measurement_outside_the_roster_stops_the_review(self):
        self.write_stage_tables(measurements=[self.measurement(2),
                                              self.measurement(3, patient='INVENTED-ABSENT')])
        with self.assertRaises(review.IntegrityError) as caught:
            review.check_patient_linkage(self.run)
        self.assertEqual(str(caught.exception), 'MEASURED_PATIENT_OUTSIDE_ROSTER')

    def test_matching_patients_pass_the_linkage_check(self):
        self.assertEqual(review.check_patient_linkage(self.run), 1)


class UnitResolutionTests(ReviewFixture):
    """A used measurement must carry the unit its test is catalogued with."""

    def test_matching_units_pass_and_are_counted(self):
        self.assertEqual(review.check_units_resolved(self.run),
                         {'used_measurements': 2, 'used_measurements_without_a_unit': 0})

    def test_a_unit_that_contradicts_the_catalogue_stops_the_review(self):
        self.write_stage_tables(measurements=[self.measurement(2, unit='G/L'),
                                              self.measurement(3, test='WBC', unit='10^9/L')])
        with self.assertRaises(review.IntegrityError) as caught:
            review.check_units_resolved(self.run)
        self.assertEqual(str(caught.exception), 'USED_MEASUREMENT_UNIT_CONFLICT')

    def test_a_used_test_missing_from_the_catalogue_stops_the_review(self):
        self.write_stage_tables(measurements=[self.measurement(2, test='INVENTED'),
                                              self.measurement(3, test='WBC', unit='10^9/L')])
        with self.assertRaises(review.IntegrityError) as caught:
            review.check_units_resolved(self.run)
        self.assertEqual(str(caught.exception), 'USED_TEST_ABSENT_FROM_CATALOGUE')

    def test_a_blank_unit_is_counted_rather_than_treated_as_a_match(self):
        self.write_stage_tables(measurements=[self.measurement(2, unit=''),
                                              self.measurement(3, test='WBC', unit='10^9/L')])
        self.assertEqual(review.check_units_resolved(self.run)['used_measurements_without_a_unit'], 1)

    def test_rows_stage06_rejected_are_not_unit_checked(self):
        rejected = dict(self.measurement(2), usable_measurement='N', test_unit='')
        self.write_stage_tables(measurements=[rejected, self.measurement(3, test='WBC', unit='10^9/L')])
        self.assertEqual(review.check_units_resolved(self.run),
                         {'used_measurements': 1, 'used_measurements_without_a_unit': 0})


class CoverageTests(ReviewFixture):
    """Coverage must count patients, and must not flatter the sample."""

    def test_a_patient_missing_one_panel_test_is_not_analysis_ready(self):
        coverage = review.count_coverage(self.run)
        self.assertEqual(coverage['patients_with_the_core_panel_at_every_analysis_cycle'], 0)
        self.assertEqual(coverage['analysis_ready_patients'], 0)

    def test_only_measurements_stage06_accepted_are_counted(self):
        rejected = dict(self.measurement(2), usable_measurement='N')
        self.write_stage_tables(measurements=[rejected, self.measurement(3, test='WBC', unit='10^9/L')])
        coverage = review.count_coverage(self.run)
        self.assertEqual(coverage['patients_per_test_per_cycle']['HB|cycle_2'], 0)
        self.assertEqual(coverage['patients_per_test_per_cycle']['WBC|cycle_2'], 1)

    def test_a_cycle_outside_the_analysis_window_is_not_counted(self):
        self.write_stage_tables(measurements=[self.measurement(2, cycle='5'),
                                              self.measurement(3, test='WBC', unit='10^9/L')])
        coverage = review.count_coverage(self.run)
        self.assertEqual(coverage['patients_with_any_usable_cycle_measurement'], {'cycle_2': 1})

    def test_the_sparse_tests_are_reported_apart_from_the_core_panel(self):
        coverage = review.count_coverage(self.run)
        self.assertEqual(coverage['sparse_panel_reported_separately'], list(review.SPARSE_PANEL))
        self.assertNotIn('LDH', coverage['core_panel'])
        self.assertNotIn('SODIUM', coverage['core_panel'])


if __name__ == '__main__':
    unittest.main()

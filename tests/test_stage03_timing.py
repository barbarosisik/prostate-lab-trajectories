"""Stage 03 tests. Every patient key, day and record here is invented.

The tests target the ways a timing check can quietly go wrong: treating an
absent day as a real one, comparing rows measured from different origins,
calling an ordinary dose delay an error, and letting a genuinely impossible
cycle order pass.
"""
import csv
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src/preparation'))
import stage02_visits as stage02
import stage03_timing as stage


class ExpectedDayTests(unittest.TestCase):
    """The schedule used for checking is the one observed in this source."""

    def test_cycle_one_starts_at_the_reference_day(self):
        self.assertEqual(stage.expected_day(1), 0)

    def test_each_later_cycle_adds_one_observed_cycle_length(self):
        self.assertEqual([stage.expected_day(n) for n in range(1, 6)], [0, 21, 42, 63, 84])


class ParseDayTests(unittest.TestCase):
    """Absent and unreadable days must not collapse into the same handling."""

    def test_absent_markers_return_no_day_rather_than_zero(self):
        for value in ['', '   ', '.']:
            with self.subTest(value=value):
                self.assertIsNone(stage.parse_day(value))

    def test_negative_and_zero_days_are_valid_recorded_values(self):
        self.assertEqual(stage.parse_day('-7'), -7)
        self.assertEqual(stage.parse_day('0'), 0)

    def test_unreadable_day_stops_the_stage_instead_of_being_dropped(self):
        for value in ['NOT DONE', 'nan', 'inf', '21;']:
            with self.subTest(value=value), self.assertRaises(stage.IntegrityError) as caught:
                stage.parse_day(value)
            self.assertEqual(str(caught.exception), 'NON_NUMERIC_COLLECTION_DAY')


class ClassifyTimingTests(unittest.TestCase):
    """One row's flags, with the cycle ordering check deliberately excluded."""

    def classify(self, role, cycle, day, reference=stage.PRIMARY_REFERENCE):
        return stage.classify_timing(role, cycle, day, reference)

    def test_a_cycle_start_on_its_scheduled_day_raises_no_flag(self):
        verdict = self.classify(stage02.CYCLE_START, 3, 42.0)
        self.assertEqual(verdict['schedule_deviation_days'], 0)
        self.assertFalse(any(verdict['flags'].values()))

    def test_an_ordinary_dose_delay_is_not_called_an_error(self):
        verdict = self.classify(stage02.CYCLE_START, 2, 28.0)
        self.assertEqual(verdict['schedule_deviation_days'], 7)
        self.assertFalse(verdict['flags']['off_schedule'])

    def test_a_day_a_whole_cycle_out_of_place_is_flagged(self):
        verdict = self.classify(stage02.CYCLE_START, 2, 65.0)
        self.assertTrue(verdict['flags']['off_schedule'])

    def test_the_tolerance_boundary_is_inclusive(self):
        self.assertFalse(self.classify(stage02.CYCLE_START, 2, 31.0)['flags']['off_schedule'])
        self.assertTrue(self.classify(stage02.CYCLE_START, 2, 31.1)['flags']['off_schedule'])

    def test_a_missing_day_is_flagged_and_never_scored_against_the_schedule(self):
        verdict = self.classify(stage02.CYCLE_START, 2, None)
        self.assertTrue(verdict['flags']['day_missing'])
        self.assertFalse(verdict['flags']['off_schedule'])
        self.assertIsNone(verdict['schedule_deviation_days'])
        self.assertFalse(verdict['comparable'])

    def test_a_different_reference_origin_is_flagged_and_not_compared(self):
        verdict = self.classify(stage02.CYCLE_START, 2, 900.0, 'CONSENT DATE')
        self.assertTrue(verdict['flags']['alternate_reference_origin'])
        self.assertFalse(verdict['flags']['off_schedule'])
        self.assertIsNone(verdict['schedule_deviation_days'])

    def test_pre_treatment_must_precede_the_first_treatment_day(self):
        self.assertFalse(self.classify(stage02.PRE_TREATMENT, None, -7.0)
                         ['flags']['pre_treatment_not_before_day_zero'])
        self.assertTrue(self.classify(stage02.PRE_TREATMENT, None, 0.0)
                        ['flags']['pre_treatment_not_before_day_zero'])
        self.assertTrue(self.classify(stage02.PRE_TREATMENT, None, 41.0)
                        ['flags']['pre_treatment_not_before_day_zero'])

    def test_non_cycle_roles_are_never_scored_against_the_schedule(self):
        for role in (stage02.UNSCHEDULED, stage02.FOLLOW_UP, stage02.DISCONTINUATION,
                     stage02.UNRESOLVED, stage02.WITHIN_CYCLE):
            with self.subTest(role=role):
                verdict = self.classify(role, None, 500.0)
                self.assertIsNone(verdict['schedule_deviation_days'])
                self.assertFalse(verdict['flags']['off_schedule'])


class CycleOrderTests(unittest.TestCase):
    """Ordering is the one check that needs no schedule assumption at all."""

    def test_increasing_days_across_cycles_are_accepted(self):
        days = {('CELGENE', 'INVENTED-ONE'): {1: [0.0], 2: [21.0], 3: [42.0]}}
        self.assertEqual(stage.cycle_order_violations(days), set())

    def test_a_later_cycle_recorded_earlier_flags_the_later_cycle(self):
        days = {('CELGENE', 'INVENTED-ONE'): {1: [0.0], 2: [40.0], 3: [20.0]}}
        self.assertEqual(stage.cycle_order_violations(days),
                         {('CELGENE', 'INVENTED-ONE', 3)})

    def test_two_cycles_recorded_on_the_same_day_is_a_violation(self):
        days = {('CELGENE', 'INVENTED-ONE'): {1: [0.0], 2: [0.0]}}
        self.assertEqual(stage.cycle_order_violations(days),
                         {('CELGENE', 'INVENTED-ONE', 2)})

    def test_a_gap_in_the_cycle_sequence_does_not_create_a_violation(self):
        days = {('CELGENE', 'INVENTED-ONE'): {1: [0.0], 4: [63.0]}}
        self.assertEqual(stage.cycle_order_violations(days), set())

    def test_one_patient_s_violation_does_not_flag_another_patient(self):
        days = {('CELGENE', 'INVENTED-ONE'): {1: [0.0], 2: [21.0]},
                ('CELGENE', 'INVENTED-TWO'): {1: [40.0], 2: [20.0]}}
        self.assertEqual(stage.cycle_order_violations(days),
                         {('CELGENE', 'INVENTED-TWO', 2)})


class BuildTimingFlagsTests(unittest.TestCase):
    """End-to-end flagging over invented laboratory rows."""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name) / 'extracted'

    def write_lab(self, rows):
        path = self.root / 'training/LabValue_training.csv'
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open('w', encoding='utf-8', newline='') as stream:
            writer = csv.writer(stream)
            writer.writerow(['STUDYID', 'RPT', 'VISIT', 'LBDT_PC', 'PER_REF_C', 'LBSTRESN'])
            writer.writerows(rows)

    def index_for(self, rows):
        index = {}
        for offset, row in enumerate(rows):
            cycle, day, stated, role = stage02.classify_visit(row[0], row[2])
            index[offset + 2] = {'source_row': str(offset + 2), 'STUDYID': row[0], 'RPT': row[1],
                                 'visit_original': row[2],
                                 'cycle_number': '' if cycle is None else str(cycle),
                                 'cycle_day': '' if day is None else str(day),
                                 'day_stated_by_label': 'Y' if stated else 'N',
                                 'visit_role': role}
        return index

    def run_rows(self, rows):
        self.write_lab(rows)
        return stage.build_timing_flags(self.root, self.index_for(rows))

    def test_a_clean_patient_yields_usable_cycle_rows_and_no_flags(self):
        rows = [['CELGENE', 'INVENTED-ONE', 'SCREENING', '-7', '1ST TREATMENT', '13.5'],
                ['CELGENE', 'INVENTED-ONE', 'CYCLE 1 DAY 1', '0', '1ST TREATMENT', '13.4'],
                ['CELGENE', 'INVENTED-ONE', 'CYCLE 2 DAY 1', '21', '1ST TREATMENT', '12.8']]
        flags, report = self.run_rows(rows)
        self.assertEqual(report['rows_read'], 3)
        self.assertEqual(report['rows_dropped'], 0)
        self.assertEqual(report['rows_relabelled'], 0)
        self.assertEqual(report['cycle_start_rows_usable'], 2)
        self.assertEqual(sum(report['flag_counts'].values()), 0)
        self.assertFalse(report['laboratory_values_read_or_transformed'])

    def test_every_input_row_appears_once_in_the_output(self):
        rows = [['EFC6546', 'INVENTED-TWO', 'CYCLE 2', '21', '1ST TREATMENT', '1'],
                ['EFC6546', 'INVENTED-TWO', 'VISIT 99', '', '1ST TREATMENT', '1'],
                ['EFC6546', 'INVENTED-TWO', 'FOLLOW-UP 1', '120', '1ST TREATMENT', '1']]
        flags, report = self.run_rows(rows)
        self.assertEqual([f['source_row'] for f in flags], [2, 3, 4])
        self.assertEqual(report['rows_assigned_a_disposition'], len(rows))
        self.assertEqual(tuple(flags[0]), stage.OUTPUT_FIELDS)

    def test_an_out_of_order_cycle_is_flagged_and_marked_unusable(self):
        rows = [['CELGENE', 'INVENTED-ONE', 'CYCLE 1 DAY 1', '0', '1ST TREATMENT', '1'],
                ['CELGENE', 'INVENTED-ONE', 'CYCLE 2 DAY 1', '21', '1ST TREATMENT', '1'],
                ['CELGENE', 'INVENTED-ONE', 'CYCLE 3 DAY 1', '20', '1ST TREATMENT', '1']]
        flags, report = self.run_rows(rows)
        self.assertEqual(flags[2]['cycle_order_violation'], 'Y')
        self.assertEqual(flags[2]['usable_for_cycle_analysis'], 'N')
        self.assertEqual(flags[1]['cycle_order_violation'], 'N')
        self.assertEqual(report['cycle_order_violation_groups'], 1)

    def test_a_row_on_another_reference_origin_is_excluded_from_comparison(self):
        rows = [['CELGENE', 'INVENTED-ONE', 'CYCLE 2 DAY 1', '900', 'CONSENT DATE', '1']]
        flags, report = self.run_rows(rows)
        self.assertEqual(flags[0]['alternate_reference_origin'], 'Y')
        self.assertEqual(flags[0]['off_schedule'], 'N')
        self.assertEqual(flags[0]['usable_for_cycle_analysis'], 'N')
        self.assertEqual(report['cycle_start_rows_usable'], 0)
        self.assertIsNone(report['max_comparable_recorded_day'])

    def test_a_missing_day_leaves_the_cycle_label_intact_but_unusable(self):
        rows = [['CELGENE', 'INVENTED-ONE', 'CYCLE 2 DAY 1', '.', '1ST TREATMENT', '1']]
        flags, report = self.run_rows(rows)
        self.assertEqual(flags[0]['cycle_number'], 2)
        self.assertEqual(flags[0]['day_missing'], 'Y')
        self.assertEqual(flags[0]['recorded_day'], '')
        self.assertEqual(flags[0]['usable_for_cycle_analysis'], 'N')
        self.assertFalse(report['cycle_labels_altered'])

    def test_a_visit_spanning_more_than_one_day_is_counted(self):
        rows = [['CELGENE', 'INVENTED-ONE', 'CYCLE 2 DAY 1', '21', '1ST TREATMENT', '1'],
                ['CELGENE', 'INVENTED-ONE', 'CYCLE 2 DAY 1', '22', '1ST TREATMENT', '1']]
        _, report = self.run_rows(rows)
        self.assertEqual(report['patient_visits_spanning_more_than_one_day'], 1)
        self.assertEqual(report['patient_visits_checked'], 1)

    def test_a_misaligned_visit_index_stops_the_stage(self):
        rows = [['CELGENE', 'INVENTED-ONE', 'CYCLE 2 DAY 1', '21', '1ST TREATMENT', '1']]
        self.write_lab(rows)
        index = self.index_for(rows)
        index[2]['RPT'] = 'INVENTED-OTHER'
        with self.assertRaises(stage.IntegrityError) as caught:
            stage.build_timing_flags(self.root, index)
        self.assertEqual(str(caught.exception), 'VISIT_INDEX_ROW_MISALIGNED')

    def test_a_source_row_absent_from_the_visit_index_stops_the_stage(self):
        rows = [['CELGENE', 'INVENTED-ONE', 'CYCLE 2 DAY 1', '21', '1ST TREATMENT', '1']]
        self.write_lab(rows)
        with self.assertRaises(stage.IntegrityError) as caught:
            stage.build_timing_flags(self.root, {})
        self.assertEqual(str(caught.exception), 'VISIT_INDEX_ROW_MISSING')


if __name__ == '__main__':
    unittest.main()

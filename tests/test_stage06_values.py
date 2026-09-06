"""Stage 06 tests. Every patient key and laboratory value here is invented.

The risks under test are the ones that would quietly fabricate data: turning an
absent result or a below-limit result into a number, counting one duplicate
record twice, choosing between two same-day results with no basis, and losing a
row that was never meant to be deleted.
"""
import csv
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src/preparation'))
import stage04_roles as stage04
import stage06_values as stage


class ReadValueTests(unittest.TestCase):
    """Four kinds of entry, and only one of them yields a number."""

    def test_an_ordinary_number_becomes_the_analysis_value(self):
        self.assertEqual(stage.read_value('13.5'), ('numeric', '13.5', '', ''))

    def test_precision_is_preserved_exactly(self):
        self.assertEqual(stage.read_value('1.03')[1], '1.03')
        self.assertEqual(stage.read_value('0.050')[1], '0.050')

    def test_a_below_limit_result_keeps_its_bound_and_yields_no_value(self):
        self.assertEqual(stage.read_value('<0.1'), ('bounded', '', '<', '0.1'))
        self.assertEqual(stage.read_value('>2000'), ('bounded', '', '>', '2000'))

    def test_an_absent_entry_never_becomes_zero(self):
        for text in ('', '.', '   '):
            with self.subTest(text=text):
                kind, value, direction, bound = stage.read_value(text)
                self.assertEqual((kind, value), ('absent', ''))
                self.assertEqual((direction, bound), ('', ''))

    def test_uninterpretable_text_never_becomes_a_number(self):
        self.assertEqual(stage.read_value('NOT DONE'), ('non_numeric_text', '', '', ''))

    def test_a_bound_without_a_readable_limit_is_text_not_a_bound(self):
        self.assertEqual(stage.read_value('<LOW'), ('non_numeric_text', '', '', ''))


class TargetDayTests(unittest.TestCase):
    """What each visit's measurement is meant to describe."""

    def test_a_cycle_measurement_targets_its_own_cycle_start(self):
        self.assertEqual(stage.target_day(stage04.CYCLE_MEASUREMENT, '3', '44'), 42.0)

    def test_a_baseline_candidate_targets_the_first_treatment_day(self):
        self.assertEqual(stage.target_day(stage04.BASELINE_CANDIDATE, '', '-14'), 0.0)

    def test_a_mid_cycle_measurement_is_judged_against_its_own_day(self):
        self.assertEqual(stage.target_day(stage04.MID_CYCLE_MEASUREMENT, '1', '14'), 14.0)

    def test_a_context_row_has_no_target(self):
        self.assertIsNone(stage.target_day(stage04.CONTEXT_ONLY, '', '40'))


class ResolveRepeatsTests(unittest.TestCase):
    """The three repeat situations, which must not be treated alike."""

    def row(self, source_row, day, value, kind='numeric', target=0.0):
        return {'source_row': source_row, 'recorded_day': day, 'analysis_value': value,
                'value_kind': kind, 'target_day': target, 'repeat_status': ''}

    def test_a_lone_row_is_marked_single(self):
        rows = [self.row(2, '21', '13.5')]
        stage.resolve_repeats(rows)
        self.assertEqual(rows[0]['repeat_status'], stage.SINGLE)

    def test_identical_records_keep_one_and_mark_the_rest(self):
        rows = [self.row(2, '21', '13.5'), self.row(3, '21', '13.5')]
        stage.resolve_repeats(rows)
        self.assertEqual([r['repeat_status'] for r in rows],
                         [stage.DUPLICATE_KEPT, stage.DUPLICATE_NOT_USED])

    def test_repeat_draws_select_the_one_closest_to_the_target_day(self):
        rows = [self.row(2, '18', '13.5', target=21.0), self.row(3, '22', '12.8', target=21.0)]
        stage.resolve_repeats(rows)
        self.assertEqual([r['repeat_status'] for r in rows],
                         [stage.REPEAT_NOT_SELECTED, stage.REPEAT_SELECTED])

    def test_a_baseline_repeat_selects_the_draw_nearest_the_first_dose(self):
        rows = [self.row(2, '-21', '13.8', target=0.0), self.row(3, '-3', '13.5', target=0.0)]
        stage.resolve_repeats(rows)
        self.assertEqual(rows[1]['repeat_status'], stage.REPEAT_SELECTED)

    def test_an_equal_distance_tie_is_broken_by_the_earlier_draw(self):
        rows = [self.row(2, '24', '12.0', target=21.0), self.row(3, '18', '13.0', target=21.0)]
        stage.resolve_repeats(rows)
        self.assertEqual(rows[1]['repeat_status'], stage.REPEAT_SELECTED)

    def test_same_day_different_values_leaves_the_group_unresolved(self):
        rows = [self.row(2, '21', '13.5'), self.row(3, '21', '12.1')]
        stage.resolve_repeats(rows)
        self.assertEqual([r['repeat_status'] for r in rows],
                         [stage.CONFLICT_UNRESOLVED, stage.CONFLICT_UNRESOLVED])

    def test_only_ordinary_numbers_can_be_selected(self):
        rows = [self.row(2, '21', '', kind='absent'), self.row(3, '22', '12.8')]
        stage.resolve_repeats(rows)
        self.assertEqual([r['repeat_status'] for r in rows],
                         [stage.REPEAT_NOT_SELECTED, stage.REPEAT_SELECTED])

    def test_a_group_with_no_usable_number_selects_nothing(self):
        rows = [self.row(2, '21', '', kind='absent'), self.row(3, '21', '', kind='non_numeric_text')]
        stage.resolve_repeats(rows)
        self.assertTrue(all(r['repeat_status'] == stage.REPEAT_NOT_SELECTED for r in rows))

    def test_a_row_without_a_recorded_day_cannot_be_selected(self):
        rows = [self.row(2, '', '13.5'), self.row(3, '22', '12.8')]
        stage.resolve_repeats(rows)
        self.assertEqual(rows[1]['repeat_status'], stage.REPEAT_SELECTED)

    def test_exactly_one_row_is_selected_in_every_resolvable_group(self):
        rows = [self.row(2, '18', '1', target=21.0), self.row(3, '21', '2', target=21.0),
                self.row(4, '30', '3', target=21.0)]
        stage.resolve_repeats(rows)
        chosen = [r for r in rows if r['repeat_status'] in
                  (stage.REPEAT_SELECTED, stage.DUPLICATE_KEPT)]
        self.assertEqual(len(chosen), 1)
        self.assertEqual(chosen[0]['recorded_day'], '21')


class BuildValuesTests(unittest.TestCase):
    """End-to-end over invented laboratory rows and Stage 04 purposes."""

    FIELDS = ['STUDYID', 'RPT', 'VISIT', 'LBTESTCD', 'LBTEST', 'LBSTRESU', 'LBSTRESC']

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name) / 'extracted'

    def build(self, rows, purposes, cycles=None, days=None):
        path = self.root / 'training/LabValue_training.csv'
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open('w', encoding='utf-8', newline='') as stream:
            writer = csv.writer(stream)
            writer.writerow(self.FIELDS)
            writer.writerows(rows)
        roles = {}
        for offset, row in enumerate(rows):
            line = offset + 2
            roles[line] = {'source_row': str(line), 'STUDYID': row[0], 'RPT': row[1],
                           'visit_original': row[2], 'visit_role': 'cycle_start',
                           'cycle_number': (cycles or {}).get(line, '2'),
                           'recorded_day': (days or {}).get(line, '21'),
                           'analysis_purpose': purposes[offset], 'exclusion_reason': ''}
        return stage.build_values(self.root, roles)

    def test_no_row_is_lost_and_nothing_is_edited(self):
        rows = [['CELGENE', 'INVENTED-ONE', 'CYCLE 2 DAY 1', 'HB', 'HEMOGLOBIN', 'G/DL', '13.5'],
                ['CELGENE', 'INVENTED-ONE', 'CYCLE 2 DAY 1', 'K', 'POTASSIUM', 'MMOL/L', '.']]
        values, report = self.build(rows, [stage04.CYCLE_MEASUREMENT] * 2)
        self.assertEqual(report['rows_read'], 2)
        self.assertEqual(report['rows_deleted'], 0)
        self.assertEqual(report['values_edited'], 0)
        self.assertEqual(report['units_converted'], 0)
        self.assertEqual(len(values), 2)
        self.assertEqual(tuple(values[0]), stage.OUTPUT_FIELDS)

    def test_only_a_real_number_on_a_valued_purpose_is_usable(self):
        rows = [['CELGENE', 'INVENTED-ONE', 'CYCLE 2 DAY 1', 'HB', 'HEMOGLOBIN', 'G/DL', '13.5'],
                ['CELGENE', 'INVENTED-ONE', 'CYCLE 2 DAY 1', 'K', 'POTASSIUM', 'MMOL/L', '<0.1'],
                ['CELGENE', 'INVENTED-ONE', 'CYCLE 2 DAY 1', 'CA', 'CALCIUM', 'MMOL/L', 'NOT DONE'],
                ['CELGENE', 'INVENTED-ONE', 'CYCLE 2 DAY 1', 'ALP', 'ALK PHOS', 'U/L', '80']]
        purposes = [stage04.CYCLE_MEASUREMENT] * 3 + [stage04.CONTEXT_ONLY]
        values, report = self.build(rows, purposes)
        self.assertEqual([v['usable_measurement'] for v in values], ['Y', 'N', 'N', 'N'])
        self.assertEqual(report['usable_measurements_total'], 1)
        self.assertEqual(report['bounds_retained_not_converted_to_numbers'], 1)

    def test_a_bound_is_carried_through_without_becoming_a_value(self):
        rows = [['CELGENE', 'INVENTED-ONE', 'CYCLE 2 DAY 1', 'PSA', 'PSA', 'NG/ML', '<0.1']]
        values, _ = self.build(rows, [stage04.CYCLE_MEASUREMENT])
        self.assertEqual(values[0]['analysis_value'], '')
        self.assertEqual((values[0]['bound_direction'], values[0]['bound_value']), ('<', '0.1'))

    def test_the_recovered_sodium_code_appears_under_its_resolved_name(self):
        rows = [['CELGENE', 'INVENTED-ONE', 'CYCLE 2 DAY 1', '.', 'SODIUM', 'MMOL/L', '140']]
        values, _ = self.build(rows, [stage04.CYCLE_MEASUREMENT])
        self.assertEqual(values[0]['test_code'], 'SODIUM')

    def test_a_duplicate_record_is_counted_once_not_twice(self):
        rows = [['CELGENE', 'INVENTED-ONE', 'CYCLE 2 DAY 1', 'HB', 'HEMOGLOBIN', 'G/DL', '13.5'],
                ['CELGENE', 'INVENTED-ONE', 'CYCLE 2 DAY 1', 'HB', 'HEMOGLOBIN', 'G/DL', '13.5']]
        values, report = self.build(rows, [stage04.CYCLE_MEASUREMENT] * 2)
        self.assertEqual(report['usable_measurements_total'], 1)
        self.assertEqual([v['repeat_status'] for v in values],
                         [stage.DUPLICATE_KEPT, stage.DUPLICATE_NOT_USED])
        self.assertEqual(report['groups_with_repeats'], 1)

    def test_a_same_day_conflict_yields_no_usable_measurement(self):
        rows = [['CELGENE', 'INVENTED-ONE', 'CYCLE 2 DAY 1', 'HB', 'HEMOGLOBIN', 'G/DL', '13.5'],
                ['CELGENE', 'INVENTED-ONE', 'CYCLE 2 DAY 1', 'HB', 'HEMOGLOBIN', 'G/DL', '11.1']]
        values, report = self.build(rows, [stage04.CYCLE_MEASUREMENT] * 2)
        self.assertEqual(report['usable_measurements_total'], 0)
        self.assertTrue(all(v['repeat_status'] == stage.CONFLICT_UNRESOLVED for v in values))
        self.assertTrue(all(v['analysis_value'] for v in values))

    def test_different_tests_at_one_visit_are_not_treated_as_repeats(self):
        rows = [['CELGENE', 'INVENTED-ONE', 'CYCLE 2 DAY 1', 'HB', 'HEMOGLOBIN', 'G/DL', '13.5'],
                ['CELGENE', 'INVENTED-ONE', 'CYCLE 2 DAY 1', 'WBC', 'WHITE CELLS', '10^9/L', '5.2']]
        values, report = self.build(rows, [stage04.CYCLE_MEASUREMENT] * 2)
        self.assertEqual(report['groups_with_repeats'], 0)
        self.assertTrue(all(v['repeat_status'] == stage.SINGLE for v in values))
        self.assertEqual(report['usable_measurements_total'], 2)

    def test_a_misaligned_role_table_stops_the_stage(self):
        rows = [['CELGENE', 'INVENTED-ONE', 'CYCLE 2 DAY 1', 'HB', 'HEMOGLOBIN', 'G/DL', '13.5']]
        path = self.root / 'training/LabValue_training.csv'
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open('w', encoding='utf-8', newline='') as stream:
            writer = csv.writer(stream)
            writer.writerow(self.FIELDS)
            writer.writerows(rows)
        roles = {2: {'source_row': '2', 'STUDYID': 'CELGENE', 'RPT': 'INVENTED-OTHER',
                     'visit_original': 'CYCLE 2 DAY 1', 'visit_role': 'cycle_start',
                     'cycle_number': '2', 'recorded_day': '21',
                     'analysis_purpose': stage04.CYCLE_MEASUREMENT, 'exclusion_reason': ''}}
        with self.assertRaises(stage.IntegrityError) as caught:
            stage.build_values(self.root, roles)
        self.assertEqual(str(caught.exception), 'ROLE_ROW_MISALIGNED')


if __name__ == '__main__':
    unittest.main()

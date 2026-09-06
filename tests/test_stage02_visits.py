"""Stage 02 tests. Every patient key and visit row here is invented.

The tests cover three risks specifically: a visit label being interpreted when
it was never enumerated, a label from one trial being applied to another, and a
mid-cycle measurement being pooled with a cycle start.
"""
import csv
import os
from pathlib import Path
import stat
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src/preparation'))
import stage02_visits as stage


class VisitTableTests(unittest.TestCase):
    """The lookup table itself must stay complete and internally consistent."""

    def test_map_and_expected_counts_describe_the_same_labels(self):
        self.assertEqual(set(stage.VISIT_MAP), set(stage.EXPECTED_VISIT_ROWS))

    def test_every_enumerated_label_covers_the_three_training_trials(self):
        self.assertEqual({trial for trial, _ in stage.VISIT_MAP},
                         {'ASCENT2', 'CELGENE', 'EFC6546'})

    def test_only_cycle_start_and_within_cycle_carry_a_cycle_number(self):
        for (trial, label), (cycle, _, _, role) in stage.VISIT_MAP.items():
            with self.subTest(trial=trial, label=label):
                has_cycle = cycle is not None
                self.assertEqual(has_cycle, role in (stage.CYCLE_START, stage.WITHIN_CYCLE))

    def test_a_day_is_recorded_only_when_the_label_states_one(self):
        for (trial, label), (_, day, stated, _) in stage.VISIT_MAP.items():
            with self.subTest(trial=trial, label=label):
                self.assertEqual(stated, day is not None)


class ClassifyVisitTests(unittest.TestCase):
    """Translation must be exact, per trial, and must refuse to guess."""

    def test_the_three_vocabularies_agree_on_cycle_two(self):
        self.assertEqual(stage.classify_visit('CELGENE', 'CYCLE 2 DAY 1')[0], 2)
        self.assertEqual(stage.classify_visit('EFC6546', 'CYCLE 2')[0], 2)
        self.assertEqual(stage.classify_visit('ASCENT2', 'CYCLE #02')[0], 2)

    def test_only_celgene_states_the_day_for_cycle_two(self):
        self.assertEqual(stage.classify_visit('CELGENE', 'CYCLE 2 DAY 1')[1:3], (1, True))
        self.assertEqual(stage.classify_visit('EFC6546', 'CYCLE 2')[1:3], (None, False))
        self.assertEqual(stage.classify_visit('ASCENT2', 'CYCLE #02')[1:3], (None, False))

    def test_mid_cycle_measurement_is_not_a_cycle_start(self):
        cycle, day, stated, role = stage.classify_visit('CELGENE', 'CYCLE 1 DAY 14')
        self.assertEqual((cycle, day, stated), (1, 14, True))
        self.assertEqual(role, stage.WITHIN_CYCLE)
        self.assertEqual(stage.classify_visit('CELGENE', 'CYCLE 1 DAY 1')[3], stage.CYCLE_START)

    def test_pre_treatment_and_non_cycle_visits_receive_no_cycle_number(self):
        for trial, label, role in [('CELGENE', 'SCREENING', stage.PRE_TREATMENT),
                                   ('ASCENT2', 'PRE-ENROLLMENT', stage.PRE_TREATMENT),
                                   ('CELGENE', 'UNSCHEDULED', stage.UNSCHEDULED),
                                   ('CELGENE', 'TX PHASE DISCONTINUATION', stage.DISCONTINUATION),
                                   ('EFC6546', 'FOLLOW-UP 1', stage.FOLLOW_UP),
                                   ('EFC6546', 'VISIT 99', stage.UNRESOLVED)]:
            with self.subTest(label=label):
                cycle, day, _, actual = stage.classify_visit(trial, label)
                self.assertEqual((cycle, day, actual), (None, None, role))

    def test_unknown_label_is_refused_rather_than_parsed(self):
        for trial, label in [('CELGENE', 'CYCLE 6 DAY 1'), ('EFC6546', 'CYCLE 9'),
                             ('ASCENT2', 'CYCLE #11'), ('CELGENE', 'INVENTED VISIT')]:
            with self.subTest(label=label), self.assertRaises(stage.IntegrityError) as caught:
                stage.classify_visit(trial, label)
            self.assertEqual(str(caught.exception), 'UNKNOWN_VISIT_LABEL')

    def test_case_and_whitespace_variants_are_not_silently_normalized(self):
        for label in ['cycle 2 day 1', ' CYCLE 2 DAY 1', 'CYCLE 2 DAY 1 ', 'CYCLE  2 DAY 1']:
            with self.subTest(label=label), self.assertRaises(stage.IntegrityError):
                stage.classify_visit('CELGENE', label)

    def test_a_label_is_not_valid_for_a_trial_that_does_not_use_it(self):
        for trial, label in [('EFC6546', 'CYCLE 2 DAY 1'), ('CELGENE', 'CYCLE 2'),
                             ('CELGENE', 'PRE-ENROLLMENT'), ('ASCENT2', 'SCREENING')]:
            with self.subTest(trial=trial, label=label), self.assertRaises(stage.IntegrityError):
                stage.classify_visit(trial, label)


class BuildVisitIndexTests(unittest.TestCase):
    """End-to-end translation over invented laboratory rows."""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name) / 'extracted'
        self.keys = {('CELGENE', 'INVENTED-ONE'), ('EFC6546', 'INVENTED-TWO')}

    def write_lab(self, rows):
        path = self.root / 'training/LabValue_training.csv'
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open('w', encoding='utf-8', newline='') as stream:
            writer = csv.writer(stream)
            writer.writerow(['STUDYID', 'RPT', 'VISIT', 'LBSTRESN'])
            writer.writerows(rows)
        return path

    def test_every_input_row_receives_exactly_one_disposition(self):
        rows = [['CELGENE', 'INVENTED-ONE', 'SCREENING', '13.5'],
                ['CELGENE', 'INVENTED-ONE', 'CYCLE 1 DAY 1', '13.4'],
                ['CELGENE', 'INVENTED-ONE', 'CYCLE 1 DAY 14', '12.9'],
                ['EFC6546', 'INVENTED-TWO', 'CYCLE 2', '12.8']]
        self.write_lab(rows)
        expected = {('CELGENE', 'SCREENING'): 1, ('CELGENE', 'CYCLE 1 DAY 1'): 1,
                    ('CELGENE', 'CYCLE 1 DAY 14'): 1, ('EFC6546', 'CYCLE 2'): 1}
        index, report = stage.build_visit_index(self.root, self.keys, expected)
        self.assertEqual(len(index), len(rows))
        self.assertEqual(report['rows_read'], report['rows_assigned_a_disposition'])
        self.assertEqual(report['rows_dropped'], 0)
        self.assertFalse(report['laboratory_values_read_or_transformed'])

    def test_index_preserves_original_text_and_omits_laboratory_values(self):
        self.write_lab([['CELGENE', 'INVENTED-ONE', 'CYCLE 2 DAY 1', '12.8']])
        index, _ = stage.build_visit_index(self.root, self.keys, {('CELGENE', 'CYCLE 2 DAY 1'): 1})
        self.assertEqual(tuple(index[0]), stage.OUTPUT_FIELDS)
        self.assertEqual(index[0]['visit_original'], 'CYCLE 2 DAY 1')
        self.assertEqual(index[0]['cycle_number'], 2)
        self.assertEqual(index[0]['source_row'], 2)
        self.assertNotIn('LBSTRESN', index[0])

    def test_a_cycle_start_without_a_stated_day_is_counted_as_assumed(self):
        self.write_lab([['CELGENE', 'INVENTED-ONE', 'CYCLE 2 DAY 1', '1'],
                        ['EFC6546', 'INVENTED-TWO', 'CYCLE 2', '1']])
        _, report = stage.build_visit_index(
            self.root, self.keys, {('CELGENE', 'CYCLE 2 DAY 1'): 1, ('EFC6546', 'CYCLE 2'): 1})
        self.assertEqual(report['cycle_start_rows_with_day_assumed_not_stated'], {'EFC6546': 1})

    def test_mid_cycle_rows_are_excluded_from_cycle_start_counts(self):
        self.write_lab([['CELGENE', 'INVENTED-ONE', 'CYCLE 1 DAY 1', '1'],
                        ['CELGENE', 'INVENTED-ONE', 'CYCLE 1 DAY 14', '1']])
        _, report = stage.build_visit_index(
            self.root, self.keys, {('CELGENE', 'CYCLE 1 DAY 1'): 1, ('CELGENE', 'CYCLE 1 DAY 14'): 1})
        self.assertEqual(report['cycle_start_rows_by_trial_and_cycle'], {'CELGENE|cycle_1': 1})
        self.assertEqual(report['rows_by_trial_and_role']['CELGENE|within_cycle'], 1)

    def test_a_row_outside_the_stage01_roster_stops_the_stage(self):
        self.write_lab([['CELGENE', 'INVENTED-ABSENT', 'SCREENING', '1']])
        with self.assertRaises(stage.IntegrityError) as caught:
            stage.build_visit_index(self.root, self.keys, {('CELGENE', 'SCREENING'): 1})
        self.assertEqual(str(caught.exception), 'LAB_ROW_OUTSIDE_STAGE01_ROSTER')

    def test_a_changed_row_count_stops_the_stage(self):
        self.write_lab([['CELGENE', 'INVENTED-ONE', 'SCREENING', '1'],
                        ['CELGENE', 'INVENTED-ONE', 'SCREENING', '1']])
        with self.assertRaises(stage.IntegrityError) as caught:
            stage.build_visit_index(self.root, self.keys, {('CELGENE', 'SCREENING'): 1})
        self.assertEqual(str(caught.exception), 'VISIT_LABEL_COUNT_MISMATCH')

    def test_an_unenumerated_label_in_real_input_stops_the_stage(self):
        self.write_lab([['CELGENE', 'INVENTED-ONE', 'CYCLE 6 DAY 1', '1']])
        with self.assertRaises(stage.IntegrityError) as caught:
            stage.build_visit_index(self.root, self.keys, {('CELGENE', 'CYCLE 6 DAY 1'): 1})
        self.assertEqual(str(caught.exception), 'UNKNOWN_VISIT_LABEL')


class WriteIndexTests(unittest.TestCase):
    """The output must be private, non-overwriting and verified on read-back."""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.path = Path(self.tmp.name) / 'stage02_visit_index.csv'
        self.rows = [dict(zip(stage.OUTPUT_FIELDS,
                              (2, 'CELGENE', 'INVENTED-ONE', 'CYCLE 2 DAY 1', 2, 1, 'Y', stage.CYCLE_START)))]

    def test_output_is_created_private_and_reads_back_identically(self):
        stage.write_index(self.path, self.rows)
        self.assertEqual(stat.S_IMODE(os.stat(self.path).st_mode), 0o600)
        with self.path.open(encoding='utf-8', newline='') as stream:
            written = list(csv.DictReader(stream))
        self.assertEqual(written, [{k: str(v) for k, v in self.rows[0].items()}])

    def test_an_existing_output_is_never_overwritten(self):
        self.path.write_text('invented existing content', encoding='utf-8')
        with self.assertRaises(OSError):
            stage.write_index(self.path, self.rows)
        self.assertEqual(self.path.read_text(encoding='utf-8'), 'invented existing content')

    def test_an_empty_index_is_refused(self):
        with self.assertRaises(stage.IntegrityError) as caught:
            stage.write_index(self.path, [])
        self.assertEqual(str(caught.exception), 'EMPTY_VISIT_INDEX')

    def test_an_unexpected_output_schema_is_refused(self):
        with self.assertRaises(stage.IntegrityError) as caught:
            stage.write_index(self.path, [{'unexpected': 1}])
        self.assertEqual(str(caught.exception), 'UNEXPECTED_OUTPUT_SCHEMA')


if __name__ == '__main__':
    unittest.main()

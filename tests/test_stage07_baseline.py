"""Stage 07 tests. Every patient key and laboratory value here is invented.

A wrong starting value does not look like an error, it looks like a change that
never happened. So the tests check that a baseline is only ever taken from
stated evidence, that a contradiction produces no baseline rather than a coin
toss, that the fallback is the draw nearest the first dose and never one taken
after it, and that a baseline is never defined by a visit's name.
"""
import csv
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src/preparation'))
import stage04_roles as stage04
import stage07_baseline as stage


def measurement(source_row, day, value, flag='', usable='Y', kind='numeric',
                purpose=stage04.BASELINE_CANDIDATE):
    """Return one invented Stage 06 measurement row carrying a baseline flag."""
    return {'source_row': source_row, 'STUDYID': 'CELGENE', 'RPT': 'INVENTED-ONE',
            'test_code': 'HB', 'test_unit': 'G/DL', 'visit_original': 'SCREENING',
            'analysis_purpose': purpose, 'cycle_number': '', 'recorded_day': day,
            'value_kind': kind, 'analysis_value': value, 'bound_direction': '',
            'bound_value': '', 'repeat_status': 'single', 'usable_measurement': usable,
            'baseline_flag': flag}


class UsableCandidateTests(unittest.TestCase):
    """Only a real, placed, accepted measurement can start a trajectory."""

    def test_an_accepted_number_with_a_day_is_a_candidate(self):
        self.assertEqual(len(stage.usable_candidates([measurement(2, '-7', '13.5')])), 1)

    def test_a_measurement_without_a_day_is_not_a_candidate(self):
        self.assertEqual(stage.usable_candidates([measurement(2, '', '13.5')]), [])

    def test_a_row_stage06_did_not_accept_is_not_a_candidate(self):
        self.assertEqual(stage.usable_candidates([measurement(2, '-7', '13.5', usable='N')]), [])

    def test_a_bounded_or_absent_entry_is_not_a_candidate(self):
        for kind in ('bounded', 'absent', 'non_numeric_text'):
            with self.subTest(kind=kind):
                self.assertEqual(stage.usable_candidates(
                    [measurement(2, '-7', '', kind=kind, usable='N')]), [])


class ChooseBaselineTests(unittest.TestCase):
    """The ordered rules, one situation at a time."""

    def test_the_sources_own_flag_is_preferred(self):
        rows = [measurement(2, '-10', '13.8'), measurement(3, '-3', '13.5', flag='Y')]
        chosen, source = stage.choose_baseline(rows)
        self.assertEqual(source, stage.FROM_SPONSOR_FLAG)
        self.assertEqual(chosen['analysis_value'], '13.5')

    def test_a_flagged_row_on_a_cycle_visit_is_still_the_baseline(self):
        rows = [measurement(2, '-8', '13.8'),
                measurement(3, '0', '13.4', flag='Y', purpose=stage04.CYCLE_MEASUREMENT)]
        chosen, source = stage.choose_baseline(rows)
        self.assertEqual(source, stage.FROM_SPONSOR_FLAG)
        self.assertEqual(chosen['baseline_day'] if 'baseline_day' in chosen else chosen['recorded_day'], '0')

    def test_two_flags_agreeing_are_one_answer_recorded_twice(self):
        rows = [measurement(2, '-3', '13.5', flag='Y'), measurement(3, '-3', '13.5', flag='Y')]
        chosen, source = stage.choose_baseline(rows)
        self.assertEqual(source, stage.FROM_SPONSOR_FLAG)
        self.assertEqual(chosen['source_row'], 2)

    def test_two_flags_disagreeing_produce_no_baseline_rather_than_a_guess(self):
        rows = [measurement(2, '-3', '13.5', flag='Y'), measurement(3, '-3', '11.1', flag='Y')]
        chosen, source = stage.choose_baseline(rows)
        self.assertIsNone(chosen)
        self.assertEqual(source, stage.NO_BASELINE_CONFLICTING_FLAGS)

    def test_without_a_flag_the_fallback_is_the_draw_nearest_the_first_dose(self):
        rows = [measurement(2, '-21', '13.9'), measurement(3, '-3', '13.5'),
                measurement(4, '-14', '13.7')]
        chosen, source = stage.choose_baseline(rows)
        self.assertEqual(source, stage.FROM_FALLBACK)
        self.assertEqual(chosen['analysis_value'], '13.5')

    def test_a_measurement_on_the_first_treatment_day_may_serve_as_the_baseline(self):
        rows = [measurement(2, '0', '13.4', purpose=stage04.CYCLE_MEASUREMENT)]
        chosen, source = stage.choose_baseline(rows)
        self.assertEqual(source, stage.FROM_FALLBACK)
        self.assertEqual(chosen['recorded_day'], '0')

    def test_the_fallback_never_takes_a_measurement_after_treatment_started(self):
        rows = [measurement(2, '21', '12.8', purpose=stage04.CYCLE_MEASUREMENT)]
        chosen, source = stage.choose_baseline(rows)
        self.assertIsNone(chosen)
        self.assertEqual(source, stage.NO_BASELINE_NO_EVIDENCE)

    def test_no_usable_measurement_at_all_produces_no_baseline(self):
        rows = [measurement(2, '-7', '', kind='absent', usable='N')]
        chosen, source = stage.choose_baseline(rows)
        self.assertIsNone(chosen)
        self.assertEqual(source, stage.NO_BASELINE_NO_EVIDENCE)

    def test_a_flag_on_an_unusable_row_does_not_win(self):
        rows = [measurement(2, '-7', '', flag='Y', kind='absent', usable='N'),
                measurement(3, '-3', '13.5')]
        chosen, source = stage.choose_baseline(rows)
        self.assertEqual(source, stage.FROM_FALLBACK)
        self.assertEqual(chosen['analysis_value'], '13.5')

    def test_a_tie_on_the_same_day_is_broken_deterministically(self):
        rows = [measurement(3, '-3', '13.5'), measurement(2, '-3', '13.6')]
        first, _ = stage.choose_baseline(rows)
        second, _ = stage.choose_baseline(list(reversed(rows)))
        self.assertEqual(first['source_row'], second['source_row'])


class BuildBaselinesTests(unittest.TestCase):
    """End-to-end over an invented source file and Stage 06 measurements."""

    FIELDS = ['STUDYID', 'RPT', 'LBTESTCD', 'LBTEST', 'LBBLFL']

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name) / 'extracted'

    def build(self, source_rows, measurements):
        path = self.root / 'training/LabValue_training.csv'
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open('w', encoding='utf-8', newline='') as stream:
            writer = csv.writer(stream)
            writer.writerow(self.FIELDS)
            writer.writerows(source_rows)
        return stage.build_baselines(self.root, measurements)

    def test_one_baseline_row_is_produced_per_patient_and_test(self):
        source = [['CELGENE', 'INVENTED-ONE', 'HB', 'HEMOGLOBIN', 'Y'],
                  ['CELGENE', 'INVENTED-ONE', 'HB', 'HEMOGLOBIN', ''],
                  ['CELGENE', 'INVENTED-ONE', 'WBC', 'WHITE CELLS', 'Y']]
        m = {2: measurement(2, '-3', '13.5'), 3: measurement(3, '21', '12.8'),
             4: dict(measurement(4, '-3', '5.2'), test_code='WBC')}
        baselines, report = self.build(source, m)
        self.assertEqual(len(baselines), 2)
        self.assertEqual(report['patient_test_combinations'], 2)
        self.assertEqual(report['baselines_established'], 2)
        self.assertEqual(report['values_edited'], 0)
        self.assertEqual(report['baselines_invented_where_evidence_was_absent'], 0)

    def test_a_combination_with_no_evidence_is_recorded_without_a_value(self):
        source = [['CELGENE', 'INVENTED-ONE', 'HB', 'HEMOGLOBIN', '']]
        m = {2: measurement(2, '21', '12.8', purpose=stage04.CYCLE_MEASUREMENT)}
        baselines, report = self.build(source, m)
        self.assertEqual(baselines[0]['baseline_value'], '')
        self.assertEqual(baselines[0]['baseline_source'], stage.NO_BASELINE_NO_EVIDENCE)
        self.assertEqual(report['baselines_not_established'], 1)

    def test_the_recovered_sodium_code_is_grouped_under_its_resolved_name(self):
        source = [['CELGENE', 'INVENTED-ONE', '.', 'SODIUM', 'Y']]
        m = {2: dict(measurement(2, '-3', '140'), test_code='SODIUM')}
        baselines, _ = self.build(source, m)
        self.assertEqual(baselines[0]['test_code'], 'SODIUM')

    def test_a_flag_recorded_after_the_first_dose_is_counted(self):
        source = [['CELGENE', 'INVENTED-ONE', 'HB', 'HEMOGLOBIN', 'Y']]
        m = {2: measurement(2, '21', '12.8', flag='Y', purpose=stage04.CYCLE_MEASUREMENT)}
        _, report = self.build(source, m)
        self.assertEqual(report['baseline_flag_rows_recorded_after_the_first_dose'], 1)

    def test_a_misaligned_measurement_table_stops_the_stage(self):
        source = [['CELGENE', 'INVENTED-ONE', 'HB', 'HEMOGLOBIN', '']]
        m = {2: dict(measurement(2, '-3', '13.5'), test_code='WBC')}
        with self.assertRaises(stage.IntegrityError) as caught:
            self.build(source, m)
        self.assertEqual(str(caught.exception), 'MEASUREMENT_ROW_MISALIGNED')

    def test_a_source_row_absent_from_the_measurements_stops_the_stage(self):
        source = [['CELGENE', 'INVENTED-ONE', 'HB', 'HEMOGLOBIN', '']]
        with self.assertRaises(stage.IntegrityError) as caught:
            self.build(source, {})
        self.assertEqual(str(caught.exception), 'MEASUREMENT_ROW_MISSING')


class WriteBaselinesTests(unittest.TestCase):
    """The output is written under the same rules as every other stage."""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.path = Path(self.tmp.name) / 'stage07_baselines.csv'
        self.rows = [dict(zip(stage.OUTPUT_FIELDS,
                              ('CELGENE', 'INVENTED-ONE', 'HB', 'G/DL', '13.5', '-3',
                               stage.FROM_SPONSOR_FLAG, 2, 1, 1)))]

    def test_the_table_reads_back_identically(self):
        stage.write_baselines(self.path, self.rows)
        with self.path.open(encoding='utf-8', newline='') as stream:
            self.assertEqual(list(csv.DictReader(stream)),
                             [{k: str(v) for k, v in self.rows[0].items()}])

    def test_an_existing_table_is_never_overwritten(self):
        self.path.write_text('invented existing content', encoding='utf-8')
        with self.assertRaises(OSError):
            stage.write_baselines(self.path, self.rows)


if __name__ == '__main__':
    unittest.main()

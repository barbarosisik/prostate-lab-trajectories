"""Stage 04 tests. Every patient key and row here is invented.

The central risks are that an excluded row is quietly deleted, that a row is
excluded without a stated reason, that the ordered rules give two rows in the
same situation different treatment, and that a row with no usable date is
allowed into a trajectory anyway.
"""
import csv
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src/preparation'))
import stage02_visits as stage02
import stage03_timing as stage03
import stage04_roles as stage


def flags(**overrides) -> dict:
    """Return a clean Stage 03 flag row, with named flags switched on."""
    row = {field: 'N' for field in stage03.FLAG_FIELDS}
    row.update({field: 'Y' for field in overrides})
    return row


class AssignPurposeTests(unittest.TestCase):
    """The ordered rule set, checked one branch at a time."""

    def test_a_verified_cycle_start_becomes_a_cycle_measurement(self):
        self.assertEqual(stage.assign_purpose(stage02.CYCLE_START, '21', flags()),
                         (stage.CYCLE_MEASUREMENT, ''))

    def test_a_pre_treatment_row_before_the_first_dose_becomes_a_baseline_candidate(self):
        self.assertEqual(stage.assign_purpose(stage02.PRE_TREATMENT, '-7', flags()),
                         (stage.BASELINE_CANDIDATE, ''))

    def test_a_pre_treatment_row_at_or_after_the_first_dose_is_excluded_with_a_reason(self):
        purpose, reason = stage.assign_purpose(
            stage02.PRE_TREATMENT, '0', flags(pre_treatment_not_before_day_zero=True))
        self.assertEqual(purpose, stage.EXCLUDED)
        self.assertEqual(reason, stage.PRE_TREATMENT_NOT_BEFORE_FIRST_DOSE)

    def test_a_mid_cycle_row_keeps_its_own_purpose_and_is_never_a_cycle_start(self):
        self.assertEqual(stage.assign_purpose(stage02.WITHIN_CYCLE, '14', flags()),
                         (stage.MID_CYCLE_MEASUREMENT, ''))

    def test_context_roles_are_retained_rather_than_excluded(self):
        for role in stage.CONTEXT_ROLES:
            with self.subTest(role=role):
                self.assertEqual(stage.assign_purpose(role, '40', flags()), (stage.CONTEXT_ONLY, ''))

    def test_a_context_row_is_kept_even_with_no_recorded_day(self):
        self.assertEqual(stage.assign_purpose(stage02.UNSCHEDULED, '', flags(day_missing=True)),
                         (stage.CONTEXT_ONLY, ''))

    def test_an_unresolved_visit_is_excluded_before_any_other_rule(self):
        purpose, reason = stage.assign_purpose(stage02.UNRESOLVED, '21', flags())
        self.assertEqual((purpose, reason), (stage.EXCLUDED, stage.VISIT_MEANING_NOT_ESTABLISHED))

    def test_a_row_without_a_usable_date_never_reaches_a_trajectory(self):
        for role in (stage02.CYCLE_START, stage02.PRE_TREATMENT, stage02.WITHIN_CYCLE):
            with self.subTest(role=role):
                self.assertEqual(stage.assign_purpose(role, '', flags(day_missing=True)),
                                 (stage.EXCLUDED, stage.NO_RECORDED_DAY))
                self.assertEqual(stage.assign_purpose(role, '900', flags(alternate_reference_origin=True)),
                                 (stage.EXCLUDED, stage.ALTERNATE_TIME_ORIGIN))

    def test_timing_failures_are_reported_by_their_own_reason(self):
        self.assertEqual(stage.assign_purpose(stage02.CYCLE_START, '65', flags(off_schedule=True)),
                         (stage.EXCLUDED, stage.CYCLE_DAY_OFF_SCHEDULE))
        self.assertEqual(stage.assign_purpose(stage02.CYCLE_START, '20', flags(cycle_order_violation=True)),
                         (stage.EXCLUDED, stage.CYCLE_ORDER_VIOLATION))

    def test_an_order_violation_outranks_an_off_schedule_day(self):
        purpose, reason = stage.assign_purpose(
            stage02.CYCLE_START, '20', flags(off_schedule=True, cycle_order_violation=True))
        self.assertEqual((purpose, reason), (stage.EXCLUDED, stage.CYCLE_ORDER_VIOLATION))

    def test_every_exclusion_carries_a_reason_and_every_inclusion_carries_none(self):
        cases = [(stage02.CYCLE_START, flags()), (stage02.PRE_TREATMENT, flags()),
                 (stage02.WITHIN_CYCLE, flags()), (stage02.UNSCHEDULED, flags()),
                 (stage02.UNRESOLVED, flags()), (stage02.CYCLE_START, flags(day_missing=True)),
                 (stage02.CYCLE_START, flags(off_schedule=True))]
        for role, flag in cases:
            with self.subTest(role=role, flag=flag):
                purpose, reason = stage.assign_purpose(role, '21', flag)
                self.assertEqual(bool(reason), purpose == stage.EXCLUDED)

    def test_every_stage02_role_is_handled(self):
        for role in (stage02.PRE_TREATMENT, stage02.CYCLE_START, stage02.WITHIN_CYCLE,
                     stage02.UNSCHEDULED, stage02.DISCONTINUATION, stage02.FOLLOW_UP,
                     stage02.UNRESOLVED):
            with self.subTest(role=role):
                purpose, _ = stage.assign_purpose(role, '21', flags())
                self.assertIn(purpose, (stage.BASELINE_CANDIDATE, stage.CYCLE_MEASUREMENT,
                                        stage.MID_CYCLE_MEASUREMENT, stage.CONTEXT_ONLY, stage.EXCLUDED))

    def test_an_unknown_role_stops_the_stage_rather_than_defaulting(self):
        with self.assertRaises(stage.IntegrityError) as caught:
            stage.assign_purpose('invented_role', '21', flags())
        self.assertEqual(str(caught.exception), 'UNHANDLED_VISIT_ROLE')


class BuildRolesTests(unittest.TestCase):
    """End-to-end assignment over invented Stage 03 flag rows."""

    def timing_row(self, line, trial, patient, visit, role, cycle, day, **flag_overrides):
        row = {'source_row': str(line), 'STUDYID': trial, 'RPT': patient,
               'visit_original': visit, 'visit_role': role,
               'cycle_number': '' if cycle is None else str(cycle), 'recorded_day': day,
               'reference_origin': stage03.PRIMARY_REFERENCE, 'expected_day': '',
               'schedule_deviation_days': '', 'usable_for_cycle_analysis': 'Y'}
        row.update(flags(**flag_overrides))
        return row

    def test_no_row_is_deleted_and_every_row_carries_a_purpose(self):
        timing = {
            2: self.timing_row(2, 'CELGENE', 'INVENTED-ONE', 'SCREENING', stage02.PRE_TREATMENT, None, '-7'),
            3: self.timing_row(3, 'CELGENE', 'INVENTED-ONE', 'CYCLE 2 DAY 1', stage02.CYCLE_START, 2, '21'),
            4: self.timing_row(4, 'CELGENE', 'INVENTED-ONE', 'UNSCHEDULED', stage02.UNSCHEDULED, None, '30'),
            5: self.timing_row(5, 'EFC6546', 'INVENTED-TWO', 'VISIT 99', stage02.UNRESOLVED, None, '10'),
        }
        rows, report = stage.build_roles(timing)
        self.assertEqual(report['rows_read'], 4)
        self.assertEqual(report['rows_deleted'], 0)
        self.assertEqual(report['rows_assigned_a_purpose'], 4)
        self.assertTrue(report['excluded_rows_retained_in_output'])
        self.assertEqual(len(rows), len(timing))
        self.assertTrue(all(r['analysis_purpose'] for r in rows))

    def test_excluded_rows_stay_in_the_output_with_their_reason(self):
        timing = {2: self.timing_row(2, 'EFC6546', 'INVENTED-TWO', 'CYCLE 2',
                                     stage02.CYCLE_START, 2, '65', off_schedule=True)}
        rows, report = stage.build_roles(timing)
        self.assertEqual(rows[0]['analysis_purpose'], stage.EXCLUDED)
        self.assertEqual(rows[0]['exclusion_reason'], stage.CYCLE_DAY_OFF_SCHEDULE)
        self.assertEqual(rows[0]['cycle_number'], '2')
        self.assertEqual(report['excluded_rows_by_trial_and_reason'],
                         {f'EFC6546|{stage.CYCLE_DAY_OFF_SCHEDULE}': 1})

    def test_patients_are_counted_once_per_purpose_not_once_per_row(self):
        timing = {2: self.timing_row(2, 'CELGENE', 'INVENTED-ONE', 'CYCLE 2 DAY 1', stage02.CYCLE_START, 2, '21'),
                  3: self.timing_row(3, 'CELGENE', 'INVENTED-ONE', 'CYCLE 2 DAY 1', stage02.CYCLE_START, 2, '21'),
                  4: self.timing_row(4, 'CELGENE', 'INVENTED-TWO', 'CYCLE 2 DAY 1', stage02.CYCLE_START, 2, '21')}
        _, report = stage.build_roles(timing)
        self.assertEqual(report['patients_by_purpose'][stage.CYCLE_MEASUREMENT], 2)
        self.assertEqual(report['cycle_measurement_patients_by_trial_and_cycle'], {'CELGENE|cycle_2': 2})
        self.assertEqual(report['rows_by_trial_and_purpose'][f'CELGENE|{stage.CYCLE_MEASUREMENT}'], 3)

    def test_output_rows_are_ordered_by_source_row(self):
        timing = {5: self.timing_row(5, 'CELGENE', 'INVENTED-ONE', 'SCREENING', stage02.PRE_TREATMENT, None, '-7'),
                  2: self.timing_row(2, 'CELGENE', 'INVENTED-ONE', 'CYCLE 2 DAY 1', stage02.CYCLE_START, 2, '21')}
        rows, _ = stage.build_roles(timing)
        self.assertEqual([r['source_row'] for r in rows], [2, 5])
        self.assertEqual(tuple(rows[0]), stage.OUTPUT_FIELDS)


class WriteRolesTests(unittest.TestCase):
    """The output must be private, non-overwriting and verified on read-back."""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.path = Path(self.tmp.name) / 'stage04_analysis_roles.csv'
        self.rows = [dict(zip(stage.OUTPUT_FIELDS,
                              (2, 'CELGENE', 'INVENTED-ONE', 'CYCLE 2 DAY 1',
                               stage02.CYCLE_START, 2, 21.0, stage.CYCLE_MEASUREMENT, '')))]

    def test_output_is_created_private_and_reads_back_identically(self):
        stage.write_roles(self.path, self.rows)
        with self.path.open(encoding='utf-8', newline='') as stream:
            self.assertEqual(list(csv.DictReader(stream)),
                             [{k: str(v) for k, v in self.rows[0].items()}])

    def test_an_existing_output_is_never_overwritten(self):
        self.path.write_text('invented existing content', encoding='utf-8')
        with self.assertRaises(OSError):
            stage.write_roles(self.path, self.rows)

    def test_an_unexpected_output_schema_is_refused(self):
        with self.assertRaises(stage.IntegrityError) as caught:
            stage.write_roles(self.path, [{'unexpected': 1}])
        self.assertEqual(str(caught.exception), 'UNEXPECTED_OUTPUT_SCHEMA')


if __name__ == '__main__':
    unittest.main()

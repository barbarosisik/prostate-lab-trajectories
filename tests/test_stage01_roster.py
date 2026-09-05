"""Stage 01 failure cases use invented records only."""
import csv
import hashlib
import io
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch
import zipfile

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src/preparation'))
import stage01_roster as stage


class Stage01Tests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.run = Path(self.tmp.name)
        self.root = self.run / 'extracted'
        self.core = self.root / 'training/CoreTable_training.csv'
        self.lab = self.root / 'training/LabValue_training.csv'
        self.write(self.core, ['STUDYID', 'RPT', 'DEATH', 'LKADT_P'],
                   [['ASCENT2', 'INVENTED-ONE', '', '100'], ['ASCENT2', 'INVENTED-TWO', 'YES', '50']])
        for table in stage.EVENT_TABLES:
            self.write(self.root / f'training/{table}_training.csv', ['STUDYID', 'RPT'],
                       [['ASCENT2', 'INVENTED-ONE'], ['ASCENT2', 'INVENTED-ONE']])
        for partition, suffix in [('leaderboard', 'leaderboard'), ('finalscoringset', 'validation')]:
            self.write(self.root / partition / f'CoreTable_{suffix}.csv',
                       ['STUDYID', 'RPT', 'DEATH', 'LKADT_P'], [['AZ', f'INVENTED-{suffix}', '', '']])
            for table in stage.EVENT_TABLES:
                self.write(self.root / partition / f'{table}_{suffix}.csv', ['STUDYID', 'RPT'], [])

    def write(self, path, columns, rows):
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open('w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(columns)
            writer.writerows(rows)

    def build(self):
        return stage.build_roster(self.root, {'ASCENT2': 2})

    def test_keeps_incomplete_patient_and_many_to_one_events(self):
        before = {p: stage.digest(p) for p in self.root.rglob('*.csv')}
        roster, report = self.build()
        self.assertEqual(len(roster), 2)
        self.assertEqual(roster[0]['LabValue_rows'], 2)
        self.assertEqual(roster[1]['LabValue_rows'], 0)
        self.assertEqual(report['death_blank_preserved'], 1)
        self.assertEqual(report['join_checks']['LabValue']['patients_without_rows'], 1)
        self.assertNotIn('INVENTED-', json.dumps(report))
        self.assertEqual(before, {p: stage.digest(p) for p in before})

    def test_duplicate_core_key_blocks_instead_of_deduplicating(self):
        with self.core.open('a') as f:
            f.write('ASCENT2,INVENTED-ONE,,100\n')
        with self.assertRaisesRegex(stage.IntegrityError, '^DUPLICATE_CORE_KEY$'):
            self.build()

    def test_unmatched_event_blocks(self):
        with self.lab.open('a') as f:
            f.write('ASCENT2,INVENTED-UNKNOWN\n')
        with self.assertRaisesRegex(stage.IntegrityError, '^UNMATCHED_EVENT_KEY$'):
            self.build()

    def test_trial_part_of_join_key(self):
        self.write(self.lab, ['STUDYID', 'RPT'], [['CELGENE', 'INVENTED-ONE']])
        with self.assertRaisesRegex(stage.IntegrityError, '^UNMATCHED_EVENT_KEY$'):
            self.build()

    def test_blank_and_padded_keys_block(self):
        for bad in ['', ' INVENTED-ONE', 'INVENTED-ONE ']:
            with self.subTest(bad=bad):
                self.write(self.lab, ['STUDYID', 'RPT'], [['ASCENT2', bad]])
                with self.assertRaisesRegex(stage.IntegrityError, '^BLANK_OR_PADDED_JOIN_KEY$'):
                    self.build()

    def test_schema_and_ragged_rows_block_without_disclosing_values(self):
        for body, code in [('STUDYID,RPT,RPT\nASCENT2,A,A\n', 'INVALID_SCHEMA'),
                           ('STUDYID\nASCENT2\n', 'INVALID_SCHEMA'),
                           ('STUDYID,RPT\nASCENT2,A,SECRET\n', 'RAGGED_CSV_RECORD'),
                           ('STUDYID,RPT\nASCENT2\n', 'RAGGED_CSV_RECORD')]:
            with self.subTest(code=code):
                self.lab.write_text(body)
                with self.assertRaisesRegex(stage.IntegrityError, f'^{code}$'):
                    self.build()

    def test_invalid_followup_and_changed_outcome_codes_block(self):
        for death, day, code in [('', '-1', 'INVALID_FOLLOWUP_DAY'),
                                 ('', 'NaN', 'INVALID_FOLLOWUP_DAY'),
                                 ('', 'Infinity', 'INVALID_FOLLOWUP_DAY'),
                                 ('', 'bad', 'INVALID_FOLLOWUP_DAY'),
                                 ('', '', 'OUTCOME_AVAILABILITY_CHANGED'),
                                 ('NO', '100', 'OUTCOME_AVAILABILITY_CHANGED')]:
            with self.subTest(death=death, day=day):
                self.write(self.core, ['STUDYID', 'RPT', 'DEATH', 'LKADT_P'],
                           [['ASCENT2', 'INVENTED-ONE', death, day], ['ASCENT2', 'INVENTED-TWO', 'YES', '50']])
                with self.assertRaisesRegex(stage.IntegrityError, f'^{code}$'):
                    self.build()

    def test_unexpected_trial_and_count_drift_block(self):
        with self.assertRaisesRegex(stage.IntegrityError, '^TRAINING_ROSTER_COUNT_MISMATCH$'):
            stage.build_roster(self.root, {'ASCENT2': 3})
        self.core.write_text(self.core.read_text().replace('ASCENT2', 'AZ'))
        with self.assertRaisesRegex(stage.IntegrityError, '^UNEXPECTED_TRAINING_TRIAL$'):
            self.build()

    def test_evaluation_labels_never_enter_training(self):
        p = self.root / 'leaderboard/CoreTable_leaderboard.csv'
        self.write(p, ['STUDYID', 'RPT', 'DEATH', 'LKADT_P'], [['AZ', 'INVENTED-THREE', 'YES', '100']])
        with self.assertRaisesRegex(stage.IntegrityError, '^EVALUATION_LABEL_AVAILABILITY_CHANGED$'):
            self.build()

    def test_duplicate_evaluation_keys_block(self):
        p = self.root / 'finalscoringset/CoreTable_validation.csv'
        self.write(p, ['STUDYID', 'RPT', 'DEATH', 'LKADT_P'], [['AZ', 'INVENTED-leaderboard', '', '']])
        with self.assertRaisesRegex(stage.IntegrityError, '^DUPLICATE_OR_OVERLAPPING_PARTITION_KEY$'):
            self.build()

    def test_literal_dot_outcomes_are_missing_not_observed_labels(self):
        p = self.root / 'leaderboard/CoreTable_leaderboard.csv'
        self.write(p, ['STUDYID', 'RPT', 'DEATH', 'LKADT_P'], [['AZ', 'INVENTED-THREE', '.', '.']])
        roster, report = self.build()
        self.assertEqual(len(roster), 2)
        self.assertEqual(report['excluded_partitions']['leaderboard']['literal_dot_missing_counts'], {'DEATH': 1, 'LKADT_P': 1})

    def test_output_roundtrip_permissions_and_no_overwrite(self):
        roster, _ = self.build()
        output = self.run / 'roster.csv'
        checksum = stage.write_roster(output, roster)
        self.assertEqual(output.stat().st_mode & 0o777, 0o600)
        with self.assertRaises(FileExistsError):
            stage.write_roster(output, roster)
        self.assertEqual(stage.digest(output), checksum)

    def test_symlink_input_rejected(self):
        target = self.run / 'original.csv'
        self.lab.rename(target)
        self.lab.symlink_to(target)
        with self.assertRaisesRegex(stage.IntegrityError, '^INPUT_NOT_REGULAR_FILE$'):
            self.build()

    def test_legacy_text_bytes_do_not_corrupt_ascii_joins(self):
        self.lab.write_bytes(b'STUDYID,RPT,TEXT\nASCENT2,INVENTED-ONE,"caf\xe9,\nlegacy text"\n')
        before = self.lab.read_bytes()
        roster, report = self.build()
        self.assertEqual(report['join_checks']['LabValue']['rows'], 1)
        self.assertEqual(self.lab.read_bytes(), before)
        self.assertEqual(roster[0]['LabValue_rows'], 1)

    def test_non_ascii_keys_block_instead_of_guessing_encoding(self):
        self.lab.write_bytes(b'STUDYID,RPT\nASCENT2,INVENTED-\xe9\n')
        with self.assertRaisesRegex(stage.IntegrityError, '^NON_ASCII_JOIN_KEY$'):
            self.build()

    def test_utf8_bom_header_supported(self):
        self.lab.write_bytes(b'\xef\xbb\xbf' + self.lab.read_bytes())
        self.assertEqual(self.build()[1]['join_checks']['LabValue']['rows'], 2)

    def test_cli_rejects_unregistered_output_location(self):
        process = subprocess.run([sys.executable, stage.__file__, '--run-root', str(self.run)],
                                 capture_output=True, text=True)
        self.assertEqual(process.returncode, 1)
        self.assertEqual(json.loads(process.stdout)['error_code'], 'UNREGISTERED_RUN_ROOT')
        self.assertEqual(process.stderr, '')

    def test_archive_verification_detects_tampered_csv(self):
        source = self.run / 'source/AllProvidedFiles_149.zip'
        source.parent.mkdir()
        with zipfile.ZipFile(source, 'w') as outer:
            for partition in ('training', 'leaderboard', 'finalscoringset'):
                buffer = io.BytesIO()
                with zipfile.ZipFile(buffer, 'w') as nested:
                    for p in (self.root / partition).glob('*.csv'):
                        nested.writestr(p.name, p.read_bytes())
                outer.writestr(f'prostate_cancer_challenge_data_{partition}.zip', buffer.getvalue())
        with patch.object(stage, 'SOURCE_SHA256', stage.digest(source)):
            self.assertEqual(len(stage.verify_archive(self.run)), 18)
            self.lab.write_text(self.lab.read_text() + '\n')
            with self.assertRaisesRegex(stage.IntegrityError, '^EXTRACTED_FILE_HASH_MISMATCH$'):
                stage.verify_archive(self.run)


if __name__ == '__main__':
    unittest.main()

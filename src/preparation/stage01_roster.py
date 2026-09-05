"""Freeze the DREAM training roster without transforming laboratory values.

Only the CLI writes restricted data. It accepts the registered local run only,
verifies CSV bytes against the pinned ZIP, and writes one new mode-600 roster.
Errors contain fixed codes, never source rows, identifiers, or result values.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import os
from collections import Counter
from decimal import Decimal, InvalidOperation
from pathlib import Path
import zipfile

REGISTERED_RUN = Path('/Users/barbarosisik/PDS-Restricted-Work/prostate-lab-trajectories/runs/2026-09-04-audit-001')
SOURCE_SHA256 = 'ab3eca19c5d0cc4106c96ac04e665dd1a5c9df58f66328ecd24e8e1067932391'
TRIAL_COUNTS = {'ASCENT2': 476, 'CELGENE': 526, 'EFC6546': 598}
EVENT_TABLES = ('LabValue', 'LesionMeasure', 'MedHistory', 'PriorMed', 'VitalSign')


class IntegrityError(Exception):
    """A fixed, disclosure-safe failure code."""


def digest(path: Path) -> str:
    """Return a file's SHA-256 without loading or displaying its contents."""
    with path.open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def records(path: Path, required: set[str]):
    """Yield (logical CSV row number, raw fields) after structural checks.

    Required headers, unique column names and equal record lengths are
    enforced. Legacy text bytes remain reversible; this function does not
    infer units, replace missing values, or decode free-text semantics.
    """
    if path.is_symlink() or not path.is_file():
        raise IntegrityError('INPUT_NOT_REGULAR_FILE')
    # Stage 01 consumes ASCII keys only. Latin-1 maps every byte reversibly,
    # allowing CSV parsing of legacy free text without replacement characters
    # or a guess about its semantic encoding. Later text cleaning needs its
    # own encoding audit. Original files are never re-encoded.
    with path.open(encoding='latin-1', newline='') as stream:
        reader = csv.DictReader(stream)
        fields = reader.fieldnames
        if fields and fields[0].startswith('\xef\xbb\xbf'):
            fields[0] = fields[0][3:]
        if not fields or len(fields) != len(set(fields)) or not required <= set(fields):
            raise IntegrityError('INVALID_SCHEMA')
        for line, row in enumerate(reader, 2):
            if None in row or any(value is None for value in row.values()):
                raise IntegrityError('RAGGED_CSV_RECORD')
            yield line, row


def key(row: dict[str, str]) -> tuple[str, str]:
    """Return the exact (trial, patient) join key, rejecting ambiguous keys.

    Whitespace is not stripped silently and non-ASCII keys are rejected so
    the byte-preserving input parser cannot change patient identity.
    """
    parts = (row['STUDYID'], row['RPT'])
    if any(not value or value != value.strip() for value in parts):
        raise IntegrityError('BLANK_OR_PADDED_JOIN_KEY')
    if any(not value.isascii() for value in parts):
        raise IntegrityError('NON_ASCII_JOIN_KEY')
    return parts


def build_roster(extracted: Path, expected_counts=None):
    """Read keys and count joins. Preserve every eligible training patient.

    This intentionally does not impose lab completeness, assign cycles, or
    recode death blanks. Event rows are many-to-one joins to the core roster.
    """
    expected = TRIAL_COUNTS if expected_counts is None else expected_counts
    roster = {}
    trials = Counter()
    death_yes = death_blank = other_death = missing_followup = 0
    for line, row in records(extracted / 'training/CoreTable_training.csv',
                             {'STUDYID', 'RPT', 'DEATH', 'LKADT_P'}):
        patient = key(row)
        if patient in roster:
            raise IntegrityError('DUPLICATE_CORE_KEY')
        if patient[0] not in expected:
            raise IntegrityError('UNEXPECTED_TRAINING_TRIAL')
        trials[patient[0]] += 1
        death_yes += row['DEATH'] == 'YES'
        death_blank += row['DEATH'] == ''
        other_death += row['DEATH'] not in ('YES', '')
        if row['LKADT_P'] == '':
            missing_followup += 1
        else:
            try:
                day = Decimal(row['LKADT_P'])
            except InvalidOperation:
                raise IntegrityError('INVALID_FOLLOWUP_DAY') from None
            if not day.is_finite() or day < 0:
                raise IntegrityError('INVALID_FOLLOWUP_DAY')
        roster[patient] = {'STUDYID': patient[0], 'RPT': patient[1],
                           'partition': 'training', 'source_core_row': line,
                           **{f'{table}_rows': 0 for table in EVENT_TABLES}}
    if dict(trials) != expected:
        raise IntegrityError('TRAINING_ROSTER_COUNT_MISMATCH')
    if other_death or missing_followup:
        raise IntegrityError('OUTCOME_AVAILABILITY_CHANGED')

    joins = {}
    for table in EVENT_TABLES:
        rows = 0
        patients = set()
        for _, row in records(extracted / f'training/{table}_training.csv', {'STUDYID', 'RPT'}):
            patient = key(row)
            if patient not in roster:
                raise IntegrityError('UNMATCHED_EVENT_KEY')
            roster[patient][f'{table}_rows'] += 1
            rows += 1
            patients.add(patient)
        joins[table] = {'rows': rows, 'matched_rows': rows, 'unmatched_rows': 0,
                        'patients': len(patients), 'patients_without_rows': len(roster) - len(patients)}

    evaluation = {}
    excluded_keys = set()
    for partition, suffix in [('leaderboard', 'leaderboard'), ('finalscoringset', 'validation')]:
        patients = set()
        dot_missing = {'DEATH': 0, 'LKADT_P': 0}
        for _, row in records(extracted / partition / f'CoreTable_{suffix}.csv',
                              {'STUDYID', 'RPT', 'DEATH', 'LKADT_P'}):
            patient = key(row)
            if patient in roster or patient in excluded_keys or patient in patients:
                raise IntegrityError('DUPLICATE_OR_OVERLAPPING_PARTITION_KEY')
            if row['STUDYID'] != 'AZ':
                raise IntegrityError('UNEXPECTED_EVALUATION_TRIAL')
            if row['DEATH'] not in ('', '.') or row['LKADT_P'] not in ('', '.'):
                raise IntegrityError('EVALUATION_LABEL_AVAILABILITY_CHANGED')
            for field in dot_missing:
                dot_missing[field] += row[field] == '.'
            patients.add(patient)
        excluded_keys.update(patients)
        evaluation[partition] = {'patients': len(patients), 'included_in_roster': 0,
                                 'literal_dot_missing_counts': dot_missing,
                                 'reason': 'released_outcome_labels_absent'}
    report = {'stage': '01', 'training_patients': len(roster), 'trial_counts': dict(sorted(trials.items())),
              'duplicate_core_keys': 0, 'join_checks': joins, 'excluded_partitions': evaluation,
              'death_yes': death_yes, 'death_blank_preserved': death_blank,
              'missing_followup': missing_followup,
              'cycle_or_test_completeness_filter_applied': False,
              'csv_parse_mode': 'latin-1 byte-preserving; ASCII keys enforced; free-text encoding unresolved',
              'outcomes_recoded': False, 'laboratory_values_transformed': False}
    return [roster[k] for k in sorted(roster)], report


def verify_archive(run: Path) -> dict[str, str]:
    """Match all 18 extracted CSVs to the pinned original nested archives.

    Return relative CSV paths and SHA-256 values for provenance. Raise an
    IntegrityError on changed bytes, missing/extra tables or unsafe inputs;
    never extract or modify source data.
    """
    source = run / 'source/AllProvidedFiles_149.zip'
    if digest(source) != SOURCE_SHA256:
        raise IntegrityError('SOURCE_ZIP_HASH_MISMATCH')
    hashes = {}
    with zipfile.ZipFile(source) as outer:
        for partition in ('training', 'leaderboard', 'finalscoringset'):
            expected_name = f'prostate_cancer_challenge_data_{partition}.zip'
            matches = [n for n in outer.namelist() if Path(n).name == expected_name]
            if len(matches) != 1:
                raise IntegrityError('NESTED_ARCHIVE_NOT_UNIQUE')
            with zipfile.ZipFile(io.BytesIO(outer.read(matches[0]))) as nested:
                files = [n for n in nested.namelist() if n.lower().endswith('.csv')]
                if len(files) != 6 or len({Path(n).name for n in files}) != 6:
                    raise IntegrityError('PARTITION_FILE_COUNT_MISMATCH')
                for name in files:
                    path = run / 'extracted' / partition / Path(name).name
                    if path.is_symlink() or not path.is_file():
                        raise IntegrityError('EXTRACTED_FILE_NOT_REGULAR')
                    expected_hash = hashlib.sha256(nested.read(name)).hexdigest()
                    if digest(path) != expected_hash:
                        raise IntegrityError('EXTRACTED_FILE_HASH_MISMATCH')
                    hashes[str(path.relative_to(run))] = expected_hash
    actual = {str(p.relative_to(run)) for p in (run / 'extracted').rglob('*.csv')}
    if actual != set(hashes):
        raise IntegrityError('UNEXPECTED_EXTRACTED_CSV_SET')
    return hashes


def write_roster(path: Path, roster: list[dict]) -> str:
    """Exclusively create a private roster, verify its read-back and hash it.

    The caller supplies a validated, nonempty roster and registered path.
    Mode 600 restricts access; O_EXCL prevents an earlier output or symlink
    from being overwritten. Return the verified output's SHA-256.
    """
    descriptor = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    with os.fdopen(descriptor, 'w', encoding='utf-8', newline='') as stream:
        writer = csv.DictWriter(stream, fieldnames=list(roster[0]))
        writer.writeheader()
        writer.writerows(roster)
        stream.flush()
        os.fsync(stream.fileno())
    with path.open(encoding='utf-8', newline='') as stream:
        written = list(csv.DictReader(stream))
    expected = [{k: str(v) for k, v in row.items()} for row in roster]
    if written != expected:
        raise IntegrityError('ROSTER_ROUNDTRIP_MISMATCH')
    return digest(path)


def main():
    """Run Stage 01 at the registered location and print aggregate evidence.

    Validate containment, source hashes, roster and joins before writing.
    Return 0 on verified success or 1 with a fixed, disclosure-safe failure
    code. This command never prints patient keys or laboratory values.
    """
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--run-root', type=Path, default=REGISTERED_RUN)
    args = parser.parse_args()
    run = args.run_root
    try:
        if run != REGISTERED_RUN or run.resolve() != run:
            raise IntegrityError('UNREGISTERED_RUN_ROOT')
        paths = [run, run / 'source', run / 'source/AllProvidedFiles_149.zip',
                 run / 'extracted', run / 'interim',
                 *(run / 'extracted' / p for p in ('training', 'leaderboard', 'finalscoringset'))]
        if any(p.is_symlink() or p.resolve() != p for p in paths):
            raise IntegrityError('SYMLINK_OR_REDIRECTED_PATH')
        input_hashes = verify_archive(run)
        roster, report = build_roster(run / 'extracted')
        if {p: x['patients'] for p, x in report['excluded_partitions'].items()} != {'leaderboard': 157, 'finalscoringset': 313}:
            raise IntegrityError('EVALUATION_PATIENT_COUNT_MISMATCH')
        if any(digest(run / p) != h for p, h in input_hashes.items()) or digest(run / 'source/AllProvidedFiles_149.zip') != SOURCE_SHA256:
            raise IntegrityError('SOURCE_CHANGED_DURING_RUN')
        output = run / 'interim/stage01_training_roster.csv'
        report['roster_sha256'] = write_roster(output, roster)
        report['source_zip_sha256'] = SOURCE_SHA256
        report['input_csv_sha256'] = input_hashes
        report['source_code_sha256'] = digest(Path(__file__))
        report['source_unchanged'] = True
        report['roster_roundtrip_verified'] = True
        print(json.dumps(report, sort_keys=True, indent=2))
    except IntegrityError as error:
        print(json.dumps({'status': 'blocked', 'error_code': str(error)}))
        return 1
    except (OSError, UnicodeError, csv.Error, zipfile.BadZipFile):
        print(json.dumps({'status': 'blocked', 'error_code': 'IO_OR_FORMAT_ERROR'}))
        return 1
    return 0


if __name__ == '__main__':
    raise SystemExit(main())

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
FIXTURE_DIR = REPO_ROOT / "tests" / "fixtures" / "synthetic_pds"
SCRIPT = REPO_ROOT / "src" / "audit" / "inventory_raw_data.py"
sys.path.insert(0, str(SCRIPT.parent))

from inventory_raw_data import inventory_directory  # noqa: E402


class InventoryRawDataTests(unittest.TestCase):
    def setUp(self):
        self.report = inventory_directory(FIXTURE_DIR)

    def test_reports_tables_and_required_field_coverage(self):
        self.assertEqual(self.report["table_count"], 2)
        self.assertEqual(self.report["field_coverage"]["lab_day"]["status"], "found")
        self.assertEqual(self.report["field_coverage"]["survival_time"]["status"], "found")
        self.assertEqual(self.report["field_coverage"]["actual_chemo_date"]["status"], "absent")
        self.assertTrue(any("actual chemotherapy" in item for item in self.report["warnings"]))

    def test_counts_repeated_laboratory_measurements_without_patient_values(self):
        psa = next(
            item
            for item in self.report["laboratory_summaries"]
            if item["study"] == "ASCENT2" and item["test"] == "PSA"
        )
        self.assertEqual(psa["rows"], 5)
        self.assertEqual(psa["patients"], 2)
        self.assertEqual(psa["patients_with_2plus_valid_timepoints"], 1)
        self.assertEqual(psa["patients_with_3plus_valid_timepoints"], 1)
        self.assertEqual(psa["patients_with_4plus_valid_timepoints"], 0)
        self.assertEqual(psa["missing_result_rows"], 1)
        self.assertEqual(psa["not_done_rows"], 1)

        rendered = json.dumps(self.report)
        self.assertNotIn("FAKE-001", rendered)
        self.assertNotIn('"10"', rendered)

    def test_cli_writes_valid_json(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            output = Path(temporary_directory) / "inventory.json"
            completed = subprocess.run(
                [sys.executable, str(SCRIPT), str(FIXTURE_DIR), "--output", str(output)],
                check=False,
                capture_output=True,
                text=True,
            )
            self.assertEqual(completed.returncode, 0, completed.stderr)
            parsed = json.loads(output.read_text(encoding="utf-8"))
            self.assertEqual(parsed["table_count"], 2)


if __name__ == "__main__":
    unittest.main()


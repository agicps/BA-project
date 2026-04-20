import csv
import sys
import tempfile
import unittest
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = PROJECT_ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from generate_big_export import create_big_export


class BigExportGeneratorTests(unittest.TestCase):
    def test_create_big_export_multiplies_rows_and_shifts_dates(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_dir_path = Path(temp_dir)
            input_path = temp_dir_path / "export.csv"
            output_path = temp_dir_path / "export-big.csv"

            with open(input_path, "w", encoding="utf-8", newline="") as file_handle:
                writer = csv.DictWriter(
                    file_handle,
                    fieldnames=[
                        "id_patient",
                        "questionnaire_title",
                        "questionnaire_question",
                        "questionnaire_answer_date",
                        "questionnaire_answer_value",
                        "questionnaire_reply_status",
                        "questionnaire_answer_type",
                        "questionnaire_id",
                        "questionnaire_answer_id",
                        "questionnaire_reply_component_id",
                        "_airbyte_raw_id",
                        "questionnaire_created_date",
                        "_airbyte_extracted_at",
                    ],
                    quoting=csv.QUOTE_ALL,
                )
                writer.writeheader()
                writer.writerow(
                    {
                        "id_patient": "patient-1",
                        "questionnaire_title": "FACIT-Erschöpfung",
                        "questionnaire_question": "Ich bin erschöpft.",
                        "questionnaire_answer_date": "2026-04-01 10:00:00",
                        "questionnaire_answer_value": "0",
                        "questionnaire_reply_status": "COMPLETED",
                        "questionnaire_answer_type": "radio",
                        "questionnaire_id": "questionnaire-1",
                        "questionnaire_answer_id": "answer-1",
                        "questionnaire_reply_component_id": "component-1",
                        "_airbyte_raw_id": "raw-1",
                        "questionnaire_created_date": "2026-04-01 09:55:00",
                        "_airbyte_extracted_at": "2026-04-02 03:00:00+01",
                    }
                )

            result_path = create_big_export(input_path=input_path, output_path=output_path, factor=20)

            self.assertEqual(result_path, output_path)
            with open(output_path, "r", encoding="utf-8", newline="") as file_handle:
                rows = list(csv.DictReader(file_handle))

            self.assertEqual(len(rows), 20)
            self.assertEqual(rows[0]["questionnaire_answer_date"], "2026-04-01 10:00:00")
            self.assertEqual(rows[1]["questionnaire_answer_date"], "2026-05-01 10:00:00")
            self.assertNotEqual(rows[0]["questionnaire_answer_id"], rows[1]["questionnaire_answer_id"])


if __name__ == "__main__":
    unittest.main()
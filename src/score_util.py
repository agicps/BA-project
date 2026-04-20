import json
from pathlib import Path


def save_patient_scores_to_json(patient_id, questionnaire_scores, output_dir):
    output_path = Path(output_dir) / "score_dumps"
    output_path.mkdir(parents=True, exist_ok=True)

    json_file = output_path / f"patient_{patient_id}_scores.json"

    # default=str ensures date objects are written in a readable JSON format.
    with open(json_file, "w", encoding="utf-8") as file_handle:
        json.dump(questionnaire_scores, file_handle, ensure_ascii=False, indent=2, default=str)

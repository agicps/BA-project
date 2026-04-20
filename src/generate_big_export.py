from __future__ import annotations

import csv
from datetime import datetime, timedelta
from pathlib import Path
from uuid import NAMESPACE_URL, uuid5

from config import BIG_INPUT_CSV_PATH, INPUT_CSV_PATH


DATE_COLUMNS = {
    "questionnaire_answer_date",
    "questionnaire_created_date",
    "_airbyte_extracted_at",
}

ID_COLUMNS = {
    "questionnaire_id",
    "questionnaire_answer_id",
    "questionnaire_reply_component_id",
    "_airbyte_raw_id",
}


def _parse_datetime(raw_value: str) -> datetime:
    return datetime.fromisoformat(raw_value)


def _format_datetime(value: datetime, template: str) -> str:
    if "T" in template:
        return value.isoformat(sep="T")
    return value.isoformat(sep=" ")


def _shift_datetime(raw_value: str, days: int) -> str:
    if raw_value is None or raw_value == "" or raw_value == "NULL":
        return raw_value

    parsed_value = _parse_datetime(raw_value)
    shifted_value = parsed_value + timedelta(days=days)
    return _format_datetime(shifted_value, raw_value)


def _regenerate_id(raw_value: str, repetition_index: int, column_name: str) -> str:
    if raw_value is None or raw_value == "":
        return raw_value

    seed = f"{column_name}:{repetition_index}:{raw_value}"
    return str(uuid5(NAMESPACE_URL, seed))


def _load_rows(input_path: Path) -> tuple[list[str], list[dict[str, str]]]:
    with open(input_path, "r", encoding="utf-8", newline="") as source_file:
        reader = csv.DictReader(source_file)
        fieldnames = reader.fieldnames
        if not fieldnames:
            raise ValueError("Input CSV has no header row")

        rows = list(reader)
        if not rows:
            raise ValueError("Input CSV is empty")

    return fieldnames, rows


def create_big_export(
    input_path: Path = INPUT_CSV_PATH,
    output_path: Path = BIG_INPUT_CSV_PATH,
    factor: int = 20,
    day_step: int = 30,
) -> Path:
    fieldnames, rows = _load_rows(input_path)

    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w", encoding="utf-8", newline="") as target_file:
        writer = csv.DictWriter(target_file, fieldnames=fieldnames, quoting=csv.QUOTE_ALL)
        writer.writeheader()

        for repetition_index in range(factor):
            offset_days = repetition_index * day_step
            for row in rows:
                new_row = dict(row)

                for column_name in DATE_COLUMNS.intersection(new_row.keys()):
                    new_row[column_name] = _shift_datetime(new_row[column_name], offset_days)

                for column_name in ID_COLUMNS.intersection(new_row.keys()):
                    new_row[column_name] = _regenerate_id(
                        new_row[column_name], repetition_index, column_name
                    )

                writer.writerow(new_row)

    return output_path


def main() -> None:
    create_big_export()


if __name__ == "__main__":
    main()
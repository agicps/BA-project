from config import (
    INPUT_CSV_PATH,
    REQUIRED_COLUMNS,
    RELEVANT_QUESTIONNAIRES,
    FACIT_TITLE,
    FACIT_CUTOFF,
    MAX_POINTS,
    CHART_DIR,
    OUTPUT_DIR,
)
from csv_reader import load_csv
from grouping import filter_relevant_questionnaires, group_responses
from scoring import build_facit_patient_scores
from plotting import create_line_chart
from pdf_generator import create_patient_pdf


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    CHART_DIR.mkdir(parents=True, exist_ok=True)

    df = load_csv(INPUT_CSV_PATH, REQUIRED_COLUMNS)
    df = filter_relevant_questionnaires(df, RELEVANT_QUESTIONNAIRES)
    groups = group_responses(df)
    patient_scores = build_facit_patient_scores(groups, FACIT_TITLE)

    print("Number of patients with FACIT scores:", len(patient_scores))

    if patient_scores:
        first_patient_id = next(iter(patient_scores))
        facit_points = patient_scores[first_patient_id][FACIT_TITLE]

        chart_path = CHART_DIR / f"{first_patient_id}_facit.png"
        pdf_path = OUTPUT_DIR / f"patient_{first_patient_id}.pdf"

        create_line_chart(
            messpunkte=facit_points,
            questionnaire_title=FACIT_TITLE,
            y_axis_label="FACIT-Score",
            y_min=0,
            y_max=52,
            cutoff=FACIT_CUTOFF,
            cutoff_label=f"Cutoff: {FACIT_CUTOFF}",
            output_path=chart_path,
            max_points=MAX_POINTS,
        )

        create_patient_pdf(
            patient_id=first_patient_id,
            questionnaire_title=FACIT_TITLE,
            chart_path=chart_path,
            interpretation_note="Je höher der Fatigue Subscale Score, desto besser die Lebensqualität.",
            output_pdf_path=pdf_path,
        )

        print("PDF created:", pdf_path)


if __name__ == "__main__":
    main()
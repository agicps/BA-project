from config import INPUT_CSV_PATH, PATIENT_DATA_PATH, REQUIRED_COLUMNS, relevantQuestionnaires, AUSGABE_DIR
from csv_reader import load_csv
from grouping import filter_relevant_rows, group_responses
from scoring import mainScoreCalculator
from pdf_generator import create_patient_pdf
from score_util import save_patient_scores_to_json
from patient_data import load_patient_data


def main():
    csv_df = load_csv(INPUT_CSV_PATH, REQUIRED_COLUMNS)
    filtered_df = filter_relevant_rows(csv_df, relevantQuestionnaires)
    sessions = group_responses(filtered_df)
    patient_scores = mainScoreCalculator(sessions)
    
    patient_data_dict = load_patient_data(PATIENT_DATA_PATH)

    for patient_id, questionnaire_scores in patient_scores.items():
        save_patient_scores_to_json(patient_id, questionnaire_scores, AUSGABE_DIR)
        create_patient_pdf(patient_id, questionnaire_scores, AUSGABE_DIR, patient_data_dict)


if __name__ == "__main__":
    main()
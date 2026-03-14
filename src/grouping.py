import pandas as pd


def filter_relevant_questionnaires(df, relevant_questionnaires):
    filtered = df[
        df["questionnaire_title"].isin(relevant_questionnaires)
        & (df["questionnaire_reply_status"] != "NOT_STARTED")
    ].copy()

    return filtered


def group_responses(df):
    groups = df.groupby(
        ["id_patient", "questionnaire_title", "answer_day"],
        sort=False,
    )

    completions = []
    for (id_patient, questionnaire_title, answer_day), group in groups:
        answers = [
            {
                "question": row["questionnaire_question"],
                "value": row["questionnaire_answer_value"],
                "reply_status": row["questionnaire_reply_status"],
            }
            for _, row in group.iterrows()
        ]

        completions.append(
            {
                "id_patient": id_patient,
                "questionnaire_title": questionnaire_title,
                "date": answer_day,
                "answers": answers,
            }
        )

    return completions

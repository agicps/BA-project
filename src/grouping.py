import pandas as pd
# hier legen wir fest wie aus den CSV-Zeilen eine Ausfüllung wird
# also wir bündeln einzelne Antworten zu einer zusammenhängenden Ausfüllung eines Fragebogens
# mit diesen Bündelungen können später die Scores berechnet werden

# eine Ausfüllung wird definiert durch:
    # id_patient
    # questionnaire_title
    # das Datum (hier beachten wir nur den Tag)



# diese Funktion filtert irrelevante Zeilen raus
# d.h. nur relevante Fragebögen, und Zeilen die NOT_STARTED oder IN_PROGRESS sind raus
# csv ist in Form eines DataFrames, relevant_questionnaires ist eine Liste
#
def filter_relevant_rows(csv_df, relevant_questionnaires):
    filtered_csv_df = csv_df[
            csv_df["questionnaire_title"].isin(relevant_questionnaires)
            & ~csv_df["questionnaire_reply_status"].isin(["NOT_STARTED","IN_PROGRESS"])
    ].copy()
    # wir machen eine copy vom gefilterten DataFrame, weil das für pandas empfohlen wird
    return filtered_csv_df



# diese Funktion macht aus den einzelnen Antwortzeilen(eines DataFrames) eine zusammenhängende Ausfüllung (pro Tag)
def group_responses(csv_df):

    # wir gruppieren den dataframe nach Patient, Fragebogen und Tag
    groups = csv_df.groupby(["id_patient", "questionnaire_title", "answer_day"])
    # mit groupby bekommt man den Gruppenschlüssel (id_patient, questionnaire_title, answer_day) 
    # und die zugehörige Teiltabelle(group) (also die Zeilen die zu diesem Schlüssel gehören)

    # hier speichern wir die fertigen Ausfüllungen
    # gruppiert nach Patient, Fragebogen und Tag
    # jede Ausfüllung ist ein Dictionary mit daten zur Ausfüllung 
    # und einer answers-Liste, die einzelne Fragebeantwortungen als Dictionaries enthält.
    complete_forms = [] 

    # wir iterieren über die Gruppen
    # mit jedem Durchlauf bauen wir für eine Antwortzeile ein Dictionary
    for (id_patient, questionnaire_title, answer_day), group in groups:

        answers = []
        # wir iterieren über die Zeilen der Gruppe, um die Antworten zu sammeln
        # iterrows gibt uns zeilen zurück
        for index, row in group.iterrows():
            answer = {
                "question": row["questionnaire_question"],
                "value": row["questionnaire_answer_value"],
                "type": row["questionnaire_answer_type"],
                "reply_status": row["questionnaire_reply_status"],
            }
            answers.append(answer)
        

        complete_forms.append(
            # hier ist jeweils eine Ausfüllung
            {
                "id_patient": id_patient,
                "questionnaire_title": questionnaire_title,
                "date": answer_day,
                "answers": answers,
            }
        )

    return complete_forms
